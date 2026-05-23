const founderLinks = [
  "/ceo",
  "/sales-cockpit",
  "/approvals",
  "/workers",
  "/trust",
  "/finance",
  "/distribution"
];

const platformLinks = [
  "/control-plane",
  "/agents",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving"
];

const links = [...founderLinks, ...platformLinks];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix Enterprise Control Plane</h1>
      <div className="card">
        <p>نقطة دخول لوحات التحكم المؤسسية.</p>
        <ul>
          {links.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
