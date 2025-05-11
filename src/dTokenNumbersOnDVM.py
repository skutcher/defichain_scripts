# Import node object
from defichain import Node
import json

# Specify connection
node =  Node("****", "*****", url="127.0.0.1", port=8554)

#List of Poolpairs with DUSD 
LMpoolsList=node.poolpair.listpoolpairs(start=367,limit=500)

#List of Oracle prices
oraclePrices=node.oracles.listprices(limit=1000)

#Variables for output
freeAssets=0
backedAssets=0
algoAssets=0
output={}
currentBlock=node.blockchain.getblockcount()


#Cycle over the list of poolpairs
for value in LMpoolsList.values():

         #Only the pools with DUSD without the Stables and BURN
         if value["symbol"].endswith("DUSD") and not value["symbol"].startswith("USD") and not value["symbol"].startswith("EUR") and not value["symbol"].startswith("BURN"):
                id = value["idTokenA"]

                #Getting the numbers for tokens
                token=node.tokens.gettoken(id)
                output[id] = {}
                output[id]["symbol"] = token[id]["symbolKey"]
                
                #Getting the prices for tokens
                oracle = next(filter(lambda oracle: oracle['token'] == token[id]["symbolKey"], oraclePrices), None)
                if oracle is not None:
                     try:
                         oracle_price = node.oracles.getprice(token[id]["symbolKey"],"USD")
                         output[id]["price"] = oracle_price

                         #Getting amounts measured in DUSD
                         output[id]["dusdAmount"] = token["freeOnDVM"]*output[id]["price"]
                         output[id]["loanAmount"] = token["openLoans"]*output[id]["price"]
                         freeAssets+=output[id]["dusdAmount"]
                         backedAssets+=output[id]["loanAmount"]   
                         
                     except :
                         print("no oracle data")

#Algo dAssets
algoAssets=freeAssets-backedAssets

#Numbers for DUSD
dusdNumbers=node.tokens.gettoken("DUSD")                
freeDUSD=dusdNumbers["freeOnDVM"]
backedDUSD=dusdNumbers["openLoans"]
algoDUSD=freeDUSD-backedDUSD

#AlgoRatios
algoRatio=round((algoAssets+algoDUSD)/(freeAssets+freeDUSD)*100,2)
algoRatioDUSD=round((algoDUSD)/(freeDUSD)*100,2)

#Output                 
#print (json.dumps(output, indent=2, default=str))

print("Current block: ",currentBlock)
print("")
print("FREE   dAssets on DVM: ", "{:,}".format(int(freeAssets)).replace(","," "), "measured in DUSD (oracle price used)")
print("BACKED dAssets on DVM: ", "{:,}".format(int(backedAssets)).replace(","," "), "measured in DUSD (oracle price used)")
print("ALGO   dAssets on DVM: ", "{:,}".format(int(algoAssets)).replace(","," "), "measured in DUSD (oracle price used)")
print("")
print("FREE   DUSD on DVM: ", "{:,}".format(int(freeDUSD)).replace(","," "), "measured in DUSD (oracle price used)")
print("BACKED DUSD on DVM: ", "{:,}".format(int(backedDUSD)).replace(","," "), "measured in DUSD (oracle price used)")
print("ALGO   DUSD on DVM: ", "{:,}".format(int(algoDUSD)).replace(","," "), "measured in DUSD (oracle price used)")
print("")
print("DUSD ALGO ratio: ",algoRatioDUSD, " %")
print("")
print("Total amount of FREE   DUSD & dAssets on DVM: ", "{:,}".format(int(freeAssets+freeDUSD)).replace(","," "), "measured in DUSD (oracle price used)") 
print("Total amount of BACKED DUSD & dAssets on DVM: ", "{:,}".format(int(backedAssets+backedDUSD)).replace(","," "), "measured in DUSD (oracle price used)")  
print("Total amount of ALGO   DUSD & dAssets on DVM: ", "{:,}".format(int(algoAssets+algoDUSD)).replace(","," "), "measured in DUSD (oracle price used)")  
print("")
print("Overall ALGO ratio: ",algoRatio, " %")
print("")                                 