import os
import shutil
import subprocess
import xml.etree.ElementTree as ET\

def delete_folder(temp_folder):
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
        print(f"Folder '{temp_folder}' has been deleted.")
    else:
        print(f"Folder '{temp_folder}' does not exist.")

def update_svg_attributes(input_svg, output_svg, new_viewbox, new_width, new_height, new_window_width, new_window_height):
    # Parse the input SVG file
    tree = ET.parse(input_svg)
    root = tree.getroot()

    # Ensure the inkscape namespace is declared
    ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")

    # Update the 'viewBox' attribute
    if 'viewBox' in root.attrib:
        print(f"Old viewBox: {root.attrib['viewBox']}")
    else:
        print("No viewBox attribute found. Adding a new one.")
    root.attrib['viewBox'] = new_viewbox

    # Update the 'width' and 'height' attributes
    root.attrib['width'] = str(new_width)
    root.attrib['height'] = str(new_height)

    # Update the 'inkscape:window-width' and 'inkscape:window-height' attributes
    # Check if these attributes exist in the root, and update them
    inkscape_ns = "{http://www.inkscape.org/namespaces/inkscape}"
    if f'{inkscape_ns}window-width' in root.attrib:
        print(f"Old inkscape:window-width: {root.attrib[f'{inkscape_ns}window-width']}")
    else:
        print("No inkscape:window-width attribute found. Adding a new one.")
    root.attrib[f'{inkscape_ns}window-width'] = str(new_window_width)

    if f'{inkscape_ns}window-height' in root.attrib:
        print(f"Old inkscape:window-height: {root.attrib[f'{inkscape_ns}window-height']}")
    else:
        print("No inkscape:window-height attribute found. Adding a new one.")
    root.attrib[f'{inkscape_ns}window-height'] = str(new_window_height)

    # Find the <image> element and update its 'width' and 'height' attributes
    for image in root.iter('{http://www.w3.org/2000/svg}image'):
        image.attrib['width'] = str(new_width)
        image.attrib['height'] = str(new_height)

    # Save the modified SVG to a new file
    tree.write(output_svg)
    print(f"New SVG saved as: {output_svg}")

    # Append the new width and height at the end of the file
    with open(output_svg, 'a') as f:
        f.write(f'\n<!-- New image width: {new_width}, New image height: {new_height} -->')

def get_svg_dimensions(svg_path):
    """Extract the width and height from an SVG file assuming they are in pixels."""
    tree = ET.parse(svg_path)
    root = tree.getroot()

    width = float(root.get('width'))
    height = float(root.get('height'))

    return width, height

def resize_svg(temp_folder, target_width):
    dimensions = []
    # Iterate over all files in the input directory
    for filename in os.listdir(temp_folder):
        if filename.endswith(".svg"):
            input_path = os.path.join(temp_folder, filename)

            # Get original dimensions
            original_width, original_height = get_svg_dimensions(input_path)

            # Calculate the target height to preserve aspect ratio
            target_height = int((target_width / original_width) * original_height)
            print(f"Original dimensions: {original_width}x{original_height}")
            print(f"Target dimensions: {target_width}x{target_height}")

            dimensions.append((target_width, target_height))
    return dimensions

def convert_images_to_svg(input_folder, temp_folder):
    # Ensure the output folder exists
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.PNG') or filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.svg'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(temp_folder, os.path.splitext(filename)[0] + '.svg')

            # Call Inkscape to convert the image to SVG
            try:
                result = subprocess.run([
                    'inkscape',  # Update this path if necessary
                    input_path,
                    '--export-filename', output_path
                ], capture_output=True, text=True)

                # Print the output and error messages from the subprocess call
                print(f"Processing {filename}")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)

                # Check if the file was created
                if os.path.exists(output_path):
                    print(f"Successfully created {output_path}")
                else:
                    print(f"Failed to create {output_path}")

            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

if __name__ == '__main__':
    input_folder = input("Enter the input folder path: ").strip()
    temp_folder = input("Enter the temp folder path: ").strip()
    output_folder = input("Enter the Output folder path: ").strip()  # Path to save the modified SVG file
    target_width_mm = int(input("Enter the Target widthin mm: ").strip())
    target_width = target_width_mm * 3.7795275591

    convert_images_to_svg(input_folder, temp_folder)
    dimensions = resize_svg(temp_folder, target_width)

    # Iterate over all files in the temp folder to update their attributes
    for i, filename in enumerate(os.listdir(temp_folder)):
        if filename.endswith(".svg"):
            input_svg = os.path.join(temp_folder, filename)
            output_svg = os.path.join(output_folder, filename)
            new_width, new_height = dimensions[i]
            new_window_width = new_width  # The new window width for Inkscape
            new_window_height = new_height  # The new window height for Inkscape
            new_viewbox = f'0 0 {new_width} {new_height}'  # The new viewBox values
            update_svg_attributes(input_svg, output_svg, new_viewbox, new_width, new_height, new_window_width, new_window_height)
    
    # Delete the temp folder after processing all files
    delete_folder(temp_folder)
