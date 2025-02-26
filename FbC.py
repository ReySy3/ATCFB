import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
import time
from faker import Faker

# Console banner
print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @jatintiwari0 
> › By      :- JATIN TIWARI00
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                """)
print('\x1b[38;5;208m⇼'*60)

# Generate a random string
def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# Fetch a temporary email from TempMail.dev
def get_temp_email():
    url = "https://api.tempmail.dev/request/mailbox"
    try:
        response = requests.post(url)
        if response.status_code == 201:
            email_data = response.json()
            return email_data['email'], email_data['token']
        else:
            print(f'[×] Error fetching temp email: {response.text}')
            return None, None
    except Exception as e:
        print(f'[×] Error: {e}')
        return None, None

# Check inbox for verification code
def get_verification_code(email, token):
    url = f"https://api.tempmail.dev/request/mailbox/{token}"
    for _ in range(15):  # Retry for 15 times
        try:
            response = requests.get(url)
            if response.status_code == 200:
                emails = response.json().get('emails', [])
                for mail in emails:
                    if "Facebook" in mail['from']:
                        # Extract verification code
                        return extract_code(mail['subject'])
            print("[×] Inbox is empty. Retrying...")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f'[×] Error fetching email: {e}')
    return None  # No code found

# Extract verification code from email subject
def extract_code(subject):
    code = ''.join(filter(str.isdigit, subject))
    return code if code else None

# Create a Facebook account
def register_facebook_account(email, password, first_name, last_name, birthday):
    api_key = '882a8490361da98702bf97a021ddc14d'
    secret = '62f8ce9f74b12f84c123cc23437a4a32'
    gender = random.choice(['M', 'F'])
    
    req = {
        'api_key': api_key,
        'attempt_login': True,
        'birthday': birthday.strftime('%Y-%m-%d'),
        'client_country_code': 'EN',
        'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': first_name,
        'format': 'json',
        'gender': gender,
        'lastname': last_name,
        'email': email,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': generate_random_string(32),
        'return_multiple_errors': True
    }

    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig

    api_url = 'https://b-api.facebook.com/method/user.register'
    reg = requests.post(api_url, data=req).json()
    
    if 'new_user_id' in reg:
        return reg['new_user_id'], reg['session_info']['access_token']
    return None, None

# Main execution
fake = Faker()
email, token = get_temp_email()
if email:
    print(f"[+] Temporary email generated: {email}")
    
    password = fake.password()
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
    first_name = fake.first_name()
    last_name = fake.last_name()

    user_id, fb_token = register_facebook_account(email, password, first_name, last_name, birthday)

    verification_code = get_verification_code(email, token)
    if not verification_code:
        verification_code = "N/A"

    print(f'''
-----------GENERATED-----------
EMAIL     : {email}
ID        : {user_id if user_id else "N/A"}
PASSWORD  : {password}
NAME      : {first_name} {last_name}
BIRTHDAY  : {birthday}
GENDER    : {random.choice(["M", "F"])}
VERIFICATION CODE: {verification_code}
-----------GENERATED-----------
Token     : {fb_token if fb_token else "N/A"}
-----------GENERATED-----------
''')
else:
    print("[×] Failed to get a temp email.")
