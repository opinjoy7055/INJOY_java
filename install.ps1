# ========================================================================
# 🔥 OP INJOY VIP ENGINE - Windows Web Panel Installer
# ========================================================================
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TargetDir = "$env:USERPROFILE\OP_INJOY_PANEL"
$RepoUrl = "https://github.com/opinjoy7055/INJOY_java.git"

# 1. Automate DNS Hosts (The Lazy Fix)
$hostsPath = "$env:windir\System32\drivers\etc\hosts"
$entry = "127.0.0.1`tinjoy"
if (!(Select-String -Path $hostsPath -Pattern "injoy" -Quiet)) {
    Write-Host "[*] Injecting 'injoy' domain into Windows Hosts..." -ForegroundColor Yellow
    try { Add-Content -Path $hostsPath -Value "`n$entry" -Force } catch {}
}

# 2. Check/Install Dependencies
$deps = @("git", "node", "python")
foreach ($dep in $deps) {
    if (!(Get-Command $dep -ErrorAction SilentlyContinue)) {
        Write-Host "[*] $dep not found. Installing..." -ForegroundColor Yellow
        if ($dep -eq "git") { winget install -e --id Git.Git --accept-package-agreements }
        if ($dep -eq "node") { winget install -e --id OpenJS.NodeJS --accept-package-agreements }
        if ($dep -eq "python") { winget install -e --id Python.Python.3.11 --accept-package-agreements }
    }
}
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')

# 3. Clone Repository
Write-Host "[*] Cloning OP INJOY Repository..." -ForegroundColor Yellow
if (Test-Path $TargetDir) { Remove-Item -Path $TargetDir -Recurse -Force -ErrorAction SilentlyContinue }
git clone $RepoUrl $TargetDir
Set-Location -Path $TargetDir

# 4. Install Dependencies
Write-Host "[*] Installing Dependencies..." -ForegroundColor Yellow
python -m pip install flask psutil -q
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund

# 5. Create Quick Start Shortcut (op-injoy command)
$batContent = "@echo off`ncd /d ""$TargetDir""`npython main.py"
$batContent | Out-File -FilePath "$env:USERPROFILE\op-injoy.bat" -Encoding ascii

Write-Host "==================================================" -ForegroundColor Green
Write-Host "[✔] INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "1. QUICK START (Shortcut):" -ForegroundColor White
Write-Host "   Open CMD/PowerShell and type: op-injoy" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White
Write-Host "2. MANUAL START (Direct):" -ForegroundColor White
Write-Host "   cd %USERPROFILE%\OP_INJOY_PANEL" -ForegroundColor Yellow
Write-Host "   python main.py" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Green
