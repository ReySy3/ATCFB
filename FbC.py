import requests
import time
import random
import string

MAILTM_API = "https://api.mail.tm"

# Step 1: Get Available Domains
def get_domain():
    response = requests.get(f"{MAILTM_API}/domains").json()
    if "hydra:member" in response and response["hydra:member"]:
        return response["hydra:member"][0]["domain"]  # Use the first available domain
    return None

# Step 2: Generate Random Email
def get_temp_email():
    session = requests.Session()
    domain = get_domain()
    
    if not domain:
        print("[×] No available domain found.")
        return None, None, None
    
    random_email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + f"@{domain}"
    password = "randompass"
    
    email_data = session.post(f"{MAILTM_API}/accounts", json={"address": random_email, "password": password}).json()
    if "id" not in email_data:
        print("[×] Error generating temp email.")
        return None, None, None
    
    email, email_id = email_data["address"], email_data["id"]
    print(f"[+] Temp Email Created: {email}")
    
    # Step 3: Get Authentication Token
    token_data = session.post(f"{MAILTM_API}/token", json={"address": email, "password": password}).json()
    if "token" not in token_data:
        print("[×] Failed to authenticate with mail.tm")
        return None, None, None
    
    token = token_data["token"]
    print("[+] Authentication successful.")
    
    return email, token, email_id

# Step 4: Wait for Verification Email
def wait_for_verification_email(email_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    
    for _ in range(15):  # Retry for 30 seconds (2s per check)
        inbox = requests.get(f"{MAILTM_API}/messages", headers=headers).json()
        
        if inbox.get("hydra:member"):
            for msg in inbox["hydra:member"]:
                email_subject = msg.get("subject", "No Subject")
                message_id = msg["id"]
                
                # Fetch Email Content
                email_content = requests.get(f"{MAILTM_API}/messages/{message_id}", headers=headers).json()
                verification_code = email_content.get("text", "N/A")
                
                print(f"[+] Verification Email Found: {email_subject}")
                return verification_code
        
        print("[×] Inbox is empty. Retrying...")
        time.sleep(2)
    
    return None

# Run the script
email, token, email_id = get_temp_email()
if email:
    verification_code = wait_for_verification_email(email_id, token)
    print(f"[+] VERIFICATION CODE: {verification_code if verification_code else 'N/A'}")
