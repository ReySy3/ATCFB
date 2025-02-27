import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
from faker import Faker
import time

# Display Banner
print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @jatintiwari0 
> › By      :- JATIN TIWARI
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""")
print('\x1b[38;5;208m⇼'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;208m⇼'*60)

# Temp-Mail API Endpoint
TEMP_MAIL_API = "https://api.tempmail.lol"

# Helper function to generate a random string
def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Function to generate a Temp-Mail email
def create_temp_mail(proxy=None):
    try:
        response = requests.get(f"{TEMP_MAIL_API}/generate", proxies=proxy, timeout=5)
        if response.status_code == 200:
            data = response.json()
            email = data.get("address")
            token = data.get("token")
            return email, token
        else:
            print(f'[×] Temp-Mail Error: {response.text}')
            return None, None
    except Exception as e:
        print(f'[×] Temp-Mail Connection Error: {e}')
        return None, None

# Function to get verification code from Temp-Mail inbox
def get_verification_code(token, proxy=None):
    try:
        url = f"{TEMP_MAIL_API}/inbox?token={token}"
        for _ in range(10):  # Retry up to 10 times
            response = requests.get(url, proxies=proxy, timeout=5)
            if response.status_code == 200:
                messages = response.json().get("emails", [])
                if messages:
                    for message in messages:
                        if "code" in message["subject"]:
                            return message["subject"]
                time.sleep(3)  # Wait before retrying
        return None
    except Exception as e:
        print(f'[×] Email Check Error: {e}')
        return None

# Function to register a Facebook account
def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
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

    # Generate signature
    sorted_req = sorted(req.items(), key=lambda x: x[0])
    sig = ''.join(f'{k}={v}' for k, v in sorted_req)
    ensig = hashlib.md5((sig + secret).encode()).hexdigest()
    req['sig'] = ensig

    # Call API
    api_url = 'https://b-api.facebook.com/method/user.register'
    reg = _call(api_url, req, proxy)
    
    if reg and 'new_user_id' in reg:
        user_id = reg['new_user_id']
        token = reg['session_info']['access_token']
        print(f'''
-----------GENERATED-----------
EMAIL     : {email}
ID        : {user_id}
PASSWORD  : {password}
NAME      : {first_name} {last_name}
BIRTHDAY  : {birthday} 
GENDER    : {gender}
-----------GENERATED-----------
Token     : {token}
-----------GENERATED-----------''')
        with open('username.txt', 'a') as f:
            f.write(f'{email} | {password} | {user_id} | {token}\n')

# Function to send API request
def _call(url, params, proxy=None, post=True):
    headers = {'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'}
    try:
        if post:
            response = requests.post(url, data=params, headers=headers, proxies=proxy, timeout=5)
        else:
            response = requests.get(url, params=params, headers=headers, proxies=proxy, timeout=5)
        return response.json()
    except Exception as e:
        print(f"[×] API Error: {e}")
        return None

# Proxy testing
def test_proxy(proxy, q, valid_proxies):
    if test_proxy_helper(proxy):
        valid_proxies.append(proxy)
    q.task_done()

def test_proxy_helper(proxy):
    try:
        response = requests.get(TEMP_MAIL_API, proxies=proxy, timeout=5)
        return response.status_code == 200
    except:
        return False

# Load proxies from file
def load_proxies():
    with open('proxies.txt', 'r') as file:
        return [{'http': f'http://{line.strip()}'} for line in file]

# Get working proxies
def get_working_proxies():
    proxies = load_proxies()
    valid_proxies = []
    q = Queue()

    for proxy in proxies:
        q.put(proxy)

    for _ in range(10):  # 10 threads
        worker = threading.Thread(target=worker_test_proxy, args=(q, valid_proxies))
        worker.daemon = True
        worker.start()

    q.join()
    return valid_proxies

def worker_test_proxy(q, valid_proxies):
    while not q.empty():
        proxy = q.get()
        test_proxy(proxy, q, valid_proxies)

# Main execution
working_proxies = get_working_proxies()

if not working_proxies:
    print('[×] No working proxies found.')
else:
    num_accounts = int(input('[+] How Many Accounts You Want: '))
    
    for _ in range(num_accounts):
        proxy = random.choice(working_proxies)
        
        # Generate a temporary email
        email, token = create_temp_mail(proxy)
        if not email or not token:
            continue
        
        fake = Faker()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
        
        # Register Facebook account
        register_facebook_account(email, password, first_name, last_name, birthday, proxy)

print('\x1b[38;5;208m⇼'*60)
