import requests
import pandas as pd
import datetime
# We use Covalent and Biquery's API's so we need to get some API Keys from them
# following are the API keys so just swap them out for personal ones
COVALENT_API_KEY = "ckey_XXXXXXXXXXXXXXXXXX"
BITQUERY_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXX"

# gets all uniswap pools and parses the information to be queried by user in other functions
def get_uniswap_pools():
    url = "https://api.covalenthq.com/v1/1/networks/uniswap_v2/assets/?quote-currency=USD&format=JSON&page-size=2280&key=" + COVALENT_API_KEY
    response = requests.get(url)

    if(response.status_code == 200 and response.headers["content-type"].strip().startswith("application/json")):
        try:
            data = response.json()
            uniswap_pools = {}
            for x in data['data']['items']:
                token_0_name = ""
                if x["token_0"]["contract_ticker_symbol"] is None:
                    token_0_name = "?"
                else:
                    token_0_name = x["token_0"]["contract_ticker_symbol"]
                token_1_name = ""
                if x["token_1"]["contract_ticker_symbol"] is None:
                    token_1_name = "?"
                else:
                    token_1_name = x["token_1"]["contract_ticker_symbol"]

                pool_name = token_0_name + "-" + token_1_name

                if pool_name in uniswap_pools.keys():
                    uniswap_pools[pool_name].append([x["exchange"], x["token_0"]["contract_decimals"], x["token_1"]["contract_decimals"]])
                else:
                    uniswap_pools[pool_name] = [[x["exchange"], x["token_0"]["contract_decimals"], x["token_1"]["contract_decimals"]]]
            print("Covalent was able to return requests")
            return uniswap_pools
        except ValueError:
            print("Covalent API unable to return requests")


# sushiswap analog of previous function
def get_sushiswap_pools():
    url = "https://api.covalenthq.com/v1/1/networks/sushiswap/assets/?quote-currency=USD&format=JSON&page-size=600&key=" + COVALENT_API_KEY
    response = requests.get(url)

    if(response.status_code == 200 and response.headers["content-type"].strip().startswith("application/json")):
        try:
            data = response.json()
            suhsiswap_pools = {}
            for x in data['data']['items']:
                token_0_name = ""
                if x["token_0"]["contract_ticker_symbol"] is None:
                    token_0_name = "?"
                else:
                    token_0_name = x["token_0"]["contract_ticker_symbol"]
                token_1_name = ""
                if x["token_1"]["contract_ticker_symbol"] is None:
                    token_1_name = "?"
                else:
                    token_1_name = x["token_1"]["contract_ticker_symbol"]

                pool_name = token_0_name + "-" + token_1_name

                if pool_name in suhsiswap_pools.keys():
                    suhsiswap_pools[pool_name].append([x["exchange"], x["token_0"]["contract_decimals"], x["token_1"]["contract_decimals"]])
                else:
                    suhsiswap_pools[pool_name] = [[x["exchange"], x["token_0"]["contract_decimals"], x["token_1"]["contract_decimals"]]]
            print("Covalent was able to return requests")
            return suhsiswap_pools
        except ValueError:
            print("Covalent API unable to return requests")


# pancakeswap analog of previous function
def get_pancake_pools():

    url = "https://api.covalenthq.com/v1/56/networks/pancakeswap_v2/assets/?quote-currency=USD&format=JSON&page-size=45000&key=" + COVALENT_API_KEY
    response = requests.get(url)

    if(response.status_code == 200 and response.headers["content-type"].strip().startswith("application/json")):
        try:
            data = response.json()
            pancake_pools = {}
            for x in data['data']['items']:
                token_0_name = ""
                if x["token_0"]["contract_ticker_symbol"] is None:
                    token_0_name = "?"
                else:
                    token_0_name = x["token_0"]["contract_ticker_symbol"]
                token_1_name = ""
                if x["token_1"]["contract_ticker_symbol"] is None:
                    token_1_name = "?"
                else:
                    token_1_name = x["token_1"]["contract_ticker_symbol"]

                pool_name = token_0_name + "-" + token_1_name

                if pool_name in pancake_pools.keys():
                    pancake_pools[pool_name].append([x["exchange"], x["token_0"]["contract_decimals"], x["token_1"]["contract_decimals"]])
                else:
                    pancake_pools[pool_name] = [[x["exchange"], x["token_0"]["contract_decimals"], x["token_1"]["contract_decimals"]]]
            print("Covalent was able to return request")
            return pancake_pools
        except ValueError:
            print("Covalent unable to return request")


