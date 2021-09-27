# Steganography
Steganography software to hide information in PNG images.\n
Commands:\n
        --help Explanations for commands\n
        -e Extract hidden message in file\n
        -i Input file to hide the secret message in\n
        -m The message you want to hide (MUST be in quotation marks AND from the ASCII printable set)\n\n

The new image vil be named "hidden_image.png" and be placed in the same directory as the original image\n\n

python stego.py -e [file to extract]\n
Example: python stego.py -e mysecretimage.png\n
python stego.py -i [input file] -m ["Message to hide in image"]\n
Example: python stego.py -i catimage.png -m "This text will be hidden"\n
