# Steganography
Steganography software to hide information in PNG images.  
IMPORTANT: This is not encryption. Anyone can see the message you write if they know where to look.  
Steganography is only meant to hide the fact that a message was sent in the first place.
# Commands:
        -h Explanations for commands
        -i Inputimage, where the message will be hidden (Requires [-m] or [-mf])
        -m The message you want to hide (MUST be in quotation marks AND from the ASCII printable set)
        -mf File where the message resides
        -e Extract hidden message from image and print to screen
        -ef Extract message from image to file (Don't set file)
        
The new image vil be named "hidden_image.png" and be placed in the same directory as the original image  
If you specify [-ef], the message will be saved in a text file called "output_message.txt" in the same directory as the original image  
### ASCII printable set:
        0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c
The ASCII printable set is used because it presents the least amount of problems when encoding, decoding and reading from the image.                                   

# How it works
This python program takes the image and converts it into a list of RGB values for each pixel. These are numbers ranging from 0-255. These numbers are then converted to binary. The input message is also converted into binary. Then, every bit in the message is inserted in place of the least significant bit (LSB) from the RGB values. This effects the color of the image the least. The image is then saved and outputted.  
To retrieve the information, the program converts the RGB values to binary and takes the LSB and appends it to a list. This list is then joined togheter and converted from binary to ASCII to form a string to be printed or written to a file.  

There are improvments to make. For example, the program could switch the 2 LSB to cram even more information in the image. This would give a larger impact on the colors of the image, but probably not too much. I plan to make it a user option.  
A better way to save the information would be to insert the message in random or set gaps. This would make it more difficult to retrieve the information for an advesary, but it presents the challenge on how the intended recipient would read the message.


# Example commands
## These commands are for inserting information in images  
        python stego.py -i [imagename.png] -m ["Message"]
        python stego.py -i [imagename.png] -mf [/path/to/messagefile]
### Example:
        python stego.py -i myimage.png -m "Secret message"
        python stego.py -i myimage.png -mf mymessage.txt


## These commands are for extracting information from images  
        python stego.py -e [/path/to/file/you/want/extracted]
        python stego.py -e [/path/to/file/you/want/extracted] -ef
### Example: 
        python stego.py -e mysecretimage.png
        python stego.py -e mysecretimage.png -ef
  
