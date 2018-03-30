import sys
import math
import numpy as np
import zlib
import bitarray as ba
import struct
from numpy import vsplit
from scipy import misc


# Argumenti deflate.py <SLIKA> <FILTER_TYPE> <BUFFER_SIZE>

def int2bin(i,len):
    s = ''
    j = 0
    while j<len:
        if i & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        i >>= 1
        j += 1
    return s

def generateHuffman():
    huffman = {}
    for i in range(0,144):
        huffman[i] = int(48 + i)
    for i in range(144,256):
        huffman[i] = int(400 + i - 144)
    for i in range(256,280):
        huffman[i] = int(i - 256)
    for i in range(280,288):    
        huffman[i] = int(192+i-280)
    return huffman

def getHuffman(num,huffman):
    if(num >= 0 and num <= 143):
        return int2bin(huffman[num],8)
    elif(num >= 144 and num <= 255):
        return int2bin(huffman[num],9)
    elif(num >= 256 and num <= 279 ):
        return int2bin(huffman[num],7)
    elif(num >= 280 and num <= 287):
        return int2bin(huffman[num],8)
    else:
        print("ERROR")
        return "err"

def getLenCode(num,huffman):
    if(num >= 3 and num <= 10):
        return getHuffman(257 - 3 + num,huffman)
    elif(num >= 11 and num <= 12):
        return getHuffman(265,huffman) + int2bin((num+1)%2,1)
    elif(num >= 13 and num <= 14):
        return getHuffman(266,huffman) + int2bin((num+1)%2,1)
    elif(num >= 15 and num <= 16):
        return getHuffman(267,huffman) + int2bin((num+1)%2,1)
    elif(num >= 17 and num <= 18):
        return getHuffman(268,huffman) + int2bin((num+1)%2,1)
    elif(num >= 19 and num <= 22):
        return getHuffman(269,huffman) + int2bin((num+1)%4,2)[::-1]
    elif(num >= 23 and num <= 26):
        return getHuffman(270,huffman) + int2bin((num+1)%4,2)[::-1]
    elif(num >= 27 and num <= 30):
        return getHuffman(271,huffman) + int2bin((num+1)%4,2)[::-1]
    elif(num >= 31 and num <= 34):
        return getHuffman(272,huffman) + int2bin((num+1)%4,2)[::-1]
    elif(num >= 35 and num <= 42):
        return getHuffman(273,huffman) + int2bin((num+5)%8,3)[::-1]
    elif(num >= 43 and num <= 50):
        return getHuffman(274,huffman) + int2bin((num+5)%8,3)[::-1]
    elif(num >= 51 and num <= 58):
        return getHuffman(275,huffman) + int2bin((num+5)%8,3)[::-1]
    elif(num >= 59 and num <= 66):
        return getHuffman(276,huffman) + int2bin((num+5)%8,3)[::-1]
    elif(num >= 67 and num <= 82):
        return getHuffman(277,huffman) + int2bin((num+13)%16,4)[::-1]
    elif(num >= 83 and num <= 98):
        return getHuffman(278,huffman) + int2bin((num+13)%16,4)[::-1]
    elif(num >= 99 and num <= 114):
        return getHuffman(279,huffman) + int2bin((num+13)%16,4)[::-1]
    elif(num >= 115 and num <= 130):
        return getHuffman(280,huffman) + int2bin((num+13)%16,4)[::-1]
    elif(num >= 131 and num <= 162):
        return getHuffman(281,huffman) + int2bin((num+29)%32,5)[::-1]
    elif(num >= 163 and num <= 194):
        return getHuffman(282,huffman) + int2bin((num+29)%32,5)[::-1]
    elif(num >= 195 and num <= 226):
        return getHuffman(283,huffman) + int2bin((num+29)%32,5)[::-1]
    elif(num >= 227 and num <= 258):
        return getHuffman(284,huffman) + int2bin((num+29)%32,5)[::-1]
    else:
        print("ERROR")
        return "err"

