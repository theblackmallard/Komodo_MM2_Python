import platform
import os
import re
import json
import requests
from slickrpc import Proxy

port = "http://127.0.0.1:7783"

def def_credentials(chain):
    rpcport = ''
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Windows':
        ac_dir = '%s/komodo/' % os.environ['APPDATA']
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if len(rpcport) == 0:
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
            print("check " + coin_config_file)
            exit(1)

    return (Proxy("http://%s:%s@127.0.0.1:%d" % (rpcuser, rpcpassword, int(rpcport))))

# The enable method enables a coin by connecting the user's software instance to the coin blockchain using the native coin daemon.

def enable(rpc_connection, userpass, coin):
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"enable\",'
                                            '\"coin\":\"{1}\",\"mm2\":1}'.format(userpass, coin))
        response = response.json()
        result = response['result']
        return result
    except requests.exceptions.RequestException as e:
        print(e)

def enable_ETH(rpc_connection, userpass, swap_contract_address):  # mm2:1 needs to be somewhere, coin to be used
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"enable\",'
                                            '\"coin\":\"ETH\",\"urls\":[\"http://195.201.0.6:8545\"],'
                                            '\"swap_contract_address\":\"{1}\"}'.format(userpass, swap_contract_address))
        response = response.json()
        result = response['result']
        return result
    except requests.exceptions.RequestException as e:
        print(e)

# The my_balance method returns the current balance of the specified coin.

def my_balance(rpc_connection, userpass, coin):
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"my_balance\",'
                                            '\"coin\":\"{1}\"}'.format(userpass, coin))
        response = response.json()
        balance = response['balance']
        return balance
    except requests.exceptions.RequestException as e:
        print(e)

# The orderbook method requests from the network the currently available orders for the specified trading pair.

def get_orderbook(rpc_connection, userpass, base, rel):
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"orderbook\",'
                                            '\"base\":\"{1}\",\"rel\":\"{2}\"}'.format(userpass, base, rel))
        response = response.json()
        bids = response['bids']
        numBids = response['numbids']
        bidDepth = response['biddepth']
        asks = response['asks'] # dictionary in a list
        numAsks = response['numasks']
        askDepth = response['askdepth']
        timeStamp = response['timestamp']
        netID = response['netid']
        return asks, bids, numBids, bidDepth, numAsks, askDepth, timeStamp, netID
    except requests.exceptions.RequestException as e:
        print(e)

# The buy method issues a buy request and attempts to match an order from the orderbook based on the provided arguments.

def buy_coin(rpc_connection, userpass, base, rel, price, relVolume):
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"buy\",'
                                            '\"base\":\"{1}\",\"rel\":\"{2}\",'
                                            '\"relvolume\":{3},\"price\":{4}'.format(userpass, base, rel, relVolume, price))
        response = response.json()
        result = response['result']
        swaps = response['swaps']
        pending = response['pending']  # dictionary
        uuid = response['uuid']
        return result, swaps, pending, uuid
    except requests.exceptions.RequestException as e:
        print(e)

# The sell method issues a sell request and attempts to match an order from the orderbook based on the provided arguments.

def sell_coin(rpc_connection, userpass, base, rel, price, baseVolume):
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"sell\",'
                                            '\"base\":\"{1}\",\"rel\":\"{2}\",'
                                            '\"basevolume\":{3},\"price\":{4}}'.format(userpass, base, rel, baseVolume, price))
        response = response.json()
        result = response['result']
        swaps = response['swaps']
        pending = response['pending']  # dictionary
        uuid = response['uuid']
        return result, swaps, pending, uuid
    except requests.exceptions.RequestException as e:
        print(e)

# The setprice method places an order on the orderbook, and it relies on this node acting as a maker -- also called a Bob node.

def set_price(rpc_connection, userpass, base, rel, price):
    try:
        response = requests.post(port, data='{\"userpass\":\"{0}\",\"method\":\"setprice\"'
                                            ',\"base\":\"{1}\",\"rel\":\"{2}\",'
                                            '\"price\":{3}}'.format(userpass, base, rel, price))
        response = response.json()
        result = response['result']
        return result
    except requests.exceptions.RequestException as e:
        print(e)


# The withdraw method generates, signs, and returns a transaction that transfers the amount of coin
# to the address indicated in the to argument.

def withdraw(rpc_connection, userpass, coin, to, amount):
    try:
        response = requests.post(port, data='{\"method\":\"withdraw\",\"coin\":\"{0}\",'
                                            '\"to\":\"{1}\",\"amount\":{2},'
                                            '\"userpass\":\"{3}\"}'.format(coin, to, amount, userpass))
        response = response.json()
        result = response
        return result
    except requests.exceptions.RequestException as e:
        print(e)

def withdraw_ETH(rpc_connection, userpass, to, amount):
    try:
        response = requests.post(port, data='{\"method\":\"withdraw\",'
                                            '\"coin\":\"ETH\",\"to\":\"{0}\",'
                                            '\"amount\":{1},\"userpass\":\"{2}\"}'.format(to, amount, userpass))
        response = response.json()
        result = response
        return result
    except requests.exceptions.RequestException as e:
        print(e)

# The send_raw_transaction method broadcasts the transaction to the network of selected coin.

def send_raw_tx(rpc_connection, userpass, coin, tx_hex):
    try:
        response = requests.post(port, data='{\"method\":\"send_raw_transaction\",\"coin\":\"{0}\",'
                                            '\"tx_hex\":\"{1}\",\"userpass\":\"{2}\"}'.format(coin, tx_hex, userpass))
        response = response.json()
        result = response['tx_hash']
        return result
    except requests.exceptions.RequestException as e:
        print(e)




#def stop(rpc_connection):  # The stop method stops the MM2 software if there are no swaps in process.

#def help(rpc_connection):  # The help method returns the full API documentation in the terminal.

