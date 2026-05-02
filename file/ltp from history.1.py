# Package import statement
from SmartApi import SmartConnect
import pyotp
from logzero import logger
from datetime import datetime, timedelta
import time
import pandas as pd
import credentials as wd

# Initialize Smart API connection
smartApi = SmartConnect(wd.api_key)

try:
    # Generate TOTP token
    totp = pyotp.TOTP(wd.Token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

try:
    # Generate session
    data = smartApi.generateSession(wd.username, wd.pwd, totp)

    if not data['status']:
        logger.error(data)
        raise ValueError("Failed to generate session")

    # Extract tokens
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']

    # Fetch the feed token
    feedToken = smartApi.getfeedToken()

    # Fetch user profile and generate token
    profile = smartApi.getProfile(refreshToken)
    smartApi.generateToken(refreshToken)
    logger.info("Session generated successfully.")
except Exception as e:
    logger.exception(f"Session generation failed: {e}")
    raise e

# Variable to track if historical data has been downloaded
historical_data_downloaded = False
historical_data_location = 'Ltpfromhistory_data1.csv'  # Specify the file location

# Load stock symbols and tokens from Excel
try:
    df = pd.read_excel(wd.XLpath, sheet_name='Multiplier_5')
    symbols_tokens = df[['SymbolName', 'token']].dropna().to_dict(orient='records')
except Exception as e:
    logger.error(f"Failed to load stock symbols and tokens from Excel: {e}")
    raise e

# Get the current datetime
current_time = datetime.now()

# Loop through all tokens and fetch historical data with rate limiting
historical_data = []
batch_size = 3  # Maximum 3 hits per second
for i in range(0, len(symbols_tokens), batch_size):
    batch = symbols_tokens[i:i + batch_size]
    
    for item in batch:
        symbol = item['SymbolName']
        token = str(item['token'])

        try:
            historicParam = {
                "exchange": "NSE",
                "symboltoken": token,
                "interval": "ONE_MINUTE",
                "fromdate": (current_time - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M"),
                "todate": current_time.strftime("%Y-%m-%d %H:%M")
            }

            # Fetch historical data
            data = smartApi.getCandleData(historicParam).get('data', [])
            logger.info(f"Downloaded historical data for {symbol} ({token}).")

            # Convert to DataFrame and append symbol and token
            df_data = pd.DataFrame(data, columns=["Datetime", "Open", "High", "Low", "Close", "Volume"])
            df_data['Datetime'] = pd.to_datetime(df_data['Datetime'])
            df_data['Symbol'] = symbol
            df_data['Token'] = token

            historical_data.append(df_data)
        except Exception as e:
            logger.error(f"Failed to fetch historical data for {symbol} ({token}): {e}")

    # Wait for 1 second before hitting the next batch
    time.sleep(1)

# Save all historical data to a CSV file
if historical_data:
    all_data = pd.concat(historical_data, ignore_index=True)
    all_data.to_csv(historical_data_location, index=False)
    logger.info(f"All historical data saved to {historical_data_location}.")

    # Append the data back to Excel
    try:
        with pd.ExcelWriter(wd.XLpath, engine='openpyxl', mode='a') as writer:
            all_data.to_excel(writer, sheet_name='Downloaded_Data', index=False)
        logger.info("Historical data added to Excel.")
    except Exception as e:
        logger.error(f"Failed to write historical data to Excel: {e}")

    historical_data_downloaded = True
else:
    logger.warning("No historical data was downloaded.")

# Logout logic
try:
    if historical_data_downloaded:
        try:
            smartApi.terminateSession(wd.username)
            logger.info("Logout successful.")
        except Exception as e:
            logger.exception(f"Logout failed: {e}")
except Exception as e:
    logger.exception(f"Error during logout logic: {e}")
