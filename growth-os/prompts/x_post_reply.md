# Prompt: X (Twitter) Post and Reply
**Used by:** asset-generator agent (official API only)
**Output:** channel_assets.jsonl (channel: x)

IMPORTANT: X is for content and reply to relevant mentions only.
No unsolicited bulk DM. Official API only.

---

## Post Prompt (Thought Leadership)

```
Write a thought leadership post for X (Twitter) about {topic} 
relevant to B2B operations in Saudi Arabia.

Rules:
- Under 280 characters
- No sales language — insight only
- Can mention Dealix as context if relevant
- No guaranteed claims
- Arabic or English based on {language}
- End with a relevant question to drive engagement
- Tag relevant hashtags: #SaudiArabia #Operations #AI #Vision2030
```

---

## Reply Prompt (Relevant Mentions)

```
Write a reply to this X post that mentions {relevant_topic}:

Original post: {post_text}
Author context: {author_context}

Reply rules:
- Under 280 characters
- Add value to the conversation — do not just promote
- If it is a direct question about AI ops in Saudi: can briefly mention what Dealix does
- Move to DM only if they explicitly ask for more info
- No cold DM — only reply to public post
```

**Arabic:**
```
اكتب رداً على هذا المنشور في X:
المنشور: {post_text}

قواعد:
- أقل من 280 حرف
- أضف قيمة للنقاش — لا ترويج مباشر
- إذا سألوا عن الذكاء الاصطناعي في العمليات: يمكن ذكر ديليكس باختصار
- لا رسائل مباشرة غير مطلوبة
```

---

## Daily Limits

```yaml
posts_per_day: 10
replies_per_day: 30
dms_per_day: 0
bulk_dm: forbidden
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
