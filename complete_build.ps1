Write-Host "Waiting for PyInstaller to finish..."
# Wait for the pyinstaller process to finish
while (Get-Process -Name "pyinstaller" -ErrorAction SilentlyContinue) {
    Start-Sleep -Seconds 5
}
Write-Host "Copying PyInstaller output..."
if (-not (Test-Path "c:\Movies\quotation-ai\quotation-ai\frontend\backend_sidecar_internal")) {
    New-Item -ItemType Directory -Force -Path "c:\Movies\quotation-ai\quotation-ai\frontend\backend_sidecar_internal"
}
Copy-Item -Path "c:\Movies\quotation-ai\quotation-ai\backend\dist\backend_sidecar\*" -Destination "c:\Movies\quotation-ai\quotation-ai\frontend\backend_sidecar_internal\" -Recurse -Force

Write-Host "Running build_client_bundle.bat..."
Set-Location -Path "c:\Movies\quotation-ai\quotation-ai"
& .\build_client_bundle.bat
