#!/usr/bin/env python3
"""
Take iPhone SE screenshots for the BBB app user guide.
Uses Playwright with iPhone SE device emulation (375x667 @ 2x = 750x1334px).

Environment URLs:
  Staging: https://staging-gv.muhibdev.biz.id (frontend)
           https://staging-dashboard-gv.muhibdev.biz.id (admin)
  Local:   http://127.0.0.1:3000 (frontend)
           http://127.0.0.1:13000 (admin)

Usage:
  python3 take-screenshots.py sample   # 4 sample screenshots
  python3 take-screenshots.py all      # all screenshots
  python3 take-screenshots.py landing  # single target
  python3 take-screenshots.py --local  # use local environment
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# URLs - use environment variables or defaults
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://staging-gv.muhibdev.biz.id")
ADMIN_URL = os.environ.get("ADMIN_URL", "https://staging-dashboard-gv.muhibdev.biz.id")
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"

# Device settings
IPHONE_SE = {
    "viewport": {"width": 375, "height": 667},
    "device_scale_factor": 2,
    "is_mobile": True,
    "has_touch": True,
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
}

# Test accounts
STUDENT_EMAIL = "demo@gv.test"
STUDENT_PASSWORD = "123qwe!Q"
ADMIN_EMAIL = "ayu-admin@gv.test"
ADMIN_PASSWORD = "123qwe!Q"
SECOND_STUDENT_EMAIL = "budi.pratama@gmail.com"
SECOND_STUDENT_PASSWORD = "Test1234!"

def save_screenshot(page, section, filename, timeout=10000):
    """Save a screenshot to the specified section folder."""
    filepath = SCREENSHOTS_DIR / section
    filepath.mkdir(parents=True, exist_ok=True)
    full_path = filepath / filename
    page.screenshot(path=str(full_path), scale="device", timeout=timeout)
    print(f"  ✓ Saved: {section}/{filename}")

def login(page, email, password):
    """Login with email and password."""
    page.goto(f"{FRONTEND_URL}/auth/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[type="email"], input[name="email"], input[placeholder*="email" i]', email)
    page.fill('input[type="password"], input[name="password"]', password)
    page.click('button[type="submit"], button:has-text("Login"), button:has-text("Masuk")')
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

def admin_login(page, email, password):
    """Login to admin dashboard."""
    page.goto(f"{ADMIN_URL}/auth/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[type="email"], input[name="email"]', email)
    page.fill('input[type="password"], input[name="password"]', password)
    page.click('button[type="submit"], button:has-text("Login"), button:has-text("Masuk")')
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

def take_landing(browser):
    """01: Landing page (logged out, no cookies)."""
    print("Taking: landing")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    page.goto(FRONTEND_URL)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    save_screenshot(page, "registration", "01-landing.png")
    context.close()

def take_exercise_start(browser):
    """02: Exercise start page."""
    print("Taking: exercise-start")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, STUDENT_EMAIL, STUDENT_PASSWORD)
    page.goto(f"{FRONTEND_URL}/courses/buteyko/basic-2")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    save_screenshot(page, "exercise", "33-start.png")
    context.close()

def take_consistency(browser):
    """03: Consistency/BOLT tracking page."""
    print("Taking: consistency")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, STUDENT_EMAIL, STUDENT_PASSWORD)
    page.goto(f"{FRONTEND_URL}/user/streaks?tab=buteyko")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    save_screenshot(page, "consistency", "38-consistency.png")
    context.close()

def take_journal_list(browser):
    """04: Journal list page."""
    print("Taking: journal-list")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, STUDENT_EMAIL, STUDENT_PASSWORD)
    page.goto(f"{FRONTEND_URL}/user/journals?course_slug=buteyko")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    save_screenshot(page, "journal", "39-journal-list.png")
    context.close()

def take_onboarding_steps(browser):
    """05-06: Onboarding steps 3-4."""
    print("Taking: onboarding-steps")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    # Step 1: Go to register
    page.goto(f"{FRONTEND_URL}/auth/register")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Fill and submit step 1
    page.fill('input[name="email"], input[type="email"]', f"test{int(time.time())}@gv.test")
    page.fill('input[name="password"], input[type="password"]', "Test1234!")
    page.fill('input[name="confirm_password"], input[name="password_confirmation"]', "Test1234!")
    page.click('button[type="submit"]')
    page.wait_for_timeout(2000)
    
    # Step 3 (after OTP is skipped)
    save_screenshot(page, "registration", "05-onboarding-step3.png")
    
    # Click next to step 4
    page.click('button:has-text("Selanjutnya"), button:has-text("Next")')
    page.wait_for_timeout(1000)
    save_screenshot(page, "registration", "06-onboarding-step4.png")
    
    context.close()

def take_health_goals(browser):
    """07: Health goals page."""
    print("Taking: health-goals")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    page.goto(f"{FRONTEND_URL}/auth/register")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Fill registration and proceed to health goals
    page.fill('input[name="email"], input[type="email"]', f"test{int(time.time())}@gv.test")
    page.fill('input[name="password"], input[type="password"]', "Test1234!")
    page.fill('input[name="confirm_password"], input[name="password_confirmation"]', "Test1234!")
    page.click('button[type="submit"]')
    page.wait_for_timeout(2000)
    
    # Skip through onboarding to reach health goals
    for _ in range(3):
        page.click('button:has-text("Selanjutnya"), button:has-text("Next")')
        page.wait_for_timeout(1000)
    
    save_screenshot(page, "registration", "07-health-goals.png")
    context.close()

def take_registration_form(browser):
    """08: Registration form (logged out)."""
    print("Taking: registration-form")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    page.goto(f"{FRONTEND_URL}/auth/register")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    save_screenshot(page, "registration", "08-registration-form.png")
    context.close()

def take_otp_page(browser):
    """09: OTP verification page."""
    print("Taking: otp-page")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    page.goto(f"{FRONTEND_URL}/auth/verify-otp")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    save_screenshot(page, "registration", "09-otp.png")
    context.close()

def take_payment_gateway(browser):
    """20-22: Payment gateway screenshots."""
    print("Taking: payment-gateway")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, SECOND_STUDENT_EMAIL, SECOND_STUDENT_PASSWORD)
    
    # Go to course and start payment
    page.goto(f"{FRONTEND_URL}/courses/buteyko")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Click pay button
    pay_button = page.locator('button:has-text("Bayar"), button:has-text("Pay")')
    if pay_button.count() > 0:
        pay_button.first.click()
        page.wait_for_timeout(2000)
        save_screenshot(page, "payment-gateway", "20-payment-select.png")
        
        # Select payment method
        page.click('button:has-text("Simulate Payment")')
        page.wait_for_timeout(2000)
        save_screenshot(page, "payment-gateway", "21-payment-detail.png")
        
        # Confirm payment
        page.click('button:has-text("Bayar"), button:has-text("Pay")')
        page.wait_for_timeout(3000)
        save_screenshot(page, "payment-gateway", "22-payment-success.png")
    
    context.close()

def take_qris_flow(browser):
    """23-25: QRIS payment flow."""
    print("Taking: qris-flow")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, SECOND_STUDENT_EMAIL, SECOND_STUDENT_PASSWORD)
    
    # Go to course and start QRIS payment
    page.goto(f"{FRONTEND_URL}/courses/buteyko")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Click pay button
    pay_button = page.locator('button:has-text("Bayar"), button:has-text("Pay")')
    if pay_button.count() > 0:
        pay_button.first.click()
        page.wait_for_timeout(2000)
        
        # Select QRIS
        qris_option = page.locator('button:has-text("QRIS"), div:has-text("QRIS")')
        if qris_option.count() > 0:
            qris_option.first.click()
            page.wait_for_timeout(2000)
            save_screenshot(page, "qris", "23-qris-select.png")
            
            # Confirm payment
            page.click('button:has-text("Bayar"), button:has-text("Pay")')
            page.wait_for_timeout(3000)
            save_screenshot(page, "qris", "24-qris-payment.png")
    
    context.close()

def take_admin_payment(browser):
    """28-29: Admin payment approval."""
    print("Taking: admin-payment")
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        device_scale_factor=1
    )
    page = context.new_page()
    admin_login(page, ADMIN_EMAIL, ADMIN_PASSWORD)
    
    # Go to payment status
    page.goto(f"{ADMIN_URL}/payments/status")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    save_screenshot(page, "admin", "28-admin-payments.png")
    
    # Click on a pending payment if available
    pending = page.locator('tr:has-text("pending"), div:has-text("pending")')
    if pending.count() > 0:
        pending.first.click()
        page.wait_for_timeout(2000)
        save_screenshot(page, "admin", "29-admin-payment-detail.png")
    
    context.close()

def take_exercise_flow(browser):
    """33-37: Exercise flow screenshots."""
    print("Taking: exercise-flow")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, STUDENT_EMAIL, STUDENT_PASSWORD)
    
    # Exercise start
    page.goto(f"{FRONTEND_URL}/courses/buteyko/basic-2")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    save_screenshot(page, "exercise", "33-start.png")
    
    # Click start exercise
    start_button = page.locator('button:has-text("Mulai"), button:has-text("Start")')
    if start_button.count() > 0:
        start_button.first.click()
        page.wait_for_timeout(3000)
        save_screenshot(page, "exercise", "34-breathing.png")
    
    context.close()

def take_journal_detail(browser):
    """40: Journal detail page."""
    print("Taking: journal-detail")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, STUDENT_EMAIL, STUDENT_PASSWORD)
    
    # Go to journal list and click first entry
    page.goto(f"{FRONTEND_URL}/user/journals?course_slug=buteyko")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    journal_entry = page.locator('div[class*="journal"], a[href*="journals"]')
    if journal_entry.count() > 0:
        journal_entry.first.click()
        page.wait_for_timeout(2000)
        save_screenshot(page, "journal", "40-journal-detail.png")
    
    context.close()

def take_profile_pages(browser):
    """47-54: Profile pages."""
    print("Taking: profile-pages")
    context = browser.new_context(**IPHONE_SE)
    page = context.new_page()
    login(page, STUDENT_EMAIL, STUDENT_PASSWORD)
    
    # Go to profile tab
    page.goto(f"{FRONTEND_URL}/")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Click profile tab
    profile_tab = page.locator('button:has-text("Profile"), a:has-text("Profile"), [data-value="profile"]')
    if profile_tab.count() > 0:
        profile_tab.first.click()
        page.wait_for_timeout(2000)
        save_screenshot(page, "profile", "47-profile.png")
    
    context.close()

# Main execution
def main():
    global IPHONE_SE, FRONTEND_URL, ADMIN_URL
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target = args[0] if args else "sample"
    
    # Handle --local flag
    if "--local" in sys.argv:
        FRONTEND_URL = "http://127.0.0.1:3000"
        ADMIN_URL = "http://127.0.0.1:13000"
        print(f"Using LOCAL environment: {FRONTEND_URL}")
    
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Admin URL: {ADMIN_URL}")
    
    # Create screenshots directory
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        if target == "sample":
            print("=== Taking sample screenshots ===")
            take_landing(browser)
            take_exercise_start(browser)
            take_consistency(browser)
            take_journal_list(browser)
            
        elif target == "all":
            print("=== Taking ALL screenshots ===")
            take_landing(browser)
            take_registration_form(browser)
            take_otp_page(browser)
            take_onboarding_steps(browser)
            take_health_goals(browser)
            take_exercise_start(browser)
            take_exercise_flow(browser)
            take_consistency(browser)
            take_journal_list(browser)
            take_journal_detail(browser)
            take_payment_gateway(browser)
            take_qris_flow(browser)
            take_admin_payment(browser)
            take_profile_pages(browser)
            
        elif target == "landing":
            take_landing(browser)
        elif target == "exercise-start":
            take_exercise_start(browser)
        elif target == "consistency":
            take_consistency(browser)
        elif target == "journal-list":
            take_journal_list(browser)
        else:
            print(f"Unknown target: {target}")
            print("Available targets: sample, all, landing, exercise-start, consistency, journal-list")
        
        browser.close()
    
    print("\n=== Done! ===")

if __name__ == "__main__":
    main()
