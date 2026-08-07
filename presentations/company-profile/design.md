# Design Document — Dealix Company Profile

## 1. Profile Baseline Declaration
- **Profile**: `profiles/strategic.md` — strategic/business plan style
- **Rationale**: Company profile targeting Saudi B2B decision-makers
- **Referenced**: Premium consulting report style (McKinsey/BCG), data-driven, Saudi professional tone
- **Deviation**: Brand colors used instead of generic navy

## 2. Style Baseline
- **Anchor**: McKinsey Digital reports + Saudi premium corporate identity
- **Referenced**: Clean grid layout, data prominence, emerald+gold authority

## 3. Style Details

### Color Design
- **Primary**: `#1B5E3B` Deep Emerald — brand identity, Saudi connection
- **Secondary**: `#0D2818` Forest Green — depth, backgrounds
- **Accent**: `#C9A94C` Gold — highlights, key numbers, CTAs
- **Background**: `#F5F3EF` Warm White — content pages
- **Dark BG**: `#1A1A1A` Charcoal — cover, chapter, emphasis pages
- **Text**: `#1A1A1A` dark, `#6B7280` secondary

### Fonts
- **Titles**: Liter Bold — modern, authoritative
- **Body**: QuattrocentoSans — classic elegance, readable
- **Arabic titles**: alimamashuheiti — commercial, geometric
- **Arabic body**: MiSans — clean, modern

### Theme
```yaml
theme:
  colors:
    primary: "#1B5E3B"
    secondary: "#0D2818"
    accent: "#C9A94C"
    background: "#F5F3EF"
    dark: "#1A1A1A"
    text: "#1A1A1A"
    muted: "#6B7280"
    light: "#FAF8F5"
  textStyles:
    title:
      fontSize: 44
      color: "$primary"
      fontFamily: "Liter, alimamashuheiti"
    subtitle:
      fontSize: 24
      color: "$muted"
      fontFamily: "QuattrocentoSans, MiSans"
    body:
      fontSize: 18
      color: "$text"
      fontFamily: "QuattrocentoSans, MiSans"
      lineHeight: 1.6
    caption:
      fontSize: 14
      color: "$muted"
      fontFamily: "QuattrocentoSans, MiSans"
  tableStyles:
    default:
      headerFill: "$primary"
      headerColor: "#FFFFFF"
      headerBold: true
      bodyFill: ["#FFFFFF", "#FAF8F5"]
      bodyColor: "$text"
      border:
        style: solid
        width: 1
        color: "#E5E5E5"
```

## 4. Layout System
- **16:9** (1280x720)
- **Margins**: 60px sides, 50px top/bottom
- **Cover**: Full-bleed dark bg + centered logo + gold headline
- **Content**: White/light bg, grid-aligned, 2-3 column layouts
- **Chapter**: Dark bg + large chapter number + gold accent

## 5. Risk Prohibitions
- No blue/cyan colors
- No gradients on content pages
- No body text below 18px
- No generic stock photos
- Rounded rectangles sparingly

## 6. Theme Definition
(See Theme section above)
