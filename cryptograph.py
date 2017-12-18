import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import requests
from matplotlib import style
import matplotlib.animation as animation
import sys
import signal

session = requests.session()
def set_cb_version_header():
	return {'CB-VERSION':datetime.datetime.now().strftime("%Y-%m-%d")}

style.use('fivethirtyeight')

f, axarr = plt.subplots(3, sharex=True)

def fetch_btc_data():
	btc_price.append(str(session.get('https://api.coinbase.com/v2/prices/BTC-USD/buy', headers=set_cb_version_header()).json()["data"]["amount"]))
	return btc_price

def fetch_eth_data():
	eth_price.append(str(session.get('https://api.coinbase.com/v2/prices/ETH-USD/buy', headers=set_cb_version_header()).json()["data"]["amount"]))
	return eth_price

def fetch_ltc_data():
	ltc_price.append(str(session.get('https://api.coinbase.com/v2/prices/LTC-USD/buy', headers=set_cb_version_header()).json()["data"]["amount"]))
	return ltc_price

def fetch_epoch():
	actual_epochs.append(str(int(time.time())))
	epoch.append(str(int(time.time())-init_time))
	return epoch

def animate(i):
	fetch_epoch()
	fetch_btc_data()
	fetch_eth_data()
	fetch_ltc_data()
	axarr[0].set_title('BTC')
	axarr[1].set_title('ETH')
	axarr[2].set_title('LTC')
	print(datetime.datetime.now())
	print(f'Plotting BTC: ({epoch[-1]},{btc_price[-1]})')
	print(f'Plotting ETH: ({epoch[-1]},{eth_price[-1]})')
	print(f'Plotting LTC: ({epoch[-1]},{ltc_price[-1]})')
	axarr[0].plot(epoch, btc_price, color='yellow')
	axarr[1].plot(epoch, eth_price, color='black')
	axarr[2].plot(epoch, ltc_price, color='grey')
	print()

def signal_handler(signal, frame):
	print('Writing values to csv...')
	with open('crypto.csv','w') as file:
		for point in range(len(actual_epochs)):
			file.write(f'{actual_epochs[point]},{btc_price[point]},{eth_price[point]},{ltc_price[point]}')
			file.write('\n')

	print('Exiting plot program...')
	sys.exit(0)

global init_time
global btc_price
global eth_price
global ltc_price
global epoch
global actual_epochs

actual_epochs = []
epoch = []
btc_price = []
eth_price = []
ltc_price = []

# Handle ctl-c and ctrl-z signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)


init_time = int(time.time())
print(f'(seconds_elapsed, $btc,eth,ltc:usd)')
ani = animation.FuncAnimation(f, animate, interval=10000)
plt.show()
