# GitHub Pages Deployment Guide

## 🚀 Quick Deploy to GitHub Pages

### Step 1: Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** button → **"New repository"**
3. Name it: `barnum-stem-showcase` (or your preferred name)
4. Make it **Public** (required for free GitHub Pages)
5. Don't initialize with README (we already have files)
6. Click **"Create repository"**

### Step 2: Upload Files
1. In your new repository, click **"uploading an existing file"**
2. Drag and drop ALL files from the `showcase/` folder:
   - `index.html` (Dashboard)
   - `gallery.html` (Student Gallery)
   - `curriculum.html` (Curriculum Timeline)
   - `about.html` (About Mr. Gonzalez)
   - `projects.json` (Data file)
   - `convert-csv-to-json.html` (Data converter)
   - `rosters/` folder (CSV templates)
   - `images/` folder (thumbnails)
3. Add commit message: "Initial STEM showcase deployment"
4. Click **"Commit changes"**

### Step 3: Enable GitHub Pages
1. Go to **Settings** tab in your repository
2. Scroll down to **"Pages"** section (left sidebar)
3. Under **"Source"**, select **"Deploy from a branch"**
4. Select **"main"** branch and **"/ (root)"** folder
5. Click **"Save"**
6. Wait 2-3 minutes for deployment

### Step 4: Access Your Site
Your site will be live at:
```
https://YOUR-USERNAME.github.io/REPO-NAME/
```

## 📁 File Structure for GitHub Pages
```
barnum-stem-showcase/
├── index.html              # 🏠 Main Dashboard (entry point)
├── gallery.html            # 🎨 Student Gallery & Slideshow
├── curriculum.html         # 📚 Curriculum Timeline
├── about.html              # 👨‍🏫 About Mr. Gonzalez
├── projects.json           # 📊 All project data
├── convert-csv-to-json.html # ⚙️ Data converter tool
├── rosters/                # 📋 CSV templates
│   ├── curriculum-template.csv
│   └── rm225-g3-kappa.csv
└── images/                 # 🖼️ Thumbnails (optional)
```

## 🔄 Updating Your Site

### Method 1: GitHub Web Interface
1. Go to your repository on GitHub
2. Click on the file you want to edit
3. Click the **pencil icon** (Edit)
4. Make your changes
5. Scroll down, add commit message
6. Click **"Commit changes"**
7. Changes go live in 1-2 minutes

### Method 2: Upload New Files
1. Go to your repository root
2. Click **"Add file"** → **"Upload files"**
3. Drag new files or use file picker
4. Commit changes

## 🎯 Custom Domain (Optional)
1. Buy a domain (e.g., `barnumstem.com`)
2. In repository Settings → Pages
3. Add your custom domain
4. Follow GitHub's DNS setup instructions

## 📱 Mobile Testing
- Test on phones/tablets
- All pages are fully responsive
- Touch-friendly navigation

## 🔧 Troubleshooting

### Site Not Loading?
- Check that all files are in the root directory
- Ensure `index.html` is in the main folder
- Wait 5-10 minutes for initial deployment

### Projects Not Showing?
- Verify `projects.json` is uploaded correctly
- Check browser console for errors
- Ensure CSV data is properly formatted

### Images Not Loading?
- Upload images to `images/` folder
- Use relative paths: `images/filename.jpg`
- Check file names match exactly

## 🎉 Success!
Your Barnum Public Schools STEM showcase is now live and ready to share with students, parents, and administrators!

**Share these links:**
- **Dashboard**: `https://YOUR-USERNAME.github.io/REPO-NAME/`
- **Gallery**: `https://YOUR-USERNAME.github.io/REPO-NAME/gallery.html`
- **Curriculum**: `https://YOUR-USERNAME.github.io/REPO-NAME/curriculum.html`
- **About**: `https://YOUR-USERNAME.github.io/REPO-NAME/about.html`
