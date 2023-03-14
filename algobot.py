import os
import random
import sys
import ccxt
import json
import pandas as pd
import numpy as np
from datetime import date, datetime, timezone, tzinfo
import time, schedule

print("********************************************")
print("* All copyrights belong to @tahabouidraren in IG*")
print("********************************************")
print("")
print("Hello and Welcome to AlgoBot")
print("")
print("If this is your first time running a script like this")
print("Just answer the questions at the start and you are set.")
print("Note : This bot dont and never will store any type of data")
print("Warning : Iam not responsible of any losses caused by my script..")
print("          .. Use at your own risk :)")
print("")
print("- Full Source code at github @ticcersofficial -")
print("")
print("First Question :")
api_key = input("Please input your Api Key here (Binance): ")
print("Second Question :")
secret_code = input("Please input your Secret Code here (Binance): ")
print("Third Question :")
newb_cash = input("Please input the amount you want to invest in your limit order (Min = 11dollars): ")
cash = int(newb_cash)

print("SCRIPT [ON]")

binance = ccxt.binance ({
    'enableRateLimit' : True,
    'apiKey' : api_key,
    'secret' : secret_code,
})


side = 'buy'
timeframe = '15m' #sma2222:2
limit = 97    #sma
sma = 20        #sma
timeframe15m = '15m'
limit5m = 100
timeframe5m = '5m'



def script():

        market_params = {'type' : 'spot'}


        markets = binance.fetch_markets(params=market_params)


        all_symbols = pd.read_csv('bin_symbols.csv')

        random_symbole_pos = random.randrange(0,367)


        random_symbol = all_symbols.iloc[random_symbole_pos]['symbol']


        print(random_symbol)



        ################## SCANNING FOR SYMBOLS IS DONE
        ############ NOW ITS TIME FOR ALGO SHI

        ####### ASK BID FOR SMA################""
        def ask_bid(symbol = random_symbol):
            ob = binance.fetch_order_book(symbol=symbol)
            bid = ob['bids'][0][0]
            ask = ob['asks'][0][0]

            return ask, bid

        ####### SMA #################
        def df_sma(symbol= random_symbol, timeframe=timeframe, limit=limit, sma=sma):

            bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df_sma = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df_sma['timestamp'] = pd.to_datetime(df_sma['timestamp'], unit='ms')
            df_sma[f'sma{sma}_{timeframe}'] = df_sma.close.rolling(sma).mean()
            bid = ask_bid(symbol)[1]
            df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] > bid, 'sig'] = 'SELL'
            df_sma.loc[df_sma[f'sma{sma}_{timeframe}'] < bid, 'sig'] = 'BUY'
            df_sma['support'] = df_sma[:-2]['close'].min()
            df_sma['resis'] = df_sma[:-2]['close'].max()
            # FOR MRV AND DFSMA5m
            df_sma['PC'] = df_sma['close'].shift(1)
            df_sma.loc[df_sma['close'] > df_sma['PC'], 'lcbpc'] = True
            df_sma.loc[df_sma['close'] < df_sma['PC'], 'lcbpc'] = False

            return df_sma

        ######## ORDER BOOK ################
        def obd(symbol=random_symbol):

            df = pd.DataFrame()
            temp_df = pd.DataFrame()
            obd = binance.fetch_order_book(symbol)
            all_bids = obd['bids']
            all_asks = obd['asks']

            bid_vol_list = []

            ask_vol_list = []

            for x in range(11):
                for set in all_bids:
                    # print(set)
                    bid_price = set[0]
                    bid_vol = set[1]
                    bid_vol_list.append(bid_vol)
                    # print(bid_price)
                    # print(bid_vol)
                    sum_bidvol = sum(bid_vol_list)

                    temp_df['bid_vol'] = [sum_bidvol]

                for set in all_asks:
                    # print(set)
                    ask_price = set[0]
                    ask_vol = set[1]
                    ask_vol_list.append(ask_vol)
                    # print(ask_price)
                    # print(ask_vol)
                    sum_askvol = sum(ask_vol_list)
                    temp_df['ask_vol'] = [sum_askvol]

                time.sleep(5)
                df = df.append(temp_df)
                print(df)
                print(' ')
                print('-----------')
            print('Done calculating volume data..')
            print('calculating the sum...')
            total_bidvol = df['bid_vol'].sum()
            total_askvol = df['ask_vol'].sum()
            print(f'last min this is total BidVol : {total_bidvol} AskVol {total_askvol}')

            if total_bidvol > total_askvol:
                control_dec = (total_askvol/total_bidvol)
                print(f'{control_dec} %')
            else:
                control_dec = (total_bidvol/total_askvol)
                print(f'{control_dec} %')
                print('******NOT GOOD EFFECT ON OBD********')
                script()
            if control_dec < 0.74: ##### CHANGE FOR SPREAD PERC
                print('******NOT ENOUGH PERCENT***********')
                script()
        ######### MEAN REVERSION############
        def mrv(timeframe=timeframe5m):
            df_sma5m = df_sma(random_symbol, timeframe, limit5m, sma)
            lcbpc5m = df_sma5m['lcbpc'].iloc[-1]
            if lcbpc5m == False:
                print('***********NOT GOOD EFFECT ON MRV**********')
                script()

        ########## THE BOT BRAIN ################
        def bot(symbol = random_symbol, timeframe5 = timeframe5m, timeframe15 = timeframe15m, cash = cash):

            df_sma1 = df_sma(symbol, timeframe, limit, sma)
            sig = df_sma1.iloc[-1]['sig']
            if sig == 'SELL':
                print('********NOT GOOD EFFECT ON SMA**********')
                script()
            print('*******GOOD EFFECT ON SMA ANALYTICS******')
            mrv(timeframe = timeframe15)
            print('******GOOD EFFECT ON MRV ANALYTICS*******')
            variable = 1
            ini_final_variable = variable + 1
            obd()
            print('*******GOOD EFFECT ON ORDER BOOK DATA************')
            mrv(timeframe = timeframe5)
            final_variable = ini_final_variable + 1
            if final_variable == 3:
                price = ask_bid()[0]
                amount = cash / price # CHANGE FOR MIN DEPOSIT
                stop_price_ini = ask_bid()[0] * 0.03  # change for pnl stop limit
                stop_price = stop_price_ini + ask_bid()[0]
                binance.create_limit_buy_order(symbol, amount, price)
                binance.create_limit_sell_order(symbol, amount, stop_price)
                print(f'You just bought {amount} {symbol} by USDT!')
                print("********************************************")
                print("* All copyrights belong to @tahabouidraren in IG*")
                print("********************************************")
                print("SCRIPT [OFF]")
                exit()

        ######### INIT OF BOT ############
        bot()
        ########END OF SCRIPT ###########
script()
