# ========================================================================
# 🔥 OP INJOY VIP ENGINE - Windows Web Panel Installer
# ========================================================================
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TargetDir = "$env:USERPROFILE\OP_INJOY_PANEL"
$RepoUrl = "https://github.com/opinjoy7055/INJOY_java.git"

Write-Host "[*] Checking System Requirements..." -ForegroundColor Yellow

# 1. Check/Install Git
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[*] Git not found. Installing..." -ForegroundColor Yellow
    winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
}

# 2. Check/Install Node.js
if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[*] Node.js not found. Installing..." -ForegroundColor Yellow
    winget install -e --id OpenJS.NodeJS --accept-package-agreements --accept-source-agreements
}

# 3. Check/Install Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[*] Python not found. Installing..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
}

# Refresh Environment Variables in current session
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')

# 4. Clone Repository
Write-Host "[*] Cloning OP INJOY Repository..." -ForegroundColor Yellow
if (Test-Path $TargetDir) {
    Remove-Item -Path $TargetDir -Recurse -Force -ErrorAction SilentlyContinue
}
git clone $RepoUrl $TargetDir

Set-Location -Path $TargetDir

# 5. Install Python Dependencies
Write-Host "[*] Installing Python Web Panel Modules..." -ForegroundColor Yellow
python -m pip install --upgrade pip -q
python -m pip install flask psutil -q

# 6. Install Node.js Dependencies
Write-Host "[*] Installing Node.js Bot Modules..." -ForegroundColor Yellow
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

# 7. Create Global Shortcut
Write-Host "[*] Creating launch command..." -ForegroundColor Yellow
$batContent = "@echo off`ncd /d ""$TargetDir""`npython main.py"
$batContent | Out-File -FilePath "$env:USERPROFILE\op-injoy.bat" -Encoding ascii

Write-Host "==================================================" -ForegroundColor Green
Write-Host "[✔] INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "[*] Open a new CMD window and type: op-injoy" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Green
