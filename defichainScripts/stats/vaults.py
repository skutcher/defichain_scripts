import os
import sys
from defichain import Node
from dotenv import load_dotenv

def calc():
    username=os.getenv('USERNAME')
    password=os.getenv('PASSWORD')
    node =  Node(username, password, url="127.0.0.1", port=8554)

    vaults=node.vault.listvaults(verbose=True, limit=20000)
    prices=node.oracles.listfixedintervalprices(limit=10000)

    new_prices=prices.copy()
    for i in range(len(new_prices)):
        if new_prices[i]['priceFeedId'] == "BTC/USD":
            new_prices[i]['activePrice'] = 0.0
            print("New BTC price: ",0.0)
        if new_prices[i]['priceFeedId'] == "ETH/USD":
            new_prices[i]['activePrice'] = 0.0
            print("New ETH price: ",0.0)
        if new_prices[i]['priceFeedId'] == "EUROC/USD":
            new_prices[i]['activePrice'] = 0.0
            print("New EUROC price: ",0.0)
        if new_prices[i]['priceFeedId'] == "USDT/USD":
            new_prices[i]['activePrice'] = 0.0
            print("New USDT price: ",0.0)
        if new_prices[i]['priceFeedId'] == "USDC/USD":
            new_prices[i]['activePrice'] = 0.0
            print("New USDC price: ",0.0)

    cv = dict()
    cctr = dict()
    ctr=0
    empty_ctr=0
    liquidations=0
    for vault in vaults:
        ctr+=1
        if not vault['collateralAmounts']:
            empty_ctr+=1
        new_collateral = 0.0
        for collateral in vault['collateralAmounts']:
            (amount,token) = collateral.split("@", 1)
            new_price = [x for x in new_prices if x['priceFeedId'] == token+"/USD"][0]
            new_collateral += new_price['activePrice'] * float(amount)
            # print("Amount: ", amount, "Token: ",token)
            if token in cv:
                cv[token] += float(amount)
                cctr[token] += 1
            else:
                cv[token] = float(amount)
                cctr[token] = 1
        factor=float(vault['loanSchemeId'][3:])/100.0
        if factor < 1.5 or factor > 10.0:
            print("Unexpected Loan Scheme Factor: ",factor)

        if new_collateral < vault['loanValue']*factor:
            liquidations += 1
            print("Liquidation vault id: ", vault['vaultId'])

    print("Total vaults: ",ctr)
    print("Empty vaults: ",empty_ctr)
    print("New prices liquidations: ",liquidations)
    if ctr > 19000:
        print("CAUTION limit is 20000 counted :",ctr)

    for (token, amount) in cv.items():
        print(token,": ",amount)
    for (token, vaults) in cctr.items():
        print(token,": ",vaults)

    # print(vaults)


def main():
    load_dotenv()
    calc()

if __name__ == "__main__":
    main()
