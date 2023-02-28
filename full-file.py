import sys
import re
import unicodedata

#STRING PARSING
charlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'," ",".",":"]

pages=[[],[],[]]

symboldict = {'@' : 'at','!' : '.','&' : 'and','=' : 'equals','+' : 'plus', '-' : 'minus', '0' : 'zero', '1' : 'one', '2' : 'two', '3' : 'three', '4' : 'four', '5' : 'five', '6' : 'six', '7' : 'seven', '8' : 'eight', '9' : 'nine'}
words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    
#Removes all letters not part of the 5 bits
def remover(text):
    text = ''.join([i for i in text if i in charlist])
    return text

#Turns all characters into lowercase
def capitals(text1):   
    return re.sub(r"([A-Z])", r"#\1", text1).lower()

#Takes a string with accented text in it and turns the accented characters into ascii text using unidecode
def accenttochar(text2):
    return ''.join(c for c in unicodedata.normalize('NFD', text2)
                  if unicodedata.category(c) != 'Mn')

def symboltoplaintext(text3):
    for word, initial in symboldict.items():
        text3 = text3.replace(word.lower(), initial)
    return text3

def encode_text(full_text):
    return remover(symboltoplaintext(capitals(accenttochar(full_text))))
    

def translate_file(filename):
    char_array = ["e","t","a","o","i","n","s","h","r","d","l","\n",":",","," "]
    char_array2 = ["w","f","g","y","p","b","v","k","j","x","q","z",".","c","u","m"]
    
    is_2nd = False
    first_byte = True
    str = ""
    
    with open(filename, "rb") as f:
        while (byte := f.read(1)):
            if ((ord(byte) >> 4) != 15):
                if (is_2nd == False):
                    str += char_array[ord(byte) >> 4]
                else:
                    str += char_array2[ord(byte) >> 4]
                    is_2nd = False
            else:
                if (is_2nd == False):
                    is_2nd = True
                else:
                    str += char_array2[ord(byte) >> 4]
                    is_2nd = False
            if ((ord(byte) & 15) != 15):
                if (is_2nd == False):
                    str += char_array[ord(byte) & 15]
                else:
                    str += char_array2[ord(byte) & 15]
                    is_2nd = False
            else:
                if (is_2nd == False):
                    is_2nd = True
                else:
                    str += char_array2[ord(byte) >> 4]
                    is_2nd = False
            
    return str

def convert_text(title, text, mode):
    char_array = [[1,2],[2,5],[2,13],[1,9],[1,0],[2,1],[2,2],[1,7],[1,4],[2,8],[2,7],[1,10],[2,15],[1,5],[1,3],[2,4],[2,10],[1,8],[1,6],[1,1],[2,14],[2,6],[2,0],[2,9],[2,3],[2,11]]

    first_byte = True
    byte = 0
    byte_list = []
    double_str = ""
    flag = False
    x = 0
    #debug_text = ""

    file = open(title, mode)
    #print(text[x])
    while (x < len(text)):
        if (text[x] == ":"):
            #debug_text += ":"
            temp_array = [1,12]
        elif (text[x] == ","):
            #debug_text += ","
            temp_array = [1,13]
        elif (text[x] == "#"):
            #debug_text += "\n"
            temp_array = [1,11]
        elif (text[x] == " "):
            #debug_text += " "
            temp_array = [1,14]
        elif (text[x] == "."):
            #debug_text += "."
            temp_array = [2,12]
        else:
            #debug_text += text[x]
            temp_array = char_array[ord(text[x]) - 97]
        
        
        if (temp_array[0] == 2):
            byte = byte | 15
            if (first_byte == True):
                byte = byte << 4
                first_byte = False
            else:
                file.write(bytes([byte]))
                byte = 0
                first_byte = True

        byte = byte | temp_array[1]
        if (first_byte == True):
            byte = byte << 4
            first_byte = False
        else:
            file.write(bytes([byte]))
            byte = 0
            first_byte = True
        x += 1

    #print(debug_text)
    #if (first_byte == False):
        #file.write(bytes([byte]))
    file.close()

def convert_file(new_file,old_file):
    with open(old_file) as topo_file:
        for line in topo_file:
            convert_text(new_file,encode_text(line)+"#","ab")
    
def translate_it(fourbf_file, txt_file):
    with open(txt_file, "w") as text_file:
        text_file.write(translate_file(fourbf_file))
    
def help():
    print('4BF COMPRESSION\n')
    print('Compressing Text:')
    print('full-file.py -c bee.4bf "hi guys" (not working?)')
    print('Compresses "hi guys" and put it into bee.4bf\n')
    print('Compressing A Text File:')
    print('full-file.py -c -f bee.txt bee.4bf')
    print('Compresses the contents of bee.txt and put it into bee.4bf\n')
    print('Decompressing A .4BF file:')
    print('full-file.py -d bee.4bf')
    print('Prints the contents of bee.4bf\n')
    print('Decompressing A .4BF file to a .TXT file:')
    print('full-file.py -d -f bee.4bf bee.txt')
    print('Puts the content of bee.4bf into bee.txt\n')
    print('Help:')
    print('full-file.py -h')
    print('Prints this menu')

try:
    if (sys.argv[1] == "-c"):
        if (sys.argv[2] == "-f"):
            #full-file.py -c -f bee.txt bee.4bf
            convert_file(sys.argv[4],sys.argv[3])
        else:
            #full-file.py -c bee.4bf "hi guys"
            convert_text(sys.argv[3],sys.argv[4],"wb")
    elif (sys.argv[1] == "-d"):
        if (sys.argv[2] == "-f"):
            #full-file.py -d -f bee.4bf bee.txt
            translate_it(sys.argv[3],sys.argv[4])
        else:
            #full-file.py -d bee.4bf
            print(translate_file(sys.argv[2]))
    elif (sys.argv[1] == "-h"):
        help()
    else:
        help()
except:
    help()
