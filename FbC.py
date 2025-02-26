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
> › By      :- JATIN TIWARI
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""")
print('\x1b[38;5;208m⇼'*60)

# Generate a random username for 1secmail
def generate_email():
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    domain = random.choice(["1secmail.com", "1secmail.org", "1secmail.net"])
    return f"{username}@{domain}", username, domain

# Fetch verification code from 1secmail inbox
def get_verification_code(username, domain):
    base_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    
    for _ in range(15):  # Retry up to 15 times
        try:
            response = requests.get(base_url).json()
            if response:
                for mail in response:
                    mail_id = mail["id"]
                    mail_details = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={mail_id}").json()
                    if "Facebook" in mail_details["from"]:
                        return extract_code(mail_details["subject"])
            print("[×] Inbox is empty. Retrying...")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f'[×] Error fetching email: {e}')
    
    return None  # No code found

# Extract verification code from subject
def extract_code(subject):
    return ''.join(filter(str.isdigit, subject)) or "N/A"

# Register a Facebook account and get the `datr` cookie
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
        'reg_instance': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
        'return_multiple_errors': True
    }

    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    req['sig'] = hashlib.md5((sig + secret).encode()).hexdigest()

    api_url = 'https://b-api.facebook.com/method/user.register'
    session = requests.Session()
    reg = session.post(api_url, data=req)

    if 'new_user_id' in reg.json():
        user_id = reg.json()['new_user_id']
        datr_cookie = session.cookies.get_dict().get('datr', 'N/A')  # Extract 'datr' cookie
        return user_id, datr_cookie
    
    return None, None

# Main execution
fake = Faker()
email, username, domain = generate_email()
print(f"[+] Temporary email generated: {email}")

password = fake.password()
birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
first_name = fake.first_name()
last_name = fake.last_name()

user_id, datr_cookie = register_facebook_account(email, password, first_name, last_name, birthday)

verification_code = get_verification_code(username, domain)
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
DATR Cookie: {datr_cookie if datr_cookie else "N/A"}
-----------GENERATED-----------
''')
