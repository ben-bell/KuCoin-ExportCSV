#!/usr/bin/env python

from kucoin.client import Client
from datetime import datetime
import json
import sys
import csv
import time

# enter your apiKey and apiSecret
# remember that KuCoin has read/write permissions, you cannot have a read only API!
apiKey = ""
apiSecret = ""

# prompt user if not hardcoded here
if (apiKey == ""):
	apiKey = input("Please enter your API Key: ")

if (apiSecret == ""):
	apiSecret = input("Please enter your API Secret: ")

client = Client(apiKey, apiSecret)

# some globals
myList = []
rowcount = 0
maxretries = 3

# this function formats the output in CoinTracking format, you could change this to 
# format the output into another format
def getRowFormat(row):
	if (row['direction'] == 'BUY'):
		return {"Type": "Trade", "Buy": round(row['amount'],8), "Cur.": row['coinType'], \
			"Sell": round(row['dealValue'],8), "sCur.": row['coinTypePair'], "Fee": "{0:.8f}".format(row['fee']), \
			"fCur.": row['coinType'], "Exchange": "KuCoin", "Group": "", "Comment": "", \
			"Date": datetime.fromtimestamp(row['createdAt']/1000).strftime('%Y-%m-%d %H:%M:%S') }
	else:
		return {"Type": "Trade", "Buy": round(row['dealValue'],8), "Cur.": row['coinTypePair'], \
		"Sell": round(row['amount'],8), "sCur.": row['coinType'], "Fee": "{0:.8f}".format(row['fee']), \
		"fCur.": row['coinTypePair'], "Exchange": "KuCoin", "Group": "", "Comment": "", \
		"Date": datetime.fromtimestamp(row['createdAt']/1000).strftime('%Y-%m-%d %H:%M:%S') }

def getDepositRowFormat(row):
	# kucoin doesnt charge fees at the moment, so havent bothered to include even
	# though the deposit json contains a fee
	return {"Type": "Deposit", "Buy": "{0:.8f}".format(row['amount']), "Cur.": row['coinType'], \
			"Sell": "", "sCur.": "", "Fee": "", \
			"fCur.": "", "Exchange": "KuCoin", "Group": "", "Comment": row['address'], \
			"Date": datetime.fromtimestamp(row['createdAt']/1000).strftime('%Y-%m-%d %H:%M:%S') }

def getWithdrawalRowFormat(row):
	return {"Type": "Withdrawal", "Buy": "", "Cur.": "", \
			"Sell": "{0:.8f}".format(row['amount']), "sCur.": row['coinType'], "Fee": "{0:.8f}".format(row['fee']), \
			"fCur.": row['coinType'], "Exchange": "KuCoin", "Group": "", "Comment": row['address'], \
			"Date": datetime.fromtimestamp(row['createdAt']/1000).strftime('%Y-%m-%d %H:%M:%S') }
		
# list all the coins on KuCoin
symbols = client.get_trading_symbols()
print("Got a list of trading symbols")

#loop through every symbol and work out if you have any trades
for row in symbols:

	# for the current symbol get your dealt orders
	symbol = row['symbol']
	
	retry = 0
	while (retry < maxretries):
		try:
			dealtOrders = client.get_dealt_orders(symbol='{0}'.format(symbol))
			data = dealtOrders['datas']
			break
		except:
			retry = retry + 1
			# quit if we hit the limit
			if (retry >= maxretries):
				raise
			else:
				# have a rest for 2 seconds
				time.sleep(2)
				

	print("Trying {0}... you have {1} records".format(symbol, dealtOrders['total']))

	#if there are records in data
	if (data):
		nextpage = 0
		for row in data:
			myList.append(getRowFormat(row))

		# KuCoin uses pages, and the limit is absolutely useless, it doesnt work
		# if you put in limit=100, it may still default to a limit of 12, so easier
		# just to loop through the pages with whatever limit they have
		currPageNo = dealtOrders['currPageNo']
		pageNos = dealtOrders['pageNos']

		# loop until we are at the end page
		# I would have used lastPage property here, but thats broken too!
		while (currPageNo < pageNos):
			nextPage = currPageNo + 1

			retry = 0
			while (retry < maxretries):
				try:
					dealtOrders = client.get_dealt_orders(symbol='{0}'.format(symbol), page=nextPage)
					currPageNo = dealtOrders['currPageNo']
					data = dealtOrders['datas']
					break
				except:
					retry = retry + 1
					# quit if we hit the limit
					if (retry >= maxretries):
						raise
					else:
						# have a rest for 2 seconds
						time.sleep(2)
				
			# loop again and get the new rows
			if (data):
				for row in data:
					myList.append(getRowFormat(row))


