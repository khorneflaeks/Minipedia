from bitstring import BitArray
import json
import requests
import re
import unidecode

charlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.',',','(',')'," "]

symboldict = {'@' : 'at','!' : '.','&' : 'and','=' : 'equals','+' : 'plus', '-' : 'minus', '0' : 'zero', '1' : 'one', '2' : 'two', '3' : 'three', '4' : 'four', '5' : 'five', '6' : 'six', '7' : 'seven', '8' : 'eight', '9' : 'nine'}
words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    
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
        
#Removes all letters not part of the 5 bits
def remover(text):
    text = ''.join([i for i in text if i in charlist])
    return text

#Turns all characters into lowercase
def capitals(text1):   
    return re.sub(r"([A-Z])", r"#\1", text1).lower()

#Takes a string with accented text in it and turns the accented characters into ascii text using unidecode
def accenttochar(text2):
    return unidecode.unidecode(text2)

def symboltoplaintext(text3):
    for word, initial in symboldict.items():
        text3 = text3.replace(word.lower(), initial)
    return text3
    
def addtitle(title):
    text = bitify(remover(accenttochar(title.lower())) + "#" + remover(symboltoplaintext(accenttochar(capitals(wikifind(title))))) + "##")
    return text

strings = input("Enter a string: ")
writefile(addtitle(strings), "test.bin")