# querying function to sift through pools with specified ticker symbol
# pools ~ one of 3 returns from previous 3 functions
# search term ~ a string of the Ticker symbol to be searched term e.g. "WTBC", "WETH", "USDC" etc
def get_pools(pools, searchTerm):
    data_list = []
    for key, value in pools.items():
        if searchTerm in key:
            for x in value:
                x.append(key.split("-")[0])
                x.append(key.split("-")[1])
                data_entry = {}
                data_entry["pool_name"] = key
                data_entry["pertinent_data"] = x
                data_list.append(data_entry)

    return pd.DataFrame(data=data_list)


# querying function to sift through pools with specified name
# ideally use after using the get_pools function to know the pool's name
# pools ~ one of 3 returns from previous 3 functions
# search term ~ string of the pool name  e.g. "WTBC-USDC"
def get_pool(pools, searchTerm):
    for key, value in pools.items():
        if searchTerm in key:
            for val in value:
                return [val[0], val[1], val[2], key.split("-")[0], key.split("-")[1]]


# helper function in charge of connecting to Bitquery's API
def run_query(query):
    headers = {'X-API-KEY': BITQUERY_API_KEY}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                                                                             query))

# helper function in charge of connection to Bitquery's API when variables are needed
# so in general will be using this function to make requests
def run_query_variables(query, variables):
    headers = {'X-API-KEY': BITQUERY_API_KEY}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                                                                             query))


