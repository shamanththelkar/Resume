from playwright.sync_api import sync_playwright
from datetime import datetime
import requests
import os
from utils import write_resume

# Load secrets from GitHub Actions
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Decode resumes stored in GitHub Secrets
write_resume("RESUME1", "resume1.pdf")
write_resume("RESUME2", "resume2.pdf")

# Alternate daily resume
today = datetime.utcnow().day
resume_path = "resume1.pdf" if today % 2 == 0 else "resume2.pdf"


# ----------------------- TELEGRAM FUNCTION -----------------------
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)
# -----------------------------------------------------------------


def upload_resume():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login
        page.goto("https://www.naukri.com/nlogin/login")
        page.fill("input[placeholder='Enter your active Email ID / Username']", NAUKRI_EMAIL)
        page.fill("input[type='password']", NAUKRI_PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_timeout(6000)

        # Go to profile
        page.goto("https://www.naukri.com/mnjuser/profile")
        page.wait_for_timeout(6000)

        # Upload resume
        page.set_input_files("input[type='file']", resume_path)
        page.wait_for_timeout(5000)

        browser.close()


if __name__ == "__main__":
    try:
        upload_resume()
        send_telegram(f"✅ Success: Uploaded {resume_path}")
    except Exception as e:
        send_telegram(f"❌ Failed to upload resume.\nError: {e}")
        raise
