# Import node object
from defichain import Node
import json
import math

# Specify connection
node =  Node("QqaKPxfe", "f7e06381f696be1a3391afac4bb1ad4536d929dd26bcf2fc9be1dbcad7f5a9e0", url="127.0.0.1", port=8554)


#Variables for output 
output={}
DeXFee=0
NI=0
currentBlock=node.blockchain.getblockcount()

#DUSD Suply part
#DUSD Numbers from DMC side - have to be solved by API to DMC
DMCdUSDv1=900000
DMCdUSD=900000
lockRatio=0.1


#DUSD Numbers from DVM side
dusdNumbers=node.tokens.gettoken("DUSD")                
freeDUSD=dusdNumbers["freeOnDVM"]
backedDUSD=dusdNumbers["openLoans"]

#DUSD Numbers overall
allFreeDUSD=freeDUSD+lockRatio*DMCdUSDv1+DMCdUSD
algoDUSD=allFreeDUSD-backedDUSD

#AlgoRatio
algoRatioDUSD=round((algoDUSD)/(allFreeDUSD),4)

#DUSD Burn Part
#Variables
endBlock=5015800
depth=30*2880
limit=8000

sumAll=0
sumBBB=0
deXFeeBurnAmount=0

#complete burn of DUSD with specified borders
allBurnList=node.accounts.listburnhistory(maxBlockHeight=endBlock, token="DUSD",depth=depth, txtype="i", limit=100000)

#Cycle for overall DUSD burn amount
for x in allBurnList:
    for amount in x["amounts"]:
        if amount.endswith("DUSD"):
            amount=amount.replace("@DUSD","")
            sumAll += float(amount)

#list of BBB tx with specified borders
BBBtxList=node.accounts.listaccounthistory(owner="df1q0ulwgygkg0lwk5aaqfkmkx7jrvf4zymj0yyfef", maxBlockHeight=endBlock, no_rewards=True, depth=depth, limit=limit)
TXcount=(len(BBBtxList))

#Cycle for BBB DUSD burn amount
for x in BBBtxList:
    burnList=node.accounts.getaccounthistory("8defichainBurnAddressXXXXXXXdRQkSm",x["blockHeight"],x["txn"])
    for amount in burnList["amounts"]:
        if amount.endswith("DUSD"):
         amount=amount.replace("@DUSD","")
         sumBBB += float(amount)

deXFeeBurnAmount=sumAll-sumBBB

NI=-((3*deXFeeBurnAmount/10)*12.16)/backedDUSD
DeXFee=0.00063 * (math.exp(4.387 * algoRatioDUSD) - 1)


#Output                 
#print (json.dumps(output, indent=2, default=str))
print("Numbers for checking the inputs")
print("Current block: ",currentBlock)
print("")
print("FREE   DMC-DUSDv1: ", DMCdUSDv1)
print("FREE   DMC-DUSD: ", DMCdUSD)
print("")
print("FREE   DUSD: ", allFreeDUSD)
print("BACKED DUSD: ", backedDUSD)
print("ALGO   DUSD: ", algoDUSD)
print("")
print("DUSD ALGO ratio: ",algoRatioDUSD*100, " %")
print("")   
print("BURN stats")
print("") 
print("End block is: ",endBlock)

print("30 days period in Blocks: ",depth)

print("Number of BBB transactions: ",TXcount)
print("") 
print("Overall burn amount: ",sumAll)         
print("BBB burn amount: ",sumBBB)
print("Burn by Dex Fee: ",(deXFeeBurnAmount)) 
print("")
print("")
print("Output for setgov") 
print("New DexFee: ",round(DeXFee*100,2)," %")
print("New NI: ",round(NI*100,2)," %")                                