# gets all historical swaps for a pool
# exchangeName <- Name of exchange; case sensitive so only “Uniswap”, “Pancake v2”, or “SushiSwap” work
# dataList [contract address, token 0 decimals, token 1 decimals, token 0 ticker symbol, token 1 ticker symbol]
# this datalIst paramter can be returned from the get_pool() function.
def get_swaps(exchangeName, dataList):
    contractAddress = dataList[0]
    token0decimal = dataList[1]
    token1decimal = dataList[2]
    query_data = event_brute(exchangeName, "Swap", contractAddress)
    if "errors" in query_data:
        # check the error message; this one is for server limit
        if "10.00 thousand" in query_data["errors"][0]["message"]:
            total_data = []

            swaps_json = event_smart(exchangeName, "Swap", contractAddress)
            swaps_sh = swaps_json['data']['ethereum']['smartContractEvents']

            collection = []
            for x in swaps_sh:
                if len(x["arguments"]) == 6:
                    if x["arguments"][1]["argument"] == "amount0In" and x["arguments"][2]["argument"] == "amount1In" and x["arguments"][3]["argument"] == "amount0Out" and x["arguments"][4]["argument"] == "amount1Out":
                        dict_entry = {}
                        dict_entry["block_height"] = x["block"]["height"]
                        dict_entry["timestamp"] = x["block"]["timestamp"]["iso8601"]

                        dict_entry[dataList[3] + "In"] = float(x["arguments"][1]["value"]) * 10**(-token0decimal)
                        dict_entry[dataList[4] + "In"] = float(x["arguments"][2]["value"]) * 10**(-token1decimal)
                        dict_entry[dataList[3] + "Out"] = float(x["arguments"][3]["value"]) * 10**(-token0decimal)
                        dict_entry[dataList[4] + "Out"] = float(x["arguments"][4]["value"]) * 10**(-token1decimal)

                        dict_entry["transaction_hash"] = x["transaction"]["hash"]
                        dict_entry["from"] = x["transaction"]["txFrom"]["address"]

                        collection.append(dict_entry)

            # add our first chunk of data
            total_data.extend(collection)
            print("1st API call done")
            num = 2

            while len(swaps_sh) == 10_000:
                swaps_json = event_smart_after(exchangeName, "Swap", contractAddress, collection[-1]["block_height"])
                temps_sh = swaps_json['data']['ethereum']['smartContractEvents']

                temp = []
                for x in swaps_sh:
                    if len(x["arguments"]) == 6:
                        if x["arguments"][1]["argument"] == "amount0In" and x["arguments"][2]["argument"] == "amount1In" and x["arguments"][3]["argument"] == "amount0Out" and x["arguments"][4]["argument"] == "amount1Out":
                            dict_entry = {}
                            dict_entry["block_height"] = x["block"]["height"]
                            dict_entry["timestamp"] = x["block"]["timestamp"]["iso8601"]

                            dict_entry[dataList[3] + "In"] = float(x["arguments"][1]["value"]) * 10**(-token0decimal)
                            dict_entry[dataList[4] + "In"] = float(x["arguments"][2]["value"]) * 10**(-token1decimal)
                            dict_entry[dataList[3] + "Out"] = float(x["arguments"][3]["value"]) * 10**(-token0decimal)
                            dict_entry[dataList[4] + "Out"] = float(x["arguments"][4]["value"]) * 10**(-token1decimal)

                            dict_entry["transaction_hash"] = x["transaction"]["hash"]
                            dict_entry["from"] = x["transaction"]["txFrom"]["address"]

                            temp.append(dict_entry)

                total_data.extend(temp)
                collection = temp
                print("API call #" + str(num) + " done")
                num += 1
                swaps_sh = temps_sh
            return pd.json_normalize(data=total_data)
        else:
            # otherwise bitquery is down so try again later preferably @ midnight
            # as ive had the most success at that time
            print("Bitquery is having serverside errors try again later")
            return
    else:
        swaps_sh = query_data['data']['ethereum']['smartContractEvents']
        collection = []
        for x in swaps_sh:
            if len(x["arguments"]) == 6:

                if x["arguments"][1]["argument"] == "amount0In" and x["arguments"][2]["argument"] == "amount1In" and x["arguments"][3]["argument"] == "amount0Out" and x["arguments"][4]["argument"] == "amount1Out":
                    dict_entry = {}
                    dict_entry["block_height"] = x["block"]["height"]
                    dict_entry["timestamp"] = x["block"]["timestamp"]["iso8601"]

                    dict_entry[dataList[3] + "In"] = float(x["arguments"][1]["value"]) * 10**(-token0decimal)
                    dict_entry[dataList[4] + "In"] = float(x["arguments"][2]["value"]) * 10**(-token1decimal)
                    dict_entry[dataList[3] + "Out"] = float(x["arguments"][3]["value"]) * 10**(-token0decimal)
                    dict_entry[dataList[4] + "Out"] = float(x["arguments"][4]["value"]) * 10**(-token1decimal)

                    dict_entry["transaction_hash"] = x["transaction"]["hash"]
                    dict_entry["from"] = x["transaction"]["txFrom"]["address"]

                    collection.append(dict_entry)
        return pd.DataFrame(data=collection)


