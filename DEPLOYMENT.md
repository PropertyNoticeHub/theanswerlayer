# Vercel Deployment Guide

Your site is now ready to deploy to Vercel! Follow these steps:

## Quick Deploy Steps

1. **Push to GitHub**
   - Create a new GitHub repository (or use existing)
   - Push all files from `theanswerlayer_full/` to your repository

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect it as a static site
   - Click "Deploy"

3. **Configure Domain** (if you have one)
   - In Vercel project settings, go to "Domains"
   - Add your domain (e.g., `theanswerlayer.com`)
   - Update DNS records as instructed by Vercel

4. **Enable GitHub Actions** (for daily updates)
   - Go to your GitHub repository settings
   - Navigate to "Actions" → "General"
   - Ensure "Allow all actions and reusable workflows" is enabled
   - The daily update workflow will run automatically at 6 AM UTC

## What's Included

✅ **vercel.json** - Vercel configuration with proper headers and caching  
✅ **package.json** - Project metadata for Vercel  
✅ **.github/workflows/daily-update.yml** - Automated daily updates  
✅ **Fixed asset paths** - All images use absolute paths (`/assets/...`)  
✅ **.gitignore** - Excludes unnecessary files  

## After Deployment

- The site will automatically redeploy on every Git push
- Daily updates will run via GitHub Actions at 6 AM UTC
- Search engines will be pinged automatically after each update
- All static assets are cached for optimal performance

## Testing Locally

To test the update script locally:
```bash
python3 update_hash.py
```

## Notes

- The Google Form embed in `index.html` will only work on the live domain (not locally)
- Make sure your domain email forwarding is set up for `contact@theanswerlayer.com`
- The site uses no build process - it's pure static HTML/CSS/JS

