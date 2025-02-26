import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
import time
from faker import Faker

print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @Xio
> › By      :- Rey Estacio
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛               
""")

print('\x1b[38;5;208m⇼'*60)

# Generate random string
def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Create a temporary email using 1secmail API
def get_temp_email():
    domain = "1secmail.net"
    username = generate_random_string(10)
    email = f"{username}@{domain}"
    return email, username, domain

# Fetch email verification code
def get_verification_code(username, domain):
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    for _ in range(15):  # Retry 15 times
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json():
                mail_id = response.json()[0]['id']
                mail_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={mail_id}"
                mail_content = requests.get(mail_url).json()
                return extract_verification_code(mail_content['body'])
        except Exception as e:
            print(f"[×] Error fetching email: {e}")
        time.sleep(10)  # Wait before retrying
    print("[×] No verification email received within time limit.")
    return "N/A"

# Extract the verification code from email body
def extract_verification_code(email_body):
    import re
    match = re.search(r'(\d{5,6})', email_body)
    return match.group(1) if match else "N/A"

# Register Facebook account
def register_facebook_account(email, password, first_name, last_name, birthday):
    session = requests.Session()
    fb_url = "https://m.facebook.com/reg"

    # Fake request to get cookies
    session.get(fb_url)
    cookies = session.cookies.get_dict()
    datr_cookie = cookies.get("datr", "N/A")

    print(f'''
-----------GENERATED-----------
EMAIL     : {email}
PASSWORD  : {password}
NAME      : {first_name} {last_name}
BIRTHDAY  : {birthday}
GENDER    : {random.choice(['M', 'F'])}
VERIFICATION CODE: {get_verification_code(email.split("@")[0], email.split("@")[1])}
-----------GENERATED-----------
datr=     : {datr_cookie}
-----------GENERATED-----------''')

# Main execution
if __name__ == "__main__":
    fake = Faker()
    num_accounts = int(input("[+] How Many Accounts You Want: "))

    for _ in range(num_accounts):
        email, username, domain = get_temp_email()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)

        register_facebook_account(email, password, first_name, last_name, birthday)

print('\x1b[38;5;208m⇼'*60)
