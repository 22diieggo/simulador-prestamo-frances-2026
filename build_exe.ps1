param(
    [string]$PythonLauncher = "py",
    [switch]$CleanOutput
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if ($CleanOutput) {
    $outputPaths = @(
        (Join-Path $projectRoot "build"),
        (Join-Path $projectRoot "dist")
    )

    foreach ($path in $outputPaths) {
        if (Test-Path -LiteralPath $path) {
            Remove-Item -LiteralPath $path -Recurse -Force
        }
    }
}

& $PythonLauncher -m PyInstaller --noconfirm --clean simulador_prestamo.spec
