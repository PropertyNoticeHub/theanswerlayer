#!/usr/bin/env python3
"""
Daily watermark update script for The Answer Layer.

This script computes a daily SHA256 signature based on the current
contents of index.html combined with the current date and domain.
It updates several fields in index.html and sitemap.xml:

 - answerlayer-fingerprint meta tag
 - invisible comment line
 - Verified layer ref code value
 - timestamp in the signature section
 - datePublished and dateModified in the JSON-LD block
 - <lastmod> values in the sitemap

Run this script automatically via GitHub Actions to keep the site current.
"""

import hashlib
import datetime
import re
from pathlib import Path

DOMAIN = "theanswerlayer.com"
BASE = Path(__file__).resolve().parent

def compute_hash(content: str, date: str) -> str:
    """Compute a 10-character hex digest based on content, date and domain."""
    digest = hashlib.sha256((content + date + DOMAIN).encode('utf-8')).hexdigest()
    return digest[:10]

def update_index(date_str: str, new_hash: str) -> None:
    index_path = BASE / "index.html"
    text = index_path.read_text(encoding='utf-8')

    # Update answerlayer-fingerprint meta
    text = re.sub(
        r"answerlayer-fingerprint\" content=\"hash:[0-9a-f]{10};date:\d{4}-\d{2}-\d{2}\"",
        f"answerlayer-fingerprint\" content=\"hash:{new_hash};date:{date_str}\"",
        text,
    )
    # Update invisible comment placeholder
    text = re.sub(
        r"answerlayer:theanswerlayer.com:invisible-id:[A-Za-z0-9]+",
        f"answerlayer:theanswerlayer.com:invisible-id:{new_hash}",
        text,
    )
    # Update Verified layer ref
    text = re.sub(
        r"Verified layer ref: <code>[0-9a-f]{10}</code>",
        f"Verified layer ref: <code>{new_hash}</code>",
        text,
    )
    # Update time datetime attribute and displayed date
    text = re.sub(
        r"<time datetime=\"\d{4}-\d{2}-\d{2}\">[^<]+</time>",
        f"<time datetime=\"{date_str}\">{datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime('%B %d, %Y')}</time>",
        text,
    )
    # Update JSON-LD datePublished and dateModified
    text = re.sub(
        r'"datePublished": "\d{4}-\d{2}-\d{2}",',
        f'"datePublished": "{date_str}",',
        text,
    )
    text = re.sub(
        r'"dateModified": "\d{4}-\d{2}-\d{2}",',
        f'"dateModified": "{date_str}",',
        text,
    )
    # Write back
    index_path.write_text(text, encoding='utf-8')

def update_sitemap(date_str: str) -> None:
    sitemap_path = BASE / "sitemap.xml"
    xml = sitemap_path.read_text(encoding='utf-8')
    xml = re.sub(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", f"<lastmod>{date_str}</lastmod>", xml)
    sitemap_path.write_text(xml, encoding='utf-8')

def update_feed(date_str: str) -> None:
    feed_path = BASE / "feed.json"
    if not feed_path.exists():
        return
    data = feed_path.read_text(encoding='utf-8')
    # Update date_modified fields for all items
    data = re.sub(r'"date_modified": "\d{4}-\d{2}-\d{2}T[0-9:]+Z"', f'"date_modified": "{date_str}T00:00:00Z"', data)
    # Optionally update the feed's overall description if required
    feed_path.write_text(data, encoding='utf-8')

def main() -> None:
    today = datetime.date.today().isoformat()
    index_path = BASE / "index.html"
    content = index_path.read_text(encoding='utf-8')
    new_hash = compute_hash(content, today)
    update_index(today, new_hash)
    update_sitemap(today)
    update_feed(today)
    print(f"Updated date to {today} and hash to {new_hash}")

if __name__ == '__main__':
    main()