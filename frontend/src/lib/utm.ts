export function readUtm(searchParams: URLSearchParams) {
  return {
    utm_source: searchParams.get("utm_source") || "direct",
    utm_medium: searchParams.get("utm_medium") || "none",
    utm_campaign: searchParams.get("utm_campaign") || "none",
    utm_content: searchParams.get("utm_content") || "none",
  };
}
