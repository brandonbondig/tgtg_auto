def extract_and_open_link(username, password, imap_server, imap_port, desired_sender, timeout_minutes, path_to_chromedriver='chromedriver'):
    import imaplib
    import email
    import time
    from bs4 import BeautifulSoup
    import datetime
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Connect to the server using SSL
    connection = imaplib.IMAP4_SSL(imap_server, imap_port)
    connection.login(username, password)

    # Select the mailbox you want to check
    connection.select('inbox')

    while True:
        # Search for all emails and get the latest one
        result, data = connection.search(None, "ALL")
        if result == "OK":
            latest_email_id = data[0].split()[-1]  # Get the last email ID
            result, message_data = connection.fetch(
                latest_email_id, '(RFC822)')
            if result == "OK":
                email_data = message_data[0]
                if isinstance(email_data, tuple):
                    email_message = email.message_from_bytes(email_data[1])
                else:
                    print("Unexpected structure of message_data.")
                    continue

                # Get the sender
                sender = email.utils.parseaddr(email_message['From'])[1]

                # Get the timestamp
                date_tuple = email.utils.parsedate_tz(email_message['date'])
                timestamp = None
                if date_tuple:
                    timestamp = datetime.datetime.fromtimestamp(
                        email.utils.mktime_tz(date_tuple))

                # Check if the email is from the desired sender and less than 5 minutes old
                if sender == desired_sender and timestamp and (datetime.datetime.now() - timestamp).total_seconds() < timeout_minutes * 60:
                    # Get the email body (assuming it's HTML content)
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(
                                part.get("Content-Disposition"))
                            if "attachment" not in content_disposition and content_type == "text/html":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = email_message.get_payload(decode=True).decode()

                    # Use BeautifulSoup to parse the HTML and extract the first link
                    soup = BeautifulSoup(body, "html.parser")
                    first_link = soup.find('a', href=True)
                    # Found the link in the previous code
                    if first_link:
                        link_to_click = first_link['href']
                        print("First link found in the email:", link_to_click)

                        # Setup Chrome to run headless
                        chrome_options = Options()
                        chrome_options.add_argument("--headless")

                        # Path to the ChromeDriver
                        path_to_chromedriver = 'chromedriver'

                        # Start the headless Chrome
                        driver = webdriver.Chrome(
                            executable_path=path_to_chromedriver, options=chrome_options)

                        # Open the link
                        driver.get(link_to_click)

                        # Do anything else you want on the page here

                        # Close the browser
                        time.sleep(15)
                        driver.quit()

                    else:
                        print("No links found in the email.")
                    break
                else:
                    print(
                        f"Email from {sender} ignored or older than {timeout_minutes} minutes. Retrying in 2 seconds...")
                    time.sleep(2)
        else:
            print("No messages found. Retrying in 2 seconds...")
            time.sleep(2)

    # Close and logout
    connection.close()
    connection.logout()

