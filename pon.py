import cryptsy
import sys
import time
import datetime
import math

c = cryptsy.Cryptsy()
mrk = "DOGE/BTC"
hist = 0
buyOrd = 0
sellOrd = 0
prevPrice = 0
prevTrade = "sell"
bitBal = 0.00002768
dogBal = 300

def buy(price):
        doge = float(bitBal) / (float(price) * float(1.002))
        #c.place_order(c.markets[mkr], "Buy", price, doge)
        print("Bought " + str(doge) + " amount of Dogecoin for " + str(price))
        with open("log.txt", "a") as file:
                file.write("Bought " +str(doge) + " amount of Dogecoin for " +str(price))

def sell(price):
        #c.place_order(c.markets[mkr], "Sell", price, dogBal)
        print("Sold " + str(dogBal) + " amount of Dogecoin for " + str(price))
        with open("log.txt", "a") as file:
                file.write("Sold " + str(dogBal) + " amount of Dogecoin for " + str(price))

while True:
	time.sleep(10)
	tyme = datetime.datetime.now().time()
	try:
		c.update_markets()
		c.update_orders_by_market(c.markets[mrk])
		c.update_trade_history(c.markets[mrk])
		c.update_my_open_orders(c.markets[mrk])
		c.update_balance()
	except ValueError:
		print("Value Error; couldn't connect to cryptsy")
		with open("log.txt", "a") as file:
			file.write(str(tyme) + ": Value Error; couldn't connect to cryptsy")
	except KeyError:
		print("Key Error; couldn't connect to cryptsy")
		with open("log.txt", "a") as file:
			file.write(str(tyme) + ": Key Error; couldn't connect to cryptsy")
	hist = c.markets[mrk].history[0].price
	buyOrd = c.markets[mrk].buy_orders[0].price
	sellOrd = c.markets[mrk].sell_orders[0].price
	b = c.get_bank()
	bitBal = b.coins["BTC"]
	#dogBal = b.coins["DOGE"]
	print("Latest Price: " + str(hist) + " | Buy: " + str(buyOrd) + " | Sell: " + str(sellOrd))
	if (prevTrade == "sell"):
		buy(hist)
		prevTrade = "buy"
		prevPrice = hist
	if (prevTrade == "buy"):
		if (math.fabs(float(hist) - float(prevPrice)) > 0.00000002):
			sell(hist)
			prevTrade = "sell"
			prevPrice = hist


	
