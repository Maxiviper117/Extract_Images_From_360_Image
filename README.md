[![alt text](/assets/e2c.png)](https://github.com/sunset1995/py360convert)
Src: https://github.com/sunset1995/py360convert


# Script to convert Equirectangular 360° images to individual images using CubeMap projection

## Pixi Python Package Manager Installation

This script uses the Pixi package manager to install the required packages. To install Pixi, follow the instructions below:

### Linux & macOS

Run the following command in your terminal:

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

The above invocation will automatically download the latest version of Pixi, extract it, and move the Pixi binary to `~/.pixi/bin`. If this directory does not already exist, the script will create it.

The script will also update your `~/.bash_profile` to include `~/.pixi/bin` in your PATH, allowing you to invoke the Pixi command from anywhere.

### Windows

You can use either PowerShell or winget to install Pixi.

#### PowerShell:

Run the following command in your terminal:

```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

#### Winget:

Alternatively, you can use winget:

```powershell
winget install prefix-dev.pixi
```

The above commands will automatically download the latest version of Pixi, extract it, and move the Pixi binary to `LocalAppData/pixi/bin`. If this directory does not already exist, the script will create it.

The command will also automatically add `LocalAppData/pixi/bin` to your path allowing you to invoke Pixi from anywhere.

## Tip

You might need to restart your terminal or source your shell for the changes to take effect.

Source: [Pixi Installation](https://pixi.sh/latest/#installation)


## Clone the Repository

To clone the `Extract_Images_From_360_Image` repository, run the following command in your terminal:

```bash
git clone https://github.com/Maxiviper117/Extract_Images_From_360_Image.git
```

This will create a new directory named `Extract_Images_From_360_Image` containing the project files.

## Installation of Pixi dependencies

Run the following command in the terminal to install the required dependencies:

First navigate to the project directory:

```bash
cd Extract_Images_From_360_Image
```

Then run the following command:

```powershell
pixi install
```


# Usage

First, create a `imgs` directory in the root of the project. Place all the 360° images in the `imgs` directory. (must be in equirectangular format)

To run the script, execute the following command in the terminal: (Make sure you are in the project directory)

```powershell
pixi run conv
```

This will convert the 360° images to individual images using CubeMap projection and save them in the `out` directory.

With faces named as:
- `B_<orig_image_name>` - Back
- `D_<orig_image_name>` - Down
- `F_<orig_image_name>` - Front
- `L_<orig_image_name>` - Left
- `R_<orig_image_name>` - Right
- `U_<orig_image_name>` - Up


Original image file name is appended to the face name. This allows for easy identification of the original image and can quickly remove specific faces in bulk.

![alt text](/assets/image.png)

## Credits

This script utilizes the `py360convert` package for converting 360° images. For more details, visit the [py360convert GitHub repository](https://github.com/sunset1995/py360convert).

