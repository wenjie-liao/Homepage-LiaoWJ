param(
    [ValidateRange(1, 65535)][int]$Port = 4173,
    [switch]$Rebuild,
    [string]$RubyRunner
)

$ErrorActionPreference = 'Stop'
$siteRoot = Split-Path -Parent $PSScriptRoot

if ($RubyRunner) {
    if (-not (Test-Path -LiteralPath $RubyRunner -PathType Leaf)) {
        throw "Ruby runner not found: $RubyRunner"
    }
    $RubyRunner = (Resolve-Path -LiteralPath $RubyRunner).Path
}

Push-Location -LiteralPath $siteRoot
try {
    if ($Rebuild -or -not (Test-Path -LiteralPath (Join-Path $siteRoot '_site\index.html'))) {
        if ($RubyRunner) {
            & $RubyRunner bundle exec jekyll build
        } elseif (Get-Command bundle -ErrorAction SilentlyContinue) {
            & bundle exec jekyll build
        } else {
            throw 'Ruby/Jekyll is required. Install Ruby and Bundler, or pass -RubyRunner. See README.md.'
        }
        if ($LASTEXITCODE -ne 0) { throw 'Website build failed.' }
    }
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'Python 3 is required for this preview server. Alternatively, use bundle exec jekyll serve.'
    }
    Write-Host "Preview: http://127.0.0.1:$Port/ (Ctrl+C to stop)"
    python -m http.server $Port --bind 127.0.0.1 --directory (Join-Path $siteRoot '_site')
    if ($LASTEXITCODE -ne 0) { throw 'Preview server stopped with an error.' }
} finally {
    Pop-Location
}
