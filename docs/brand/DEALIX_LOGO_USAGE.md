# Dealix Logo Usage

Do/don't rules for the Dealix mark. Every external surface — proposal, deck, landing page, email signature, partner deck — must comply.

## DO

- **Do** use the primary lockup on Deep Navy `#0B1220` or Slate `#0F1726` for default brand surfaces.
- **Do** use the icon-only (D monogram) form for favicons, app icons, social avatars, and any space narrower than 160px.
- **Do** preserve the clear space (= height of the D monogram on all four sides).
- **Do** use the white monochrome SVG for press and partner co-branding when the host surface forbids dark backgrounds.
- **Do** verify contrast for the wordmark against any background — minimum 4.5:1 against text-treated wordmark.
- **Do** export at native vector (SVG) for any surface that will be scaled.

## DON'T

- **Don't** rotate, skew, or mirror the mark.
- **Don't** recolour the teal swoosh. The swoosh is always Emerald Teal `#00D1A1`.
- **Don't** outline the wordmark. It is always filled.
- **Don't** apply drop shadows, glows, bevels, or any 3D effect.
- **Don't** typeset "DEALIX" in a different font and call it the wordmark. The wordmark is a frozen SVG.
- **Don't** place the lockup on a photo without a dark gradient overlay (≥ 60% opacity from bottom).
- **Don't** crop the lockup. If it does not fit, switch to the icon-only form.
- **Don't** add the tagline to standalone wordmark or icon variants.
- **Don't** add `™`, `®`, or `©` to the lockup unless the legal team has approved (currently not approved).

## Misuse — examples to refuse

| Misuse                                          | Correct fix                                   |
|-------------------------------------------------|-----------------------------------------------|
| Coloured swoosh (e.g. orange, red, pink)        | Restore Emerald Teal `#00D1A1`                |
| Lockup on a low-contrast photo                  | Add dark overlay or switch to monochrome      |
| Wordmark typeset in Helvetica/Inter             | Use the frozen wordmark SVG                   |
| Icon stretched non-uniformly                    | Restore 1:1 aspect ratio                      |
| "Dealix Pro", "Dealix AI" added to lockup       | Refuse — sub-brands not approved              |
| Lockup at < 160px wide                          | Switch to icon-only form                      |
| Cropped lockup in nav bar                       | Switch to wordmark-only or icon-only form     |

## File naming

All exported logo files follow the pattern:

```
dealix-<variant>-<treatment>-<size>.<ext>

# Examples
dealix-lockup-onnavy-1024.png
dealix-lockup-onwhite-1024.png
dealix-icon-color-512.png
dealix-icon-mono-black-512.svg
dealix-wordmark-white-1024.svg
```

## Co-branding

When pairing the Dealix mark with a customer or partner mark:

- Use the horizontal lockup form.
- Insert a 1px Soft Silver `#B2BBC6` vertical divider between marks.
- Match optical cap height, not bounding box height.
- The relationship line ("in partnership with", "proof-pack by", "client of") must be present in adjacent copy.
- Never present the customer mark larger than the Dealix mark on Dealix-owned surfaces.

## Approval

Any new use case that does not fit one of the documented patterns must be reviewed by the founder before publication. The brand verifier blocks PRs that introduce undocumented logo applications inside `apps/web/`, `landing/`, or `docs/brand/`.