def getDistCode(num):
    if(num >= 1 and num <= 4):
        return int2bin(num-1,5)
    elif(num >= 5 and num <= 6):
        return int2bin(4,5)+int2bin((num+1)%2,1)
    elif(num >= 7 and num <= 8):
        return int2bin(5,5)+int2bin((num+1)%2,1)
    elif(num >= 9 and num <= 12):
        return int2bin(6,5)+int2bin((num+3)%4,2)[::-1]
    elif(num >= 13 and num <= 16):
        return int2bin(7,5)+int2bin((num+3)%4,2)[::-1]
    elif(num >= 17 and num <= 24):
        return int2bin(8,5)+int2bin((num+7)%8,3)[::-1]
    elif(num >= 25 and num <= 32):
        return int2bin(9,5)+int2bin((num+7)%8,3)[::-1]
    elif(num >= 33 and num <= 48):
        return int2bin(10,5)+int2bin((num+15)%16,4)[::-1]
    elif(num >= 49 and num <= 64):
        return int2bin(11,5)+int2bin((num+15)%16,4)[::-1]
    elif(num >= 65 and num <= 96):
        return int2bin(12,5)+int2bin((num+31)%32,5)[::-1]
    elif(num >= 97 and num <= 128):
        return int2bin(13,5)+int2bin((num+31)%32,5)[::-1]
    elif(num >= 129 and num <= 192):
        return int2bin(14,5)+int2bin((num+63)%64,6)[::-1]
    elif(num >= 193 and num <= 256):
        return int2bin(15,5)+int2bin((num+63)%64,6)[::-1]
    elif(num >= 257 and num <= 384):
        return int2bin(16,5)+int2bin((num+127)%128,7)[::-1]
    elif(num >= 385 and num <= 512):
        return int2bin(17,5)+int2bin((num+127)%128,7)[::-1]
    elif(num >= 513 and num <= 768):
        return int2bin(18,5)+int2bin((num+255)%256,8)[::-1]
    elif(num >= 769 and num <= 1024):
        return int2bin(19,5)+int2bin((num+255)%256,8)[::-1]
    #TO DO: Zavrsi do 2^31-1
    else:
        print("ERROR")
        return "err"
def imgFilter(scanline, F_TYPE):
    #TO DO: Dodaj sve tipove filtera
    if(F_TYPE == 0):
        return
    if(F_TYPE == 1):
        n = scanline.shape[0]
        for j in range (n-1,0,-1):
            scanline[j] -= scanline[j-1]
    # Formiram input za Deflate scanline = F_TYPE R G B R G B R G B ... 
def mergeScanlines(scanlines, F_TYPE):
    mSize = len(scanlines)
    sShape = scanlines[0].shape
    slList = []

    for i in range (0,mSize):
        newScanline = np.zeros(sShape[1]*3+1,dtype = np.uint8)
        newScanline[0] = F_TYPE
        for j in range (0,sShape[1]):
            newScanline[3*j+1] = scanlines[i][0,j,0]
            newScanline[3*j+2] = scanlines[i][0,j,1]
            newScanline[3*j+3] = scanlines[i][0,j,2]
        slList.append(newScanline)
    return slList

def findInWindow(subArray, searchBuffer,startSearchLen):
    n = len(searchBuffer)
    m = len(subArray)
    #print(subArray)
    exists = 0
    location = 0;  
    v_len = 0
    for i in range(n-m,-1,-1):
        if searchBuffer[i:i+m] == subArray:
            exists = 1
            location = startSearchLen-i
            v_len = len(subArray)
            #print(subArray)
            #print(location)
            #print(v_len)
            break
    return [exists, location, v_len]


    # Vraca niz sa 3 moguce vrednosti Literal, Duzina, Udaljenost