# gets all historical mints for a pool
# exchangeName <- Name of exchange; case sensitive so only “Uniswap”, “Pancake v2”, or “SushiSwap” work
# dataList [contract address, token 0 decimals, token 1 decimals, token 0 ticker symbol, token 1 ticker symbol]
# this datalIst paramter can be returned from the get_pool() function.
def get_mints(exchangeName, dataList):
    contractAddress = dataList[0]
    token0decimal = dataList[1]
    token1decimal = dataList[2]
    mints_json = event_brute(exchangeName, "Mint", contractAddress)

    if "errors" in mints_json:
        if "10.00 thousand" in mints_json["errors"][0]["message"]:
            total_data = []
            mints_json = event_smart(exchangeName, "Mint", contractAddress)
            mints_json_sh = mints_json['data']['ethereum']['smartContractEvents']
            mints_historical = []
            for x in mints_json_sh:
                amount0s = []
                amount1s = []
                for y in x['arguments']:
                    if y['argument'] == 'amount0' or y['argument'] == "_amount":
                        amount0s.append(int(y['value']))
                    if y['argument'] == 'amount1' or y["argument"] == "_newTotalSupply":
                        amount1s.append(int(y['value']))
                for i in range(len(amount0s)):
                    data_dict = {}
                    data_dict["block_height"] = x["block"]["height"]
                    data_dict["timestamp"] = x["block"]["timestamp"]["iso8601"]
                    data_dict["transaction_hash"] = x["transaction"]["hash"]
                    data_dict["from"] = x["transaction"]["txFrom"]["address"]
                    data_dict[dataList[3]] = amount0s[i] * 10**(-token0decimal)
                    data_dict[dataList[4]] = amount1s[i] * 10**(-token1decimal)
                    mints_historical.append(data_dict)
            total_data.extend(mints_historical)

            print("1st API call done")
            num = 2
            while len(mints_historical) >= 10_000:
                mints_json = event_smart_after(exchangeName, "Mint", contractAddress, mints_historical[-1]["block_height"])
                mints_json_sh = mints_json['data']['ethereum']['smartContractEvents']
                mints_historic = []

                for x in mints_json_sh:
                    amount0s = []
                    amount1s = []
                    for y in x['arguments']:
                        if y['argument'] == 'amount0' or y['argument'] == "_amount":
                            amount0s.append(int(y['value']))
                        if y['argument'] == 'amount1' or y["argument"] == "_newTotalSupply":
                            amount1s.append(int(y['value']))
                    for i in range(len(amount0s)):
                        data_dict = {}
                        data_dict["block_height"] = x["block"]["height"]
                        data_dict["timestamp"] = x["block"]["timestamp"]["iso8601"]
                        data_dict["transaction_hash"] = x["transaction"]["hash"]
                        data_dict["from"] = x["transaction"]["txFrom"]["address"]
                        data_dict[dataList[3]] = amount0s[i] * 10**(-token0decimal)
                        data_dict[dataList[4]] = amount1s[i] * 10**(-token1decimal)
                        mints_historic.append(data_dict)
                total_data.extend(mints_historic)
                print("API call #" + str(num) + " done")
                num += 1
                mints_historical = mints_historic

            return pd.DataFrame(data=total_data)
        else:
            print("Bitquery is having serverside errors try again later")
            return
    else:
        mints_json_sh = mints_json['data']['ethereum']['smartContractEvents']
        mints_historical = []

        for x in mints_json_sh:
            amount0s = []
            amount1s = []
            for y in x['arguments']:
                if y['argument'] == 'amount0' or y['argument'] == "_amount":
                    amount0s.append(int(y['value']))
                if y['argument'] == 'amount1' or y["argument"] == "_newTotalSupply":
                    amount1s.append(int(y['value']))
            for i in range(len(amount0s)):
                data_dict = {}
                data_dict["block_height"] = x["block"]["height"]
                data_dict["timestamp"] = x["block"]["timestamp"]["iso8601"]
                data_dict["transaction_hash"] = x["transaction"]["hash"]
                data_dict["from"] = x["transaction"]["txFrom"]["address"]
                data_dict[dataList[3]] = amount0s[i] * 10**(-token0decimal)
                data_dict[dataList[4]] = amount1s[i] * 10**(-token1decimal)

                mints_historical.append(data_dict)
        return pd.DataFrame(data=mints_historical)


# helper function. Brute force method to get all burns/mints/swaps
def event_brute(exchangeName, eventType, contractAddress):
    query = """
    query ($address: String, $net: EthereumNetwork, $event: String) {
      ethereum(network: $net) {
        smartContractEvents(
          smartContractAddress: {is: $address}
          smartContractEvent: {is: $event}
          options: {asc: "block.height"}
        ) {
          block {
            height
            timestamp {
              iso8601
            }
          }
          arguments {
            value
            argument
          }
          transaction {
            hash
            txFrom {
              address
            }
          }
        }
      }
    }

    """
    variables = {}
    if exchangeName in ["Uniswap", "SushiSwap"]:
        if eventType == "Mint":
            variables = {"address": contractAddress, "net": "ethereum", "event": "Mint"}
        elif eventType == "Swap":
            variables = {"address": contractAddress, "net": "ethereum", "event": "Swap"}
        else:
            variables = {"address": contractAddress, "net": "ethereum", "event": "Burn"}
    else:
        if eventType == "Mint":
            variables = {"address": contractAddress, "net": "bsc", "event": "Mint"}
        elif eventType == "Swap":
            variables = {"address": contractAddress, "net": "bsc", "event": "Swap"}
        else:
            variables = {"address": contractAddress, "net": "bsc", "event": "Burn"}

    return run_query_variables(query, variables)


