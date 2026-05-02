# Project-2_Historical_data
historical data for trading stratergies and pattern recognition

## historical data download for pattern recognition and backtesting

### Duration: Dec 2023 - april 2024 
**Git upload : 2 may 2026**

## Summary:

Trading bot template for NSE historical data extraction + visualization with auto-session management.

## Basic workflow 
    START
      ↓
    [IMPORTS ✓] ──(credentials.py)──> [SmartConnect INIT ✓]
      ↓
    [TOTP 2FA ✓] ──(30-sec token)──> [generateSession ✓]
      ↓
    [JWT+REFRESH ✓] ──(getfeedToken)──> [getProfile ✓]
      ↓
    [HISTORIC PARAMS] ──(NSE:3045)──> [getCandleData ✓]
      ↓
    [DataFrame ✓] ──(datetime index)──> [SAVE CSV ✓]
      ↓
    [historical_data_downloaded=TRUE] ──> [mplfinance ✓]
      ↓
    [SAVE PNG ✓] ──(flag triggered)───> [LOGOUT LOOP ✓]
      ↓
    [TIME 15:25 OR FLAG] ──> [terminateSession ✓]
      ↓
    END (Clean Exit)

## Tools 
Python, SQL, VS code, Excel, Json

## Libraries used 
Pandas, Matplotlib, tKinter, SmartApi, pyotp, asyncio, Telegram

## API connection
AngelOne API

## Market 
NSE

## Steps 

1- Credentials and TOTP
  Initialize API client with credentials and generate TOTP-authenticated session

2- Data Collection
  Fetch historical candle data for NSE symbols on particular dates

3- Convertion and data storage
  process data using pandas dataframe, then save the file in csv and chart in PNG format

4- data monitoring
  data monitoring for data or time skip and filtering out in the csv

5- termination of each session
  terminating session cleanly with logging

## Architecture
    MAIN EXECUTION FLOW 
    ├── 1. DEPENDENCY LOADING 
    │   ├── SmartConnect import → Angel One API client ✓
    │   ├── pyotp → TOTP 2FA generator ✓
    │   ├── logzero.logger → Structured logging ✓
    │   ├── datetime/time → Time management ✓
    │   ├── pandas → DataFrame operations ✓
    │   ├── matplotlib/mplfinance → Candlestick charts ✓
    │   └── credentials.py → Secure config loading ✓
    │
    ├── 2. API INITIALIZATION 
    │   ├── SmartConnect(api_key) → Client instance ✓
    │   ├── TOTP validation → 30-sec token ✓
    │   └── Exception handling → Token failure detection ✓
    │
    ├── 3. SESSION AUTHENTICATION 
    │   ├── generateSession(user,pwd,totp) → Primary auth ✓
    │   ├── Extract jwtToken → API authorization ✓
    │   ├── Extract refreshToken → Session renewal ✓
    │   ├── getfeedToken() → Live data subscription ✓
    │   ├── getProfile(refreshToken) → User verification ✓
    │   ├── generateToken(refreshToken) → Session refresh ✓
    │   ├── Status validation → API response check ✓
    │   └── Full token stack → Production ready ✓
    │
    ├── 4. HISTORICAL DATA ENGINE 
    │   ├── NSE exchange → Primary market ✓
    │   ├── symboltoken=3045 → BANKNIFTY index ✓
    │   ├── ONE_MINUTE interval → High frequency ✓
    │   ├── fromdate=15:29 → Precise timestamp ✓
    │   ├── todate=15:00 → Format issue 
    │   ├── getCandleData() → OHLCV response ✓
    │   ├── DataFrame conversion → Structured data ✓
    │   ├── Datetime parsing → Time-series index ✓
    │   ├── CSV export → Persistent storage ✓
    │   ├── Flag update → Workflow control ✓
    │   └── Data validation → Integrity check ✓
    │
    ├── 5. VISUALIZATION PIPELINE 
    │   ├── mplfinance.candle → OHLC rendering ✓
    │   ├── style='charles' → Professional theme ✓
    │   ├── volume=True → Trading volume overlay ✓
    │   ├── savefig PNG → Shareable asset ✓
    │   └── Title/ylabel → Production labels ✓
    │
    └── 6. LOGOUT WATCHDOG 
        ├── Infinite monitoring loop ✓
        ├── Time check (15:25) → Market hours ✓
        ├── Flag check → Data completion ✓
        ├── 60-sec polling → Resource efficient ✓
        ├── terminateSession() → Clean logout ✓
        ├── Exception recovery → Robust termination ✓
        ├── Loop break → Controlled exit ✓
        └── Full logging → Audit trail ✓
## Results: 
  ### (historical_data2.4.csv + candlestick_chart2.4.png) files are generated and downloaded

  ### session closed

the script call API for login and authentication 

then fetches data from input symbol number and datetime

stores the data in the path as CSV file along with PNG of candlestick data

the script ends session with a terminate with watchdog option

## Conclusion:

Production-ready NSE data harvesting script with enterprise-grade error handling, logging, and auto-cleanup. 

# Acheivements

1. NSE Historical Data Automation (1-min - 1-day granularity)
2. Enterprise-grade Session Management
3. Professional Candlestick Visualization
4. Auto-cleanup Watchdog
5. Persistent Storage
6. Full Error Handling + Logging Stack
7. Zero manual intervention required
8. Resource-efficient monitoring
