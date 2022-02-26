from bitstring import BitArray

def bitify(inputs):
    file = open("test.bin", "rb") #filename
    byte = file.read(1)
    while byte:
        checknum = int.from_bytes(byte, "little") #reads byte as integer
        byte = file.read(1) #new byte     

def readbits(var,start,amount):
    var = var >> (8-(start+amount)) & (int((8-amount)*"0"+amount*"1",2)) #reads amount amount of bits from position start starting from 0
    return var

def bitcheck(fivebit):
    match fivebit: #decodes integer to character
        case "0":
            return " "
        case "27":
            return "."
        case "28":
            return ","
        case "29":
            return "("
        case "30":
            return ")"  
        case "31":
            return "#"               
        case _:
            return chr(fivebit+96)     
    return binry 

strings = input("Enter a string: ")
print(bitify(strings))
           


