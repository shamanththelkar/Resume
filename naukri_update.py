from playwright.sync_api import sync_playwright
import os
from datetime import datetime, UTC

# Read email + password from GitHub Secrets
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")

# These paths must be full file paths in your GitHub repository
RESUME1 = os.getenv("RESUME1")  # Example: /home/runner/work/Resume/Resume/shamanthexp1.pdf
RESUME2 = os.getenv("RESUME2")  # Example: /home/runner/work/Resume/Resume/shamanthexp2.pdf

# 🔁 Alternate resume daily
today = datetime.now(UTC).day
resume_path = RESUME1 if today % 2 == 0 else RESUME2


def upload_resume():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to login page
        page.goto("https://www.naukri.com/nlogin/login")
        page.wait_for_load_state("networkidle")

        # Login
        page.get_by_role("textbox", name="Enter Email ID / Username").fill(NAUKRI_EMAIL)
        page.get_by_role("textbox", name="Enter Password").fill(NAUKRI_PASSWORD)

        with page.expect_navigation():
            page.get_by_role("button", name="Login", exact=True).click()

        # Go to profile
       # Go to login page (Corrected URL)
page.goto("https://www.naukri.com/nlogin/login?URL=https://www.naukri.com/mnjuser/profile")
page.wait_for_load_state("networkidle")


        # Upload resume
        print(f"Uploading resume: {resume_path}")
        page.get_by_role("button", name="Update resume").set_input_files(resume_path)

        # Wait for upload to finish
        page.wait_for_load_state("networkidle")

        print("Resume uploaded successfully!")
        browser.close()


if __name__ == "__main__":
    upload_resume()