# helper function. Smarter method to get all burns/mints/swaps i.e. partition all data
# into sizeable chunks
def event_smart(exchangeName, eventType, contractAddress):
    query = """
    query ($address: String, $net: EthereumNetwork, $event: String) {
      ethereum(network: $net) {
        smartContractEvents(
          smartContractAddress: {is: $address}
          smartContractEvent: {is: $event}
          options: {asc: "block.height", limit: 10000}
        ) {
          block {
            height
            timestamp {
              iso8601
            }
          }
          arguments {
            value
            argument
          }
          transaction {
            hash
            txFrom {
              address
            }
          }
        }
      }
    }

    """
    variables = {}
    if exchangeName in ["Uniswap", "SushiSwap"]:
        if eventType == "Mint":
            variables = {"address": contractAddress, "net": "ethereum", "event": "Mint"}
        elif eventType == "Swap":
            variables = {"address": contractAddress, "net": "ethereum", "event": "Swap"}
        else:
            variables = {"address": contractAddress, "net": "ethereum", "event": "Burn"}
    else:
        if eventType == "Mint":
            variables = {"address": contractAddress, "net": "bsc", "event": "Mint"}
        elif eventType == "Swap":
            variables = {"address": contractAddress, "net": "bsc", "event": "Swap"}
        else:
            variables = {"address": contractAddress, "net": "bsc", "event": "Burn"}

    return run_query_variables(query, variables)


# helper function. Smarter method to get all burns/mints/swaps i.e. partition all data
# into sizeable chunks. This function is called after the event_smart() method
# basically does:
# event_smart() gets oldest 10K swaps/burns/mints. This function then gets the next
# 10K swaps/burns/mints starting at the most recent blockHeight event_smart() found. We call this
# function in a while loop until are size of each data is <10000 i.e. are the newer/tail end of data
def event_smart_after(exchangeName, eventType, contractAddress, blockHeight):
    query = """
    query ($address: String, $block: Int, $net: EthereumNetwork, $event: String) {
      ethereum(network: $net) {
        smartContractEvents(
          smartContractAddress: {is: $address}
          smartContractEvent: {is: $event}
          options: {asc: "block.height", limit: 10000}
          height: {gt: $block}
        ) {
          block {
            height
            timestamp {
              iso8601
            }
          }
          arguments {
            value
            argument
          }
          transaction {
            hash
            txFrom {
              address
            }
          }
        }
      }
    }

    """
    variables = {}
    if exchangeName in ["Uniswap", "SushiSwap"]:
        if eventType == "Mint":
            variables = {"address": contractAddress, "block": blockHeight, "net": "ethereum", "event": "Mint"}
        elif eventType == "Swap":
            variables = {"address": contractAddress, "block": blockHeight, "net": "ethereum", "event": "Swap"}
        else:
            variables = {"address": contractAddress, "block": blockHeight, "net": "ethereum", "event": "Burn"}
    else:
        if eventType == "Mint":
            variables = {"address": contractAddress, "block": blockHeight, "net": "bsc", "event": "Mint"}
        elif eventType == "Swap":
            variables = {"address": contractAddress, "block": blockHeight, "net": "bsc", "event": "Swap"}
        else:
            variables = {"address": contractAddress, "block": blockHeight, "net": "bsc", "event": "Burn"}

    return run_query_variables(query, variables)


