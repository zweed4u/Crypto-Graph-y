import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import requests
from matplotlib import style
import matplotlib.animation as animation

session = requests.session()

def set_cb_version_header():
	return {'CB-VERSION':datetime.datetime.now().strftime("%Y-%m-%d")}

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

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
	epoch.append(str(int(time.time())-init_time))
	return epoch

def animate(i):
	fetch_epoch()
	fetch_btc_data()
	fetch_eth_data()
	fetch_ltc_data()
	ax1.clear()
	print(f'Plotting BTC: ({epoch[-1]},{btc_price[-1]})')
	print(f'Plotting ETH: ({epoch[-1]},{eth_price[-1]})')
	print(f'Plotting LTC: ({epoch[-1]},{ltc_price[-1]})')
	ax1.plot(epoch, btc_price)
	ax1.plot(epoch, eth_price)
	ax1.plot(epoch, ltc_price)

global init_time
global btc_price
global eth_price
global ltc_price
global epoch

epoch = []
btc_price = []
eth_price = []
ltc_price = []

init_time = int(time.time())
print(f'(seconds_elapsed, $btc,eth,ltc:usd)')
ani = animation.FuncAnimation(fig, animate, interval=10000)
plt.show()
