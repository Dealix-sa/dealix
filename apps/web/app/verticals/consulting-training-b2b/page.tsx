import type { Metadata } from "next";
import { VerticalDetail, verticalMetadata } from "../_VerticalDetail";

const SLUG = "consulting-training-b2b";

export const metadata: Metadata = verticalMetadata(SLUG);

export default function Page() {
  return <VerticalDetail slug={SLUG} />;
}
