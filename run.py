import encoder
import decoder

pages=[]
cont=""
gaplimit="80"
filename="wiki"

pages=encoder.wikigraball(cont,gaplimit)
for i in range(len(pages[0])):
    encoder.writefile(encoder.addmultititle(pages[0][i],pages[1][i]),filename)
cont=pages[2][0]

def decode():
    filename = input("Enter article name: ")
    print(decoder.bitify(filename))

decode()
