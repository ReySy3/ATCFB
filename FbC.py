import requests
import random
import string
import time
from faker import Faker

# Banner
print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- @Xio
> › By      :- Rey Estacio
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛               
""")

print('\x1b[38;5;208m⇼'*60)

# Generate a random email
def get_temp_email():
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{random_str}@1secmail.net"
    return email, random_str

# Fetch verification code from inbox
def get_verification_code(email, username):
    domain = "1secmail.net"
    for _ in range(15):  # Retry 15 times
        try:
            inbox_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
            messages = requests.get(inbox_url).json()
            
            if messages:
                msg_id = messages[0]["id"]
                email_data = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={msg_id}").json()
                return extract_verification_code(email_data["body"])
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
    response = session.get(fb_url)
    cookies = session.cookies.get_dict()
    
    # Debugging cookies received
    print(f"[DEBUG] Cookies received: {cookies}")

    return cookies.get("datr", "N/A")

# Simulate Facebook registration
def register_facebook_account(email, password, first_name, last_name, birthday, username):
    datr_cookie = get_facebook_cookies()
    verification_code = get_verification_code(email, username)
    
    # Simulating Facebook Registration Request
    fb_register_url = "https://www.facebook.com/api/register"  # Example URL (not real)
    payload = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "birthday": birthday,
        "verification_code": verification_code
    }
    
    response = requests.post(fb_register_url, data=payload)  # Simulated request
    try:
        user_id = response.json().get("id", "N/A")  # Extract user ID
    except:
        user_id = "N/A"

    print(f'''
-----------GENERATED-----------
EMAIL     : {email}
ID        : {user_id}
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
        email, username = get_temp_email()
        if not email:
            print("[×] Failed to get a temp email.")
            continue
        
        password = fake.password()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)

        register_facebook_account(email, password, first_name, last_name, birthday, username)

print('\x1b[38;5;208m⇼'*60)
