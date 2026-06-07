export function FounderTaskCard({ title, score, source }: { title: string; score: number; source: string }) {
  return (
    <article style={{border: '1px solid #ddd', borderRadius: 16, padding: 18}}>
      <p style={{opacity: .65}}>{source}</p>
      <h3>{title}</h3>
      <strong>Score: {score}</strong>
    </article>
  )
}
