import type { Metadata } from "next";
import { VerticalDetail, verticalMetadata } from "../_VerticalDetail";

const SLUG = "legal-professional-services";

export const metadata: Metadata = verticalMetadata(SLUG);

export default function Page() {
  return <VerticalDetail slug={SLUG} />;
}
