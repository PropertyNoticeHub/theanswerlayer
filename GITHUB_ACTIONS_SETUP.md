# GITHUB ACTIONS SETUP - AUTOMATED VIDEO SCRIPT GENERATION

## What Changed

**BEFORE:** Video script saved to your Desktop (`C:\Users\Owner\Desktop\...`)  
**NOW:** Video script saved to repo folder (`DAILY_VIDEO_SCRIPTS/`)

**Result:** GitHub Actions creates the script file daily and commits it automatically.

---

## Files You Need to Update

### 1. Replace `update_hash.py`
[Download the new version](computer:///mnt/user-data/outputs/update_hash.py)

Replace your current `update_hash.py` with this new version.

**Key change:** Script now saves to `DAILY_VIDEO_SCRIPTS/` folder inside your repo (not your Desktop).

### 2. Replace `.github/workflows/daily-update.yml`
[Download the new version](computer:///mnt/user-data/outputs/daily-update.yml)

Replace your current GitHub Actions workflow file.

**Key change:** Now commits the `DAILY_VIDEO_SCRIPTS/` folder along with the website files.

### 3. Create `.gitignore` Entry (Optional)

If you want to keep old script files out of your repo history, add this to `.gitignore`:

```
# Keep only the most recent script
DAILY_VIDEO_SCRIPTS/*
!DAILY_VIDEO_SCRIPTS/.gitkeep
```

(But honestly, it's fine to commit them all - they're tiny text files)

---

## How It Works Now

### Every Day at 6 AM UTC:

1. **GitHub Actions runs** `update_hash.py`
2. **Script updates:**
   - index.html (hash, date)
   - sitemap.xml (dates)
   - feed.json (dates)
   - **NEW:** Creates `DAILY_VIDEO_SCRIPTS/DAILY_SCRIPT_2025-11-14.txt`
3. **GitHub Actions commits** all changes
4. **Vercel deploys** the website
5. **Script file is ready** in your repo

---

## Your New Daily Workflow

### Option A: View on GitHub (Fastest)

1. Go to: `https://github.com/[YOUR-USERNAME]/TheAnswerLayer/tree/main/DAILY_VIDEO_SCRIPTS`
2. Click today's file: `DAILY_SCRIPT_2025-11-14.txt`
3. Click **"Raw"** button (top right)
4. **Ctrl+A** (select all) → **Ctrl+C** (copy)
5. Paste into your video tool

**Time: 10 seconds**

### Option B: Pull to Local Computer

1. Open your terminal/command prompt
2. Navigate to your repo: `cd C:\Users\Owner\Desktop\TheAnswerLayer`
3. Pull latest: `git pull`
4. Open: `DAILY_VIDEO_SCRIPTS\DAILY_SCRIPT_2025-11-14.txt`
5. Copy and paste into your video tool

**Time: 20 seconds**

### Option C: Direct Raw URL (Advanced)

Bookmark this URL pattern and just change the date daily:
```
https://raw.githubusercontent.com/[YOUR-USERNAME]/TheAnswerLayer/main/DAILY_VIDEO_SCRIPTS/DAILY_SCRIPT_2025-11-14.txt
```

Open in browser, Ctrl+A, Ctrl+C, done.

**Time: 5 seconds**

---

## Setup Steps (One-Time)

1. **Commit the new files:**
   ```bash
   git add update_hash.py .github/workflows/daily-update.yml
   git commit -m "Update script to generate video scripts in repo"
   git push
   ```

2. **Test it manually:**
   - Go to your GitHub repo
   - Click "Actions" tab
   - Click "Daily Update" workflow
   - Click "Run workflow" dropdown
   - Click "Run workflow" button
   - Wait 30 seconds
   - Check if `DAILY_VIDEO_SCRIPTS/` folder appears with today's script

3. **Done!** From now on, it runs automatically every day at 6 AM UTC.

---

## Benefits of This Approach

✅ **Perfect hash sync** - Script always matches website  
✅ **No local running** - You don't need to run Python daily  
✅ **Always accessible** - View from any device with internet  
✅ **Version history** - All scripts saved in Git history  
✅ **Zero maintenance** - Set it and forget it  

---

## Troubleshooting

**Q: The folder didn't get created**  
A: Check GitHub Actions logs - might be a permissions issue

**Q: The script has the wrong hash**  
A: Impossible now - hash is computed in the same run

**Q: I want to also keep scripts on my Desktop**  
A: After pulling from GitHub, copy the file to your Desktop manually

**Q: Can I run the script locally still?**  
A: Yes! It will create the file in `DAILY_VIDEO_SCRIPTS/` folder in your local repo

---

## What Happens to Old Scripts?

Every day creates a new file:
```
DAILY_VIDEO_SCRIPTS/
├── DAILY_SCRIPT_2025-11-12.txt
├── DAILY_SCRIPT_2025-11-13.txt
├── DAILY_SCRIPT_2025-11-14.txt
└── DAILY_SCRIPT_2025-11-15.txt
```

They accumulate in your repo. If you want to clean them up monthly, just delete old ones and commit.

---

**That's it! Your video script generation is now fully automated and synced with your website.**
