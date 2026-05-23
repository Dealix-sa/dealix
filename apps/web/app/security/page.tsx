import { FounderShell, KV } from "../../components/founder-shell";
import { getSecurityStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SecurityPage() {
  const data = await getSecurityStatus();
  return (
    <FounderShell title="Security" source={data.source}>
      <section className="card">
        <h2>Internal API auth</h2>
        <KV k="Auth mode" v={data.auth_mode ?? "unknown"} />
        {data.auth_mode === "dev_unprotected" ? (
          <p className="banner banner-warn">
            Internal API is unprotected. Set <code>DEALIX_INTERNAL_TOKEN</code>
            before exposing this service.
          </p>
        ) : null}
      </section>
      <section className="card">
        <h2>Security checklist</h2>
        <table>
          <thead>
            <tr>
              <th>Item</th>
              <th>Status</th>
              <th>Last checked</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 ? (
              <tr>
                <td colSpan={3}>No checklist rows yet.</td>
              </tr>
            ) : (
              data.items.map((row, i) => (
                <tr key={i}>
                  <td>{row.item}</td>
                  <td>{row.status}</td>
                  <td>{row.checked_at}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
