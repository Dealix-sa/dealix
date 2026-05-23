const founderConsole = [
  "/ceo",
  "/sales-cockpit",
  "/approvals",
  "/workers",
  "/trust",
  "/finance",
  "/distribution",
  "/delivery",
  "/retention",
  "/proof"
];

const enterpriseControlPlane = [
  "/control-plane",
  "/agents",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving"
];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix</h1>
      <div className="card">
        <h2>Founder Console v3</h2>
        <p>غرفة قيادة المؤسس. لكل رابط مصدر بيانات، فئة موافقة، وسجل تدقيق.</p>
        <ul>
          {founderConsole.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h2>Enterprise Control Plane</h2>
        <p>نقطة دخول لوحات التحكم المؤسسية.</p>
        <ul>
          {enterpriseControlPlane.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
