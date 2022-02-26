from bitstring import BitArray
iscapital = False
istitle = True

def bitify(inputs):
    file = open("test.bin", "rb") #filename
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

strings = input("Enter a string: ")
print(bitify(strings))
           


