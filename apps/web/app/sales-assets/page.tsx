import { FounderPage } from "../../components/brand/founder-page";

export default function SalesAssetsPage() {
  return (
    <FounderPage
      title="Sales Assets"
      subtitle="One-pagers · proposals · samples · objection responses."
      blocks={[
        { title: "Asset registry", body: <p>sales/sales_asset_registry.csv</p> },
        {
          title: "Folders",
          body: (
            <ul>
              <li>assets/sales/one_pagers/</li>
              <li>assets/sales/proposals/</li>
              <li>assets/sales/samples/</li>
              <li>assets/sales/objections/</li>
              <li>assets/sales/proof_safe/</li>
            </ul>
          ),
        },
      ]}
    />
  );
}
