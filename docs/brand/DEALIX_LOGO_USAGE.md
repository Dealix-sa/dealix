# DEALIX Logo Usage

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This document is the operational layer on top of `DEALIX_VISUAL_IDENTITY.md`.
It tells designers and engineers what they can and cannot do with the mark
in the wild. When in doubt, the rules here win.

---

## 1. Quick reference

| Question | Answer |
| --- | --- |
| Can I recolor the swoosh? | Only when the whole mark is monochrome. |
| Can I stretch the mark? | No. |
| Can I rotate it? | No. |
| Can I add a drop shadow? | No. |
| Can I crop the swoosh tail? | Only at clear-space boundary. |
| Can I use it as a watermark? | Yes, in monochrome at <=10% opacity. |
| Can I use the monogram alone? | Yes, in the sanctioned use cases. |
| Can I make a new lockup? | Only with brand director approval. |

---

## 2. Do — the sanctioned uses

### 2.1 Primary horizontal lockup
Use this in the marketing site header, sales deck cover, proposal cover,
contract first page, and email signature header. It is the most legible
form of the mark and should be the default whenever the surface has room.

### 2.2 Stacked lockup
Use this in narrow vertical placements: mobile splash screens, side
panels, vertical banners. Keep the wordmark and the tagline together;
do not split them across two columns.

### 2.3 Monogram-only
Use this in:
- Favicons (`favicon.ico`, `apple-touch-icon.png`)
- App icons (PWA, mobile app)
- Tight nav corners under 24 px height
- Loading spinners (monogram with an optional teal swoosh pulse)
- Social profile avatars (LinkedIn, X, GitHub)

### 2.4 Wordmark-only
Use inside the product UI once the user is authenticated and the surface
is already obviously Dealix. The monogram becomes redundant there; the
wordmark in the top-left chrome is enough.

### 2.5 Mono partner lockup
Use in co-branded surfaces: partner case studies (where the partner has
approved publication), joint webinars, joint reports. Dealix mark is
always on the left in LTR / right in RTL; the partner mark sits opposite
with a thin vertical rule between them.

---

## 3. Don't — the prohibited uses

### 3.1 Visual prohibitions
- Do **not** stretch, squash, or otherwise distort the mark.
- Do **not** rotate, tilt, or reflect the mark.
- Do **not** apply drop shadows, glows, bevels, or gradients to the mark.
- Do **not** outline the wordmark.
- Do **not** swap the typeface of the wordmark.
- Do **not** recolor the swoosh to any color other than Emerald Teal,
  except in full monochrome.
- Do **not** isolate the swoosh and use it as a standalone graphic device.
- Do **not** crop the monogram such that the growth arrow is hidden.
- Do **not** place the mark on a busy photograph without a navy 80%+
  overlay.
- Do **not** place the mark on Soft Silver or Emerald Teal backgrounds.
- Do **not** animate the mark beyond the single sanctioned swoosh sweep.

### 3.2 Linguistic prohibitions
- Do **not** transliterate "DEALIX" into Arabic script as part of the
  mark itself. The wordmark stays Latin. (Arabic body copy may refer to
  the company as "دِيليكس" in running text, but never inside the lockup.)
- Do **not** pair the mark with a tagline other than
  "INTELLIGENT DEALS. REAL GROWTH." without brand director approval.
- Do **not** use the mark with promotional copy that claims guaranteed
  revenue, sales, or meetings.

### 3.3 Commercial prohibitions
- Do **not** use the mark on merchandise that is not produced by Dealix.
- Do **not** allow partners to embed the mark in their own marketing
  without a written usage grant.
- Do **not** allow the mark to appear in a customer case study that has
  not been formally approved and logged in the proof ledger.

---

## 4. Monochrome rules

Monochrome is the fallback when color printing is not possible or when the
surface demands restraint.

| Variant | Foreground | Background |
| --- | --- | --- |
| Mono white | White (`#FFFFFF`) | Deep Navy / Slate |
| Mono navy | Deep Navy (`#0B1220`) | White / Soft Silver* |
| Mono black | Black (`#000000`) | White |
| Mono ink | Single ink color | Any |

\* Mono navy on Soft Silver is allowed because the mark is in navy, not
white — contrast is preserved.

In monochrome, the swoosh inherits the foreground color. Do **not** keep
the swoosh in teal while the rest of the mark is monochrome.

---

