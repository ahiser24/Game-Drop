   Read-Host -Prompt "Press Enter to install PowerShell 7 or CTRL+C to exit"
    iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"