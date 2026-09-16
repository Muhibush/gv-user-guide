# User Guides — AGENTS.md

## Overview

This directory contains the **BBB (Body Breath Beyond) App User Guide** — a standalone HTML presentation with 54 slides and iPhone SE screenshots. Designed for conversion to Google Slides.

## Key Files

| File | Purpose |
|------|---------|
| `GV-App-User-Guide-FULL.html` | Complete guide (54 slides, two-column layout) |
| `README.md` | TOC, test accounts, quick reference |
| `take-screenshots.py` | Automated screenshot script (Playwright) |
| `screenshots/` | All PNG screenshots organized by section |
| `checkpoints/` | Individual HTML checkpoint files (8 sections) |

## Environment URLs

| Environment | Frontend | Dashboard | API |
|-------------|----------|-----------|-----|
| **Staging** | `https://staging-gv.muhibdev.biz.id` | `https://staging-dashboard-gv.muhibdev.biz.id` | `https://staging-api-gv.muhibdev.biz.id` |
| **Local** | `http://127.0.0.1:3000` | `http://127.0.0.1:13000` | `http://127.0.0.1:10000` |

- The screenshot script (`take-screenshots.py`) uses **staging URLs** by default
- For local development, update `FRONTEND_URL` and `ADMIN_URL` in the script, or use `--local` flag
- Admin dashboard is desktop-only — use 1280×720 viewport, not iPhone SE

## Screenshot Requirements

| Property | Value |
|----------|-------|
| **Device** | iPhone SE (3rd gen) |
| **Viewport** | 375×667 CSS pixels |
| **DPR** | 2x |
| **Output size** | 750×1334 pixels |
| **Format** | PNG |
| **Scale** | `scale="device"` in Playwright |

### Why iPhone SE (3rd gen)?

Playwright's `devices["iPhone SE"]` is 1st gen (320×568). The 3rd gen matches the 375×667 viewport the app targets:

```python
from playwright.sync_api import sync_playwright
pw = sync_playwright().start()
device = pw.devices["iPhone SE (3rd gen)"]
# viewport: 375x667, device_scale_factor: 2
```

## Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Demo student | `demo@gv.test` | `123qwe!Q` |
| Test student | `budi.pratama@gmail.com` | `Test1234!` |
| Admin | `ayu-admin@gv.test` | `123qwe!Q` |

- `demo@gv.test` has 45 days of exercise data (use for consistency/journal/exercise screenshots)
- `budi.pratama@gmail.com` is used for QRIS payment flow
- Admin is used for payment approval screenshots (desktop viewport, not iPhone SE)

## Taking Screenshots

### Quick start

```bash
cd gv-knowledge/user-guides
python3 take-screenshots.py sample   # 4 sample screenshots
python3 take-screenshots.py all      # all screenshots
python3 take-screenshots.py landing  # single target
python3 take-screenshots.py --local  # use local environment (127.0.0.1)
```

### Available targets

| Target | Description |
|--------|-------------|
| `sample` | Landing + exercise-start + consistency + journal (quick test) |
| `all` | All iPhone SE screenshots |
| `landing` | Landing page (logged out) |
| `exercise-start` | Exercise start page |
| `consistency` | Consistency/BOLT tracking page |

### Adding new screenshots

Edit `take-screenshots.py`:

1. Add a new function following the pattern:
```python
def take_new_page(page):
    """XX: Description."""
    p = page.context.new_page()
    p.goto(f"{FRONTEND_URL}/your-path")
    p.wait_for_timeout(3000)
    save_screenshot(p, "section", "XX-name.png")
    p.close()
```

2. Add to the `screenshots` list or call from `main()`

3. Reference in HTML:
```html
<img src="screenshots/section/XX-name.png" alt="Description">
```

## HTML Guide Structure

### Slide format

```html
<div class="slide">
    <div class="slide-left">
        <h2>Title</h2>
        <div class="instruction"><p><strong>Step N:</strong> Description</p></div>
        <div class="tip"><p>💡 Tip text</p></div>
    </div>
    <div class="slide-right">
        <img src="screenshots/section/XX-name.png" alt="Alt text">
    </div>
    <div class="slide-number">N / 54</div>
</div>
```

### CSS conventions

