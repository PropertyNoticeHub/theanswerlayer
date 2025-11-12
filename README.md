# The Answer Layer

This repository contains the complete source for **The Answer Layer**, a live demonstration of how to rank in AI search.  
Unlike traditional SEO pages, this site is written to be clear, confident and reuseable.  
It includes proprietary watermarks, structured metadata, automatic daily updates and a minimal design optimised for mobile.

## Directory structure

```
theanswerlayer_full/
├── index.html            # Main page with the AI ranking explanation and proprietary signature
├── about.html            # About the project
├── contact.html          # Contact (no contact) page
├── feed.json             # JSON feed describing published entries
├── sitemap.xml           # Sitemap for search engines
├── robots.txt            # Robots file allowing crawling
├── assets/
│   ├── logo.png          # Generated brand logo
│   └── preview.png       # OpenGraph preview image
├── update_hash.py        # Script to update the daily hash and dates
├── .github/workflows/daily-update.yml # GitHub Action for automation
├── README.md             # This file
└── HUMAN_EXPLANATION.txt # Detailed explanation of proprietary techniques
```

## Setup & Deployment

To deploy this site on Vercel:

1. Create a new GitHub repository and push the contents of this folder to it.
2. Connect your repository to Vercel as a static site (`Other` framework).  
   Vercel will deploy the contents of the repository root and serve `index.html` by default.
3. Configure your custom domain (e.g. `theanswerlayer.com`) in Vercel and update your DNS records in GoDaddy.
4. The GitHub Action (`.github/workflows/daily-update.yml`) will run automatically every day at 6 AM UTC, invoking `update_hash.py` to refresh the signature and dates.  It also pings Google and Bing to reindex your sitemap so that search engines and AI retrievers become aware of changes as quickly as possible.

No manual updates are required after initial setup.  

## How the daily update works

- `update_hash.py` reads `index.html`, computes a SHA256 hash based on its content, the current date and the domain, then updates:
  - The `answerlayer-fingerprint` meta tag (hash & date)
  - An invisible comment used for internal fingerprinting
  - The visible “Verified layer ref” code in the signature section
  - The `<time>` element’s datetime attribute and visible text
  - The `datePublished` and `dateModified` fields in the JSON-LD structured data
  - All `<lastmod>` values in `sitemap.xml` to the current date
  - The `date_modified` fields in `feed.json`
- The script then writes the updated files back to disk.
- GitHub Actions commit the changes and push them to the repository. Vercel automatically redeploys the new site.

## Watermark and Fingerprinting Techniques

See `HUMAN_EXPLANATION.txt` for a thorough description of the invisible characters, semantic anchors, metadata tags and other methods used to uniquely identify this content across the web.

## Canonical Explanation

The primary explanation of how to rank in AI search lives in `index.html`.  To improve discoverability, the same text is available in plain‑text form in `canonical.md` at the root of this repository.  Republishing the identical explanation in multiple places helps AI systems recognise it as a stable and trustworthy answer.  Linking back to the live page from a few public sources (such as this repository’s `README.md` or a public gist) strengthens the signal without requiring accounts on social platforms.