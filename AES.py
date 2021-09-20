from initials import *
from Functions import *


def GetPlainTextMatrix(FinalMatrix):
    PlainText=""
    for i in range(4):
        for j in range(4):
            if len(FinalMatrix[j][i])==3:
                PlainText+='0'
            PlainText+=FinalMatrix[j][i][2:]
    return PlainText


# In[15]:


def Encrypt(Key,PlainText):
    StateMatrix=GetStateMatrix(PlainText)
    KeyMatrix=GetStateMatrix(Key) #Key Matrix is built same way as state matrix
    RoundKeyMatrix=AddRoundKey(StateMatrix,KeyMatrix)
    KeyList=KeySchedule(KeyMatrix)

    for i in range(9):
        SubBytesMatrix= GetSubBytes(RoundKeyMatrix)
        ShiftRowsMatrix=GetShiftRows(SubBytesMatrix)
        MixColoumnsMatrix=GetMixColumns(ShiftRowsMatrix)
        RoundKeyMatrix=AddRoundKey(MixColoumnsMatrix,KeyList[i])


    SubBytesMatrix= GetSubBytes(RoundKeyMatrix)
    ShiftRowsMatrix=GetShiftRows(SubBytesMatrix)
    RoundKeyMatrix=AddRoundKey(ShiftRowsMatrix,KeyList[9])
    PlainText=GetPlainTextMatrix(RoundKeyMatrix)
    return PlainText


# In[16]:


def Decrypt(Key,PlainText):
    StateMatrix=GetStateMatrix(PlainText)
    KeyMatrix=GetStateMatrix(Key)
    KeyList=KeySchedule(KeyMatrix)


    RoundKeyMatrix=AddRoundKey(StateMatrix,KeyList[-1])
    index=8
    for i in range(9):
        if i ==0:
            InverseShiftRowsMatrix=GetInverseShiftRows(RoundKeyMatrix)
        else:
            InverseShiftRowsMatrix=GetInverseShiftRows(InverseKeyMixColumnsMatrix)

        InverseSubBytesMatrix=GetInverseSubBytes(InverseShiftRowsMatrix)
        RoundKeyMatrix=AddRoundKey(InverseSubBytesMatrix,KeyList[index])
        InverseKeyMixColumnsMatrix=GetInverseMixColumns(RoundKeyMatrix)
        index-=1

    InverseShiftRowsMatrix=GetInverseShiftRows(InverseKeyMixColumnsMatrix)
    InverseSubBytesMatrix= GetInverseSubBytes(InverseShiftRowsMatrix)

    RoundKeyMatrix=AddRoundKey(InverseSubBytesMatrix,KeyMatrix)
    PlainText=GetPlainTextMatrix(RoundKeyMatrix)
    return PlainText


# In[ ]:


if __name__== "__main__":

#     PlainText="3243f6a8885a308d313198a2e0370734"
#     Key="2b7e151628aed2a6abf7158809cf4f3c"
#     dy="3925841d02dc09fbdc118597196a0b32"

    #print(Decrypt(Key,dy))
    #print(Encrypt(Key,PlainText))

    Choice=input("Please enter E if you want encrypt or D if you want decrypt : ")
    Key=input("Please enter the key: ")

    if Choice=='E':
        PlainText=input("Please enter the Plain Text: ")
        cipheredText = Encrypt(Key,PlainText)
        print("Ciphered Text: "+ cipheredText)
        input()

    elif Choice=='D':
        PlainText=input("Enter the encrypted Text: ")
        decryptedText=Decrypt(Key,PlainText)
        print("Decrypted Text: "+ decryptedText)
        input()


