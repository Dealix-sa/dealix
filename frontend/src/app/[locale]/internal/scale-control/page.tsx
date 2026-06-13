export default function InternalScaleControlPage() {
  const items = [
    ['Pipeline', 'qualified prospects, replies, discovery, proposals'],
    ['Revenue', 'invoices, collected cash, retainers'],
    ['Delivery', 'client health, hours, proof reports'],
    ['Capacity', 'founder, operator, partner channel'],
    ['Automation', 'backlog priority and safety gates'],
  ]
  return (
    <main style={{maxWidth: 1040, margin: '0 auto', padding: '64px 24px', fontFamily: 'Inter, Arial, sans-serif'}}>
      <h1>Dealix Scale Control Tower</h1>
      <p>Internal dashboard blueprint for weekly scale decisions.</p>
      <div style={{display: 'grid', gap: 12}}>
        {items.map(([title, desc]) => <div key={title} style={{border:'1px solid #e5e7eb', borderRadius: 12, padding: 16}}><strong>{title}</strong><p>{desc}</p></div>)}
      </div>
    </main>
  )
}
