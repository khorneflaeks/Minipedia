import encoder
import decoder

pages=[]
cont=""
gaplimit="80"

pages=encoder.wikigraball(cont,gaplimit)
for i in range(len(pages[0])):
    text=encoder.bitify(encoder.remover(encoder.symboltoplaintext(encoder.accenttochar(encoder.capitals(pages[1][i])))))
    encoder.writefile(text,pages[0][i])
cont=pages[2][0]

def decode():
    filename = input("Enter article name: ")
    print(decoder.bitify(filename))

decode()
