# Schemas — مخططات

JSON Schema (draft 2020-12) definitions for cross-surface contracts. The
WhatsApp Client OS records mirror the dataclasses in
[`auto_client_acquisition/whatsapp_client_os/schemas.py`](../auto_client_acquisition/whatsapp_client_os/schemas.py):

| Schema | Record |
| --- | --- |
| `whatsapp_session.schema.json` | Client session (hashed WhatsApp id only) |
| `whatsapp_message_event.schema.json` | Inbound/outbound message (redacted text) |
| `whatsapp_action_card.schema.json` | Structured option-driven card |
| `whatsapp_flow_state.schema.json` | Per-session flow state |
| `client_assessment.schema.json` | Readiness scan output |
| `client_permission.schema.json` | Permission grant (L0–L5) |

These are documentation/validation contracts. The Python dataclasses remain the
runtime source of truth.

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة_
