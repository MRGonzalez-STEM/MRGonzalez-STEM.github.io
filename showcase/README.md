# STEM Curriculum Showcase 2025

A comprehensive, interactive showcase system for your year-long STEM curriculum featuring **3D Design**, **Coding**, **Web Development**, **Game Creation**, **Digital Media**, and **Robotics**.

## 🎯 What You Get

- **📚 Curriculum Timeline**: Month-by-month view of all focus areas with your beautiful color scheme
- **🎨 Student Gallery**: Filterable, searchable gallery of all student projects
- **📊 Progress Stats**: Real-time statistics and completion tracking
- **🎮 Interactive Slideshow**: Full-screen presentation mode with autoplay
- **📱 Mobile Responsive**: Works perfectly on all devices
- **🔗 Easy Sharing**: Direct links to GitHub Pages

## 📁 Structure
```
showcase/
├── index.html              # Main project gallery & slideshow
├── curriculum.html         # Curriculum timeline view
├── projects.json           # All project data
├── convert-csv-to-json.html # Web-based CSV converter
├── rosters/                # CSV templates per class
│   ├── curriculum-template.csv  # Full year template
│   └── rm225-g3-kappa.csv      # Sample class
└── images/                 # Optional thumbnails
```

## 🚀 Quick Start

### 1. Test Locally
Open `showcase/index.html` in your browser to see the gallery, then `showcase/curriculum.html` for the timeline view.

### 2. Add Your Projects
- **Option A**: Use the web converter at `showcase/convert-csv-to-json.html`
- **Option B**: Edit `showcase/rosters/curriculum-template.csv` and use the Python script

### 3. Deploy to GitHub Pages
1. Create a new GitHub repository
2. Upload the contents of the `showcase/` folder
3. Go to Settings → Pages → Deploy from main branch
4. Share your live URL!

## 📋 Curriculum Overview

| Month | Focus Area | Key Tools | Student Outcomes |
|-------|------------|-----------|------------------|
| **September** | 3D Design | Tinkercad | Design & prototype treehouse models |
| **October** | Coding Foundations | Scratch, Tynker | Create interactive games/stories |
| **November** | Web Development | HTML, CSS, JS | Build personal portfolio websites |
| **December** | 3D World Development | Unreal Engine 5 | Build landscapes & character navigation |
| **January** | Digital Media | Photo Editing, Design | Master photo editing & digital design |
| **February-March** | Game Development | Scratch, Construct 3 | Design & program interactive games |
| **April-May** | Robotics/Engineering | LEGO Spike, Ozobots | Build & program robotic solutions |
| **June** | Independent Projects | Student Choice | Self-directed STEM projects |

## 🎨 Color Scheme
Each month has its own beautiful color theme:
- **September**: Light Green (3D Design)
- **October**: Light Orange (Coding)
- **November**: Light Blue (Web Dev)
- **December**: Light Purple (3D Worlds)
- **January**: Light Pink (Digital Media)
- **February-March**: Light Red (Game Dev)
- **April-May**: Light Green (Robotics)
- **June**: Light Yellow (Independent)

## 📝 Adding Projects

### For Tinkercad Projects:
1. Open design → **Share** → **Change visibility to Public**
2. Click **Embed** → copy the iframe src URL
3. Add to your CSV with `month: september` and `tool: Tinkercad`

### For Other Tools:
- **Scratch**: Use embed URLs like `https://scratch.mit.edu/projects/ID/embed`
- **Web Projects**: Use direct URLs to student websites
- **LEGO/Ozobot**: Use video URLs or documentation links
- **Unreal Engine**: Use screen recordings or demo links

## 🔧 CSV Format
```csv
id,title,student,klass,grade,month,tool,thumbnail,embedUrl,tags,date
september-treehouse-1,Treehouse Design,Ava G.,RM225 - G3 - Kappa,Grade 3,september,Tinkercad,,https://www.tinkercad.com/embed/XXXXXXXXX?autostart=true,"treehouse;architecture",2025-09-15
```

## 🎯 Display Modes

### 1. **Project Gallery** (`index.html`)
- Filter by grade and class
- Search across all projects
- Interactive slideshow mode
- Perfect for presentations

### 2. **Curriculum Timeline** (`curriculum.html`)
- Month-by-month progression
- Color-coded focus areas
- Project counts per month
- Perfect for showing curriculum flow

### 3. **Progress Stats**
- Total projects completed
- Active students count
- Focus area completion
- Perfect for reporting

## 🔗 Sharing & Links

- **Main Gallery**: `yoursite.github.io/repo-name/`
- **Curriculum View**: `yoursite.github.io/repo-name/curriculum.html`
- **Grade Filter**: `yoursite.github.io/repo-name/?grade=Grade%203`
- **Class Filter**: `yoursite.github.io/repo-name/?class=RM225%20-%20G3%20-%20Kappa`

## 💡 Pro Tips

1. **Privacy**: Use first name + last initial only
2. **Thumbnails**: Add to `images/` folder for better visual appeal
3. **Updates**: Rebuild `projects.json` after adding new projects
4. **Backup**: Keep your CSV files as your source of truth
5. **Mobile**: Test on phones - it's fully responsive!

## 🆘 Need Help?

- **No Python?** Use the web converter at `convert-csv-to-json.html`
- **Tinkercad Issues?** Make sure designs are set to Public
- **GitHub Pages?** Check that all files are in the root of your repo
- **Customization?** Edit the CSS variables in the `<style>` sections

---

**Ready to showcase your amazing STEM curriculum? Let's get started!** 🚀
