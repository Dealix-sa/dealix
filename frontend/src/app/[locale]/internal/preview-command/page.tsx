export default function PreviewCommandPage() {
  return (
    <main style={{maxWidth: 980, margin: '0 auto', padding: '64px 24px', lineHeight: 1.8}} dir="rtl">
      <h1>Preview Command Center</h1>
      <p>لوحة داخلية لمتابعة أسبوع الإطلاق: prospects، drafts، calls، pilots، proof reports، incidents.</p>
      <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(180px,1fr))', gap:16}}>
        {['Prospects reviewed','Drafts created','Discovery calls','Pilots won','Proof reports','Incidents'].map((x)=>(
          <section key={x} style={{border:'1px solid #ddd', borderRadius:12, padding:16}}><strong>{x}</strong><p>راجع التقرير اليومي</p></section>
        ))}
      </div>
    </main>
  )
}
