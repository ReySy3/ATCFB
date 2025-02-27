import requests
import time
import random

# Temp mail APIs
MAILTM_API = "https://api.mail.tm"
SECMAIL_API = "https://www.1secmail.com/api/v1/"

def check_api_status(url):
    """Check if an API is reachable."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True
        print(f"[×] API {url} is down. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[×] API {url} unreachable: {e}")
    return False

def get_mail_tm_email():
    """Create a temp email using mail.tm API."""
    try:
        response = requests.post(f"{MAILTM_API}/accounts", json={})
        if response.status_code == 201:
            data = response.json()
            return data["id"], data["address"], data["token"]
        print(f"[×] mail.tm error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[×] mail.tm request failed: {e}")
    return None, None, None

def get_1secmail_email():
    """Generate a temp email from 1secmail API."""
    try:
        domains = ["1secmail.com", "1secmail.org", "1secmail.net"]
        username = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=10))
        email = f"{username}@{random.choice(domains)}"
        return email
    except Exception as e:
        print(f"[×] 1secmail generation error: {e}")
    return None

def wait_for_verification_email(email_id, token):
    """Wait for the verification email with exponential backoff."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    retries = 0
    while retries < 10:
        try:
            if token:  # mail.tm API
                response = requests.get(f"{MAILTM_API}/messages", headers=headers, timeout=10)
            else:  # 1secmail API
                domain = email_id.split("@")[1]
                username = email_id.split("@")[0]
                response = requests.get(f"{SECMAIL_API}?action=getMessages&login={username}&domain={domain}")

            if response.status_code == 200:
                messages = response.json()
                if messages:
                    return messages[0]  # Return the first email
            print("[×] Inbox is empty. Retrying...")
        except requests.exceptions.RequestException as e:
            print(f"[×] Error fetching email: {e}")

        time.sleep(2 ** retries)  # Exponential backoff
        retries += 1

    print("[×] No verification email received within time limit.")
    return None

def main():
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("> › Temp Mail Account Generator")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    email_id, email, token = None, None, None

    # Try mail.tm first, then fallback to 1secmail
    if check_api_status(MAILTM_API):
        email_id, email, token = get_mail_tm_email()
    elif check_api_status(SECMAIL_API):
        email = get_1secmail_email()

    if email:
        print(f"[+] Temp Email Created: {email}")
        email_data = wait_for_verification_email(email_id, token)
        if email_data:
            print(f"[+] Verification Email Received: {email_data}")
        else:
            print("[×] Failed to retrieve verification email.")
    else:
        print("[×] No temp email available. Try again later.")

if __name__ == "__main__":
    main()
