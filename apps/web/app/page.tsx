const enterpriseLinks = [
  "/control-plane",
  "/agents",
  "/approvals",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving"
];

const marketAttackLinks = [
  "/market-attack",
  "/campaigns",
  "/partners",
  "/sales-assets",
  "/authority"
];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix Enterprise Control Plane</h1>
      <div className="card">
        <p>نقطة دخول لوحات التحكم المؤسسية.</p>
        <ul>
          {enterpriseLinks.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h2>Market Attack &amp; Scaling</h2>
        <p>
          طبقة Dealix Market Attack — تركيز على القطاع، اختبار العروض،
          الحملات، الشركاء، وأصول البيع.
        </p>
        <ul>
          {marketAttackLinks.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
