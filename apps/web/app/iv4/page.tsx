import { iv4Snapshot } from '../../lib/iv4-snapshot';

export default function Page() {
  const summary = iv4Snapshot.summary;
  return (
    <main>
      <h1>Dealix IV4</h1>
      <p>Integrated leadership, commercial growth, and negotiation command queue.</p>
      <p>DX3 items: {summary.dx3_items}</p>
      <p>Growth cards: {summary.growth_cards}</p>
      <p>Negotiation plans: {summary.negotiation_plans}</p>
      <p>Command queue: {summary.command_queue}</p>
      <p>External sends: {summary.external_sends}</p>
      <h2>Queue</h2>
      <ul>
        {iv4Snapshot.command_queue.map((item) => (
          <li key={`${item.source}-${item.title}`}>{item.lane}: {item.title} → {item.next_step}</li>
        ))}
      </ul>
    </main>
  );
}