def deflate(scanline, searchWindowL, outputPNG, isLast, huffman,outputBitStream):

    #Zlib stream header
    #cINF = int(math.log2(searchWindowL)-8)
    #cINFBin = int2bin(cINF,4)
             #|--CINF-|-CM-|
    #CMF = int(cINFBin+'1000', 2)

    #FLG = int('01000000', 2)
    #FLG += 31 - (CMF<<8 + FLG)%31

    #Za racunanje duzine
    startLoc = outputPNG.tell()

    #zLibHeaderArray = bytearray([CMF,FLG])
    #Prva tri bita svakog bloka

    if(isLast != 1):
        outputBitStream += ba.bitarray('010')
    else:
        outputBitStream += ba.bitarray('110')

    resultArray = np.uint16(scanline[0])
    searchBuffer = [scanline[0]]

    outputBitStream += ba.bitarray(getHuffman(scanline[0],huffman))

    i = 1
    n = len(scanline)
    while (i < n):
        #Start index
        Is = i - searchWindowL
        if(Is < 0):
            Is = 0
        #End Index
        Ie = n     
        searchBuffer = list(scanline[Is:(i)])
        aheadBuffer = list(scanline[i:Ie])
        startSearchLen = len(searchBuffer)
        #Prvi element
        searchedEle = [aheadBuffer[0]]
        ELV = findInWindow(searchedEle,searchBuffer,startSearchLen)

        if ELV[0]:
            searchBuffer.append(searchedEle[0])

        num_br = 1

        endOfRow = 0


        # Trazim dok god imam brojeva u bufferu
        if len(aheadBuffer) > num_br:
            newSearch = searchedEle
            n_ex = ELV[0]
            while n_ex == 1:
                num_br += 1
                if(num_br <= len(aheadBuffer)):
                    newSearch.append(aheadBuffer[num_br-1])

                    nELV = findInWindow(newSearch, searchBuffer,startSearchLen)

                    n_ex = nELV[0]

                    if(nELV[2] == 256):
                        break

                    if(nELV[0] == 1):
                        searchBuffer.append(aheadBuffer[num_br-1])

                else:
                    endOfRow = 1
                    if(nELV[0] == 1):
                        searchBuffer.pop()
                    break
        
        if(num_br > 1 and endOfRow == 0):
            num_br -= 1
            searchBuffer = searchBuffer[:len(searchBuffer)-1]
        
        # Ako je postojao pre 
        if (ELV[0] == 1):
            newEle = aheadBuffer[0:num_br]
            rELV = findInWindow(newEle, searchBuffer[0:len(searchBuffer)],startSearchLen)
            if (rELV[2] > 2):
                i += rELV[2]
                resultArray = np.append(resultArray,[rELV[2],rELV[1]])
                #print(rELV[2])
                outputBitStream += ba.bitarray(getLenCode(rELV[2],huffman))
                outputBitStream += ba.bitarray(getDistCode(rELV[1]))
               
            else:
                i += rELV[2]
                resultArray = np.append(resultArray,aheadBuffer[0:num_br])
                if(rELV[2] == 1):
                    outputBitStream += ba.bitarray(getHuffman(aheadBuffer[0],huffman))
                else:
                    outputBitStream += ba.bitarray(getHuffman(aheadBuffer[0],huffman))
                    outputBitStream += ba.bitarray(getHuffman(aheadBuffer[1],huffman))
        else:
        #Ako nije
            i += 1
            resultArray = np.append(resultArray, searchedEle)
            outputBitStream += ba.bitarray(getHuffman(int(searchedEle[0]),huffman))

    #Oznaka kraja bloka
    outputBitStream += ba.bitarray(getHuffman(256,huffman))
    #print(resultArray)
    #Za racunanje duzine
    #print(scanline)

    endLoc = outputPNG.tell() 
    #outputPNG.seek(-endLoc+startLoc,1)
    #print(outputBitStream)
    #print(bytes(outputPNG.read(endLoc-startLoc)).hex())
    #print(resultArray)
    return endLoc-startLoc 
         


source = sys.argv[1]
filterType = int(sys.argv[2])
windowSize = int(sys.argv[3])



image = misc.imread(source)
imSize = image.shape
scanCount = imSize[0]

channelCount = imSize[2]

huffman = generateHuffman()
#Delim sirinu na 4 byte-a
w1, w2, w3, w4 = (imSize[1] & 0xFFFFFFFF).to_bytes(4, 'big')
h1, h2, h3, h4 = (imSize[0] & 0xFFFFFFFF).to_bytes(4, 'big')
scanlines = vsplit(image,imSize[0])

outputPNG = open("output.png", "wb+")

              #|-----PNG SIGNATURE ----|--LEN --|---IHDR ---|---WIDTH---|--HEIGHT --|D|C|M|F|I|
headerBytes = [137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,w1,w2,w3,w4,h1,h2,h3,h4,8,2,0,0,0]

