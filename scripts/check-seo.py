"""Check production SEO metadata and the sitemap using Python's standard library."""

import argparse
from html.parser import HTMLParser
import ipaddress
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Head(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.meta, self.links = {}, []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        attrs = dict(attributes)
        if tag == "meta":
            self.meta.setdefault((attrs.get("name") or "").lower(), []).append(attrs.get("content") or "")
        elif tag == "link":
            self.links.append(attrs)

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False

    def link_values(self, relation, language=None):
        return [link.get("href", "") for link in self.links
                if relation in (link.get("rel") or "").lower().split()
                and (language is None or (link.get("hreflang") or "").lower() == language.lower())]


def production_base(value):
    parsed = urlsplit(value)
    host = parsed.hostname or ""
    if (parsed.scheme != "https" or not host or parsed.username or parsed.password
            or parsed.query or parsed.fragment or parsed.port not in (None, 443)
            or any(char.isspace() for char in value) or "\\" in value
            or host == "localhost" or host.endswith((".localhost", ".local"))
            or ".." in unquote(parsed.path).split("/") or "//" in parsed.path):
        raise ValueError("Use an absolute public HTTPS base URL without credentials, query or fragment.")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError("The base URL must not be a local address.")
    return value.rstrip("/") + "/"


def check(directory, base):
    root = Path(directory)
    pages = sorted(root.rglob("*.html"))
    errors, public_urls = [], set()
    error_pages = {"404.html", "zh/404.html"}
    required = {"index.html", "zh/index.html"} | error_pages
    relative_pages = {page.relative_to(root).as_posix() for page in pages}
    for missing in sorted(required - relative_pages):
        errors.append(f"{missing}: required page missing")
    for page in pages:
        relative = page.relative_to(root).as_posix()
        url = base + relative.removesuffix("index.html")
        head = Head(page.read_text(encoding="utf-8"))
        def require(condition, rule):
            if not condition:
                errors.append(f"{relative}: {rule}")
        require(head.link_values("canonical") == [url], "one canonical URL must match the production page URL")
        description = head.meta.get("description", [])
        require(len(description) == 1 and bool(description[0].strip()), "one nonempty description is required")
        english = relative.removeprefix("zh/")
        for language, counterpart in (("en", english), ("zh-CN", "zh/" + english)):
            require(counterpart in relative_pages, f"missing {language} counterpart page")
            require(head.link_values("alternate", language) == [base + counterpart.removesuffix("index.html")],
                    f"incorrect {language} alternate URL")
        robots = ",".join(head.meta.get("robots", [])).lower().replace(",", " ").split()
        if relative in error_pages:
            require("noindex" in robots, "error page requires noindex")
        else:
            require("noindex" not in robots and "none" not in robots, "public page must permit indexing")
            public_urls.add(url)
        for name in ("google-site-verification", "msvalidate.01", "baidu-site-verification"):
            values = head.meta.get(name, [])
            require(len(values) <= 1 and all(value.strip() for value in values), f"invalid or duplicate {name} tag")
    sitemap = ET.parse(root / "sitemap.xml").getroot()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locations = [(node.text or "").strip() for node in sitemap.findall(f"{namespace}url/{namespace}loc")]
    if sitemap.tag != namespace + "urlset" or len(locations) != len(set(locations)) or set(locations) != public_urls:
        errors.append("sitemap.xml: URLs must match all public HTML pages exactly, without duplicates or error pages")
    for location in locations:
        parts = unquote(urlsplit(location).path).lower().split("/")
        pairs = set(zip(parts, parts[1:]))
        if (any(part in {"private", "secrets", "output", "papers", "teach", ".git"} for part in parts)
                or ("assets", "teaching") in pairs):
            errors.append("sitemap.xml: private material URL detected")
    for error in errors:
        print("FAIL:", error)
    if not errors:
        print(f"PASS: {len(pages)} HTML pages, {len(public_urls)} public sitemap URLs, canonical, language and verification metadata.")
    return bool(errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir")
    parser.add_argument("base_url", help="public HTTPS site URL, including the project path")
    args = parser.parse_args()
    try:
        return check(args.build_dir, production_base(args.base_url))
    except (OSError, ValueError, ET.ParseError):
        print("FAIL: check the public HTTPS base URL, built HTML and sitemap.xml; raw details are suppressed.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
