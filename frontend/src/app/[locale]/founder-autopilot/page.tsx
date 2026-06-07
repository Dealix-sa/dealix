export default function FounderAutopilotPage() {
  return (
    <main style={{padding: '48px', maxWidth: 1040, margin: '0 auto'}}>
      <p style={{letterSpacing: '.12em', textTransform: 'uppercase', opacity: .7}}>Dealix Founder OS</p>
      <h1>Founder Daily Execution Autopilot</h1>
      <p>لوحة تشغيل يومية ترتب أعلى مهام الفاوندر: الإيراد، التسليم، الأدلة، المخاطر، والمتابعة.</p>
      <section style={{display: 'grid', gap: 16, gridTemplateColumns: 'repeat(auto-fit,minmax(220px,1fr))'}}>
        <div><h3>Command Brief</h3><p>قرار اليوم، أعلى رقم، وأقرب إجراء للإيراد.</p></div>
        <div><h3>Top 10 Tasks</h3><p>مهام محدودة ومرتبة حسب أثرها على الإطلاق.</p></div>
        <div><h3>Review Queue</h3><p>رسائل، عروض، فواتير، وتقارير تحتاج اعتمادًا بشريًا.</p></div>
      </section>
    </main>
  )
}
