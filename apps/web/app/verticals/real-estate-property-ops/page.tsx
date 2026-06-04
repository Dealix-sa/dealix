import type { Metadata } from "next";
import { VerticalDetail, verticalMetadata } from "../_VerticalDetail";

const SLUG = "real-estate-property-ops";

export const metadata: Metadata = verticalMetadata(SLUG);

export default function Page() {
  return <VerticalDetail slug={SLUG} />;
}
