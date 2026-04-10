# Windows PowerShell runner
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
Write-Host "Running figure scripts ..."
Get-ChildItem -Path (Join-Path $here "scripts") -Filter "fig_*.py" | ForEach-Object {
  Write-Host ("  -> " + $_.Name)
  python $_.FullName
}
Write-Host "Done. See figures/"
