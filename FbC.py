import requests
import time

MAILTM_API = "https://api.mail.tm"

# Step 1: Generate a Random Email
def get_temp_email():
    session = requests.Session()
    
    # Generate a random email
    email_data = session.post(f"{MAILTM_API}/accounts", json={"address": "", "password": "randompass"}).json()
    if "id" not in email_data:
        print("[×] Error generating temp email.")
        return None, None, None
    
    email, password, email_id = email_data["address"], "randompass", email_data["id"]
    print(f"[+] Temp Email Created: {email}")
    
    # Step 2: Get Authentication Token
    token_data = session.post(f"{MAILTM_API}/token", json={"address": email, "password": password}).json()
    if "token" not in token_data:
        print("[×] Failed to authenticate with mail.tm")
        return None, None, None
    
    token = token_data["token"]
    print("[+] Authentication successful.")
    
    return email, token, email_id

# Step 3: Wait for Verification Email
def wait_for_verification_email(email_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    
    for _ in range(15):  # Retry for 30 seconds (2s per check)
        inbox = requests.get(f"{MAILTM_API}/messages", headers=headers).json()
        
        if inbox.get("hydra:member"):
            for msg in inbox["hydra:member"]:
                email_subject = msg.get("subject", "No Subject")
                email_id = msg["id"]
                
                # Fetch Email Content
                email_content = requests.get(f"{MAILTM_API}/messages/{email_id}", headers=headers).json()
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
