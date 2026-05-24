import { FounderPage } from "../../components/brand/founder-page";

export default function PlaybooksPage() {
  return (
    <FounderPage
      title="Playbooks"
      subtitle="Sector-specific playbooks · message angles · objection responses."
      blocks={[
        { title: "Sector playbook", body: <p>docs/playbooks/SECTOR_PLAYBOOK.md</p> },
        { title: "Objection intelligence", body: <p>docs/intelligence/OBJECTION_INTELLIGENCE.md</p> },
      ]}
    />
  );
}
