<#
.SYNOPSIS
    Installs the HOI4 mods in this repo into your local Hearts of Iron IV
    mod folder, generating the launcher pointer (.mod) files automatically.

.DESCRIPTION
    Each subfolder of .\mods\ is a self-contained HOI4 mod. This script copies
    the chosen mod's folder into your HOI4 user "mod" directory and places the
    matching .mod pointer file next to it so the launcher can find it.

.PARAMETER Mod
    Name of a single mod folder under .\mods\ to install. Omit to install all.

.EXAMPLE
    .\install.ps1
    Installs every mod in the repo.

.EXAMPLE
    .\install.ps1 -Mod usa_presidential_cabinet
    Installs just that mod.

.NOTES
    If you get an execution-policy error, run PowerShell as your user and use:
        powershell -ExecutionPolicy Bypass -File .\install.ps1
#>
param(
    [string]$Mod = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$modsSrc  = Join-Path $repoRoot "mods"

if (-not (Test-Path $modsSrc)) {
    Write-Error "Could not find a 'mods' folder next to this script ($modsSrc)."
}

# Resolve the HOI4 user data 'mod' directory (honours OneDrive-redirected Documents).
$docs   = [Environment]::GetFolderPath("MyDocuments")
$hoiDir = Join-Path $docs "Paradox Interactive\Hearts of Iron IV\mod"

if (-not (Test-Path $hoiDir)) {
    New-Item -ItemType Directory -Force -Path $hoiDir | Out-Null
    Write-Host "Created HOI4 mod directory: $hoiDir"
}

# Pick which mod folder(s) to install.
$modFolders = Get-ChildItem -Path $modsSrc -Directory
if ($Mod -ne "") {
    $modFolders = $modFolders | Where-Object { $_.Name -eq $Mod }
    if (-not $modFolders) {
        $available = (Get-ChildItem -Path $modsSrc -Directory | Select-Object -ExpandProperty Name) -join ", "
        Write-Error "No mod folder named '$Mod' under .\mods\. Available: $available"
    }
}

# Helper: write a UTF-8 file WITHOUT a byte-order mark (Paradox parsers dislike BOMs).
function Write-NoBom([string]$Path, [string]$Content) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

foreach ($m in $modFolders) {
    $name        = $m.Name
    $destFolder  = Join-Path $hoiDir $name
    $pointerDest = Join-Path $hoiDir "$name.mod"
    $pointerSrc  = Join-Path $modsSrc "$name.mod"

    # Replace any previous copy of the mod folder.
    if (Test-Path $destFolder) { Remove-Item -Recurse -Force $destFolder }
    Copy-Item -Recurse -Force -Path $m.FullName -Destination $destFolder

    # Place the launcher pointer .mod next to the folder.
    if (Test-Path $pointerSrc) {
        Copy-Item -Force -Path $pointerSrc -Destination $pointerDest
    } else {
        # Fall back to generating one from the mod's descriptor.mod.
        $descPath = Join-Path $m.FullName "descriptor.mod"
        $desc = (Get-Content $descPath -Raw).TrimEnd()
        Write-NoBom $pointerDest ($desc + "`r`npath=`"mod/$name`"`r`n")
    }

    Write-Host "Installed '$name'"
    Write-Host "    files   -> $destFolder"
    Write-Host "    pointer -> $pointerDest"
}

Write-Host ""
Write-Host "Done. Open the HOI4 launcher, refresh mods, add them to a Playset,"
Write-Host "and (for the USA cabinet mod) put Road to 56 ABOVE it in the load order."
