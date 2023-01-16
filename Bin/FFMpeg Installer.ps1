[CmdletBinding()]
param
(
    [Parameter()][Switch]$AddEnvironmentVariable = $false
)

Read-Host -Prompt "Press Enter to download and install the latest FFMPEG Essentials build to 'C:\FFmpeg' or press CTRL+C to exit"
Write-Host "Downloading the latest FFMPEG Essentials build. Please wait..." -ForegroundColor Magenta

#Set Variables
$FFMPEGPath = 'C:\FFmpeg\'
$URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$Download = $FFMPEGPath + "ffmpeg.zip"
$Extract = $FFMPEGPath
$OldFolders = Get-ChildItem -Directory "ffmpeg*"


#Check if the FFMPEG Path in C:\ exists if not create it
Write-Verbose "Detecting if FFMPEG directory already exists"
If (-Not (Test-Path $FFMPEGPath))
{
    Write-Verbose "Creating FFMPEG directory"
    New-Item -Path $FFMPEGPath -ItemType Directory | Out-Null
}
else 
{
    Get-ChildItem $FFMPEGPath | Remove-item -Recurse -Confirm:$false
}


#Download the latest FFmpeg .zip file
Invoke-WebRequest -Uri $URL -OutFile $Download


#Unzip the downloaded archive to a temp location
Write-Verbose "Extracting the downloaded FFMPEG application zip"
Expand-Archive $Download -DestinationPath $Extract


#Clean up of files that were used
Write-Verbose "Clean up of the downloaded FFMPEG zip package"
if (Test-Path ($Download))
{
    Remove-Item $Download -Confirm:$false
}

#Copy folders and files from extracted folder to root ffmpeg folder
$MainFolder = Get-ChildItem -Path $FFMPEGPath | Select-Object -ExpandProperty FullName
$Subs = Get-ChildItem -Path $MainFolder | Select-Object -ExpandProperty FullName
Move-Item -Path $Subs -Destination $FFMPEGPath


#Clean up extracted folder
rm $MainFolder -Force


#Add to the PATH Environment Variables
    Write-Verbose "Adding the FFMPEG bin folder to the User Environment Variables"
    $oldpath = (Get-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH).path
    $string = $oldpath
    $ffmpeg = "$oldpath;C:\ffmpeg\bin"

    if($string -match 'ffmpeg') {
        Write-Host 'Environmental Variable already set...'
        } else {
        Write-Host 'Setting Environmental Variable...'
        Set-ItemProperty -Path 'Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment' -Name PATH -Value $ffmpeg
        Write-Host 'Variable Set'
        Start-Sleep -s 5
        exit
        }

Write-Host "FFMPEG has been installed to 'C:\FFmpeg' and the environmental variables have been set"
Read-Host "Press any key to exit"