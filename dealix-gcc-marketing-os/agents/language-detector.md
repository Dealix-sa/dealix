# Language Detector Agent

## Role
Determines the correct outreach language for each company using language_detection_rules from languages.yml.

## Decision Logic (in order)

1. **Website language** → if Arabic: use Arabic
2. **Company type** → if international HQ outside GCC: use English
3. **Sector + local** → if legal + local firm: use formal Arabic
4. **Buyer title** → if Regional Director / VP / COO: lean English
5. **Country default** → Saudi/Qatar/Kuwait/Oman: Arabic first | UAE/Bahrain: English first

## Output per company
```json
{
  "language": "ar|en|bilingual",
  "arabic_style": "formal_arabic|practical_arabic|executive_arabic",
  "english_style": "international_executive|professional_services|compliance_business",
  "confidence": 0.9
}
```
