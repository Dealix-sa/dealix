import { FounderPage } from "../../components/brand/founder-page";

export default function SettingsPage() {
  return (
    <FounderPage
      title="Settings"
      subtitle="Internal API base URL · keys · workspace."
      blocks={[
        {
          title: "Env",
          body: (
            <ul>
              <li>NEXT_PUBLIC_DEALIX_INTERNAL_API</li>
              <li>NEXT_PUBLIC_DEALIX_INTERNAL_KEY</li>
              <li>DEALIX_PRIVATE_OPS (server-side)</li>
            </ul>
          ),
        },
        { title: "Workspace", body: <p>/opt/dealix-ops-private (private ops, not in git)</p> },
      ]}
    />
  );
}
