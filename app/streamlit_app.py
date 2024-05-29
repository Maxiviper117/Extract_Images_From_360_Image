import os
import pathlib
import streamlit as st
from PIL import Image
from cubemap_converter import CubemapConverter

# Initialize the CubemapConverter object
converter = CubemapConverter()

# Set current working directory
cwd = pathlib.Path().absolute()

# Define input and output directories
input_dir = cwd.joinpath("imgs")
output_dir = cwd.joinpath("out")

# Create the input directory if it does not exist
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    st.warning(
        f"Directory '{input_dir}' not found. Created a new directory. Please place 360 equirectangular images in this directory."
    )

st.title("Cubemap Converter")

st.markdown(
    """
    | Front (F) | Back (B) | Left (L) | Right (R) | Up (U) | Down (D) |
    | --- | --- | --- | --- | --- | --- |
    """
)
# Options for faces
face_options = ["F", "B", "L", "R", "U", "D"]

# Checkboxes for Flip faces
st.subheader("Flip Faces")
st.warning(
    "DO NOT modify the default flip selection unless you observe images that are incorrectly flipped horizontally."
)
st.warning(
    "Faces B and R are flipped by default because they are initially outputted as flipped. Therefore, they need to be flipped back."
)
flip_faces = []
default_flips = ["B", "R"]
cols = st.columns(len(face_options))
for i, face in enumerate(face_options):
    if cols[i].checkbox(
        face, key=f"flip_{face}_checkbox", value=(face in default_flips)
    ):
        flip_faces.append(face)

# Checkboxes for Keep faces
st.subheader("Keep Faces")
keep_faces = []
default_keeps = ["F", "L", "R"]
cols = st.columns(len(face_options))
for i, face in enumerate(face_options):
    if cols[i].checkbox(
        face, key=f"keep_{face}_checkbox", value=(face in default_keeps)
    ):
        keep_faces.append(face)

st.subheader("Front Direction")
st.info(
    """
    Set the front direction of the cubemap in degrees. \n
    - Positive values rotate clockwise. \n
    - Negative values rotate counterclockwise. \n
    Default: 0 degrees.
    """
)
# Slider for front direction
front_direction = st.slider("Front direction (degrees)", -360, 360, 0)

st.info('The files will be saved in this format: ')
st.code("cubemap_dice_{front_direction}deg_{base_filename}{file_extension}")


if st.button("Convert"):
    # Convert images in the folder
    converter.convert_folder(
        input_dir,
        output_dir,
        save_all=False,
        flip_faces=flip_faces,
        keep_faces=keep_faces,
        front_direction=front_direction,
    )

    st.success("Conversion completed!")
    st.info(f"Output saved in: {output_dir}")

    # Display the first 3 images in the output/faces directory
    faces_dir = output_dir.joinpath("faces")
    if not faces_dir.exists():
        st.write("No 'faces' directory found in the output directory.")
    else:
        example_images = [
            img
            for img in os.listdir(faces_dir)
            if img.lower().endswith(("png", "jpg", "jpeg"))
        ]
        if len(example_images) == 0:
            st.write("No images found in the output/faces directory.")
        else:
            st.write("First 3 images in the output/faces directory:")
            for example_img in example_images[:3]:  # Display first 3 images as example
                img_path = os.path.join(faces_dir, example_img)
                st.image(img_path, caption=example_img)
