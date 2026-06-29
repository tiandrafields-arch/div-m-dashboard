# Division M Field Dashboard

Interactive map and field dashboard for the 19th Judicial District Court, Division M race (Election Section 1) in East Baton Rouge Parish, with the Metro Council District 5 overlay. Built from public EBRGIS boundaries and aggregate precinct totals. No individual voter records are included.

## Use it

**Just open `index.html`.** Double click it and it opens in any browser. The map, shading, popups, and dashboard all work with no setup. An internet connection is needed only for the background map tiles.

What you can do:

- **Recolor the map** by registered voters, recent turnout, Democratic share, or Black share (dropdown).
- **Click any precinct** for its ward, number, council district, registration, active count, turnout, and party and race share.
- **Search a precinct** by id (for example `1-077`) to zoom to it.
- **Read the live tallies:** Section 1 total, District 5 total, precinct counts, and District 5 share of the section, plus a District 5 versus rest of section comparison.

## What is in this folder

```
index.html              the dashboard (self contained, open this)
index_template.html     layout and code without data, used to rebuild
data/                   public boundary and aggregate layers (GeoJSON)
join_voter_data.py      helper to refresh counts from a new export
.gitignore              blocks raw voter files from ever being committed
```

## Deploy to GitHub Pages

1. Push this folder to a **private** repository.
2. Repo **Settings, Pages**: Source **Deploy from a branch**, branch **main**, folder **/ (root)**. Save.
3. Your link appears in about a minute: `https://YOURNAME.github.io/REPO/`.

Note: on a free plan, Pages on a private repo still publishes a public page. Password gate it (Netlify or Cloudflare Access) if even this aggregate map should stay internal.

## Refreshing the numbers later

The counts are baked into `index.html`. When you get an updated voter file or official Registrar export, rerun the join against `data/precincts_section1.geojson`, then rebuild `index.html` from `index_template.html`. Keep the raw individual file on your machine only; `.gitignore` already blocks it.

## Data and ethics

- Boundaries: EBRGIS open data (Voting Precinct, 19th JDC Court Sections, Metropolitan Council District).
- Counts: aggregate precinct totals derived from a campaign voter file. They reflect that file, not official Registrar totals. Confirm the official section, division, and registration with the Registrar before relying on them.
- No individual voter records, names, or addresses appear anywhere in this repo. Strategic analysis stays in the internal brief, not on a hosted page.
