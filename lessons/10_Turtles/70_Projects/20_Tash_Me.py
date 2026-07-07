"""
Tash Me

Write a program that:
1) Loads an emoji image as the background
2) Make the turtle shape a moustache
3) Move the moustache to the right spot on the emoji

Hint: See the `10_More_Turtle_Programs` section labeled 'Set a Background Picture'.
"""

import turtle

def set_background_image(window, image_name):
    """Set the background image of the turtle window to the image with the given name."""
    from pathlib import Path                                        # Import Path from pathlib module
    from PIL import Image                                           # Import Image from PIL (Pillow) library

    image_dir = Path(__file__).parent / "images"                    # Define the directory containing images
    image_path = str(image_dir / image_name)                        # Create the full path to the image file

    image = Image.open(image_path)                                  # Open the image to get its dimensions
    
    window.setup(image.width, image.height, startx=0, starty=0)     # Set window size to image size
    window.bgpic(image_path)                                        # Set the background picture of the window

turtle.setup(width=600, height=600)         # Set the size of the window

tina = turtle.Turtle()                      # Create a turtle named tina

screen = turtle.Screen()                    # Get the screen that tina is on
set_background_image(screen, 'emoji.png')   # Set the background image of the screen

turtle.exitonclick() 
```