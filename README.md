# GV App User Guide - BBB (Body Breath Beyond)

Complete user guide for the BBB breathing exercise application, designed for iPhone SE (375×667) viewports and optimized for Google Slides conversion.

## Overview

This user guide provides a comprehensive walkthrough of the BBB application, from registration to completing breathing exercises. All screenshots are captured at iPhone SE resolution (375×667) for consistent mobile presentation.

**Target URL:** https://staging-gv.muhibdev.biz.id

**Admin Dashboard:** https://staging-dashboard-gv.muhibdev.biz.id

## Directory Structure

```
gv-knowledge/user-guides/
├── README.md                              # This file
├── GV-App-User-Guide-FULL.html            # Complete guide (46 slides)
├── checkpoints/                           # Standalone HTML checkpoint files
│   ├── checkpoint-01-registration.html    # Registration journey (11 slides)
│   ├── checkpoint-02-login-dashboard.html # Login & dashboard (4 slides)
│   ├── checkpoint-03-courses-checkout.html # Courses & checkout (4 slides)
│   ├── checkpoint-04-payment-gateway.html # Payment gateway flow (4 slides)
│   ├── checkpoint-05-qris-flow.html       # QRIS payment flow (6 slides)
│   ├── checkpoint-06-admin-approval.html  # Admin approval process (6 slides)
│   ├── checkpoint-07-exercise.html        # Exercise flow (3 slides)
│   └── checkpoint-08-profile-settings.html # Profile & settings (8 slides)
└── screenshots/                           # Organized screenshots by section
    ├── registration/                      # 11 screenshots (01-landing to 11-complete)
    ├── login/                             # 1 screenshot (12-login-page)
    ├── dashboard/                         # 3 screenshots (13-dashboard to 15-streak)
    ├── courses/                           # 4 screenshots (16-courses to 19-buteyko)
    ├── payment-gateway/                   # 3 screenshots (20-method to 22-success)
    ├── qris/                              # 5 screenshots (23-selected to 27-pending)
    ├── admin/                             # 5 screenshots (28-login to 32-approved)
    ├── exercise/                          # 2 screenshots (33-preference to 34-player)
    ├── profile/                           # 4 screenshots (35-page to 38-trainer)
    └── misc/                              # 3 screenshots (39-info, 40-faq, 41-password, 42-sessions)
```

## Table of Contents

### Checkpoint 01: Registration Journey
1. Welcome & Landing Page
2. Onboarding - Essential
3. Onboarding - Poor Breathing
4. Onboarding - 5 Minutes
5. Onboarding - Neuroscience
6. Health Goal Selection
7. Registration Form
8. Review & Confirm Details
9. Phone Verification (OTP)
10. Email Verification
11. Registration Complete

### Checkpoint 02: Login & Dashboard
1. Login Page
2. Dashboard Overview
3. Health Form

### Checkpoint 03: Courses & Checkout
1. Courses Listing
2. Course Details
3. Checkout Page

### Checkpoint 04: Payment Gateway Flow
1. Select Payment Gateway
2. Mock Payment Page
3. Payment Success

### Checkpoint 05: QRIS Payment Flow
1. Select QRIS Payment
2. QR Code Display
3. Download QR Code
4. Pending Payment Status
5. Purchase History

### Checkpoint 06: Admin Approval Process
1. Admin Dashboard Login
2. Payment Status Page
3. Search for User
4. Payment Detail Dialog
5. Payment Approved

### Checkpoint 07: Exercise Flow
1. Exercise Preference
2. Exercise Player

### Checkpoint 08: Profile & Settings
1. Profile Page
2. Profile Detail
3. Trainers List
4. Trainer Profile
5. FAQ
6. Change Password
7. Device Sessions

## Test Account

**User Account:**
- Email: `agungsantoso@gmail.com`
- Password: `123qwe!Q`
- Name: Agung Santoso
- Phone: 081234567890
- DOB: 15/01/1990
- City: Kota Administrasi Jakarta Pusat

**Admin Account:**
- Email: `ayu-admin@gv.test`
- Password: `123qwe!Q`

## Payment Methods

### Payment Gateway
- Auto-completes in staging via mock payment page
- Click "Simulate Payment Success" to complete
- Redirects to success page

### QRIS
- Shows QR code with bank details (BCA)
- User clicks "Download QR" (opens new tab with qris.png)
- User clicks "I have paid"
- Status becomes PENDING
- Admin approves via dashboard `/payments/status`

## Converting to Google Slides

Each HTML checkpoint is designed for easy conversion to Google Slides:

1. Open the HTML file in Chrome
2. Use a screenshot tool to capture each slide (1280×720px)
3. Import screenshots into Google Slides
4. Add transitions and animations as needed

**Alternative:** Use a PDF converter to convert HTML to PDF, then import PDF pages into Google Slides.

## Styling

- **Primary Teal:** #5AB0A1
- **Primary Blue:** #0F5590
- **Slide Dimensions:** 1280×720px (16:9)
- **iPhone Frame:** 375×667px (iPhone SE)
- **Font:** Segoe UI, Tahoma, Geneva, Verdana, sans-serif

## Screenshot Standards

All screenshots must follow consistent capture standards for quality and presentation.

**See:** [SCREENSHOT-STANDARDS.md](./SCREENSHOT-STANDARDS.md) for the complete guide.

**Quick Reference:**
- **Mobile (BBB app):** Chrome DevTools emulation `375x667x2,mobile,touch` → 750×1334px output
- **Desktop (Admin):** Chrome DevTools emulation `1280x720x1` → 1280×720px output
- **Never use:** Playwright CLI `--device="iPhone SE"` (targets 1st gen SE, wrong dimensions)

---

## Notes

- All screenshots use iPhone SE viewport (375×667) with 2x Retina scaling
- Each HTML checkpoint is standalone and can be opened independently
- The full guide combines all checkpoints into one file
- Skip empty/blocked screens as needed
- Payment Gateway and QRIS flows are shown separately
- Admin approval process is included for completeness