# Bennett vs. Bot: Who can perform better trading credit spreads?

## Criteria
**Option Expiration:** To keep the competition more manageable, both me and the bot will only be trading options contracts with 10 days to expiration
**Trade Frequency:** Every week a new spread will be made for each stock shown below
**Risk Management:** To keep simplicity, neither me or the bot is allowed to close any positions before expiration
**Stocks Available:** Below are the stocks that will be traded
- TSLA – Tesla Inc. (High volatility, growth/EV sector)
- NVDA – NVIDIA Corp. (Tech/AI momentum, very liquid options)
- COIN – Coinbase Global Inc. (Crypto, highly volatile)
- XLE – Energy Select Sector SPDR Fund (Energy exposure & macro sensitivity)
- JPM – JPMorgan Chase & Co. (Financial sector with strong option chains)

**Start Date:** Wednesday, June 18th
**End Date:** Trading will stop Wednesday, July 12th

# Current Metrics
## Leaderboard:
1st. Me
2nd. Bot

## Current Portfolios (As of EOD of previous day)

# Strucutre of Bot
![Screenshot 2025-06-17 at 7 55 52 PM](https://github.com/user-attachments/assets/13350b93-a335-4a94-a1aa-316b6313a328)
- **Green:** Start of the process, where the user enters the stock ticker and expiration date
- **Purple:** The class the analyzer is under
- **Blue:** Initial option chain scrape for the ticker, collected using the Tradier API (red diamond)
- **Light Red/Pink:** Spread metric calculator that takes the optoin chain dataframe and creates the metrics below:
    - Net Premium/Max Profit: Short market bid - long market ask
    - Width: The distance (in $) between the short and long strikes
    - Max Loss: (Short strike - long strike) - net premium
    - Breakeven: Short strike - net premium
    - Reward Risk Ratio: net premium / ((short strike - long strike) - net premium)
    - Probability of Profit: 1 - |short delta|
    - Black-Scholes Theoretical Price: Calcualted using a Black-Scholes pricing model to obtain a theoretical price of the option
    - Black-Scholes Z-score: The normalized distance (error) between the Black-Scholes price and the actual price
- **Yellow:** Where the model gives a score from 0-100 based on a personal weighing system using the metrics calculated above
- **Teal:** A streamlit dashboard where the user can filter and make their personal choice on what option spread to take
- **Orange:** Following certain criteria, the model picks the best option contract

# Dashboard

