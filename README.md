# algobot
Algobot is a full blown Algorithm bot that uses 3 market leading trading startegies (Order Book Data - SMA - Mean Reversion) to find the best opportunities in the limit market and then it places your limit order instantly.

- Requirement:

You need to have Python 3 installed in your OS
[Tested on Python 3.8]

and also :
`pip3 install ccxt`
`pip3 install pandas`
`pip3 install schedule`

you can also do:
`pip3 install -r req.txt`

- Usage:

After installing Python and all the modules above , all you have to do now is run the script and answer the questions inside the script.

- Features:

This bot is a full standalone bot that is capable of a lot of stuff

In a nutshell :

It takes your information at first and it connects to your Binance platform, after that it starts scanning all the currencies available in the Limit Market inside Binance (You can find them all inside the file `bin_symbols.csv` '366' Currency), then it randomly picks one and starts to scan it, The first trading strategy the bot uses is SMA, the second one is MRV or Mean Reversion, and last but not least is the Order Book Data, and if only all of them check out as correct or convenient to buy in this currency only then the bot will place the Limit Order and the Stop Loss (3% gain).

![Capture](https://user-images.githubusercontent.com/59410756/197873935-ab872039-134f-4905-9934-fe7d787443eb.PNG)

![Capture1](https://user-images.githubusercontent.com/59410756/197873984-22fab63c-4781-4d63-b8c2-d90d4f0f5e57.PNG)
`If one strategy is not valid , the bot picks another currency automatically and starts to scan it`

- Screenshots:

![Capture2](https://user-images.githubusercontent.com/59410756/197876744-b753c6dc-8692-46b4-8bae-93b38ba5aebe.PNG)

![Capture3](https://user-images.githubusercontent.com/59410756/197876749-be02cd95-77a9-4ea4-a8e8-4178ef62d55f.PNG)

- Side Note:

This project took me approximately 1 week from researching the strategies and applying them to python and the fusion between them and `ccxt`.

While trying out this bot I had a stable 10% pnl gain.

- Warning :

I'm not responsible for any losses you get from using my script, Use it at your own risk :)

Signed : @tahabouidraren

