from tgtgpython.tgtg import TgtgClient
from datetime import datetime, timedelta
import time
import inquirer

import os
from dotenv import load_dotenv

load_dotenv()



# Function to ask for time input


def ask_for_time():

    hour_question = [
        inquirer.List('hour',
                      message="Choose an hour",
                      choices=[str(h).zfill(2) for h in range(24)],
                      ),
    ]
    minute_question = [
        inquirer.List('minute',
                      message="Choose a minute",
                      choices=[str(m).zfill(2) for m in range(60)],
                      ),
    ]
    second_question = [
        inquirer.List('second',
                      message="Choose a second",
                      choices=[str(s).zfill(2) for s in range(60)],
                      ),
    ]

    hour_answer = inquirer.prompt(hour_question)
    minute_answer = inquirer.prompt(minute_question)
    second_answer = inquirer.prompt(second_question)

    return int(hour_answer['hour']), int(minute_answer['minute']), int(second_answer['second'])


def place_order_at_time():
    # Email address of the account to use
    email = input("Enter your email: ")

    # ENV card variables
    card_number = os.getenv("CARD_NUMBER")
    cvv = os.getenv("CVV")
    month = os.getenv("MONTH")
    year = os.getenv("YEAR")

    # Initialize the TGTG client
    client = TgtgClient(email=email)
    client.get_credentials()

    # Get the item ID of the first favorited item
    favorite_item = client.get_favorites()

    # create dict for the items
    item_dict = {}

    for entry in favorite_item:
        item = entry['item']
        store = entry['store']
        item_id = item['item_id']
        name = item['name']
        seller_address = store['store_location']['address']['address_line']
        price = item['price_including_taxes']['minor_units'] / \
            (10 ** item['price_including_taxes']['decimals'])
        currency_code = item['price_including_taxes']['code']
        seller_name = entry['store']['store_name']

        # store the items in a dict and inside the item_id every item should be stored by their name as key
        item_dict[item_id] = {'name': name, 'seller_address': seller_address,
                              'price': price, 'currency_code': currency_code, 'seller_name': seller_name}

    choices = {f"{product['name']} - {product['seller_name']} - {product['seller_address']} - {product['price']} {product['currency_code']}":
               product_id for product_id, product in item_dict.items()}

    questions = [
        inquirer.List('product_id',
                      message="Choose a product",
                      choices=list(choices.keys()),
                      ),
    ]

    answers = inquirer.prompt(questions)
    selected_product_id = choices[answers['product_id']]

    # Example usage
    hour, minute, second = ask_for_time()
    print(f"Order will be placed at {hour}:{minute}:{second}")

    # Determine the target time for placing the order
    now = datetime.now()
    target_time = now.replace(hour=hour, minute=minute,
                              second=second, microsecond=0)
    if now > target_time:
        target_time += timedelta(days=1)
    wait_seconds = (target_time - now).total_seconds()

    # Wait until the target time
    time.sleep(wait_seconds)

    # Place the order and pay
    order = client.create_order(selected_product_id, 1)
    order_status = client.get_order_status(order['id'])
    pay = client.pay_order(order_id=order["id"], card_data={
                           "card":card_number, "cvv": cvv, "month": month, "year": year})

    # Print order details
    print("------------------")
    print("[ORDER]:", order)
    print("------------------")
    print("[ORDER_STATUS]:", order_status)
    print("------------------")
    print("[PAY]:", pay)
    print("------------------")
