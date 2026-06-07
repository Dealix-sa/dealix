export default function ControlledPreviewPage() {
  return (
    <main style={{maxWidth: 980, margin: '0 auto', padding: '64px 24px', lineHeight: 1.8}} dir="rtl">
      <p style={{fontWeight: 700}}>Dealix Controlled Preview</p>
      <h1>إطلاق مُدار لأول 5 عملاء</h1>
      <p>هذه الصفحة تعرض نطاق الإطلاق الحالي: خدمة مُدارة، مراجعة بشرية، proof reports، ولا يوجد إطلاق self-serve واسع بعد.</p>
      <section>
        <h2>المؤشرات</h2>
        <ul>
          <li>أول 5 عملاء فقط</li>
          <li>لا إرسال آلي</li>
          <li>كل claim يحتاج evidence</li>
          <li>كل Pilot له client room وacceptance gate</li>
        </ul>
      </section>
    </main>
  )
}
