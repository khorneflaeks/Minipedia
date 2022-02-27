import encoder
import decoder

pages=[]
cont=""
gaplimit="80"

def encode(cont,gaplimit)
    pages=encoder.wikigraball(cont,gaplimit)

    for i in range(len(pages[0])):
        text=encoder.bitify(encoder.symboltoplaintext(encoder.accenttochar(encoder.capitals(encoder.remover(pages[1][i])))))
        encoder.writefile(text,pages[0][i])
    return pages[2]
