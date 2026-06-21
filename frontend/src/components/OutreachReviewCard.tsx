export default function OutreachReviewCard() {
  return (
    <div style={{border: '1px solid #ddd', borderRadius: 16, padding: 20}}>
      <h2>Human Review Queue</h2>
      <p>كل مسودة تواصل تحتاج موافقة بشرية قبل الاستخدام الخارجي.</p>
      <ul>
        <li>Check claim safety</li>
        <li>Check personalization</li>
        <li>Check source of contact</li>
        <li>Approve / edit / reject</li>
      </ul>
    </div>
  );
}
