# GV App User Guide — Screenshot Standards

Consistent screenshot capture for the BBB (Body Breath Beyond) app user guide.

---

## Device Profiles

### iPhone SE (Mobile Screenshots)

| Property | Value |
|----------|-------|
| **Viewport** | 375×667 CSS pixels |
| **Device Scale Factor** | 2 |
| **Output Size** | 750×1334 pixels |
| **Use Case** | All BBB app screens (registration, login, dashboard, courses, exercises, profile) |

### Desktop (Admin Dashboard Screenshots)

| Property | Value |
|----------|-------|
| **Viewport** | 1280×720 CSS pixels |
| **Device Scale Factor** | 1 |
| **Output Size** | 1280×720 pixels |
| **Use Case** | Admin dashboard screens (login, payment approval, user management) |

---

## Capture Method

**Always use Chrome DevTools emulation** — not Playwright CLI `--device` flag.

### Why Chrome DevTools?

- Playwright CLI `--device="iPhone SE"` targets the **1st gen iPhone SE** (320×568 viewport → 640×1136px output)
- Chrome DevTools emulation targets the **2nd/3rd gen iPhone SE** (375×667 viewport → 750×1334px output)
- Chrome DevTools produces higher quality, properly scaled screenshots

### Step-by-Step Process

#### 1. Emulate iPhone SE

```
chrome-devtools_emulate with viewport: "375x667x2,mobile,touch"
```

This configures:
- Width: 375px
- Height: 667px
- Device Scale Factor: 2 (Retina)
- Mobile: true
- Touch: true

#### 2. Navigate to Page

```
chrome-devtools_navigate_page with type: "url" and url: "<target URL>"
```

#### 3. Wait for Content

```
chrome-devtools_wait_for with text: ["<key element text>"] and timeout: 5000
```

Always wait for the primary CTA or content element to appear before capturing.

#### 4. Take Screenshot

```
chrome-devtools_take_screenshot with filePath: "<absolute path>"
```

Save to the appropriate `screenshots/<section>/` directory.

#### 5. Verify Dimensions

```bash
sips -g pixelWidth -g pixelHeight <screenshot file>
```

Expected output for iPhone SE:
```
pixelWidth: 750
pixelHeight: 1334
```

Expected output for Desktop:
```
pixelWidth: 1280
pixelHeight: 720
```

---

## File Naming Convention

```
screenshots/<section>/<NN>-<descriptive-name>.png
```

| Section | Directory | Example |
|---------|-----------|---------|
| Registration | `registration/` | `01-landing.png` |
| Login | `login/` | `12-login-page.png` |
| Dashboard | `dashboard/` | `13-dashboard.png` |
| Courses | `courses/` | `16-courses.png` |
| Payment Gateway | `payment-gateway/` | `20-method.png` |
| QRIS | `qris/` | `23-selected.png` |
| Admin | `admin/` | `28-login.png` |
| Exercise | `exercise/` | `33-preference.png` |
| Consistency | `consistency/` | `38-consistency.png` |
| Journal | `journal/` | `39-journal.png` |
| Profile | `profile/` | `47-profile.png` |

---

## Quality Checklist

Before saving a screenshot, verify:

- [ ] Correct device emulation active (375×667×2 for mobile, 1280×720 for desktop)
- [ ] Page fully loaded (wait for key element)
- [ ] No loading spinners or skeleton states visible
- [ ] Content properly scrolled to show relevant section
- [ ] No browser chrome (address bar, tabs) visible
- [ ] Text is readable and not cut off
- [ ] Primary CTA buttons visible in viewport
- [ ] Output dimensions match expected (750×1334 or 1280×720)

---

## Common Pitfalls

### 1. Wrong Device Emulation

**Problem:** Using Playwright CLI `--device="iPhone SE"` produces 640×1136px (1st gen SE)

**Solution:** Always use Chrome DevTools emulation with `375x667x2,mobile,touch`

### 2. Screenshot Before Page Load

**Problem:** Capturing before content renders (shows blank or loading state)

**Solution:** Always use `chrome-devtools_wait_for` with the primary CTA text

### 3. Content Cut Off

**Problem:** Bottom of page not visible (e.g., "Have an account? Login Here" link)

**Solution:** Ensure viewport is tall enough, or scroll to show full content

### 4. Inconsistent Naming

**Problem:** Files named inconsistently across sections

**Solution:** Follow `<NN>-<descriptive-name>.png` pattern with sequential numbering

---

## Reference

- Device profiles: [Playwright devices](https://playwright.dev/docs/api/class-browsertype#browser-type-new-page)
- Chrome DevTools emulation: [Viewport emulation](https://developer.chrome.com/docs/devtools/rendering/emulate-device)
- iPhone SE 2nd/3rd gen: 375×667 viewport, 2x Retina = 750×1334px output
