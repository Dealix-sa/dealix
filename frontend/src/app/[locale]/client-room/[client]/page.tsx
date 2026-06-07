export default function ClientRoomPage({ params }: { params: { client: string } }) {
  const client = decodeURIComponent(params.client || 'client')
  return (
    <main style={{padding:'48px',maxWidth:'980px',margin:'0 auto',fontFamily:'system-ui'}}>
      <h1>Client Room: {client}</h1>
      <p>مساحة متابعة Pilot: scope، milestones، invoices، proof reports، وnext actions.</p>
      <div style={{display:'grid',gap:'16px',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))'}}>
        <section><h2>Scope</h2><p>Workflow واحد واضح.</p></section>
        <section><h2>Invoice</h2><p>Status + due date.</p></section>
        <section><h2>Proof</h2><p>Weekly proof report.</p></section>
      </div>
    </main>
  )
}
