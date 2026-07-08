# ========================================================================
# 🔥 OP INJOY VIP ENGINE - Windows Installer
# ========================================================================
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "             🔥 OP INJOY VIP ENGINE 🔥            " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TargetDir = "$env:USERPROFILE\OP_INJOY_ENGINE"
$RepoUrl = "https://raw.githubusercontent.com/opinjoy7055/OPINJOY_/main/index.js"

# Check Node.js
if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[*] Node.js not found. Installing..." -ForegroundColor Yellow
    winget install -e --id OpenJS.NodeJS --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
}

# Create Directory
if (!(Test-Path $TargetDir)) { New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null }
Set-Location -Path $TargetDir

# Install Dependencies
Write-Host "[*] Installing Engine Dependencies..." -ForegroundColor Yellow
npm init -y | Out-Null
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

# Download Engine
Write-Host "[*] Downloading Core Engine..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $RepoUrl -OutFile "index.js"

# Create Shortcut
$batContent = "@echo off`ncd /d ""$TargetDir""`nnode index.js"
$batContent | Out-File -FilePath "$env:USERPROFILE\op-injoy.bat" -Encoding ascii

Write-Host "==================================================" -ForegroundColor Green
Write-Host "[✔] INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "[*] Open a new CMD window and type: op-injoy" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Green
