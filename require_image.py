# import os
# import glob
#
# def print_image_requires(directory_path):
#     # Check if the directory exists
#     if not os.path.exists(directory_path):
#         print(f"The directory '{directory_path}' does not exist.")
#         return
#
#     # Define a list of common image file extensions
#     image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]
#
#     # Initialize an empty list to store image file names
#     image_files = []
#
#     # Iterate through each image extension and search for matching files
#     for extension in image_extensions:
#         search_pattern = os.path.join(directory_path, extension)
#         image_files.extend(glob.glob(search_pattern))
#
#     # Print the image names in the require format with extensions
#     if image_files:
#         for image_file in image_files:
#             image_name = os.path.basename(image_file)
#             filename = os.path.splitext(os.path.basename(image_file))[0]
#
#             print(f"{filename}: require('../Images/{image_name}');")
#     else:
#         print("No image files found in the directory.")
#
#
# directory_path = "Images"
# print_image_requires(directory_path)
import os
import glob


def generate_image_requires(directory_path, output_file):
    if not os.path.exists(directory_path):
        print(f"The directory '{directory_path}' does not exist.")
        return

    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"]

    image_files = []

    for extension in image_extensions:
        search_pattern = os.path.join(directory_path, extension)
        image_files.extend(glob.glob(search_pattern))

    with open(output_file, "w") as js_file:
        js_file.write("module.exports = {\n")
        for image_file in image_files:
            image_name = os.path.splitext(os.path.basename(image_file))[0]
            js_file.write(f'  {image_name}: require("../Images/{image_name}.jpg"),\n')
        js_file.write("};")

directory_path = "Images_Mohini"
output_file = "images_by_mohini.js"
generate_image_requires(directory_path, output_file)
