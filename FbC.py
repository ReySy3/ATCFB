import threading
import requests
import random
import string
import json
import hashlib
import time
import re
from queue import Queue
from faker import Faker

print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- Xio
> › By      :- Rey Estacio
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""")

print('\x1b[38;5;208m⇼' * 60)

def generate_random_string(length):
    """Generate a random alphanumeric string."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def create_1secmail_account():
    """Generates a random email using 1secmail domains."""
    username = generate_random_string(10)
    domain = random.choice(["1secmail.com", "1secmail.net", "1secmail.org"])
    email = f"{username}@{domain}"
    return email

def get_1secmail_verification_code(email, debug=False):
    """Fetches the verification code from 1secmail inbox."""
    login, domain = email.split("@")
    inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"

    print(f"[+] Waiting for verification email at: {email}")

    for attempt in range(15):  # Wait up to 30 seconds (15 attempts, 2s delay each)
        try:
            response = requests.get(inbox_url)

            if response.status_code == 200 and response.text.strip():
                messages = response.json()

                if messages:
                    latest_email_id = messages[0]["id"]
                    message_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={latest_email_id}"
                    message_response = requests.get(message_url)

                    if message_response.status_code == 200 and message_response.text.strip():
                        content = message_response.json().get("body", "")
                        if debug:
                            print(f"[DEBUG] Email Content:\n{content}")

                        code_match = re.search(r'\b\d{6}\b', content)  # Find a 6-digit code
                        if code_match:
                            return code_match.group()
                        else:
                            print("[×] No verification code found in the email.")
                    else:
                        print("[×] Failed to read the email content.")
            else:
                print("[×] Inbox is empty. Retrying...")
        except Exception as e:
            print(f"[×] Error fetching email: {e}")

        time.sleep(2)  # Wait before retrying

    print("[×] No verification email received within time limit.")
    return None

def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    """Registers a Facebook account."""
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
    reg = _call(api_url, req, proxy)
    
    if 'new_user_id' in reg:
        user_id = reg['new_user_id']
        token = reg['session_info']['access_token']
    else:
        user_id = "N/A"
        token = "N/A"

    verification_code = get_1secmail_verification_code(email)

    print(f'''
-----------GENERATED-----------
EMAIL     : {email}
ID        : {user_id}
PASSWORD  : {password}
NAME      : {first_name} {last_name}
BIRTHDAY  : {birthday} 
GENDER    : {gender}
VERIFICATION CODE: {verification_code if verification_code else "N/A"}
-----------GENERATED-----------
Token     : {token}
-----------GENERATED-----------''')

def _call(url, params, proxy=None, post=True):
    headers = {'User-Agent': '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'}
    if post:
        response = requests.post(url, data=params, headers=headers, proxies=proxy)
    else:
        response = requests.get(url, params=params, headers=headers, proxies=proxy)
    return response.json()

def load_proxies():
    with open('proxies.txt', 'r') as file:
        proxies = [line.strip() for line in file]
    return [{'http': f'http://{proxy}'} for proxy in proxies]

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

    q.join()  # Block until all tasks are done
    return valid_proxies

def worker_test_proxy(q, valid_proxies):
    while True:
        proxy = q.get()
        if proxy is None:
            break
        test_proxy(proxy, q, valid_proxies)

def test_proxy(proxy, q, valid_proxies):
    if test_proxy_helper(proxy):
        valid_proxies.append(proxy)
    q.task_done()

def test_proxy_helper(proxy):
    try:
        response = requests.get('https://api.mail.tm', proxies=proxy, timeout=5)
        return response.status_code == 200
    except:
        return False

working_proxies = get_working_proxies()

if not working_proxies:
    print('[×] No working proxies found. Please check your proxies.')
else:
    for _ in range(int(input('[+] How Many Accounts You Want:  '))):
        proxy = random.choice(working_proxies)
        fake = Faker()
        email = create_1secmail_account()
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)

        register_facebook_account(email, password, first_name, last_name, birthday, proxy)

print('\x1b[38;5;208m⇼' * 60)
