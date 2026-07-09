Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TargetDir = "$env:USERPROFILE\OP_INJOY_PANEL"
$RepoUrl = "https://github.com/opinjoy7055/INJOY_java.git"

# 1. Install Dependencies 
$deps = @("git", "node", "python", "cmake")
foreach ($dep in $deps) {
    if (!(Get-Command $dep -ErrorAction SilentlyContinue)) {
        Write-Host "[*] $dep not found. Installing..." -ForegroundColor Yellow
        if ($dep -eq "git") { winget install -e --id Git.Git --accept-package-agreements }
        if ($dep -eq "node") { winget install -e --id OpenJS.NodeJS --accept-package-agreements }
        if ($dep -eq "python") { winget install -e --id Python.Python.3.11 --accept-package-agreements }
        if ($dep -eq "cmake") { winget install -e --id Kitware.CMake --accept-package-agreements }
    }
}
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')

# 2. Smart Git Update (DO NOT DELETE FOLDER)
Write-Host "[*] Updating OP INJOY Repository..." -ForegroundColor Yellow
if (Test-Path "$TargetDir\.git") { 
    Set-Location -Path $TargetDir
    git pull origin main
} else {
    if (Test-Path $TargetDir) { Remove-Item -Path $TargetDir -Recurse -Force -ErrorAction SilentlyContinue }
    git clone $RepoUrl $TargetDir
    Set-Location -Path $TargetDir
}

# 3. Fast NPM Install (Multi-core & Cached)
Write-Host "[*] Installing Python & Node Modules..." -ForegroundColor Yellow
python -m pip install flask psutil -q

$Env:JOBS = "max"
$Env:npm_config_jobs = "max"
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund --prefer-offline --loglevel error

# 4. Shortcut
$batContent = "@echo off`ncd /d ""$TargetDir""`npython main.py"
$batContent | Out-File -FilePath "$env:USERPROFILE\op-injoy.bat" -Encoding ascii

Write-Host "[✔] INSTALLATION COMPLETE! Type 'op-injoy' to start." -ForegroundColor Green
