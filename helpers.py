from PIL import Image

import json

import requests

def remove_background(input_image_path, output_image_path, api_key):
    """
    Remove the background of an image using the ClipDrop API.

    Parameters:
    - input_image_path (str): Path to the input image.
    - output_image_path (str): Path to save the output image.
    - api_key (str): ClipDrop API key.

    Returns:
    - bool: True if successful, otherwise False.
    """

    # Set the API endpoint
    endpoint = 'https://clipdrop-api.co/remove-background/v1'

    # Load the image
    with open(input_image_path, 'rb') as image_file:
        # Send the request
        response = requests.post(
            endpoint,
            files={
                'image_file': (input_image_path.split("/")[-1], image_file)
            },
            headers={
                'x-api-key': api_key
            }
        )

        # Check if the request was successful
        if response.ok:
            # Save the output image
            with open(output_image_path, 'wb') as out_file:
                out_file.write(response.content)
            return True
        else:
            response.raise_for_status()
            return False

def compose_images_from_json(input_image_path, json_path, output_image_path):
    """
    Compose an image from a JSON configuration file.

    Parameters:
    - input_image_path (str): Path to the input image.
    - json_path (str): Path to the JSON configuration file.
    - output_image_path (str): Path to the output image.


    The JSON file should contain the following keys:
    - "image_name": Name of the background image file.
    - "fraction_from_left": Fraction of the background image width from the left where the input image should be placed.
    - "fraction_of_width": Fraction of the background image width that the input image should cover.
    - "fraction_from_top": Fraction of the background image height from the top where the input image should be placed.
    - "fraction_of_height": Fraction of the background image height that the input image should cover.
    """
    
    # Load the configuration from the JSON file
    with open(json_path, 'r') as file:
        config = json.load(file)
    
    # Extract the configuration values
    background_image_path = "backgrounds/" + config["image_name"]
    fraction_from_left = config["fraction_from_left"]
    fraction_of_width = config["fraction_of_width"]
    fraction_from_top = config["fraction_from_top"]

    # Call the compose_images function with the loaded configuration
    compose_images(input_image_path, background_image_path, 
                  fraction_from_left, fraction_of_width,
                  fraction_from_top, output_image_path)

def compose_images(input_image_path, background_image_path, 
                   fraction_from_left, fraction_of_width,
                   fraction_from_top, output_image_path):
    # Load the background and input images
    bg = Image.open(background_image_path)
    input_img = Image.open(input_image_path)
    
    # Calculate the new width for the input image
    new_width = int(bg.width * fraction_of_width)
    
    # Calculate the height while preserving the aspect ratio
    aspect_ratio = input_img.height / input_img.width
    new_height = int(new_width * aspect_ratio)
    
    input_img = input_img.resize((new_width, new_height), Image.LANCZOS)
    
    # Calculate the position to paste the input image on the background
    position = (int(bg.width * fraction_from_left), int(bg.height * fraction_from_top))
    
    # Composite the images
    bg.paste(input_img, position, input_img)  # The last argument is for transparency
    
    # Save the resulting image
    bg.save(output_image_path, "PNG")
    print(f"Composed image saved to {output_image_path}")

# Example usage:
# compose_images("input_image_path.png", "background_image_path.png", 0.1, 0.5, 0.2, 0.5)
