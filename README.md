# TGTG - Automated Order Placement Script

## Overview
This script facilitates automated order placement at a specific time using the TGTG platform. It combines the functionality of TGTG Client for order processing and email-based triggers for execution initiation. Using py-adyen payment encryption.


## Usage
1. **Environment Setup**: Initialize required environment variables for payment card details (refer to `.env.example`).
2. **Script Execution**: Run `main.py`. This is the starting point of the automation process.
3. **Email Verification**: Enter your email address. You'll receive a verification link via email. Click the link to authenticate.
4. **Product Selection**: The script fetches your favorited products from TGTG. Choose a product for automation.
5. **Time Configuration**: Specify the exact time for the script to execute the purchase.
6. **Order Automation**: The script will automatically place the order for the selected product at the set time.

## Files
- `main.py`: Entry point of the script. Calls `place_order_at_time` from `functions.py`.
- `mail.py`: Contains the `extract_and_open_link` function. It logs into an email account, checks for new emails from a specific sender, extracts the first link in the email, and opens it using Selenium with Chrome in headless mode.
- `functions.py`: Contains two functions: `ask_for_time` and `place_order_at_time`. The former prompts the user to specify the time for order placement, and the latter automates the order placement process using the TGTG Client.

## Functionality
1. **Email Monitoring (`mail.py`)**: Monitors a specified email account for new emails from a certain sender. Opens the first link found in a new email using a headless Chrome browser.
   
2. **Time-based Order Placement (`functions.py`)**:
   - `ask_for_time`: Prompts the user to enter the time for placing the order.
   - `place_order_at_time`: Automates the order placement process at the specified time. It logs into the TGTG Client, retrieves the user's favorite items, allows the user to select an item, and places the order at the specified time.

## Requirements
- Python 3.x
- Libraries: `imaplib`, `email`, `datetime`, `bs4`, `selenium`, `tgtgpython`, `inquirer`, `dotenv`
- A valid TGTG account and email account credentials.
- Environment variables for card details (`CARD_NUMBER`, `CVV`, `MONTH`, `YEAR`).
**(see `.env.example`)**



## Notes
- The script is designed for educational purposes and should be used responsibly.
- Ensure that the `chromedriver` is compatible with your Chrome version and is correctly set in your PATH.