## 5. Social profile assets

### 5.1 LinkedIn
- Company avatar: monogram, white on Deep Navy, 400×400 px.
- Banner: wordmark + tagline on Deep Navy, 1584×396 px, with subtle
  teal swoosh in the lower-right third. No additional graphics, no
  customer logos in the banner.
- Founder avatar: a headshot, not the Dealix logo. Founder pages do not
  use the company mark as an avatar.

### 5.2 X (Twitter)
- Avatar: monogram, white on Deep Navy, 400×400 px.
- Banner: wordmark + tagline on Deep Navy, 1500×500 px.

### 5.3 OG and social cards
- Default OG card: monogram top-left, white wordmark center, tagline
  underneath, navy background. 1200×630 px.
- Article OG cards: monogram top-left, article title center-left in
  Inter Semibold, navy background. 1200×630 px.

---

## 6. Favicon set

The favicon set is generated from `assets/brand/source/dealix-favicon.svg`.

| File | Size | Notes |
| --- | --- | --- |
| `favicon.ico` | 16/32/48 | Multi-resolution ICO |
| `favicon-16x16.png` | 16×16 | PNG fallback |
| `favicon-32x32.png` | 32×32 | PNG fallback |
| `apple-touch-icon.png` | 180×180 | iOS home screen |
| `android-chrome-192x192.png` | 192×192 | Android PWA |
| `android-chrome-512x512.png` | 512×512 | Android PWA |
| `safari-pinned-tab.svg` | vector | Safari pinned tab (monochrome) |

The monogram is centered on a solid Deep Navy field with 12.5% padding on
all sides. Do not generate favicons from screenshots or rasterized exports
— always start from the canonical SVG.

---

## 7. Print and physical surfaces

| Surface | Variant | Notes |
| --- | --- | --- |
| Business card (front) | Primary horizontal, white-on-navy | Tagline optional |
| Business card (back) | Monogram, navy-on-white | Contact details right |
| Letterhead | Primary horizontal, top-left (LTR) / top-right (RTL) | 32 px tall |
| Envelope | Monogram + wordmark, navy-on-white | Top-left |
| Event backdrop | Primary horizontal, large scale | Tagline mandatory |
| Roll-up banner | Stacked lockup | Tagline mandatory |
| Embroidery | Mono navy or mono white | Single-color thread only |

---

## 8. Email signature

The mark appears in the email signature as the **wordmark-only** variant
at 28–36 px height, navy-on-white, with the tagline directly underneath
in Inter Medium at 60% size. Full signature variants live in
`DEALIX_EMAIL_SIGNATURE_GUIDE.md`.

---

## 9. Partner co-branding

When Dealix appears alongside a partner mark:

1. Both marks share the same optical height (measured by cap height).
2. Dealix is on the leading edge: left in LTR, right in RTL.
3. A thin Soft Silver rule separates the two marks.
4. The partner mark must be used per the partner's own guidelines.
5. Co-branding requires a written usage grant from both sides, logged in
   the proof ledger.

---

## 10. Misuse — examples of off-brand patterns to call out

| Misuse | Correction |
| --- | --- |
| Logo over a vibrant photo | Add navy 80%+ overlay |
| Logo squashed to fit a button | Use monogram instead |
| Logo with "Guaranteed revenue" copy | Remove the claim |
| Logo in green-on-green | Use sanctioned mono variant |
| Logo with custom outline glow | Strip the glow |
| Logo tilted 7° for "energy" | Set to 0° |
| Logo with partner mark larger than Dealix | Match cap height |

---

## 11. Bilingual note — العربية

عند استخدام الشعار في تخطيطات RTL، يبقى الشعار بصيغته اللاتينية الأصلية،
ولكنه يُحاذى إلى يمين الشاشة. لا تُكتب كلمة "دِيليكس" داخل القفل البصري —
الكلمة العربية تستخدم فقط في النص الجاري. الموقع الافتراضي للشعار في الواجهات
العربية هو الزاوية العلوية اليمنى، مع احترام مساحة الفسحة الدنيا المحددة في
وثيقة الهوية البصرية.

---

## 12. Approval path

If a use case is not covered here:

1. Draft the proposed use.
2. Tag the brand director on the design review.
3. Get a written ok (Slack message or email is fine, recorded in the
   proof ledger).
4. Ship.

Unsanctioned use without approval is treated as a brand defect and rolled
back.
