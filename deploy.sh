#!/bin/bash
set -e

echo "🚀 revzio Website Deploy Script"
echo "================================"

# Clean up any partial .git from previous attempt
if [ -d ".git" ]; then
  echo "🧹 Removing existing .git folder..."
  rm -rf .git
fi

# Init fresh repo
echo "📁 Initialising git repo..."
git init
git checkout -b main

# Set author to revzio org identity (edit these if needed)
git config user.email "dev@revzio.ai"
git config user.name "revzio"

# Stage all files
echo "📦 Staging all files..."
git add .

# Commit
echo "✅ Committing..."
git commit -m "feat: new website — full redesign with all pages, CSS, JS and assets"

# Add remote (existing GitHub repo)
echo "🔗 Adding remote..."
git remote add origin https://github.com/revzio/website.git

# Force push to main (replaces old code on GitHub)
echo "🚢 Pushing to GitHub (force)..."
git push -f origin main

echo ""
echo "✅ Done! Vercel will auto-deploy from main. Check https://vercel.com/revzio for status."
