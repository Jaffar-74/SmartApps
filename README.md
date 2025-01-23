# SmartApps
# Inkscape Image Processing Script

This documentation provides a comprehensive guide for using the automation script designed to reduce manual efforts in image processing for documents. The script utilizes the Inkscape tool to convert images from various formats (.png, .jpg, .svg) to the .svg format and also helps in resizing the images to required dimensions. This tool facilitates batch conversion of images within a few minutes.

## Why SVG as Output?

SVG images are vector-based, allowing them to be scaled up or down without losing quality. Additionally, in tools like Tridion Docs (SDL), SVG images can be edited directly by checking them out, rather than replacing the image in the document after editing. The Inkscape tool is used for .svg conversion.

## Requirements

- Python
- Inkscape (must be installed in the default path for the script to work)

## Working of the Script

Create three folders:

- **Input Folder**: Contains the image files to be processed. Segment input files into multiple folders (e.g., images for 80 mm, 90 mm, 100 mm, etc.) based on the output width requirements and use the same temp and output folders.
- **Temp Folder**: Create a temp folder with no files inside it (used by the script during processing).
- **Output Folder**: Stores the processed output (.svg files).

## Steps to Run the Script

1. Download the zip file from the GitHub page.
2. Extract the zip file to the preferred location.
3. Navigate to the location `..\resize`, and in the folder structure path, select all and type `cmd` to open the command prompt.
4. This will open the script in this location. Type `python resize.py` and press `<enter>`.
5. The script will prompt for the input folder path. Enter the path and press `<enter>`.
6. The script will prompt for the Temp folder location. Enter the path and press `<enter>`.
7. The script will prompt for the Output folder location. Enter the path and press `<enter>`.
8. The script will prompt for the width constraint. Provide the width details in mm.
   - **Note**: The image height is automatically rescaled to maintain the aspect ratio and image quality.
9. The script will process the images and store the files in the output folder. After processing the images, it deletes the temp folder.
