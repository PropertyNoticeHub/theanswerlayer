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

def generate_video_script(date_str: str, new_hash: str) -> None:
    """Generate the daily video script with exact website text, date, and hash."""
    # Convert date to spoken format (e.g., "November 14th, 2025")
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    spoken_date = date_obj.strftime('%B %d, %Y')
    # Add ordinal suffix (st, nd, rd, th)
    day = date_obj.day
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    spoken_date = date_obj.strftime(f'%B {day}{suffix}, %Y')
    
    # Create script content - EXACT text from website
    script = f"""Today is {spoken_date}. This is The Answer Layer.

This video is an example of the method while you're watching it. If this feels clear and easy to understand, then the method is working.

AI search is replacing old Google search. People don't click through lists of links anymore. They ask a system like ChatGPT, Google AI, or Perplexity, and it responds directly.

So the question is: How does that system decide what to say?

What AI Actually Chooses

AI does not pick results the way Google Search used to. It does not care about keywords, backlinks, or article length. It looks for clear explanations it can reuse as answers.

When someone asks a question, the system tries to give a reply that is simple, direct, confident, and easy to understand. If your writing already fits that pattern, the AI is more likely to use it.

What Most People Get Wrong

Most people still write SEO-style content: long, generic, padded, and trying to sound impressive. AI ignores that because it can generate that content itself. Unclear or repetitive explanations are never reused.

The Format AI Reuses

What the topic is. Who it is for. What the real problem is. Why that problem happens. The clear solution or understanding.

Write as you would explain to a friend — no filler, no buildup, just the idea, clean.

Where To Put The Explanation So AI Sees It

Your website. Reddit, reply in a relevant thread. Quora, reply in a relevant thread. Twitter or X, broken into short lines. A short YouTube video where you read it out loud, the transcript matters.

When the same explanation appears in multiple places, the AI treats it as stable and reliable — that's what makes it reuse your answer.

Summary

Ranking in AI isn't about SEO anymore. It's about being clear, reusable, and consistent. AI will pick it up once the pattern is stable.

This is The Answer Layer, a live demonstration of the method it describes.

Verified layer ref: {new_hash}. Updated {spoken_date}.

Learn more at theanswerlayer.com."""
    
    # Create output directory inside repo (works with GitHub Actions)
    output_dir = BASE / "DAILY_VIDEO_SCRIPTS"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write script file
    script_filename = f"DAILY_SCRIPT_{date_str}.txt"
    script_path = output_dir / script_filename
    script_path.write_text(script, encoding='utf-8')
    print(f"Generated video script: {script_path}")

def main() -> None:
    today = datetime.date.today().isoformat()
    index_path = BASE / "index.html"
    content = index_path.read_text(encoding='utf-8')
    new_hash = compute_hash(content, today)
    update_index(today, new_hash)
    update_sitemap(today)
    update_feed(today)
    generate_video_script(today, new_hash)
    print(f"Updated date to {today} and hash to {new_hash}")

if __name__ == '__main__':
    main()