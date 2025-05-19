import os
import sys
import subprocess
import json
#pip install python-dotenv
from dotenv import load_dotenv
from defichain import Node
#enable line buffering so that pipes to tee works
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()
bin=os.getenv('CLI')
# Specify connection
username=os.getenv('USERNAME')
password=os.getenv('PASSWORD')
node =  Node(username, password, url="127.0.0.1", port=8554)

block=dict()
#block['previousblockhash'] = 'af177f05bcb29050bd628f6c69929c24bc7e9652468856ea268a8f3fb08c5203' #9d3a53bab39808d275354cff1e59a94c3e45c7417b842dae9fd8d6c7e837abcd' #
block['previousblockhash'] = node.blockchain.getbestblockhash()

addresses = set(sys.argv[1:])
print("Tracked addresses", addresses)
addresses_size = len(addresses)

run = True
while run:
    block = node.blockchain.getblock(blockhash=block['previousblockhash'], verbosity=2)
    # print(block)
    if block['height'] % 10000 == 0:
        print(block['height'])
    for tx in block['tx']:
        type=''
        vout_in_list = False
        for vout in tx['vout']:
            try:
                s = set(vout['scriptPubKey']['addresses']).intersection(addresses)
                if len(s) > 0:
                    vout_in_list = True
                    # print("In list ",vout_in_list)
            except:
                pass
        # if one address is in the list add all others as well
        if vout_in_list:
            for vout in tx['vout']:
                try:
                    addresses.update(set(vout['scriptPubKey']['addresses']))
                except:
                    pass


        args=(bin, 'decodecustomtx', tx['hex'])
        try:
            sub = subprocess.run(args, capture_output=True)
            try:
                res = json.loads(sub.stdout.decode('utf-8'))
                type = res['type']
                if res['type']=='TakeLoan':
                    if vout_in_list:
                        addresses.add(res['results']['to'])
                    if (not vout_in_list) and res['results']['to'] in addresses:
                        for vout in tx['vout']:
                            try:
                                addresses.update(set(vout['scriptPubKey']['addresses']))
                            except:
                                pass
                if res['type']=='PaybackLoan':
                    if vout_in_list:
                        addresses.add(res['results']['from'])
                    if (not vout_in_list) and res['results']['from'] in addresses:
                        for vout in tx['vout']:
                            try:
                                addresses.update(set(vout['scriptPubKey']['addresses']))
                            except:
                                pass
                if res['type']=='AccountToUtxos' or res['type']=='AccountToAccount':
                    # print(res)
                    to = set(res['results']['to'].keys())
                    try:
                        if res['results']['from'] in addresses:
                            addresses.update(to)
                    except:
                        pass

                    try:
                        if to in addresses:
                            addresses.add(res['results']['from'])
                    except:
                        pass
            except:
                pass
        except:
            pass
            # some tx are too long so we need try except here for subprocess run
            # i would expect these long ones are EVM stuff
            # print(args)

        if addresses_size != len(addresses):
            print("BlockHeight: ",block['height'])
            print("TxType: ", type)
            print("Txid: ", tx['txid'])
            print("Extended address list: ", addresses)
            addresses_size = len(addresses)
    # quit()