headerData = bytearray([73,72,68,82,w1,w2,w3,w4,h1,h2,h3,h4,8,2,0,0,0])
#print(headerBytes)
#print(headerData)
dataLenPlace = len(headerBytes)
headerByteArray = bytearray(headerBytes)
outputPNG.write(headerByteArray)

iHDRCRC32 = zlib.crc32(headerData) 
#print(hex(iHDRCRC32))
crc1, crc2, crc3, crc4 = (iHDRCRC32 & 0xFFFFFFFF).to_bytes(4, 'big')
#print(int2bin(crc1,8)+int2bin(crc2,8) + int2bin(crc3,8) + int2bin(crc4,8))
iHDRCRC32Array = bytearray([crc1, crc2, crc3, crc4])
outputPNG.write(iHDRCRC32Array)

#TO DO: Postavi Len na broj byte-ova
iDATLenLocation = outputPNG.tell()

           #|--LEN--|---IDAT ---|
iDATBtyes = [0,0,0,0,73,68,65,84]
iDATByteArray = bytearray(iDATBtyes)
outputPNG.write(iDATByteArray)

for sl in scanlines:
    for i in range(0,channelCount):
            imgFilter(sl[0,:,i],filterType)

           
newScanlines = mergeScanlines(scanlines,filterType)
iDATStart = outputPNG.tell()


zLibHeaderArray = bytearray([120,1])
outputPNG.write(zLibHeaderArray)

uncompressedArray  = bytearray()
outputBitStream = ba.bitarray(endian = 'little')

for i in range(0,len(newScanlines)):
        print(i)
        if(i != (len(newScanlines)-1)):
            #print(newScanlines[i])
            deflate(newScanlines[i],windowSize,outputPNG,0,huffman,outputBitStream)
            uncompressedArray += bytearray(newScanlines[i])
        else:
            #print(newScanlines[i])
            deflate(newScanlines[i],windowSize,outputPNG,1,huffman,outputBitStream)
            uncompressedArray += bytearray(newScanlines[i])

#print(len(uncompressedArray))

outputBitStream.tofile(outputPNG)

adler32Value = zlib.adler32(bytearray(uncompressedArray))
a1, a2, a3, a4 = (adler32Value & 0xFFFFFFFF).to_bytes(4, 'big')
adler32Array = bytearray([a1,a2,a3,a4])
outputPNG.write(adler32Array)

iDATEnd = outputPNG.tell()

#print(newScanlines[0])
outputPNG.seek(iDATLenLocation,0)
iD1, iD2, iD3, iD4 = (iDATEnd-iDATStart & 0xFFFFFFFF).to_bytes(4, 'big')
iDatLenByteArray = bytearray([iD1, iD2, iD3, iD4])

outputPNG.write(iDatLenByteArray)

outputPNG.seek(4,1)
iDATData = bytearray([73,68,65,84])
for i in range(0,iDATEnd-iDATStart):
    iDATData.append(int.from_bytes(bytes(outputPNG.read(1)), byteorder='big'))
#iDATData.join(bytearray)


#print(bytes(zlib.compress(scanlines[0])).hex())


iDATCRC32 = zlib.crc32(iDATData) 

icrc1, icrc2, icrc3, icrc4 = (iDATCRC32 & 0xFFFFFFFF).to_bytes(4, 'big')
iDATCRC32Array = bytearray([icrc1, icrc2, icrc3, icrc4])
outputPNG.write(iDATCRC32Array)

iENDBtyes = [0,0,0,0,73,69,78,68]
iENDByteArray = bytearray(iENDBtyes)
outputPNG.write(iENDByteArray)

empty = bytearray([73,69,78,68])

iENDCRC32 = zlib.crc32(empty) 
ecrc1, ecrc2, ecrc3, ecrc4 = (iENDCRC32 & 0xFFFFFFFF).to_bytes(4, 'big')
iENDCRC32Array = bytearray([ecrc1, ecrc2, ecrc3, ecrc4])
outputPNG.write(iENDCRC32Array)

#outputPNG.seek(iDATStart,0)
#decompValue = zlib.decompress(outputPNG.read(iDATEnd-iDATStart))
#print(bytes(decompValue).hex())

outputPNG.close()
#test = lz77(newScanlines[0],windowSize)
#print(scanlines[0][0,:,0])