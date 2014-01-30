import cryptsy
import sys
import time
import datetime
import math
import smtplib
from email.MIMEText  import MIMEText
from email.MIMEMultipart import MIMEMultipart

c = cryptsy.Cryptsy()
mrk = "DOGE/BTC"
hist = 0
buyOrd = 0
sellOrd = 0
prevPrice = 0.00000187
prevTrade = "sell"
bitBal = 0.00061714
dogBal = 0
pastTradeD = 0
pastTradeP = 0
pastTradeT = "sell"

def email(type,price,doge):
	sender = "Pon Trader"
	to = "taylor.pridgen@colorado.edu"
	subject = "You made a trade!"
	content = "You put in an order for a " + str(type) + " sale for " + str(price) + " at " + str(doge)
	msg = MIMEMultipart()
	msg['From'] = 'musicinsilence13@gmail.com'
	msg['To'] = to
	msg['Subject'] = subject
	msg.attach(MIMEText(content))

	server = smtplib.SMTP(host='smtp.gmail.com', port=587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('musicinsilence13@gmail.com', 'M1ss1ss1pp1')
	server.sendmail("musicinsilence13@gmail.com", "musicinsilence13@gmail.com", content)
	server.close()

def buy(price):
        doge = float(bitBal) / (float(price) * float(1.002))
        c.place_order(c.markets[mrk], "Buy", price, doge)
        prevTradeT = "buy"
        prevTradeP = price
        prevTradeD = doge
	global dogBal
	dogBal = doge
	global bitBal
	bitBal = 0
        print("--Bought " + str(doge) + " amount of Dogecoin for " + str(price))
        with open("log.txt", "a") as file:
                file.write("Bought " +str(doge) + " amount of Dogecoin for " +str(price))

def sell(price):
        c.place_order(c.markets[mrk], "Sell", price, dogBal)
        prevTradeT = "sell"
        prevTradeP = price
        prevTradeD = dogBal
        print("-Sold " + str(dogBal) + " amount of Dogecoin for " + str(price))
	global bitBal
	bitBal = float(dogBal) * (float(price) * float(1.002))
	global dogBal
	dogBal = 0
        with open("log.txt", "a") as file:
                file.write("Sold " + str(dogBal) + " amount of Dogecoin for " + str(price))
                

c.update_balance()
c.update_my_open_orders(c.markets[mrk])
b = c.get_bank()
if (b.coins["BTC"] > 0):
	bitBal = b.coins["BTC"]
if (b.coins["DOGE"] > 0):
	dogBal = b.coins["DOGE"
if (dogBal > 0 && len(c.markets[mrk].my_orders) == 0):
	prevTrade = "sell"
while True:
	time.sleep(10)
	tyme = datetime.datetime.now().time()
	try:
		c.update_markets()
		c.update_orders_by_market(c.markets[mrk])
		c.update_trade_history(c.markets[mrk])
		c.update_my_open_orders(c.markets[mrk])
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
	if (len(c.markets[mrk].my_orders) == 0):
		email(pastTradeT, pastTradeP, pastTradeD)
		print("Latest Price: " + str(hist) + " | Buy: " + str(buyOrd) + " | Sell: " + str(sellOrd))
		if (prevTrade == "sell"):
			buy(float(hist)-0.00000002)
			prevTrade = "buy"
			prevPrice = float(hist)
		if (prevTrade == "buy"):
			sell(float(hist)+0.00000002)
			prevTrade = "sell"
			prevPrice = float(hist)


	
