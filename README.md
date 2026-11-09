# Najd Alharthi — Editable Portfolio

This is a **GitHub Pages + Pages CMS** portfolio. The site is English-language, mobile-friendly, and includes 14 editable academic project case studies. It does not need paid hosting, a database, or local programming tools to publish.

## First-time setup (about 10–20 minutes)

1. Create or sign into your account at https://github.com.
2. Create a **public** repository named `YOUR-USERNAME.github.io` (replace `YOUR-USERNAME` with your exact GitHub username). You can use another repository name, but then the site URL includes the repository name.
3. Upload **the contents of this folder**, including the hidden `.pages.yml` file and `.github` folder, to the repository's root. Do not upload the ZIP as a single file. Keep the default branch named `main`.
4. Open the repository's **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
5. Open **Actions** and wait for **Publish portfolio** to complete successfully. Visit `https://YOUR-USERNAME.github.io/` (or `https://YOUR-USERNAME.github.io/REPO-NAME/` if using another repository name).
6. Go to https://app.pagescms.org, sign in with GitHub, install/authorize the Pages CMS GitHub App for **this repository only**, then open the repository and `main` branch. Pages CMS reads `.pages.yml` automatically.

## Everyday editing (no coding)

- **Homepage and contact:** edit `Homepage and contact`, then Save. Fill in your public email, LinkedIn URL and resume URL when ready.
- **Projects:** choose `University projects` → open an existing project to edit it; use **New** to add one; use **Delete** to remove one. Keep `slug` unique and lowercase with hyphens. Set `Show publicly` to false to hide a draft. `Featured` moves a project toward the top.
- **Articles:** choose `Engineering journey articles` → New → write and publish. An example article exists but is unpublished.
- **Images:** upload an image through the cover-image field or media library. Images are committed to `media/images/` and displayed in the relevant project or article.
- **Documents:** upload PDFs to `media/documents/`. For a resume, put its published path (such as `/media/documents/resume.pdf`) in the homepage settings. Only upload documents you have permission to publish.
- **Save** in Pages CMS commits the change to GitHub. GitHub Actions automatically rebuilds the website. Wait for the green deployment check, then refresh the live website. It may take a few minutes.

## Privacy and publishing checks

- Do not upload confidential Hitachi Energy factory data, internal reports, photos, personal contact information, or client details without authorization.
- Some project entries are provisional and flagged `Needs fact checking`. Verify these against original reports before sharing the portfolio publicly.
- The project metrics are described as graduation-project results, not company-wide operational results.
- Do not publish a draft until you have reviewed it. If you accidentally delete something, GitHub commit history can help restore it.

## Local preview (optional)

Run `python build.py` from this folder, then open `dist/index.html`. All generated project and article pages are inside `dist/`. For the best media preview, run `python -m http.server 8000 -d dist` and open http://localhost:8000.

**Do not edit `dist/`**. It is automatically regenerated from `content/site.json`, `content/projects/*.json`, and `content/articles/*.json`.

## File layout

- `.pages.yml`: Pages CMS editor definitions
- `.github/workflows/deploy.yml`: automatic GitHub Pages publishing
- `content/site.json`: homepage and contact settings
- `content/projects/*.json`: 14 editable project pages
- `content/articles/*.json`: editable learning articles
- `media/images/`: uploaded images
- `media/documents/`: public PDFs
- `build.py`: generates the static website from the content files
- `styles.css`: visual design

The Pages CMS dashboard is hosted at `app.pagescms.org`; it is **not** an `/admin` page on your own site. Editing requires GitHub access. The public website does not expose an editing dashboard.
