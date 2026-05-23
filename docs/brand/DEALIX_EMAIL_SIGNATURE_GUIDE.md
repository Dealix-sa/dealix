# DEALIX Email Signature Guide

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This document defines the Dealix email signature — the variants for
different roles, the visual and copy rules, and the technical guidance
that keeps signatures rendering correctly across email clients. The
signature is the smallest, most-repeated brand surface we own. It must
read on-brand on every send.

---

## 1. Signature stance

The signature does not sell. It identifies the sender, reinforces the
brand mark, and provides one link. It is sober, short, and easy to
parse on a phone screen.

Three rules:

1. **One image: the wordmark.** Signatures do not carry photos,
   icons, or marketing banners.
2. **Two lines max for role.** Long role descriptions belong in the
   bio, not in the signature.
3. **No legal disclaimers in the signature.** Legal language belongs in
   contracts and proposals, not in every email.

---

## 2. Signature variants

| Variant | Role | When to use |
| --- | --- | --- |
| Founder | Founder / CEO | All founder correspondence |
| Operations | Ops / CSM / Delivery | Internal-facing customer ops |
| Sales | Sales / GTM | Inbound or warm outbound, customer-facing sales |
| Generic | Anyone else | Default for new joiners until a specific variant is assigned |
| Bilingual | Any role | When the recipient is Arabic-first |

Each variant uses the same visual template and differs only in role
line, name, and CTA link.

---

## 3. Visual template

A two-block layout, vertical:

```
[DEALIX wordmark image — 36 px tall]
INTELLIGENT DEALS. REAL GROWTH.

Name Surname
Role · Dealix
email@dealix.com  ·  +966 xx xxx xxxx
dealix.com
```

Visual specs:

- Wordmark: PNG export at 2× resolution (72 px source → 36 px rendered).
  Navy color (`#0B1220`) on white email body.
- Tagline: Inter Medium, all caps, letter-spacing `0.12em`, `xs` size,
  Soft Silver.
- Name: Inter Semibold, `base` size, Deep Navy.
- Role line: Inter Regular, `sm` size, Soft Silver (or `#4A5563` in
  light mode).
- Contact line: Inter Regular, `sm`, Deep Navy. Use middle dot `·` as
  separator, not pipes.
- Link: Inter Regular, `sm`, Deep Navy. Underline on hover only.

No social icons, no calendar booking widget, no banner.

---

## 4. Founder signature

```
[DEALIX wordmark image]
INTELLIGENT DEALS. REAL GROWTH.

Bassam Assiri
Founder · Dealix
bassam@dealix.com
dealix.com
```

The founder signature uses the founder name and the role "Founder" only
— not "Founder & CEO" unless the context demands it. The founder
signature does **not** include a phone number on first-touch
correspondence (we add it after consent).

---

## 5. Operations signature

```
[DEALIX wordmark image]
INTELLIGENT DEALS. REAL GROWTH.

Name Surname
Customer Success · Dealix
name@dealix.com  ·  +966 xx xxx xxxx
dealix.com
```

The operations signature carries a phone because operations
correspondence is in-flight delivery: customers need a fast path to
reach the team.

---

## 6. Sales signature

```
[DEALIX wordmark image]
INTELLIGENT DEALS. REAL GROWTH.

Name Surname
Revenue · Dealix
name@dealix.com
dealix.com  ·  Book a 30-minute call: [cal.dealix.com/name]
```

The sales signature includes a calendar link. The link is a plain text
URL or a single tracked link — never an embedded booking widget that
adds an iframe to the email.

We avoid "Account Executive" as a role title — it is generic. "Revenue"
or "Pilot Lead" reads sharper and is honest about what the person does.

---

## 7. Generic signature

```
[DEALIX wordmark image]
INTELLIGENT DEALS. REAL GROWTH.

Name Surname
Dealix
name@dealix.com
dealix.com
```

The generic signature drops the role line and the phone. It is the
default until a specific role variant is assigned.

---

## 8. Bilingual signature

For Arabic-first recipients, the signature is rendered with both
language blocks, Arabic first.

```
[DEALIX wordmark image]
INTELLIGENT DEALS. REAL GROWTH.

[الاسم بالعربية]
[المسمى الوظيفي] · دِيليكس
name@dealix.com
dealix.com

Name Surname
Role · Dealix
```

The Arabic block is RTL (set explicitly with `dir="rtl"` on the
container `<table>` row). The wordmark and tagline stay Latin, as the
wordmark itself is Latin-only.

---

## 9. Color rules

