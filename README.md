# KuCoin-ExportCSV
Python script to export transactions to a CSV file readable by CoinTracking.info.  This includes Deposits, Withdrawals and Transactions.

Prerequisites

This uses Sam McHardy's unofficial Python wrapper for KuCoin API: https://github.com/sammchardy/python-kucoin

To install the wrapper:

pip install python-kucoin

Make sure you have a KuCoin account and API key generated (under the Settings menu)

Setup:

1. Hardcode the API Key and Secret into the file (not recommended but easier - however remember KuCoin API has no read-only version)

or 

2. Wait for the prompts and enter API Key and Secret then

Running:

python Export-CSV.py

Notes:

When KuCoin servers are overloaded, expect to get "Invalid nonce" errors, its probably best to run this later.  I've tried to build retries in, but its still not great.


ToDo:

I don't think you can get KuCoin bonus amounts unfortunately (ie: KCS bonus and Gas amounts from holding NEO - if you can let me know!)

Donations:

If this helps you, feel free to send a coin :P

ETH/ETC: 0x5986591391B5Dd78c7170e6e16A17aEd05b50B1d

Waves: 3PL6V1dcNgajfEx5YbMAZJ8xKkVHJkm9Uba

LTC: LVJ4EFyPRPUMZEt4ird88CrtrRtDoK2vKP

BTC: 1MRKyWeUV15VguoruyPVZpveTTT9yKZjMo