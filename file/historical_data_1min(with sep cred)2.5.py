# Package import statement
from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
from datetime import datetime
import time
import pandas as pd  # Import pandas for data handling
import matplotlib.pyplot as plt
import mplfinance as mpf

import credentials as wd

# API credentials

# Initialize Smart API connection
smartApi = SmartConnect(wd.api_key)

try:
     # Your TOTP token here
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
historical_data_location = 'historical_data2.5.csv'  # Specify the file location

# Historic API call
try:
    historicParam = {
        "exchange": "NSE",
        "symboltoken": "3045",
        "interval": "ONE_MINUTE",
        "fromdate": "2025-01-03 09:16",
        "todate": "2025-01-03 15:29"
    }

    # Fetch historical data
    historical_data = smartApi.getCandleData(historicParam)['data']
    logger.info("Historical data downloaded successfully.")
    
    # Convert to DataFrame
    df = pd.DataFrame(historical_data, columns=["Datetime", "Open", "High", "Low", "Close", "Volume"])
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)
    
    # Save the DataFrame to a CSV file
    df.to_csv(historical_data_location)
    logger.info(f"Historical data saved to {historical_data_location}.")
    
    
    historical_data_downloaded = True  # Mark as downloaded
except Exception as e:
    logger.exception(f"Historic API call failed: {e}")

# Logout logic
try:
    while True:
        current_time = datetime.now()

        # Check if it's after 3:25 PM or if historical data has been downloaded
        if (current_time.hour == 15 and current_time.minute >= 25) or historical_data_downloaded:
            try:
                smartApi.terminateSession(wd.username)
                logger.info("Logout successful.")
            except Exception as e:
                logger.exception(f"Logout failed: {e}")
            finally:
                break  # Exit the loop after logout

        # Sleep for a minute before checking again
        time.sleep(60)
except Exception as e:
    logger.exception(f"Error during logout loop: {e}")

