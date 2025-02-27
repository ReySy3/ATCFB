import requests
import time
import random
import re

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    LOGO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logo = """\033[92m
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
> › Github :- @Xio
> › By      :- Rey Estacio
> › Proxy Support Added by @coopers-lab
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
\033[0m"""

print(logo)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MAILTM_API = "https://api.mail.tm"

def get_temp_email():
    """Get a new temporary email from mail.tm."""
    response = requests.post(f"{MAILTM_API}/accounts", json={})
    if response.status_code == 201:
        data = response.json()
        return data["address"], data["id"], data["password"]
    else:
        print("[×] Error generating temp email.")
        return None, None, None

def get_inbox_messages(email_id, token):
    """Fetch messages from the inbox."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{MAILTM_API}/messages", headers=headers)
    if response.status_code == 200:
        messages = response.json()["hydra:member"]
        return messages
    return []

def get_verification_code(email_id, token):
    """Retrieve the verification code from the latest email."""
    for _ in range(10):  # Retry for 10 seconds
        messages = get_inbox_messages(email_id, token)
        if messages:
            for msg in messages:
                if "Your Verification Code" in msg["subject"]:
                    email_response = requests.get(f"{MAILTM_API}/messages/{msg['id']}", headers={"Authorization": f"Bearer {token}"})
                    if email_response.status_code == 200:
                        return extract_code(email_response.json()["text"])
        time.sleep(2)
    return None

def extract_code(text):
    """Extracts a 6-digit verification code from text."""
    match = re.search(r"\b\d{6}\b", text)
    return match.group(0) if match else None

def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    """Simulate Facebook registration (You need to complete this part)."""
    session = requests.Session()
    
    # Simulated Facebook registration request
    print(f"[+] Registering Facebook account: {email}")
    
    # Simulate getting DATR Cookie (Replace this with real scraping)
    cookies = session.cookies.get_dict()
    datr_cookie = cookies.get("datr", "N/A")
    
    return {"email": email, "password": password, "name": f"{first_name} {last_name}", "birthday": birthday, "datr": datr_cookie}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    MAIN FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    print("\n[+] How Many Accounts You Want: 1")
    
    email, email_id, password = get_temp_email()
    if not email:
        print("[×] Failed to get a temp email.")
        return
    
    first_name = random.choice(["John", "Alice", "Michael", "Emma"])
    last_name = random.choice(["Smith", "Johnson", "Brown", "Williams"])
    birthday = f"{random.randint(1980, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    
    print(f"[+] Temporary Email: {email}")
    print("[+] Waiting for verification email...")
    
    # Simulate Facebook registration
    fb_data = register_facebook_account(email, password, first_name, last_name, birthday)
    
    token = "your_mailtm_token_here"  # Replace with real token
    verification_code = get_verification_code(email_id, token)
    
    print("\n-----------GENERATED-----------")
    print(f"EMAIL     : {fb_data['email']}")
    print(f"ID        : {email_id or 'N/A'}")
    print(f"PASSWORD  : {fb_data['password']}")
    print(f"NAME      : {fb_data['name']}")
    print(f"BIRTHDAY  : {fb_data['birthday']}")
    print(f"GENDER    : M")
    print(f"VERIFICATION CODE: {verification_code or 'N/A'}")
    print("-----------GENERATED-----------")
    print(f"datr=     : {fb_data['datr']}")
    print("-----------GENERATED-----------")

if __name__ == "__main__":
    main()
