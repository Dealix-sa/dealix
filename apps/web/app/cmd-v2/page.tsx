import { cmdV2Snapshot } from '../../lib/cmd-v2-snapshot';

export default function Page() {
  return (
    <main>
      <h1>Dealix Command v2</h1>
      <p>Leadership command room foundation.</p>
      <p>Lanes: {cmdV2Snapshot.summary.lanes}</p>
      <p>Actions: {cmdV2Snapshot.summary.actions}</p>
      <p>Cards: {cmdV2Snapshot.summary.decision_cards}</p>
      <ul>
        {cmdV2Snapshot.decision_cards.map((card) => <li key={card.lane}>{card.owner}: {card.title}</li>)}
      </ul>
    </main>
  );
}
