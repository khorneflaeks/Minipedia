from bitstring import BitArray

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
    print(binry)        
    return binry 

def writefile(binarys, filename):
    binary_file = open(filename, 'wb')
    b = BitArray(bin=binarys)
    b.tofile(binary_file)
    binary_file.close()

strings = input("Enter a string: ")
writefile(bitify(strings), "test.bin")
           


