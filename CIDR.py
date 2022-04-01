import os
nBinaryEquiv = []

####################################################################################################
# Function: prepareBinaryEquiv(number):
# Convert 0-255 decimal to a binary equivalent [11111111]
def prepareBinaryEquiv():
    nBinaryEquiv = []
    numVal = 1
    for num in range(1, 33):
        numVal = ((num > 1 and numVal * 2) or 1)
        nBinaryEquiv.append(numVal)
    return nBinaryEquiv


####################################################################################################
# Function: convertToBinary(number):
# Convert 0-255 decimal to a binary equivalent [11111111]
def convertToBinary(number, baseNum):
    retValue = ""
    thisIteration = '0'
    remNumber = number

    # determine what numbers to use or rather base 8 will use first 8 numbers in reversed order
    rangeToUse = [nBinaryEquiv[x] for x in range(0, baseNum)]
    for i in reversed(rangeToUse):
        if remNumber >= i:
            remNumber-=i
            thisIteration = '1'
        else:
            thisIteration = '0'
        retValue=retValue+thisIteration
    return retValue

####################################################################################################
# Function: convertToDecimal(number):
#convert binary to decimal
def convertToDecimal(number):
    retValue = 0
    rangeToUse = [nBinaryEquiv[x] for x in range(0, 8)]
    for i in range(0, 8):
        if number[i] == '1':
            retValue+=rangeToUse[7-i]
    return retValue

####################################################################################################
# Main routine
os.system('clear')
nBinaryEquiv = prepareBinaryEquiv()
ipAddress = input("     IP Address and subnet mask {xxx.xxx.xxx.xxx/xx}: ")
ipOnly  = ipAddress.split('/')[0]
netmask = int(ipAddress.split('/')[1])

# calculate subnet mask to be shown on the screen
charCounter = 0
subnetMask = ""
for i in range(1, netmask+1):
    subnetMask+='1'
    charCounter+=1
    if i%8 == 0 and i < netmask+1:
        subnetMask+='-'

bitsNeededCounter = 0
for i in range(netmask, 32):
    subnetMask+='*'
    charCounter+=1
    bitsNeededCounter+=1
    if charCounter%8 == 0 and i<30:
        subnetMask+='-'

# Subnet IP make this using the above information
ipSubnet = ""
subnetVal = ""
dividedSubnet = subnetMask.split('-')
for xSubNet in dividedSubnet:
    if (xSubNet.count('*')) == 0:
        ipSubnet+=((len(ipSubnet)>0 and '.') or '') + str(convertToDecimal(xSubNet))
    else:
        # Replace all '*' with '0'
        subnetVal = ""
        for xVal in range(0, 8):
            subnetVal+=((xSubNet[xVal] == '*' and '0') or xSubNet[xVal])
        ipSubnet+=((len(ipSubnet)>0 and '.') or '') + str(convertToDecimal(subnetVal))

# now convert decimal values to binary
ipAddressInBinary = ""

# now show each octate in binary code
eachOctate = ipOnly.split('.')
nLenOfValues = len(eachOctate)
counter = 1
for i in eachOctate:
    ipAddressInBinary += convertToBinary(int(i), 8) + ((counter<nLenOfValues and  '-' ) or '')
    counter+=1

possibleIPAddesses = 2**bitsNeededCounter   # 2 to the power of bitsNeededCounter

# We have (4) four binary numbers which make an IP address.
# We need to determine how many of these 4 we need for the host numbers
# We have a counter which says how many bits are needed. Lets see if we can calculate 
# how it translates to how many bytes we need
noOfBinaryNeeded = int(bitsNeededCounter/8) + (((bitsNeededCounter%8) > 0 and 1) or 0)

# Now determine what is not to be changed and put it in a variable
ipAddCounter = 4 - noOfBinaryNeeded
ipHostStart = ""
counter = 1
for x in eachOctate:
    if counter <= ipAddCounter:
        ipHostStart += ((len(ipHostStart) > 0 and '.') or '') + x
        counter+=1

