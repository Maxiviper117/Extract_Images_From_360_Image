

# Script to convert Equirectangular 360° images to individual images using CubeMap projection

## Pixi Python Package Manager Installation

This script uses the Pixi package manager to install the required packages. To install Pixi, follow the instructions below:

To install Pixi on Windows, you can use either PowerShell or winget.

### PowerShell:

Run the following command in your terminal:

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

### Winget:

Alternatively, you can use winget:

```powershell
winget install prefix-dev.pixi
```

The above commands will automatically download the latest version of Pixi, extract it, and move the Pixi binary to `LocalAppData/pixi/bin`. If this directory does not already exist, the script will create it.

The command will also automatically add `LocalAppData/pixi/bin` to your path allowing you to invoke Pixi from anywhere.

Source: [Pixi Installation](https://pixi.sh/latest/#installation)

## Installation




