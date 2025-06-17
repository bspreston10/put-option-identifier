# Bennett vs. Bot: Who can perform better trading credit spreads?

## Criteria
**Option Expiration:** To keep the competition more manageable, both me and the bot will only be trading options contracts with 10 days to expiration
**Trade Frequency:** Every week a new spread will be made for each stock shown below
**Risk Management:** To keep simplicity, neither me or the bot is allowed to close any positions before expiration
**Stocks Available:** Below are the stocks that will be traded
- TSLA – Tesla Inc. (High volatility, growth/EV sector)
- NVDA – NVIDIA Corp. (Tech/AI momentum, very liquid options)
- AAPL – Apple Inc. (Mega-cap stability, tight spreads, great volume)
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
flowchart TD
    A[Start: Initialize SPYOptionsAnalyzer] --> B[Fetch Option Chains from Tradier API]
    B --> C[Find Put Spreads]
    C --> D[Calculate Spread Metrics<br/>(BS Model + Greeks)]
    D --> E[Score Spreads<br/>(MinMaxScaler + Weighted Sum)]
    E --> F[Filter for Personal Picks]
    F --> G[Find Option Contracts (long/short legs)]
    F --> H[Unscaled Metrics]
    E --> I[Computer-Picked Spreads<br/>Filters + Score]
    G --> J[Verify with Broker]

    style A fill:#f9f,stroke:#333,stroke-width:1px
    style J fill:#9f9,stroke:#333,stroke-width:1px

