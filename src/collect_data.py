import requests
from config import INFURA_MAINNET_CONNECTION_URL, ETHERSCAN_API_KEY
from decode_call_data import decode_transaction_input
from web3 import Web3
import csv

# Function that collects all necessary data and stores them in a csv file
# The columns of this csv are ["hash","success","num_orders","gas_used","gas_price"]
def collect_data(solverAddress, startBlock, endBlock):
    url = "https://api.etherscan.io/api?module=account&action=txlist&address=" \
            + solverAddress \
            + "&startblock=" + str(startBlock) \
            + "&endblock=" +str(endBlock) \
            + "&sort=asc&apikey=" + ETHERSCAN_API_KEY
    try:
        response = requests.get(url)
    except Exception as e:
        print("Error while trying to connect to Etherscan")
        return False
    
    data = response.json()

    web3 = Web3(Web3.HTTPProvider(INFURA_MAINNET_CONNECTION_URL))

    fileName = solverAddress + "_from_" + str(startBlock) + "_to_" + str(endBlock) + ".csv"
    file = open(fileName, 'w', newline='')
    writer = csv.writer(file)
    #The resulting .csv file has the following name format:
    #    #solver_address_from_$startBlock_to_$endBlock.csv"
    # and its columns are labeled with the self-explanatory labels:
    #   hash,success,num_orders,gas_used,gas_price
    firstLine = ["hash","success","num_orders","gas_used","gas_price"]
    writer.writerow(firstLine)

    for t in data['result']:
        if t['to'] == '0x9008d19f58aabd9ed0d60971565aa8510560ab41':
            if t['isError'] == '1':
                success = False
            else:
                success = True
        else:
            continue
        if t['to'] == solverAddress:
            continue
        gasUsed = int(t['gasUsed'])
        gasPrice = int(t['gasPrice']) / 10**9  # price in Gwei
        txHash = t['hash']

        compEndpointUrl = "https://api.cow.fi/mainnet/api/v1/solver_competition/by_tx_hash/" + txHash
        numberOfOrders = 0
        response = requests.get(compEndpointUrl)
        endpointData = response.json()
        if 'errorType' in endpointData:
            tx = web3.eth.get_transaction(txHash)
            # Decode transaction data. We only need this to check how many orders were included in the settlement,
            # in case we fail to fetch this information via the competition endpoint.
            # Note that in case we end up using the calldata, we might overestimate the number of orders that are there
            # since foreign_liquidity_orders are counted as orders in  this case.
            input_data = decode_transaction_input(tx)
            numberOfOrders = len(input_data['params'][2])
        else:
            numberOfOrders = len(endpointData['solutions'][-1]['orders'])
        
        output = [txHash,str(success),str(numberOfOrders),str(gasUsed),str(gasPrice)]
        writer.writerow(output)

    file.close()
    return True


####################################

# Simple execution; we enter solver address and start and end block via the console,
# and a csv file containing all the necessary information for training a model 
# is generated
solverAddress = input("Enter solver address: ")
startBlock = int(input("Enter starting block: "))
endBlock = int(input("Enter end block: "))

collect_data(solverAddress, startBlock, endBlock)
