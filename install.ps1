Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "        🔥 OP INJOY MINECRAFT WEB PANEL 🔥        " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$TargetDir = "$env:USERPROFILE\OP_INJOY_PANEL"
$RepoUrl = "https://github.com/opinjoy7055/INJOY_java.git"

# 1. Install Dependencies (Including Windows CMake compiler support)
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

# 2. Smart Git Update (Prevents rebuilding node_modules)
Write-Host "[*] Updating OP INJOY Repository..." -ForegroundColor Yellow
if (Test-Path "$TargetDir\.git") { 
    Set-Location -Path $TargetDir
    git pull origin main
} else {
    if (Test-Path $TargetDir) { Remove-Item -Path $TargetDir -Recurse -Force -ErrorAction SilentlyContinue }
    git clone $RepoUrl $TargetDir
    Set-Location -Path $TargetDir
}

# 3. High-Speed Live Compilation Build Phase
Write-Host "[*] Installing Python & Node Modules..." -ForegroundColor Yellow
python -m pip install flask psutil -q

$Env:JOBS = "max"
$Env:npm_config_jobs = "max"
npm install mineflayer@latest bedrock-protocol@latest minecraft-data@latest --no-audit --no-fund --foreground-scripts

# 4. Create Shortcut
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