- The signature renders on **white email backgrounds**. Email clients
  almost universally use white body backgrounds.
- The wordmark image is the **mono navy** variant (Deep Navy `#0B1220`
  glyphs on transparent background).
- Text is Deep Navy or Soft Silver.
- No Emerald Teal in the signature text — the wordmark image itself
  may carry the teal swoosh.

For dark-mode email clients (some iOS Mail dark modes, some Outlook
themes), the signature inverts gracefully because the wordmark is a
transparent PNG. Test on Gmail dark mode, Apple Mail dark mode, and
Outlook dark mode before shipping a new variant.

---

## 10. Implementation

### 10.1 Source
Signatures are stored as HTML snippets in
`assets/brand/marketing/email/signatures/`. One file per variant. The
HTML uses tables for layout (because email clients still demand it),
inline CSS (because most clients strip `<style>`), and no JavaScript
(because email clients block it).

### 10.2 Wordmark hosting
The wordmark image is hosted at a stable URL:
`https://cdn.dealix.com/brand/dealix-wordmark-navy-72.png`. The image
is 72 px tall at 2× resolution, displayed at 36 px CSS height.

Do **not** inline a base64-encoded image — many clients (notably
Outlook) handle base64 poorly and either drop or distort the image.

### 10.3 Fallback
If the image fails to load, the alt text "DEALIX — Saudi B2B Revenue
Operating System" is shown. Always set the alt attribute.

### 10.4 Width
The signature is set to a max-width of 480 px so it does not stretch
on wide screens.

---

## 11. What the signature does not contain

- A photo of the sender.
- A "trusted by" list of customer logos.
- A "Download our app" banner.
- An animated GIF.
- A "Save the planet, don't print this email" line.
- A list of awards or "as seen in" press logos.
- A legal disclaimer ("This message is confidential...").
- Five social media icons.
- A quote of the day.

If a sender wants to add any of the above, the answer is no.

---

## 12. Out-of-office variants

The out-of-office reply uses a shortened signature: wordmark + tagline
+ "I am out until [date]. For urgent matters, contact
[colleague@dealix.com]." No additional copy.

Out-of-office replies do not advertise. They notify and route.

---

## 13. Auto-responder language

For automated email responses (form submissions, support intake), the
signature still appears at the bottom but with an explicit "automated
response" line above the name: "This is an automated acknowledgement.
A human will reply within 1 business day."

We do not pretend an automated reply is a human reply.

---

## 14. Forbidden patterns

- Outdated role titles ("Acting CEO", "Interim Head of...") that do
  not match the company's actual structure.
- Bilingual signatures rendered in the wrong direction (Arabic LTR is
  unreadable).
- Wordmark stretched to fit a banner placeholder.
- A "PS:" with a marketing message bolted onto every email.
- Tracking pixels in the signature image (we do not need to know who
  opened our regular replies).

---

## 15. Signature audit

The brand director audits signatures quarterly:

- Pull a sample of 5 recent sent emails per role.
- Verify the signature matches the canonical variant.
- Verify the wordmark image renders on Gmail, Apple Mail, Outlook web,
  and Outlook desktop.
- Verify links are alive and not redirecting through a tracker.
- Verify Arabic signatures render RTL.

Discrepancies are logged and fixed.

---

## 16. Bilingual note — العربية

التوقيع البريدي هو أصغر سطح علامة وأكثرها تكراراً. هيكله ثابت: شعار
DEALIX النصّي (مونوكروم كحلي)، الشعار الفرعي "INTELLIGENT DEALS. REAL
GROWTH."، الاسم، المسمى الوظيفي، البريد، رقم الهاتف عند الحاجة،
والرابط. لا صورة شخصيّة، لا شعارات عملاء، لا تنبيهات قانونية. للنسخة
العربية يُفعَّل اتجاه RTL على القسم العربي، ويبقى الشعار النصّي
لاتينياً. أي تعديل خارج المتغيّرات المعتمدة يتطلّب موافقة مدير
العلامة.

---

## 17. Variant reference

| Variant | File | Use |
| --- | --- | --- |
| Founder | `signature-founder.html` | Founder correspondence |
| Operations | `signature-ops.html` | Customer success, delivery |
| Sales | `signature-sales.html` | Revenue, GTM |
| Generic | `signature-generic.html` | New joiners, default |
| Bilingual | `signature-bilingual.html` | Arabic-first recipients |
| Out-of-office | `signature-ooo.html` | Auto-reply |

Each file is the canonical source. Sender mail clients pull the HTML
verbatim — no edits.
