import requests
import random
import string
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

# Generate a random string
def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Get temp email from TempMail.dev
def get_temp_email():
    try:
        response = requests.get("https://api.tempmail.dev/request/mailbox")
        if response.status_code == 200:
            return response.json()["mailbox"]
    except Exception as e:
        print(f"[×] Error getting temp email: {e}")
    return None

# Fetch verification email
def get_verification_code(email):
    for _ in range(15):  # Retry 15 times
        try:
            inbox_url = f"https://api.tempmail.dev/request/mailbox/{email}/messages"
            response = requests.get(inbox_url)
            if response.status_code == 200 and response.json():
                for msg in response.json():
                    if "Facebook" in msg["from"]:
                        return extract_verification_code(msg["body"])
        except Exception as e:
            print(f"[×] Error fetching email: {e}")
        time.sleep(10)  # Wait before retrying
    print("[×] No verification email received within time limit.")
    return "N/A"

# Extract verification code
def extract_verification_code(email_body):
    import re
    match = re.search(r'(\d{5,6})', email_body)
    return match.group(1) if match else "N/A"

# Get Facebook `datr` cookie
def get_facebook_cookies():
    session = requests.Session()
    fb_url = "https://www.facebook.com/"
    session.get(fb_url)
    cookies = session.cookies.get_dict()
    return cookies.get("datr", "N/A")

# Register Facebook account
def register_facebook_account(email, password, first_name, last_name, birthday):
    datr_cookie = get_facebook_cookies()
    verification_code = get_verification_code(email)

    print(f'''
-----------GENERATED-----------
EMAIL     : {email}
PASSWORD  : {password}
NAME      : {first_name} {last_name}
BIRTHDAY  : {birthday}
GENDER    : {random.choice(['M', 'F'])}
VERIFICATION CODE: {verification_code}
-----------GENERATED-----------
datr=     : {datr_cookie}
-----------GENERATED-----------''')

# Main execution
if __name__ == "__main__":
    fake = Faker()
    num_accounts = int(input("[+] How Many Accounts You Want: "))

    for _ in range(num_accounts):
        email = get_temp_email()
        if not email:
            print("[×] Failed to get a temp email.")
            continue
        
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)

        register_facebook_account(email, password, first_name, last_name, birthday)

print('\x1b[38;5;208m⇼'*60)
