"""Package editable sources and a file://-friendly preview. Uses Python stdlib only."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import zipfile
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parents[1]
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root)
tracked_names = {name.decode('utf-8') for name in tracked.split(b'\0') if name}
if 'scripts/check-privacy.py' not in tracked_names:
    raise SystemExit('Stage scripts/check-privacy.py before packaging; source archives only include tracked files.')
output = root / 'output'
if output.resolve().parent != root:
    raise SystemExit('Refusing an output directory outside the project root.')
output.mkdir(exist_ok=True)
preview = output / 'preview'

# Only reviewed, tracked sources may enter the source ZIP. Scan the actual
# build as well: Jekyll can copy untracked static assets into its output.
for arguments in ([], ['--site', '_site']):
    subprocess.run([sys.executable, str(root / 'scripts/check-privacy.py'), *arguments],
                   cwd=root, check=True)


def linked_path(path, base):
    """Reject symlinks/junctions and paths escaping the selected source tree."""
    if not path.resolve().is_relative_to(base.resolve()):
        return True
    current = path
    while current != base:
        if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
            return True
        current = current.parent
    return base.is_symlink() or (hasattr(base, 'is_junction') and base.is_junction())


def private_material(path, base):
    """Exclude originals and local extraction files, including renamed symlinks."""
    relative_parts = path.relative_to(base).as_posix().lower().split('/')
    if linked_path(path, base):
        return True
    if any(part in {'private', 'secrets', '.git', '.aws', '.ssh', '.agents', '.codex', '.claude', 'output', '__pycache__'} for part in relative_parts):
        return True
    name = relative_parts[-1]
    if name == '.env' or name.startswith('.env.') or name == 'credentials.json' or name.startswith('service-account'):
        return True
    if Path(name).suffix in {'.pem', '.key', '.p12', '.pfx', '.log', '.bak', '.tmp', '.pyc'}:
        return True
    pairs = set(zip(relative_parts, relative_parts[1:]))
    if ('assets', 'papers') in pairs or ('assets', 'teach') in pairs or ('assets', 'teaching') in pairs or ('output', 'paper-review') in pairs or ('output', 'teaching-review') in pairs:
        return True
    resolved = path.resolve()
    return any(resolved.is_relative_to(private_root) for private_root in (
        (root / 'assets/papers').resolve(),
        (root / 'assets/teach').resolve(),
        (root / 'assets/teaching').resolve(),
        (root / 'output/paper-review').resolve(),
        (root / 'output/teaching-review').resolve(),
    ))


def preview_ignore(directory, names):
    return [name for name in names
            if private_material(Path(directory) / name, root / '_site')]

if not (root / '_site/index.html').is_file():
    raise SystemExit('Build the site with Jekyll first.')
# Rebuild the generated preview so files from older builds cannot survive.
# Resolve and verify the exact deletion target before recursive removal.
if preview.is_symlink() or preview.resolve().parent != output.resolve():
    raise SystemExit('Refusing to remove a preview path outside project/output.')
if preview.exists():
    if not preview.is_dir():
        raise SystemExit('The generated preview path is not a directory.')
    shutil.rmtree(preview)
shutil.copytree(root / '_site', preview, ignore=preview_ignore)
for html in preview.rglob('*.html'):
    def local_link(match):
        value = match[2]
        if not value.startswith('/') or value.startswith('//'):
            return match[0]
        parts = urlsplit(value)
        target = preview / unquote(parts.path).lstrip('/')
        if target.is_dir():
            target /= 'index.html'
        relative = Path(os.path.relpath(target, html.parent)).as_posix()
        suffix = ('?' + parts.query if parts.query else '') + ('#' + parts.fragment if parts.fragment else '')
        return match[1] + relative + suffix + match[3]
    content = html.read_text(encoding='utf-8')
    content = re.sub(r'''((?:href|src)\s*=\s*["'])([^"']+)(["'])''', local_link, content)
    html.write_text(content, encoding='utf-8')

def archive(path, members, base):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for file in members:
            if file.is_file() and not private_material(file, base):
                z.write(file, file.relative_to(base).as_posix())

source_files = [root / name for name in sorted(tracked_names)]
archive(output / 'wenjie-liao-source.zip', source_files, root)
archive(output / 'wenjie-liao-preview.zip', preview.rglob('*'), preview)
print(f'Offline preview: {preview / "index.html"}')
print(f'Source archive: {output / "wenjie-liao-source.zip"}')
print(f'Preview archive: {output / "wenjie-liao-preview.zip"}')
