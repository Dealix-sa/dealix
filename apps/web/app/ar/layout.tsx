import ArNav from "@/components/ar/ArNav";
import ArFooter from "@/components/ar/ArFooter";

// Shared shell for all public Arabic pages: sticky nav + footer around
// each page's own <main>.
export default function ArLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-[#06111f]">
      <ArNav />
      {children}
      <ArFooter />
    </div>
  );
}
