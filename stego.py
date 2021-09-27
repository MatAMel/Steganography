"""
Todo:
Make it possible to retrieve message from file
Check if message is longer than image
"""


import PIL.Image as Image
from textwrap import wrap
import sys
import string
from os.path import splitext

#Message from user
def inserted_message(string):
    message = message_binary(string)
    for x in range(0, len(message)):
        message[x] = message[x][2:]
    return "".join(message)


#Converts message string to binary
def message_binary(message):
    binary_message_list = []
    for b in bytearray(message, "ascii"):
        binary_message_list.append(format(int(bin(b), 2), "#010b"))
    return binary_message_list


#Inserts the message into the picture provided by the user
def insert_message_to_image(path):
    img = Image.open(path).convert('RGB')
    width, height = img.size

    listofRGB = []
    #Scans from left to right, jumping down 1 pixel after each sweep
    for h in range(0, height):
        for w in range(0, width):
            listofRGB.append(img.getpixel((w, h))) 
            
    #Make list of list
    list_listofRGB = []
    for x in listofRGB:
        list_listofRGB.append(list(x))

    index = 0
    for x in list_listofRGB:
        for i in range(0, 3):
            binary = bin(x[i])
            try:
                x[i] = int(binary[:-1] + message[index], 2)
                if len(message) > index:         
                    index += 1
            except IndexError:
                break
    
    #Make tuple list
    final_listRGB = []
    for x in list_listofRGB:
        final_listRGB.append(tuple(x))

    #Creats the new image based on the changed list of rgb tuples
    im2 = Image.new(img.mode, img.size)
    im2.putdata(final_listRGB)
    im2.save("hidden_image.png")


#Extracts the hidden message in the image
def read_stego_image(path):
    img = Image.open(path).convert('RGB')
    width, height = img.size
    listofRGB = []
    
    for h in range(0, height):
        for w in range(0, width):
            listofRGB.append(img.getpixel((w, h)))
    
    list_listofRGB = []
    for x in listofRGB:
        list_listofRGB.append(list(x))
    
    binary_message = []
    for x in list_listofRGB:
        for i in range(0, 3):
            binary_message.append(bin(x[i])[-1])
    
    #Joins bits to one long str, and then splits it into 8 bits in a list
    binary_message = wrap("".join(binary_message[:]), 8)     
    
    text = []  
    for x in binary_message:
        text.append(chr(int(x, 2)))
    
    #Removes all of the charachters not in the printable ASCII char set
    index = 0
    for x in text:
        if x not in string.printable:
            del text[index:]
        index += 1
    
    print(str("".join(text)))
    with open("decoded_message.txt", "w", encoding="ascii") as decoded_txt:
        #decoded_txt.write(str("".join(text).encode("ascii")))
        decoded_txt.write(str("".join(text)))
    decoded_txt.close()
    

def checkFile(path):
    filename, extension = splitext(path)
    if extension != ".png":
        print(f"{extension} is not supported\nOnly PNG is supported!")
        sys.exit()


#Takes commands from command-line
try:
    if len(sys.argv) == 1:
        print("No argument provided!\nEnter stego.py --help for help")
        
    elif "--help" == sys.argv[1]:
        print("""
        Steganography software to hide information in PNG images.
        Commands:\n
        --help Explanations for commands
        -e Extract hidden message from image
        -i Input image to hide the secret message in
        -m The message you want to hide (MUST be in quotation marks AND from the ASCII printable set)
        The new image vil be named "hidden_image.png" and be placed in the same directory as the original image\n
        python stego.py -e [file to extract]
        Example: python stego.py -e mysecretimage.png\n\n
        python stego.py -i [input file] -m ["Message to hide in image"]
        Example: python stego.py -i catimage.png -m "This text will be hidden"\n
        """)

    elif "-e" == sys.argv[1]:
        path = sys.argv[2]
        checkFile(path)
        read_stego_image(path)

    elif "-i" == sys.argv[1] and "-m" == sys.argv[3]:
        path = sys.argv[2]
        checkFile(path)
        string = sys.argv[4]
        message = inserted_message(string)
        message_binary(message)
        insert_message_to_image(path)
    else:
        print("Invalid argument. Try again\nEnter stego.py --help for help")
except IndexError:
    print("Invalid argument. Try again\nEnter stego.py --help for help")