# gets all historical burns for a pool
# exchangeName <- Name of exchange; case sensitive so only “Uniswap”, “Pancake v2”, or “SushiSwap” work
# dataList [contract address, token 0 decimals, token 1 decimals, token 0 ticker symbol, token 1 ticker symbol]
# this datalIst paramter can be returned from the get_pool() function.
def get_burns(exchangeName, dataList):

    contractAddress = dataList[0]
    token0decimal = dataList[1]
    token1decimal = dataList[2]
    burns_json = event_brute(exchangeName, "Burn", contractAddress)

    if "errors" in burns_json:
        if "10.00 thousand" in burns_json["errors"][0]["message"]:
            total_data = []
            burns_json = event_smart(exchangeName, "Burn", contractAddress)
            burns_json_sh = burns_json['data']['ethereum']['smartContractEvents']
            burns_historical = []
            for x in burns_json_sh:
                amount0s = []
                amount1s = []
                for y in x['arguments']:
                    if y['argument'] == 'amount0' or y['argument'] == "_amount":
                        amount0s.append(int(y['value']))
                    if y['argument'] == 'amount1' or y["argument"] == "_newTotalSupply":
                        amount1s.append(int(y['value']))
                for i in range(len(amount0s)):
                    data_dict = {}
                    data_dict["block_height"] = x["block"]["height"]
                    data_dict["timestamp"] = x["block"]["timestamp"]["iso8601"]
                    data_dict["transaction_hash"] = x["transaction"]["hash"]
                    data_dict["from"] = x["transaction"]["txFrom"]["address"]
                    data_dict[dataList[3]] = amount0s[i] * 10**(-token0decimal)
                    data_dict[dataList[4]] = amount1s[i] * 10**(-token1decimal)
                    burns_historical.append(data_dict)
            total_data.extend(burns_historical)

            print("1st API call done")
            num = 2
            while len(burns_historical) >= 10_000:
                burns_json = event_smart_after(exchangeName, "Burn", contractAddress, burns_historical[-1]["block_height"])
                burns_json_sh = burns_json['data']['ethereum']['smartContractEvents']
                burns_historic = []

                for x in burns_json_sh:
                    amount0s = []
                    amount1s = []
                    for y in x['arguments']:
                        if y['argument'] == 'amount0' or y['argument'] == "_amount":
                            amount0s.append(int(y['value']))
                        if y['argument'] == 'amount1' or y["argument"] == "_newTotalSupply":
                            amount1s.append(int(y['value']))
                    for i in range(len(amount0s)):
                        data_dict = {}
                        data_dict["block_height"] = x["block"]["height"]
                        data_dict["timestamp"] = x["block"]["timestamp"]["iso8601"]
                        data_dict["transaction_hash"] = x["transaction"]["hash"]
                        data_dict["from"] = x["transaction"]["txFrom"]["address"]
                        data_dict[dataList[3]] = amount0s[i] * 10**(-token0decimal)
                        data_dict[dataList[4]] = amount1s[i] * 10**(-token1decimal)
                        burns_historic.append(data_dict)
                total_data.extend(burns_historic)
                print("API call #" + str(num) + " done")
                num += 1
                burns_historical = burns_historic

            return pd.DataFrame(data=total_data)
        else:
            print("Bitquery is having serverside errors try again later")
            return
    else:
        burns_json_sh = burns_json['data']['ethereum']['smartContractEvents']
        burns_historical = []

        for x in burns_json_sh:
            amount0s = []
            amount1s = []
            for y in x['arguments']:
                if y['argument'] == 'amount0' or y['argument'] == "_amount":
                    amount0s.append(int(y['value']))
                if y['argument'] == 'amount1' or y["argument"] == "_newTotalSupply":
                    amount1s.append(int(y['value']))
            for i in range(len(amount0s)):
                data_dict = {}
                data_dict["block_height"] = x["block"]["height"]
                data_dict["timestamp"] = x["block"]["timestamp"]["iso8601"]
                data_dict["transaction_hash"] = x["transaction"]["hash"]
                data_dict["from"] = x["transaction"]["txFrom"]["address"]
                data_dict[dataList[3]] = amount0s[i] * 10**(-token0decimal)
                data_dict[dataList[4]] = amount1s[i] * 10**(-token1decimal)

                burns_historical.append(data_dict)

        return pd.DataFrame(data=burns_historical)


