from bitstring import BitArray
import json
import requests
charlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','.',',','(',')']

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
            case _:
                binry = binry + "{0:b}".format(ord(x) - 96).zfill(5)       
    return binry 

def writefile(binarys, filename):
    binary_file = open(filename, 'wb')
    b = BitArray(bin=binarys)
    b.tofile(binary_file)
    binary_file.close()
    
def wikifind(webname):
    x = requests.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=1&explaintext=1&titles=' + webname)
    wikitext = x.json()
    for k,item in wikitext["query"]["pages"].items():
        return item['extract']
        
def remover(text):

    ''.join([i for i in text if i in aminoacids])
    

strings = input("Enter a string: ")
writefile(bitify(wikifind(strings)), "test.bin")
           


