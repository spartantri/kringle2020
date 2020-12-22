#!/bin/env python3
from Crypto.Hash import MD5, SHA256

frosted="frosted129459.block"

#offsets
index = 16
nonce = 16
pid = 16
rid = 16
doc_count = 1
score = 8
sign = 1

naughtyoffset=index+nonce+pid+rid+doc_count+score
pdfattackoffset=265

#original values
o73=b'1'
o137=b'\xd6'
o265=b'2'
o329=b'\x1c'
#desired values
d73=b'0'
d137=b'\xd7'
d265=b'3'
d329=b'\x1b'

print("MD5 collisions")
print("We can modify a byte value up or down and maintain the same MD5")
print("if we modify the byte at 64 bytes in the opposite direction\n")
print("Lets fix the Naughty byte first")
print("Naughty byte is %d byte long at : %d" % (sign,naughtyoffset))
print("Nice is 1, Naughty is 0, change from 1 to 0")
print("Adjust collision at offset %d (%d + 64) from whatever value to +1" % (naughtyoffset+64, naughtyoffset))

with open(frosted,"rb") as target:
    original=target.read()

oSHA256=SHA256.new(original).hexdigest()
oMD5=MD5.new(original).hexdigest()
print("Original MD5 and SHA256 :",oMD5, oSHA256)

offset=naughtyoffset
naughty=original[0:offset] + d73 + original[offset+1:offset+64] + d137 + original[offset+64+1:]
nSHA256=SHA256.new(naughty).hexdigest()
nMD5=MD5.new(naughty).hexdigest()
if oMD5==nMD5:
    print("Naughty byte fixed!")
    print("Naughty MD5 and SHA256 :",nMD5, nSHA256)

print("\nLets fix the the PDF attack changing the reference to display the orignal PDF page")
print("PDF attack byte is 1 byte long at : %d" % (pdfattackoffset))
print("Change the page reference from 2 0 R to 3 0 R")
print("Adjust collision at offset %d (%d + 64) from whatever value to +1" % (pdfattackoffset+64, pdfattackoffset))

offset=pdfattackoffset
naughty=naughty[0:offset] + d265 + naughty[offset+1:offset+64] + d329 + naughty[offset+64+1:]
pSHA256=SHA256.new(naughty).hexdigest()
pMD5=MD5.new(naughty).hexdigest()
if oMD5==pMD5:
    print("PDF attack byte fixed!!!\n")
    print("SOLUTION MD5:%s and SHA256:%s" % (pMD5, pSHA256))