# lets go get any deposits and withdrawls now
print("Start getting deposits and withdrawls")

coins = client.get_coin_list()

#loop through every coin and work out if there are deposits or withdrawls
for row in coins:

	coin = row['coin']
	
	retry = 0
	while (retry < maxretries):
		try:
			deposits = client.get_deposits(coin='{0}'.format(coin))
			data = deposits['datas']
			break
		except:
			retry = retry + 1
			# quit if we hit the limit
			if (retry >= maxretries):
				raise
			else:
				# have a rest for 2 seconds
				time.sleep(2)
				

	print("Trying {0}... you have {1} deposit records".format(coin, deposits['total']))

	#if there are records in data
	if (data):
		nextpage = 0
		for row in data:
			myList.append(getDepositRowFormat(row))

		# KuCoin uses pages, and the limit is absolutely useless, it doesnt work
		# if you put in limit=100, it may still default to a limit of 12, so easier
		# just to loop through the pages with whatever limit they have
		currPageNo = deposits['currPageNo']
		pageNos = deposits['pageNos']

		# loop until we are at the end page
		# I would have used lastPage property here, but thats broken too!
		while (currPageNo < pageNos):
			nextPage = currPageNo + 1

			retry = 0
			while (retry < maxretries):
				try:
					deposits = client.get_deposits(coin='{0}'.format(coin), page=nextPage)
					currPageNo = deposits['currPageNo']
					data = deposits['datas']
					break
				except:
					retry = retry + 1
					# quit if we hit the limit
					if (retry >= maxretries):
						raise
					else:
						# have a rest for 2 seconds
						time.sleep(2)
				
			# loop again and get the new rows
			if (data):
				for row in data:
					myList.append(getDepositRowFormat(row))

					
	#withdrawals next
	retry = 0
	while (retry < maxretries):
		try:
			withdrawals = client.get_withdrawals(coin='{0}'.format(coin))
			data = withdrawals['datas']
			break
		except:
			retry = retry + 1
			# quit if we hit the limit
			if (retry >= maxretries):
				raise
			else:
				# have a rest for 2 seconds
				time.sleep(2)
				

	print("Trying {0}... you have {1} withdrawal records".format(coin, withdrawals['total']))

	#if there are records in data
	if (data):
		nextpage = 0
		for row in data:
			myList.append(getWithdrawalRowFormat(row))

		# KuCoin uses pages, and the limit is absolutely useless, it doesnt work
		# if you put in limit=100, it may still default to a limit of 12, so easier
		# just to loop through the pages with whatever limit they have
		currPageNo = withdrawals['currPageNo']
		pageNos = withdrawals['pageNos']

		# loop until we are at the end page
		# I would have used lastPage property here, but thats broken too!
		while (currPageNo < pageNos):
			nextPage = currPageNo + 1

			retry = 0
			while (retry < maxretries):
				try:
					withdrawals = client.get_withdrawals(coin='{0}'.format(coin), page=nextPage)
					currPageNo = withdrawals['currPageNo']
					data = withdrawals['datas']
					break
				except:
					retry = retry + 1
					# quit if we hit the limit
					if (retry >= maxretries):
						raise
					else:
						# have a rest for 2 seconds
						time.sleep(2)
				
			# loop again and get the new rows
			if (data):
				for row in data:
					myList.append(getWithdrawalRowFormat(row))




# this will get the column headers that were formatted
keys = myList[0].keys()

# dict writer doesnt let you quote which would be preferable, but doesnt seem to be commas anyway
with open("Transactions.csv", "w", newline='') as f:
	writer = csv.DictWriter(f, keys)
	writer.writeheader()
	writer.writerows(myList)
