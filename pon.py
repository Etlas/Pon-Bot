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
ActiveOrder = false
prevPrice = 0
prevTrade = "sell"
bitBal = 0
dogBal = 0


while True:
	time.sleep(10)
	tyme = datetime.datetime.now().time()
	try:
		c.update_markets()
		c.updates_orders_by_market(c.markers[mrk])
		c.update_trade_history(c.markets[mrk])
		c.update_my_open_orders(c.markets[mrk])
		c.update_balance()
	except ValueError:
		print "Value Error; couldn't connect to cryptsy"
		with open("log.txt", "a") as file:
			file.write(tyme + ": Value Error; couldn't connect to cryptsy")
	except KeyError:
		print "Key Error; couldn't connect to cryptsy"
		with open("log.txt", "a") as file:
			file.write(tyme + ": Key Error; couldn't connect to cryptsy")
	hist = c.markets[mrk].history[0].price
	buyOrd = c.markets[mrk].buy_orders[0].price
	sellOrd = c.markets[mrk].sell_orders[0].price
	b = c.get_bank()
	bitBal = b.coins["BTC"]
	dogBal = b.coins["DOGE"]
	if ((len(c.markets[mrk].my_orders) == 0):
		print "No orders! Looking to trade!"
		if (prevTrade == "sell"):
			if (math.fabs(hist - buyOrd) > 10):
				buy(hist)
				prevTrade = "buy"
				prevPrice = hist
		if (prevTrade == "buy"):
			if (math.fabs(hist - prevPrice) > 2):
				sell(hist)
				prevTrade = "sell"
				prevPrice = hist


def buy(price):
	doge = float(bitBal) / (float(price) * float(1.002))
	c.place_order(c.markets[mkr], "Buy", price, doge)
	print "Bought " + doge + " amount of Dogecoin for " + price
	with open("log.txt", "a") as file:
		file.write("Bought " + doge + " amount of Dogecoin for " + price)

def sell(price):
	c.place_order(c.markets[mkr], "Sell", price, dogBal)
	print "Sold " + dogBal " amount of Dogecoin for " + price
	with open("log.txt", "a") as file:
		file.write("Sold " + dogBal + " amount of Dogecoin for " + price)
	
