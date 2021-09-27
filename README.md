# Steganography
Steganography software to hide information in PNG images.  
IMPORTANT: This is not encryption. Anyone can see the message you write if they know where to look.  
Steganography is meant to hide the fact that a message was sent in the first place.
# Commands:
        --help Explanations for commands
        -e Extract hidden message from image
        -i Input image to hide the secret message in
        -m The message you want to hide (MUST be in quotation marks AND from the ASCII printable set)

The new image vil be named "hidden_image.png" and be placed in the same directory as the original image

# Example commands
python stego.py -e [file to extract]  
Example: python stego.py -e mysecretimage.png  
  
python stego.py -i [input file] -m ["Message to hide in image"]  
Example: python stego.py -i catimage.png -m "This text will be hidden"  
