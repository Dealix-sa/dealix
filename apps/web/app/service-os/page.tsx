export default function ServiceOSPage() {
  const layers = [
    { name: 'RCMax', status: 'ready', label: 'Practical Revenue Command' },
    { name: 'Auto14', status: 'ready', label: 'Execution Max' },
    { name: 'Client Ops', status: 'ready', label: '7-Stage Client Lifecycle' },
    { name: 'Conversation Intelligence', status: 'ready', label: 'Arabic + English Intent Classification' },
    { name: 'Deal Strategy', status: 'ready', label: 'Score · Offer · Negotiate' },
    { name: 'Client Autopilot', status: 'ready', label: '13 Auto-Prepared Items' },
  ];

  const approvalGates = [
    'External email send',
    'WhatsApp send',
    'Calendar invite send',
    'Final price commitment',
    'Legal terms acceptance',
    'Contract signature',
    'Guaranteed revenue claim',
    'Public claim without review',
  ];

  const dailyDelivery = [
    'Review open opportunities',
    'Update command queue',
    'Prepare draft routes',
    'Record proof note',
    'Log owner activity',
    'Flag blocked items',
    'Update stage',
  ];

  return (
    <main style={{ fontFamily: 'monospace', padding: '2rem', maxWidth: '800px' }}>
      <h1>Dealix Service OS</h1>
      <p style={{ color: '#666' }}>Real client service system — sell, onboard, serve, prove, renew.</p>

      <h2>System Layers</h2>
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ccc' }}>Layer</th>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ccc' }}>Status</th>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ccc' }}>Description</th>
          </tr>
        </thead>
        <tbody>
          {layers.map((layer) => (
            <tr key={layer.name}>
              <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{layer.name}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #eee', color: '#16a34a' }}>✓ {layer.status}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #eee', color: '#555' }}>{layer.label}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 style={{ marginTop: '2rem' }}>Safety Counters</h2>
      <ul>
        <li>Live sends: <strong>0</strong></li>
        <li>Final commitments: <strong>0</strong></li>
        <li>Approval gates active: <strong>{approvalGates.length}</strong></li>
      </ul>

      <h2>Approval Gates (never auto-run)</h2>
      <ul>
        {approvalGates.map((gate) => (
          <li key={gate}>{gate}</li>
        ))}
      </ul>

      <h2>Daily Delivery Checklist</h2>
      <ul>
        {dailyDelivery.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>

      <h2>Client Timeline</h2>
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ccc' }}>Day</th>
            <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ccc' }}>What Happens</th>
          </tr>
        </thead>
        <tbody>
          {[
            ['Day 0', 'Client intake — channels, owners, sample data'],
            ['Day 1', 'Workflow diagnosis + command queue'],
            ['Day 2', 'First proof note'],
            ['Day 3–5', 'Daily operating updates'],
            ['Day 7', 'Weekly review + next plan'],
          ].map(([day, desc]) => (
            <tr key={day}>
              <td style={{ padding: '8px', borderBottom: '1px solid #eee', fontWeight: 'bold' }}>{day}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #eee' }}>{desc}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <p style={{ marginTop: '2rem', color: '#888', fontSize: '0.85rem' }}>
        Run: <code>python run_dealix_service_os.py</code> → <code>reports/commercial/service_os/latest.md</code>
      </p>
    </main>
  );
}