# sanity check for swaps since we are on the free plan i.e. same paramters as before but pass in the last
# block height get_swaps() showed. If the rate limit was not exceeded this should return an empty dataframe
# if not it will return the last remaining data.
def verify_swaps(exchangeName, dataList, lastKnownBlockHeight):
    contractAddress = dataList[0]
    token0decimal = dataList[1]
    token1decimal = dataList[2]
    query_data = event_smart_after(exchangeName, "Swap", contractAddress, lastKnownBlockHeight)
    if "errors" in query_data:
        # check the error message; this one is for server limit
        if "10.00 thousand" in query_data["errors"][0]["message"]:
            total_data = []

            swaps_json = event_smart_after(exchangeName, "Swap", contractAddress, lastKnownBlockHeight)
            swaps_sh = swaps_json['data']['ethereum']['smartContractEvents']

            collection = []
            for x in swaps_sh:
                if len(x["arguments"]) == 6:
                    if x["arguments"][1]["argument"] == "amount0In" and x["arguments"][2]["argument"] == "amount1In" and x["arguments"][3]["argument"] == "amount0Out" and x["arguments"][4]["argument"] == "amount1Out":
                        dict_entry = {}
                        dict_entry["block_height"] = x["block"]["height"]
                        dict_entry["timestamp"] = x["block"]["timestamp"]["iso8601"]

                        dict_entry[dataList[3] + "In"] = float(x["arguments"][1]["value"]) * 10**(-token0decimal)
                        dict_entry[dataList[4] + "In"] = float(x["arguments"][2]["value"]) * 10**(-token1decimal)
                        dict_entry[dataList[3] + "Out"] = float(x["arguments"][3]["value"]) * 10**(-token0decimal)
                        dict_entry[dataList[4] + "Out"] = float(x["arguments"][4]["value"]) * 10**(-token1decimal)

                        dict_entry["transaction_hash"] = x["transaction"]["hash"]
                        dict_entry["from"] = x["transaction"]["txFrom"]["address"]

                        collection.append(dict_entry)

            # add our first chunk of data
            total_data.extend(collection)
            print("1st API call done")
            num = 2

            while len(swaps_sh) == 10_000:
                swaps_json = event_smart_after(exchangeName, "Swap", contractAddress, collection[-1]["block_height"])
                temps_sh = swaps_json['data']['ethereum']['smartContractEvents']

                temp = []
                for x in swaps_sh:
                    if len(x["arguments"]) == 6:
                        if x["arguments"][1]["argument"] == "amount0In" and x["arguments"][2]["argument"] == "amount1In" and x["arguments"][3]["argument"] == "amount0Out" and x["arguments"][4]["argument"] == "amount1Out":
                            dict_entry = {}
                            dict_entry["block_height"] = x["block"]["height"]
                            dict_entry["timestamp"] = x["block"]["timestamp"]["iso8601"]

                            dict_entry[dataList[3] + "In"] = float(x["arguments"][1]["value"]) * 10**(-token0decimal)
                            dict_entry[dataList[4] + "In"] = float(x["arguments"][2]["value"]) * 10**(-token1decimal)
                            dict_entry[dataList[3] + "Out"] = float(x["arguments"][3]["value"]) * 10**(-token0decimal)
                            dict_entry[dataList[4] + "Out"] = float(x["arguments"][4]["value"]) * 10**(-token1decimal)

                            dict_entry["transaction_hash"] = x["transaction"]["hash"]
                            dict_entry["from"] = x["transaction"]["txFrom"]["address"]

                            temp.append(dict_entry)

                total_data.extend(temp)
                collection = temp
                print("API call #" + str(num) + " done")
                num += 1
                swaps_sh = temps_sh
            # return len(query_data)
            # return query_data[-1]["block"]["height"]

            # query_data = swap_smart_after(contractAddress, 10150072)
            return pd.json_normalize(data=total_data)
        else:
            # otherwise bitquery is down so try again later preferably @ midnight
            # as ive had the most success at that time
            print("Bitquery is having serverside errors try again later")
            return
    else:
        swaps_sh = query_data['data']['ethereum']['smartContractEvents']
        collection = []
        for x in swaps_sh:
            if len(x["arguments"]) == 6:

                if x["arguments"][1]["argument"] == "amount0In" and x["arguments"][2]["argument"] == "amount1In" and x["arguments"][3]["argument"] == "amount0Out" and x["arguments"][4]["argument"] == "amount1Out":
                    dict_entry = {}
                    dict_entry["block_height"] = x["block"]["height"]
                    dict_entry["timestamp"] = x["block"]["timestamp"]["iso8601"]

                    dict_entry[dataList[3] + "In"] = float(x["arguments"][1]["value"]) * 10**(-token0decimal)
                    dict_entry[dataList[4] + "In"] = float(x["arguments"][2]["value"]) * 10**(-token1decimal)
                    dict_entry[dataList[3] + "Out"] = float(x["arguments"][3]["value"]) * 10**(-token0decimal)
                    dict_entry[dataList[4] + "Out"] = float(x["arguments"][4]["value"]) * 10**(-token1decimal)

                    dict_entry["transaction_hash"] = x["transaction"]["hash"]
                    dict_entry["from"] = x["transaction"]["txFrom"]["address"]

                    collection.append(dict_entry)
        return pd.DataFrame(data=collection)


