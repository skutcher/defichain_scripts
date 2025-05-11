# Import node object
from defichain import Node

# Specify connection
node =  Node("QqaKPxfe", "f7e06381f696be1a3391afac4bb1ad4536d929dd26bcf2fc9be1dbcad7f5a9e0", url="127.0.0.1", port=8554)



#Variables
endBlock=5015800
depth=30*2880
limit=8000

sumAll=0
sumBBB=0

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

#Output data:
print("BBB stats")

print("End block is: ",endBlock)

print("30 days period in Blocks: ",depth)

print("Number of BBB transactions: ",TXcount)

print("Overall burn amount: ",sumAll)         
print("BBB burn amount: ",sumBBB)
print("Burn by Dex Fee: ",(sumAll-sumBBB))

