import { x5Snapshot } from '../../lib/x5-snapshot';

export default function Page() {
  const summary = x5Snapshot.summary;
  return (
    <main>
      <h1>Dealix X5</h1>
      <p>Action registry, approval inbox, and audit foundation.</p>
      <p>Actions: {summary.actions}</p>
      <p>Approvals: {summary.approval_items}</p>
      <p>Audit events: {summary.audit_events}</p>
      <p>Auto execute: {summary.auto_execute}</p>
      <ul>
        {x5Snapshot.actions.map((item) => (
          <li key={item.action_id}>{item.owner}: {item.title} ({item.status})</li>
        ))}
      </ul>
    </main>
  );
}
