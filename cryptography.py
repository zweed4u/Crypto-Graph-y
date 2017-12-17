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

def fetch_crypto_data():
	crypto_price.append(str(session.get('https://api.coinbase.com/v2/prices/BTC-USD/buy', headers=set_cb_version_header()).json()["data"]["amount"]))
	return crypto_price

def fetch_epoch():
	epoch.append(str(int(time.time())-init_time))
	return epoch

def animate(i):
	fetch_epoch()
	fetch_crypto_data()
	ax1.clear()
	print(f'Plotting ({epoch[-1]},{crypto_price[-1]})')
	ax1.plot(epoch, crypto_price)

global init_time
global crypto_price
global epoch

epoch = []
crypto_price = []
init_time = int(time.time())
print(f'(seconds_elapsed, $btc:usd)')
ani = animation.FuncAnimation(fig, animate, interval=10000)
plt.show()