const items = ["Create organization", "Invite team", "Review billing stub", "Keep outbound draft-only", "Run first Command Room demo"];

export function OnboardingChecklist() {
  return <ul className="space-y-2">{items.map((item) => <li key={item}>✓ {item}</li>)}</ul>;
}
