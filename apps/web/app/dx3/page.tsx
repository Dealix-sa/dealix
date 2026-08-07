import { dx3Snapshot } from '../../lib/dx3-snapshot';

export default function Page() {
  const summary = dx3Snapshot.summary;
  return (
    <main>
      <h1>Dealix DX3</h1>
      <p>Expanded leadership operating layer.</p>
      <p>Lanes: {summary.lanes}</p>
      <p>Items: {summary.items}</p>
      <p>Review required: {summary.review_required}</p>
      <p>Auto execute: {summary.auto_execute}</p>
      <h2>Top priorities</h2>
      <ul>
        {dx3Snapshot.top_items.map((item) => (
          <li key={`${item.lane}-${item.title}`}>{item.lane}: {item.title} → {item.next_step} ({item.score})</li>
        ))}
      </ul>
    </main>
  );
}
