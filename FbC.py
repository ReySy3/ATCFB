import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# === Configuration ===
chrome_driver_path = "/path/to/chromedriver"  # Update this with your actual path
FACEBOOK_SIGNUP_URL = "https://www.facebook.com/r.php"

# === 1secmail API ===
TEMPMAIL_API = "https://www.1secmail.com/api/v1/"

# === Generate Temporary Email ===
def get_temp_email():
    """Generate a temporary email from 1secmail."""
    try:
        response = requests.get(f"{TEMPMAIL_API}?action=genRandomMailbox")
        email = response.json()[0]
        print(f"[+] Temporary email generated: {email}")
        return email
    except Exception as e:
        print(f"[×] Error generating temp email: {e}")
        return None

# === Wait for Verification Email ===
def wait_for_verification_email(email):
    """Poll the email inbox for the Facebook verification code."""
    username, domain = email.split('@')
    inbox_url = f"{TEMPMAIL_API}?action=getMessages&login={username}&domain={domain}"

    print("[+] Waiting for Facebook verification email...")

    for _ in range(30):  # Retry up to 30 times (every 5 seconds)
        time.sleep(5)
        try:
            inbox = requests.get(inbox_url).json()
            if inbox:
                mail_id = inbox[0]["id"]
                print(f"[+] Email received! ID: {mail_id}")
                mail_url = f"{TEMPMAIL_API}?action=readMessage&login={username}&domain={domain}&id={mail_id}"
                mail_content = requests.get(mail_url).json()
                return extract_verification_code(mail_content["body"])
        except:
            pass
        print("[×] Inbox is empty. Retrying...")

    print("[×] No verification email received within time limit.")
    return None

# === Extract Verification Code ===
def extract_verification_code(email_body):
    """Extract verification code from Facebook email."""
    import re
    match = re.search(r"\b\d{5,6}\b", email_body)
    return match.group(0) if match else None

# === Fetch `datr` Cookie using Selenium ===
def get_datr_cookie():
    """Retrieve the `datr` cookie after accessing Facebook."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print("[+] Opening Facebook login page...")
        driver.get("https://www.facebook.com/")
        time.sleep(5)  # Allow time for cookies to load

        cookies = driver.get_cookies()
        datr_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'datr'), None)

        driver.quit()
        return datr_cookie if datr_cookie else "N/A"

    except Exception as e:
        print(f"[×] Error fetching `datr` cookie: {e}")
        driver.quit()
        return "N/A"

# === Facebook Registration Automation ===
def register_facebook_account():
    """Simulate Facebook account registration (Manual completion required)."""
    email = get_temp_email()
    if not email:
        print("[×] Failed to get a temp email.")
        return

    # User needs to manually register using the temp email
    print(f"[!] Go to {FACEBOOK_SIGNUP_URL} and register manually using this email:")
    print(f"    EMAIL: {email}")

    # Wait for verification email
    verification_code = wait_for_verification_email(email)
    
    # Fetch the `datr` cookie
    datr_cookie = get_datr_cookie()

    # Print results
    print("\n----------- GENERATED -----------")
    print(f"EMAIL     : {email}")
    print(f"PASSWORD  : [SET MANUALLY]")
    print(f"VERIFICATION CODE: {verification_code if verification_code else 'N/A'}")
    print(f"datr=     : {datr_cookie}")
    print("--------------------------------\n")

# === Run the script ===
if __name__ == "__main__":
    register_facebook_account()
