# Client Onboarding — Day 0 Checklist — تهيئة العميل

## Purpose
A repeatable Day 0 onboarding for every paid engagement. The first 72 hours decide whether the engagement runs on rails or runs on improvisation. This checklist eliminates improvisation.

## Owner
Founder (delivery lead) for first 10 clients. Delivery analyst takes over once 10 onboardings are documented and identical (see hiring trigger).

## Inputs
- Signed Statement of Work and proposal.
- Client primary contact + escalation contact.
- Data scope (what the client will share, in writing).
- Communication preference (Slack, WhatsApp Business, email).

## Outputs
- Filed onboarding record under `evidence/onboarding/<client_id>/`.
- Kickoff call held within 72 hours of payment confirmation.
- First weekly report scheduled.

## Day 0 (Payment Confirmed)
- [ ] Signed SOW and proposal filed.
- [ ] Client primary + escalation contact stored.
- [ ] Welcome message sent (bilingual AR + EN).
- [ ] Kickoff call scheduled within 72 hours.
- [ ] Shared workspace (folder/channel) created.
- [ ] PDPL data handling brief shared (`docs/14_trust_os/`).
- [ ] Disclosure of what Dealix will and won't do (`docs/03_commercial_mvp/`).

## Day 1 (Kickoff Call — 60 min)
- [ ] Confirm goals, success criteria, scope boundaries.
- [ ] Confirm what data the client will share, in what format, by when.
- [ ] Confirm cadence (weekly report day, contact channel).
- [ ] Walk through delivery plan and milestones.
- [ ] Set kill criterion (when do we stop).
- [ ] Capture initial feedback channel.

## Day 3
- [ ] Data received and validated.
- [ ] First working artifact draft started.
- [ ] Issues raised within first 48 hours logged.

## Day 7
- [ ] First weekly report delivered (see template).
- [ ] Mid-week temperature check (15 min call or message).
- [ ] Health score initial baseline recorded.

## Rules
1. No work starts before signed SOW + payment confirmation.
2. PDPL brief is mandatory before any client data is touched.
3. The kill criterion is set in the kickoff and revisited weekly.
4. Communication channels limited to the agreed ones; no shadow chats.
5. No outbound automation on the client's behalf without written approval.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" appears on the kickoff deck and every weekly report.

## Metrics
- Onboarding on-time completion rate (target 100%).
- Time from payment to kickoff (target ≤ 72h).
- Initial health score (target ≥ 70).
- Day-7 weekly report delivered (target 100%).

## Cadence
- Per-client, once.

## Evidence
- `evidence/onboarding/<client_id>/checklist.md`.
- Signed SOW reference.

## Verifier
Founder.

## Runtime Command
`make onboard CLIENT=<id>` — opens checklist, blocks marking complete until all required items are checked.

## Arabic Summary — ملخص عربي
قائمة تهيئة من اليوم الصفر حتى اليوم السابع. لا عمل قبل التوقيع والدفع. الإحاطة بحماية البيانات إلزامية قبل لمس أي بيانات. القيم التقديرية ليست مُتحقَّقة.
