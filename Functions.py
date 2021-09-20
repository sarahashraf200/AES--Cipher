


from initials import *

def GetStateMatrix(PlainText):
    StateMatrix = [["0" for x in range(4)] for y in range(4)]
    PlainTextList=list(PlainText)
    index=0
    for i in range(4):
        for j in range(4):
            StateMatrix[j][i]=PlainTextList[index]+PlainTextList[index+1]
            index+=2
    return StateMatrix


def GetSubBytes(StateMatrix):
    HexaArray=""
    SubBytesMatrix = [["0" for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            HexaArray=list(StateMatrix[i][j])
            if len(HexaArray)==4:
                SubBytesMatrix[i][j]=hex(s_box[int(HexaArray[2],16)][int(HexaArray[3],16)] )
            elif len(HexaArray)==3 :
                SubBytesMatrix[i][j]=hex(s_box[0][int(HexaArray[2],16)] )
            else:
                SubBytesMatrix[i][j]=hex(s_box[int(HexaArray[0],16)][int(HexaArray[1],16)] )
    return SubBytesMatrix



def GetInverseSubBytes(StateMatrix):
    HexaArray=""
    InverseSubBytesMatrix = [["0" for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            HexaArray=list(StateMatrix[i][j])
            if len(HexaArray)==4:
                InverseSubBytesMatrix[i][j]=hex(inv_s_box[int(HexaArray[2],16)][int(HexaArray[3],16)] )
            elif len(HexaArray)==3 :
                InverseSubBytesMatrix[i][j]=hex(inv_s_box[0][int(HexaArray[2],16)] )
            else:
                InverseSubBytesMatrix[i][j]=hex(inv_s_box[int(HexaArray[0],16)][int(HexaArray[1],16)] )
    return InverseSubBytesMatrix



def GetShiftRows(SubBytesMatrix):
    i=0
    index=0
    for row in SubBytesMatrix:
        row=row[i:] + row[:i]
        SubBytesMatrix[index] = row
        index+=1
        i+=1
    return SubBytesMatrix


def GetInverseShiftRows(InverseSubBytesMatrix):
    i=0
    index=0
    for row in InverseSubBytesMatrix:
        row=row[-i:] + row[:-i]
        InverseSubBytesMatrix[index] = row
        index+=1
        i+=1
    return InverseSubBytesMatrix

def Galois(FirstNum, SecondNum):
    i = 0
    for counter in range(8):
        if SecondNum & 1: i ^= FirstNum
        BitSet = FirstNum & 0x80
        FirstNum <<= 1
        FirstNum &= 0xFF
        if BitSet:
            FirstNum ^= 0x1b
        SecondNum >>= 1
    return i


def GetMixColumns(ShiftRowsMatrix):
    fixed = [2, 1, 1, 3]
    row = [0, 3, 2, 1]
    coloumn = 0
    OutputArray = []
    for _ in range(4):
        for _ in range(4):
            OutputArray.append('%02x' % (Galois(int(ShiftRowsMatrix[row[0]][coloumn], 16), fixed[0]) ^Galois(int(ShiftRowsMatrix[row[1]][coloumn], 16), fixed[1]) ^ Galois(int(ShiftRowsMatrix[row[2]][coloumn], 16), fixed[2]) ^Galois(int(ShiftRowsMatrix[row[3]][coloumn], 16), fixed[3])))
            row = [row[-1]] + row[:-1]
        coloumn += 1
    ShiftRowsMatrix = [OutputArray[i:i+4] for i in range(0, 16, 4) ]
    MixColoumnsMatrix=[["0" for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            MixColoumnsMatrix[i][j]=ShiftRowsMatrix[j][i]
    return MixColoumnsMatrix


def GetInverseMixColumns(ShiftRowsMatrix):
    fixed = [14, 9, 13, 11]
    row = [0, 3, 2, 1]
    coloumn = 0
    OutputArray = []
    for _ in range(4):
        for _ in range(4):
            OutputArray.append('%02x' % (Galois(int(ShiftRowsMatrix[row[0]][coloumn], 16), fixed[0]) ^Galois(int(ShiftRowsMatrix[row[1]][coloumn], 16), fixed[1]) ^ Galois(int(ShiftRowsMatrix[row[2]][coloumn], 16), fixed[2]) ^Galois(int(ShiftRowsMatrix[row[3]][coloumn], 16), fixed[3])))
            row = [row[-1]] + row[:-1]
        coloumn += 1
    ShiftRowsMatrix = [OutputArray[i:i+4] for i in range(0, 16, 4) ]
    InverseMixColoumnsMatrix=[["0" for x in range(4)] for y in range(4)]
    for i in range(4):
        for j in range(4):
            InverseMixColoumnsMatrix[i][j]=ShiftRowsMatrix[j][i]
    return InverseMixColoumnsMatrix

def KeySchedule(StateMatrix):
    Keys=[]
    for num in range(10):
        if num > 0:
            StateMatrix=RoundKey
        RoundKey=[["0" for x in range(4)] for y in range(4)]
        x=0
        index=0
        RowMatrix=[["0" for x in range(4)] for y in range(4)]
        for i in range(4):
            for j in range(4):
                RowMatrix[i][j]=StateMatrix[j][i]
        state=RowMatrix

        Result=[["0" for x in range(4)] for y in range(4)]
        for row in state:
            row=row[1:] + row[:1]
            state[index] = row
            index+=1
            x+=1
        state=GetSubBytes(state)

        for i in range(4):
            Result[0][i]=hex(int(StateMatrix[i][0],16) ^ int(state[3][i],16) ^ int(rcon[i][num],16) )


        for i in range(1,4):
            for j in range(4):
                Result[i][j] = hex(int(Result[i-1][j],16) ^ int(StateMatrix[j][i],16))

        for i in range(4):
            for j in range(4):
                RoundKey[i][j]=Result[j][i]

        Keys.append(RoundKey)

    return Keys

def AddRoundKey(StateMatrix,KeyMatrix):
    RoundKey=[["0" for x in range(4)] for y in range(4)]

    for i in range(4):
        for j in range(4):
            RoundKey[j][i]=hex(int(StateMatrix[j][i],16) ^ int(KeyMatrix[j][i],16))
    return RoundKey