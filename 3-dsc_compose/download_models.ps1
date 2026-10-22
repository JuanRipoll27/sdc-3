# Download the course models (or copy an existing local download).
# Run from PowerShell: powershell -ExecutionPolicy Bypass -File .\3-dsc_compose\download_models.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$destination = Join-Path $root "backend\models"
$previous = Join-Path $root "..\2-dsc_streamlit\streamlit\models"
$baseUrl = "https://cs.stanford.edu/people/jcjohns/fast-neural-style/models"

New-Item -ItemType Directory -Force -Path $destination | Out-Null

$models = @(
    @{ Name = "candy.t7"; Path = "instance_norm/candy.t7" }
    @{ Name = "la_muse.t7"; Path = "instance_norm/la_muse.t7" }
    @{ Name = "mosaic.t7"; Path = "instance_norm/mosaic.t7" }
    @{ Name = "feathers.t7"; Path = "instance_norm/feathers.t7" }
    @{ Name = "the_scream.t7"; Path = "instance_norm/the_scream.t7" }
    @{ Name = "udnie.t7"; Path = "instance_norm/udnie.t7" }
    @{ Name = "the_wave.t7"; Path = "eccv16/the_wave.t7" }
    @{ Name = "starry_night.t7"; Path = "eccv16/starry_night.t7" }
    @{ Name = "la_muse_eccv16.t7"; Path = "eccv16/la_muse.t7" }
    @{ Name = "composition_vii.t7"; Path = "eccv16/composition_vii.t7" }
)

foreach ($model in $models) {
    $target = Join-Path $destination $model.Name
    $source = Join-Path $previous $model.Name

    if ((Test-Path $target) -and ((Get-Item $target).Length -gt 1000000)) {
        Write-Host "Already available: $($model.Name)"
    }
    elseif (Test-Path $source) {
        Copy-Item -Path $source -Destination $target -Force
        Write-Host "Copied: $($model.Name)"
    }
    else {
        Write-Host "Downloading: $($model.Name)"
        curl.exe -fL --retry 2 -o $target "$baseUrl/$($model.Path)"
        if ($LASTEXITCODE -ne 0) {
            throw "Download failed: $($model.Name)"
        }
    }
}

Write-Host "Done. Models are in $destination"
