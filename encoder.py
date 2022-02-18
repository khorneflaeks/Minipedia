from bitstring import BitArray
import json
import requests
import re
import unidecode

charlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.',',','(',')']

#Turns 8bit binary into 5bit
def bitify(inputs):
    binry = ""
    testval = 0
    for x in inputs.lower():
        match x:
            case " ":
                binry = binry + "00000"
            case ".":
                binry = binry + "11011"
            case ",":
                binry = binry + "11100"
            case "(":
                binry = binry + "11101"    
            case ")":
                binry = binry + "11110"  
            case "#":
                binry = binry + "11111"                 
            case _:
                binry = binry + "{0:b}".format(ord(x) - 96).zfill(5)       
    return binry 

#Writes input to file with filename
def writefile(binarys, filename):
    binary_file = open(filename, 'wb')
    b = BitArray(bin=binarys)
    b.tofile(binary_file)
    binary_file.close()
    
#Downloads webpage off wikipedia, set link for now
def wikifind(webname):
    x = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=1&explaintext=1&titles=' + webname)
    wikitext = x.json()
    for k,item in wikitext["query"]["pages"].items():
        return item['extract']
        
#IDK, pls explain @pugalotl
def remover(text):
    text = ''.join([i for i in text if i in charlist])
    return text

#Turns all characters into lowercase
def capitals(text1):   
    return re.sub(r"(\w)([A-Z])", r"\1#\2", text1).lower()

#Takes a string with accented text in it and turns the accented characters into ascii text using unidecode
def accenttochar(text2);
    return unidecode.unidecode(text2)

strings = input("Enter a string: ")
writefile(bitify(remover(capitals(wikifind(strings)))), "test.bin")
           


