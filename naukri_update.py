from playwright.sync_api import sync_playwright
from datetime import datetime, UTC
import os

# Secrets
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")

RESUME1 = os.getenv("RESUME1")
RESUME2 = os.getenv("RESUME2")

today = datetime.now(UTC).day
resume_path = RESUME1 if today % 2 == 0 else RESUME2


def upload_resume():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # ✅ Login URL with redirect
        page.goto(
            "https://www.naukri.com/nlogin/login?URL=https://www.naukri.com/mnjuser/profile",
            timeout=60000
        )

        # ✅ Wait for email field (CSS selector, not role)
        page.wait_for_selector("input[type='text']", timeout=60000)

        # Fill credentials
        page.fill("input[type='text']", NAUKRI_EMAIL)
        page.fill("input[type='password']", NAUKRI_PASSWORD)

        # Click login
        page.click("button[type='submit']")

        # ✅ Wait until profile page loads
        page.wait_for_url("**/mnjuser/profile", timeout=60000)
        page.wait_for_load_state("networkidle")

        # Upload resume
        print(f"Uploading resume: {resume_path}")
        page.set_input_files("input[type='file']", resume_path)

        page.wait_for_load_state("networkidle")
        print("Resume uploaded successfully")

        browser.close()


if __name__ == "__main__":
    upload_resume()
