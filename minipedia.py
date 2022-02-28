from bitstring import BitArray
import json
import requests
import re
import unidecode
import argparse

charlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.',',','(',')'," "]

pages=[[],[],[]]

symboldict = {'@' : 'at','!' : '.','&' : 'and','=' : 'equals','+' : 'plus', '-' : 'minus', '0' : 'zero', '1' : 'one', '2' : 'two', '3' : 'three', '4' : 'four', '5' : 'five', '6' : 'six', '7' : 'seven', '8' : 'eight', '9' : 'nine'}
words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

iscapital = False
istitle = True

pages=[]
cont=""
gaplimit=""
filename=""

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
    binary_file = open(filename+".5bf", 'ab')
    b = BitArray(bin=binarys)
    b.tofile(binary_file)
    binary_file.close()
    
def overwritefile(binarys, filename):
    binary_file = open(filename+".5bf", 'wb')
    b = BitArray(bin=binarys)
    b.tofile(binary_file)
    binary_file.close()

#Downloads webpage off wikipedia, set link for now
def wikifind(webname):
    x = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=1&explaintext=1&titles=' + webname)
    wikitext = x.json()
    for k,item in wikitext["query"]["pages"].items():
        return item['extract']

#Grab all pages starting from forward. gaplimit must be a given as a string.
def wikigraball(forward, gaplimit):
    x = requests.get('https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&generator=allpages&exintro=1&explaintext=1&&gapcontinue='+forward+'&gapfilterredir=nonredirects&gaplimit='+gaplimit)
    wikitext = x.json()
    for k,item in wikitext["query"]["pages"].items():
        pages[0].append(item['title'])
        pages[1].append(item['extract'])
        pages[2].append(wikitext['continue']['continue'])
    return pages

def addtitle(title):
    text = bitify(remover(symboltoplaintext(accenttochar(title.lower()))) + "#" + remover(symboltoplaintext(accenttochar(capitals(wikifind(title))))) + "##")
    return text

def addmultititle(title,inputtext):
    text = bitify(remover(symboltoplaintext(accenttochar(title.lower()))) + "#" + remover(symboltoplaintext(accenttochar(capitals(inputtext)))) + "##")
    return text

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

def debitify(filename):
    file = open(filename+".5bf", "rb")
    byte = file.read(1) #add while byte:
    fullnum = ""
    fullstr = ""
    while byte:
        checknum = "{0:b}".format(int.from_bytes(byte, "little")).zfill(8) #reads byte as integer
        fullnum = fullnum + checknum
        if (len(fullnum) > 39):
            fullnum2 = int(fullnum, 2)
            for x2 in range(8):
                fullstr = fullstr + bitcheck(readbits40(fullnum2,x2*5,5))
            fullnum = ""
        byte = file.read(1) #new byte 
    return fullstr

def readbits40(var,start,amount):
    var = var >> (40-(start+amount)) & (int((40-amount)*"0"+amount*"1",2)) #reads amount amount of bits from position start starting from 0
    return var

def bitcheck(fivebit):
    global iscapital
    global istitle
    match fivebit: #decodes integer to character
        case 0:
            return " "
        case 27:
            return "."
        case 28:
            return ","
        case 29:
            return "("
        case 30:
            return ")"  
        case 31:
            if (istitle == True):
                istitle = False
                return "\n\n"
            iscapital = True
            return ""               
        case _:
            if (iscapital == False):
                return chr(fivebit+96) 
            else:
                iscapital = False
                return chr(fivebit+64)
    return binry 

def encoder(cont):
    pages=wikigraball(cont,gaplimit)
    for i in range(len(pages[0])):
        writefile(addmultititle(pages[0][i],pages[1][i]),filename)
    cont=pages[2][0]
    return cont

def decode():
    filename = input("Enter article name: ")
    print(debitify(filename))

parser=argparse.ArgumentParser()
parser.parse_args()
