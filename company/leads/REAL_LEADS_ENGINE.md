# Dealix Real Leads Engine

## Purpose
Replace placeholder targets with real business leads using Google Places Text Search.

## Inputs
- GOOGLE_MAPS_API_KEY
- Target segments
- City queries

## Outputs
- real_leads.csv
- real_leads_report.md
- enriched outbound rows for Revenue Engine

## Safety
- Does not send messages.
- Does not scrape private data.
- Uses public business/place data returned by Google Places API.
- Requests only needed fields.
