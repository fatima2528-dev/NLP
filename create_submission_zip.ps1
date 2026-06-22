# Creates Fatimas_Assistant_Submission.zip for course submission.
# Excludes .env, venv, and other sensitive/local files.

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$staging = Join-Path $root "_submission"
$zipPath = Join-Path $root "Fatimas_Assistant_Submission.zip"

if (Test-Path $staging) { Remove-Item -Recurse -Force $staging }
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

New-Item -ItemType Directory -Path $staging | Out-Null

$files = @(
    "app.py",
    "build_vectorstore.py",
    "rag.ipynb",
    "requirements.txt",
    "requirements-deploy.txt",
    "README.md",
    "DEPLOY.md",
    "Dockerfile",
    ".env.example",
    ".gitignore",
    ".dockerignore"
)
foreach ($f in $files) {
    Copy-Item (Join-Path $root $f) -Destination $staging
}
Copy-Item -Recurse (Join-Path $root "frontend") -Destination $staging
Copy-Item -Recurse (Join-Path $root "data") -Destination $staging
Copy-Item -Recurse (Join-Path $root "vectorstore") -Destination $staging

Compress-Archive -Path "$staging\*" -DestinationPath $zipPath -Force
Remove-Item -Recurse -Force $staging

Write-Host "Created: $zipPath"
