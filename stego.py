"""
Todo:
Make it possible to input other messagetypes. (Other images, videos, ...)
"""

import PIL.Image as Image
import argparse
import string
from textwrap import wrap
from os.path import splitext
from sys import exit


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
    
    #Checks if the message is longer than the image can support. If it is, terminate the program
    if len(listofRGB)*3 < len(message_binary(message)):
        print(f"ERROR\nMessage is too long.\nMessage length in binary:\t{len(message_binary(message))}\nLength of RGB pixel values:\t{len(listofRGB)*3}")
        exit()        
    
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
def read_stego_image(path, output_message=False):
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
    
    if output_message:
        with open("output_message.txt", "w") as output_file:
            output_file.write(str("".join(text)))  
    else:
        print(str("".join(text)))
 
   
#Checks if filetype is supported    
def checkFile(path):
    filename, extension = splitext(path)
    if extension.lower() != ".png":
        print(f"{extension} is not supported\nOnly PNG is supported!")
        exit()


#Command-line arguments
parser = argparse.ArgumentParser(description="Hides and extracts text in images")

parser.add_argument("-i", help="Input image (Requires [-m] or [-mf]), Example: [stego.py -i myfile.png -m \"MyMessage\"]", action="store", metavar='')
parser.add_argument("-m", help="Message string (Must be enclosed in quotation marks and in the ASCII printable set)", action="store", metavar='')
parser.add_argument("-mf", help="Message file, Example: [stego.py -i image.png -mf message.txt]", action="store", metavar='')
parser.add_argument("-e", help="Extract message from image, Example: [stego.py -e image.png]", action="store", metavar='')
parser.add_argument("-ef", help="Extract message from image to file (Don't set file), Example: [stego.py -e image.png -ef]", action="store_true")

args = parser.parse_args()

if args.i and args.m:
    path = args.i
    checkFile(path)
    string = args.m
    message = inserted_message(string)
    message_binary(message)
    insert_message_to_image(path)
    
elif args.i and args.mf:
    path = args.i
    checkFile(path)
    string = args.mf
    with open(string, "r") as message_file:
        string = message_file.read()
    message = inserted_message(string)
    message_binary(message)
    insert_message_to_image(path)

elif args.e and args.ef:
    path = args.e
    checkFile(path)
    read_stego_image(path, args.ef)
    
elif args.e:
    path = args.e
    checkFile(path)
    read_stego_image(path)
    
else:
    print("Error\nTry again")