# Now we have the initial portion of the ip Address, lets see how does the rest of the information 
# looks like, We need to convert the number to decimal and show it 
ipCalculating = ""
counter = 1
#reversed - noOfBinaryNeeded
for useByty in range(0, 4):
    bitToAdd = convertToBinary(int(eachOctate[useByty]), 8)
    if useByty >= ipAddCounter :
        ipCalculating += ((len(ipCalculating) > 0 and '.') or '') + bitToAdd
    counter+=1

# now remove the bits to 0 which are a part of the subnet mask
nStartReplacingFrom = 8 - bitsNeededCounter
lhasMoreThanOneBytes = (ipCalculating.count('.') > 0)
allPortionsInipCalculate = ipCalculating.split('.')
byteToUpdate = allPortionsInipCalculate[0]
newNumber = ""
for updatebits in range(0, 8):
    newNumber += (updatebits < nStartReplacingFrom and byteToUpdate[updatebits]) or '0'

decimalEquivToAdd = convertToDecimal(newNumber)

# Now see if there is a remaining portion available to be calculated. That will be all 0 anyways

cNetworkIP = ipHostStart + "." + str(decimalEquivToAdd)

if lhasMoreThanOneBytes:
    noOfOtherPortionsInCalc = len(allPortionsInipCalculate) - 1
    cFirstHostAddress = ipHostStart
    for nAdd in range(0, noOfOtherPortionsInCalc):
        cNetworkIP += '.0'
        cFirstHostAddress += ".0" 
    cFirstHostAddress+= '.' + str(decimalEquivToAdd + 1)

    ## now all the 0 portions i added will be filled with 
    tBaseNum = 32 - netmask
    tBaseNum = ((tBaseNum > 24 and 32) or (tBaseNum > 16 and 24) or (tBaseNum > 8 and 16) or 8)
    binToAddToTheEnd = convertToBinary(possibleIPAddesses-2, tBaseNum)
    nBitsCounter = 1
    nNumToAdd = 0
    cByteToAdd = ''
    clastHostAddress  = ipHostStart
    for nBit in range(0, len(binToAddToTheEnd)):
        cByteToAdd+=binToAddToTheEnd[nBit]
        if nBitsCounter > 7:
            nBitsCounter = 0
            clastHostAddress+="." + str(convertToDecimal(cByteToAdd))
            cByteToAdd = ''
        nBitsCounter+=1
   
    binToAddToTheEnd = convertToBinary(possibleIPAddesses-1, tBaseNum)
    nBitsCounter = 1
    nNumToAdd = 0
    cByteToAdd = ''
    cBroadcastAddress  = ipHostStart
    for nBit in range(0, len(binToAddToTheEnd)):
        cByteToAdd+=binToAddToTheEnd[nBit]
        if nBitsCounter > 7:
            nBitsCounter = 0
            cBroadcastAddress  += "." + str(convertToDecimal(cByteToAdd))
            cByteToAdd = ''
        nBitsCounter+=1

else:
    # First host address
    cFirstHostAddress = ipHostStart + "." + str(decimalEquivToAdd + 1)

    clastHostAddress  = ipHostStart + "." + str(decimalEquivToAdd + (possibleIPAddesses - 2))
    cBroadcastAddress = ipHostStart + "." + str(decimalEquivToAdd + (possibleIPAddesses - 1))

# remove the last '-' we do not need that
print(''' 
         IP Address : {}  Subnet Mask : {}
    ------------------------------------------------------------------------
         ip Address : {}
        subnet Mask : {}

        Number of addresses possible : {}
     Number of Binary numbers needed : {} - Bits needed : {}
      Host address start information : {}
         ip portion to be calculated : {}
             starting number in bits : {} - Decimal equivalent : {}

    ------------------------------------------------------------------------
                     Network address : {}
                  First host address : {}
                   Last host address : {}
                   Broadcast address : {}
'''.format(ipOnly, ipSubnet, ipAddressInBinary, 
        subnetMask, 
        possibleIPAddesses, 
        noOfBinaryNeeded, 
        bitsNeededCounter, 
        ipHostStart, 
        ipCalculating,
        newNumber,
        decimalEquivToAdd,
        cNetworkIP,
        cFirstHostAddress,
        clastHostAddress,
        cBroadcastAddress))