- Slides: 1280×720px, `display: flex`
- Left panel: `flex: 1`, text content
- Right panel: `width: 375px`, screenshot container
- Images: `border-radius: 24px`, `border: 2px solid #d1d5db`, `box-shadow`
- Brand colors: `--brand: #5AB0A1`, `--brand-dark: #3d8a7d`

### Slide numbering

- Total slides: **54**
- Update `slide-number` div and total count when adding/removing slides
- Current sections:
  - 1-11: Registration
  - 12: Login
  - 13-14: Dashboard
  - 16-18: Courses
  - 20-22: Payment Gateway
  - 23-27: QRIS
  - 28-32: Admin
  - 33-37: Exercise
  - 38: Consistency
  - 39-40: Journal
  - 47-54: Profile

## Screenshot Sections

```
screenshots/
├── registration/    # 01-11 (landing, onboarding, form, OTP)
├── login/           # 12
├── dashboard/       # 13-14
├── courses/         # 16-18
├── payment-gateway/ # 20-22
├── qris/            # 23-27
├── admin/           # 28-32 (desktop viewport)
├── exercise/        # 33-37
├── consistency/     # 38
├── journal/         # 39-40
└── profile/         # 35-42
```

## Common Issues

### Screenshot is 375×667 instead of 750×1334

**Cause:** Missing device scale factor.

**Fix:** Use `scale="device"` in Playwright:
```python
page.screenshot(path="file.png", scale="device")
```

Or use the iPhone SE (3rd gen) device descriptor which has `device_scale_factor: 2`.

### Screenshot shows wrong page (logged-in instead of landing)

**Cause:** Browser context has auth cookies.

**Fix:** Create a fresh context for logged-out pages:
```python
logged_out_ctx = browser.new_context(**IPHONE_SE)
# ... take landing screenshot
logged_out_ctx.close()
```

### Screenshot is blurry

**Cause:** CSS pixel screenshot scaled up, or wrong DPR.

**Fix:** Ensure device emulation is set before navigation:
```python
context = browser.new_context(**IPHONE_SE)  # includes deviceScaleFactor: 2
page = context.new_page()
page.goto(url)
page.screenshot(path="file.png", scale="device")
```

### Admin screenshots need desktop viewport

**Cause:** Admin dashboard is desktop-only.

**Fix:** Use a separate desktop context:
```python
desktop_ctx = browser.new_context(
    viewport={"width": 1280, "height": 720},
    device_scale_factor=1
)
```

### Exercise page shows wrong level (e.g., "Active 5" instead of "Basic 2")

**Cause:** Navigating to wrong exercise slug.

**Fix:** Use the correct exercise slug from the URL pattern:
```
/courses/buteyko/basic-2    # Basic level
/courses/buteyko/active-5   # Active level
```

## URLs Reference

### App pages (iPhone SE)

| Page | URL |
|------|-----|
| Landing | `/auth` |
| Login | `/auth/login` |
| Register | `/auth/register` |
| Dashboard | `/` |
| Courses list | `/` (Courses tab) |
| Course detail | `/courses/buteyko` |
| Exercise start | `/courses/buteyko/basic-2` |
| Exercise settings | `/courses/buteyko/basic-2?settings` |
| Exercise finish | `/courses/buteyko/basic-2?finish` |
| Consistency | `/user/streaks?tab=buteyko` |
| Journal list | `/user/journals?course_slug=buteyko` |
| Journal detail | `/user/journals/{id}` |
| Profile | `/` (Profile tab) |
| Trainers | `/trainers` |

### Admin pages (Desktop)

| Page | URL |
|------|-----|
| Login | `/auth/login` |
| Payment status | `/payments/status` |

## Workflow for Adding New Screenshots

1. **Identify the page** — find the URL and what account to use
2. **Add to script** — add a `take_*` function in `take-screenshots.py`
3. **Test** — run `python3 take-screenshots.py <target>` to capture
4. **Verify** — check dimensions with `sips -g pixelWidth -g pixelHeight file.png`
5. **Add to HTML** — add `<img>` tag in the appropriate slide
6. **Update slide count** — adjust total in `slide-number` elements
7. **Update README** — add new screenshot to the file list if needed

## Dependencies

- Python 3.12+
- `playwright` Python package (`pip install playwright`)
- Playwright browsers (`playwright install chromium`)
- `sips` (macOS) for dimension verification
