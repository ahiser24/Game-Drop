#Execution Policy to allow script to run for current user
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

#Install PowerShell Module PSDsHook for sending files to Discord WebHook
Write-Host "Checking for PSDsHook module in PowerShell" -ForegroundColor Magenta
Install-Module -Name PSDshook -Force
Import-Module -Name $args[4] -Force

Write-Host 'Starting 2 Pass Conversion' -ForegroundColor Magenta
invoke-expression "Write-Host 'Converting Video...Please Wait'"
    ffmpeg -y -loglevel 0 -nostats -sseof -30 -i $args[0] -c:v $args[3] -vf scale=1280:720 -an -b:v 1693k  -pass 1 -2pass -1 $args[1]
    ffmpeg -y -loglevel 0 -nostats -sseof -30 -i $args[0] -c:v $args[3] -vf scale=1280:720 -acodec copy -b:v 1693k -pass 2 -2pass -1 -y $args[1]
    
#Remove the log files
$file_path = $args[0]
$directory_path = Split-Path -Path $args[0] -Parent
rm -force $directory_path\*.log
Write-Host 'Temporary logs removed' -ForegroundColor Magenta


#Read WebHook and send video to Discord
#Read WebHook URL from Text file
    try { Invoke-PSDsHook -CreateConfig $args[2] -ErrorAction Stop}
        Catch {Write-Host 'Discord Webhook URL invalid' -ForegroundColor Red}
    try { Invoke-PSDsHook -FilePath $args[1] -ErrorAction Stop }
        Catch {Write-Host 'Discord Webhook URL Invalid' -ForegroundColor Red}
    Write-Host 'Complete. Closing in 5 seconds' -ForegroundColor Magenta
Start-Sleep -Seconds 5
Exit