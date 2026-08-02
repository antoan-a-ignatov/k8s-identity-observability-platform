# bootstrap-windows.ps1
# Run as Administrator

$ErrorActionPreference = "Stop"

Write-Host "Checking WSL status..." -ForegroundColor Cyan
$wslFeature = Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

if ($wslFeature.State -ne "Enabled") {
    Write-Host "Enabling WSL feature - a reboot will be required after this." -ForegroundColor Yellow
    wsl --install --no-distribution
    Write-Host "Please reboot now, then rerun this script." -ForegroundColor Yellow
    exit
}

Write-Host "Installing Ubuntu-24.04 (a window will open asking for a username/password)..." -ForegroundColor Cyan
wsl --install -d Ubuntu-24.04

Write-Host "Writing .wslconfig (6GB memory / 2GB swap - adjust below if this laptop can spare more)..." -ForegroundColor Cyan
$wslConfigPath = "$env:USERPROFILE\.wslconfig"
@"
[wsl2]
memory=6GB
swap=2GB
"@ | Out-File -FilePath $wslConfigPath -Encoding ascii -Force

Write-Host "Restarting WSL to apply config..." -ForegroundColor Cyan
wsl --shutdown

Write-Host "Done. Open the 'Ubuntu-24.04' terminal next and run bootstrap-wsl.sh." -ForegroundColor Green
