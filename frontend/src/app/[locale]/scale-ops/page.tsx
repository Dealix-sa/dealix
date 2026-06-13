export default function ScaleOpsPage() {
  return (
    <main style={{maxWidth: 980, margin: '0 auto', padding: '64px 24px', fontFamily: 'Inter, Arial, sans-serif'}}>
      <p style={{letterSpacing: 2, textTransform: 'uppercase', color: '#64748b'}}>Dealix V12</p>
      <h1 style={{fontSize: 44, lineHeight: 1.05}}>Scale & Operating Cadence</h1>
      <p style={{fontSize: 20, color: '#334155'}}>حوّل أول إيراد إلى نظام أسبوعي قابل للتوسع: pipeline، delivery، margin، hiring، partners، وautomation backlog.</p>
      <section style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16, marginTop: 32}}>
        {['Weekly Operating Rhythm','Client Portfolio Review','Sales Capacity','Service Margin','Automation Backlog','Partner Quotas'].map((x) => (
          <div key={x} style={{border: '1px solid #e2e8f0', borderRadius: 16, padding: 20}}>
            <h2 style={{fontSize: 18}}>{x}</h2>
            <p style={{color: '#475569'}}>Managed scale control for Dealix growth operations.</p>
          </div>
        ))}
      </section>
    </main>
  )
}
