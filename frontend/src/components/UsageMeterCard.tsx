export function UsageMeterCard({ label='Agent Runs', used=0, limit=100 }) {
  return <section><h3>{label}</h3><p>{used} / {limit}</p></section>
}
