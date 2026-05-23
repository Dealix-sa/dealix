from pathlib import Path
import argparse
import csv
from datetime import date

SOURCES = [
    {
        "sector": "ERP CRM",
        "source_name": "Invest Saudi Companies Directory",
        "source_url": "https://imm.investsaudi.sa/companies_directory",
        "source_type": "directory",
        "next_action": "search ERP CRM Saudi companies",
    },
    {
        "sector": "Cybersecurity",
        "source_name": "Google Search",
        "source_url": "https://www.google.com/search?q=Saudi+cybersecurity+companies",
        "source_type": "search",
        "next_action": "collect public company websites",
    },
    {
        "sector": "B2B Agencies",
        "source_name": "Blue Pages Directory",
        "source_url": "https://bluepages.com.sa/en",
        "source_type": "directory",
        "next_action": "search agencies in Riyadh",
    },
    {
        "sector": "Logistics",
        "source_name": "Google Search",
        "source_url": "https://www.google.com/search?q=Saudi+logistics+B2B+companies",
        "source_type": "search",
        "next_action": "collect logistics B2B leads",
    },
    {
        "sector": "Consulting Implementation",
        "source_name": "Riyadh Chamber Directory",
        "source_url": "https://www.chamber.sa/en/CommercialDelegations/Pages/directoryTP.aspx",
        "source_type": "directory",
        "next_action": "collect consulting and implementation companies",
    },
]

HEADERS = [
    "date",
    "sector",
    "source_name",
    "source_url",
    "source_type",
    "status",
    "next_action",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", required=True)
    args = parser.parse_args()
    root = Path(args.private_ops).resolve()
    out = root / "acquisition/source_targets.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    exists = out.exists() and out.stat().st_size > 0
    with out.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not exists:
            writer.writeheader()
        for item in SOURCES:
            writer.writerow({
                "date": date.today().isoformat(),
                "sector": item["sector"],
                "source_name": item["source_name"],
                "source_url": item["source_url"],
                "source_type": item["source_type"],
                "status": "Planned",
                "next_action": item["next_action"],
            })
    print(f"PASS: source targets written to {out}")


if __name__ == "__main__":
    main()
