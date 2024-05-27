import os
import py360convert
import numpy as np
from PIL import Image, ImageOps
import pathlib


class CubemapConverter:
    def __init__(self, mode="bilinear", cube_format="dice"):
        self.mode = mode
        self.cube_format = cube_format

    @staticmethod
    def save_image(image_array, path):
        image_pil = Image.fromarray(image_array)
        image_pil.save(path)

    @staticmethod
    def get_base_filename(filepath):
        return os.path.splitext(os.path.basename(filepath))[0]

    @staticmethod
    def calculate_face_width(e_img):
        height, width = e_img.shape[:2]
        return height // 2

    @staticmethod
    def rotate_equirectangular(e_img, front_direction):
        h, w = e_img.shape[:2]
        # Calculate the number of pixels to shift based on the front direction in degrees
        shift_pixels = int((front_direction / 360.0) * w)
        # Roll the image horizontally
        e_img = np.roll(e_img, shift_pixels, axis=1)
        return e_img

    def save_cubemap_dice(self, cubemap_dice, output_dir, base_filename):
        # Create subdirectory for dice format
        dice_dir = os.path.join(output_dir, "dice")
        os.makedirs(dice_dir, exist_ok=True)

        # Save the cubemap in 'dice' format
        dice_img_path = os.path.join(dice_dir, f"cubemap_dice_{base_filename}.jpg")
        self.save_image(cubemap_dice, dice_img_path)

    def convert_e2c(self, e_img, face_w, output_horizon_views, output_list_views, output_faces, save_cube_dice):
        # Convert equirectangular image to cubemap in 'dice' format
        cubemap_dice = None
        cubemap_horizon = None
        cubemap_dict = None
        cubemap_list = None

        if save_cube_dice or output_faces or output_horizon_views or output_list_views:
            cubemap_dice = py360convert.e2c(e_img, face_w, self.mode, self.cube_format)

        if output_horizon_views:
            cubemap_horizon = py360convert.cube_dice2h(cubemap_dice)

        if output_faces:
            cubemap_horizon = cubemap_horizon if cubemap_horizon is not None else py360convert.cube_dice2h(cubemap_dice)
            cubemap_dict = py360convert.cube_h2dict(cubemap_horizon)

        if output_list_views:
            cubemap_horizon = cubemap_horizon if cubemap_horizon is not None else py360convert.cube_dice2h(cubemap_dice)
            cubemap_list = py360convert.cube_h2list(cubemap_horizon)

        return cubemap_dice, cubemap_horizon, cubemap_dict, cubemap_list

    def save_faces(self, cubemap_dict, output_dir, base_filename, flip_faces=[]):
        # Create subdirectory for faces
        faces_dir = os.path.join(output_dir, "faces")
        os.makedirs(faces_dir, exist_ok=True)

        # Save each face in the 'dict' format
        for face, face_img in cubemap_dict.items():
            if face in flip_faces:
                face_img = np.fliplr(face_img)  # Flip specified faces
            face_img_path = os.path.join(faces_dir, f"{face}_face_{base_filename}.jpg")
            self.save_image(face_img, face_img_path)

    def save_horizon(self, cubemap_horizon, output_dir, base_filename):
        # Create subdirectory for horizon format
        horizon_dir = os.path.join(output_dir, "horizon")
        os.makedirs(horizon_dir, exist_ok=True)

        # Save the 'horizon' format cubemap
        horizon_img_path = os.path.join(horizon_dir, f"cubemap_horizon_{base_filename}.jpg")
        self.save_image(cubemap_horizon, horizon_img_path)

    def save_list_faces(self, cubemap_list, output_dir, base_filename, flip_list_faces=[]):
        # Create subdirectory for list faces
        list_faces_dir = os.path.join(output_dir, "list_faces")
        os.makedirs(list_faces_dir, exist_ok=True)

        # Save each face in the 'list' format
        for i, face_img in enumerate(cubemap_list):
            if i in flip_list_faces:
                face_img = np.fliplr(face_img)  # Flip specified list faces
            face_img_path = os.path.join(list_faces_dir, f"face_{i}_{base_filename}.jpg")
            self.save_image(face_img, face_img_path)

    def convert_and_save(self, input_img_path, output_dir, output_horizon_views=False,
                         output_list_views=False, output_faces=True, save_cube_dice=False,
                         save_all=False, flip_faces=[], flip_list_faces=[], front_direction=0):
        # Create the output directory if it does not exist
        os.makedirs(output_dir, exist_ok=True)

        # Load the equirectangular image
        image = Image.open(input_img_path)
        e_img = np.array(image)

        # Rotate the equirectangular image to set the front direction
        e_img = self.rotate_equirectangular(e_img, front_direction)

        # Calculate face width dynamically based on the original image size
        face_w = self.calculate_face_width(e_img)

        # Get the base filename
        base_filename = self.get_base_filename(input_img_path)

        if save_all:
            output_horizon_views = True
            output_list_views = True
            output_faces = True
            save_cube_dice = True

        # Convert equirectangular image to cubemap formats
        cubemap_dice, cubemap_horizon, cubemap_dict, cubemap_list = self.convert_e2c(
            e_img, face_w, output_horizon_views, output_list_views, output_faces, save_cube_dice
        )

        # Save cubemap dice image
        if save_cube_dice and cubemap_dice is not None:
            self.save_cubemap_dice(cubemap_dice, output_dir, base_filename)

        # Save faces
        if output_faces and cubemap_dict is not None:
            self.save_faces(cubemap_dict, output_dir, base_filename, flip_faces=flip_faces)

        # Save horizon format
        if output_horizon_views and cubemap_horizon is not None:
            self.save_horizon(cubemap_horizon, output_dir, base_filename)

        # Save list faces
        if output_list_views and cubemap_list is not None:
            self.save_list_faces(cubemap_list, output_dir, base_filename, flip_list_faces=flip_list_faces)

        # Print shapes for verification
        print("cubemap_dice.shape:", cubemap_dice.shape if cubemap_dice is not None else "Not created")
        print("cubemap_horizon.shape:", cubemap_horizon.shape if cubemap_horizon is not None else "Not created")
        print("cubemap_dict.keys():", cubemap_dict.keys() if cubemap_dict is not None else "Not created")
        if cubemap_dict is not None:
            print('cubemap_dict["F"].shape:', cubemap_dict["F"].shape)
        print("len(cubemap_list):", len(cubemap_list) if cubemap_list is not None else "Not created")
        if cubemap_list is not None:
            print("cubemap_list[0].shape:", cubemap_list[0].shape)

    def convert_folder(self, input_dir, output_dir, output_horizon_views=False,
                       output_list_views=False, output_faces=True, save_cube_dice=False,
                       save_all=False, flip_faces=[], flip_list_faces=[], front_direction=0):
        # Check if input directory exists
        if not os.path.exists(input_dir):
            print(f"Directory '{input_dir}' not found. Please create a directory named 'imgs' in the root with 360 equirectangular images to process.")
            return

        # Iterate through all files in the input directory
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_img_path = os.path.join(input_dir, filename)
                self.convert_and_save(
                    input_img_path, output_dir, output_horizon_views,
                    output_list_views, output_faces, save_cube_dice, save_all,
                    flip_faces=flip_faces, flip_list_faces=flip_list_faces,
                    front_direction=front_direction
                )


# Set current working directory
cwd = pathlib.Path().absolute()

# Define input and output directories
input_dir = cwd.joinpath("imgs")
output_dir = cwd.joinpath("out")

# Create converter object
converter = CubemapConverter()

# Convert images in the folder
converter.convert_folder(
    input_dir, output_dir, save_all=False,
    flip_faces=["B", "R"], flip_list_faces=[1, 2],
    front_direction=0  # Set the front direction in degrees 0-360
)
