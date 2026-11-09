"""Build editable JSON content into a self-contained static portfolio (stdlib only)."""
from pathlib import Path
import json,html,re,shutil
R=Path(__file__).resolve().parent; OUT=R/'dist'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def e(s): return html.escape(str(s or ''),quote=True)
def para(s): return ''.join('<p>'+e(p).replace('\n','<br>')+'</p>' for p in str(s or '').split('\n\n') if p.strip())
def img(path,cls='cover',prefix=''):
 if not path or not str(path).startswith('/media/'): return ''
 return f'<img class="{cls}" src="{e(prefix + path.lstrip(chr(47)))}" alt="" loading="lazy">'
def safe_slug(s):return re.sub('[^a-z0-9-]','-',str(s).lower()).strip('-') or 'item'
def layout(title,body,root=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Najd Alharthi — Industrial Engineer, projects and engineering journey"><title>{e(title)} | Najd Alharthi</title><link rel="stylesheet" href="{root}styles.css"><style>
body{{color:#24374b}}[hidden]{{display:none!important}}.page-intro{{padding:85px 0 30px}}.page-intro h1{{max-width:850px}}.project-card{{overflow:hidden}}.project-card .cover{{width:100%;height:180px;object-fit:cover;display:block}}.project-card .card-body{{padding:24px}}.project-grid{{align-items:stretch}}.project-card{{display:flex;flex-direction:column}}.project-card .card-body{{display:flex;flex-direction:column;flex:1}}.card-bottom{{margin-top:auto}}.detail{{max-width:800px;margin:auto;padding:55px 22px 100px}}.detail h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15}}.detail h2{{margin-top:36px;font-size:1.3rem}}.detail p{{line-height:1.8}}.detail .cover{{width:100%;max-height:430px;object-fit:cover;border-radius:14px;margin:25px 0}}.article-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px}}.article-card{{padding:25px;border:1px solid #e1e7ef;border-radius:14px;background:white}}.article-card a,.project-card a{{color:#183456}}.article-card .cover{{width:100%;height:170px;object-fit:cover;border-radius:10px}}.back-link{{display:inline-block;margin-bottom:20px;color:#315d88}}.text-body{{white-space:pre-line}}.review{{background:#fff6df;border-left:3px solid #c79535;padding:12px 16px}}.site-header nav{{display:flex;gap:18px;flex-wrap:wrap}}@media(max-width:600px){{.page-intro{{padding-top:45px}}.site-header .nav{{flex-wrap:wrap;gap:12px}}}}
</style></head><body><header class="site-header"><div class="wrap nav"><a class="brand" href="{root}index.html">NAJD ALHARTHI<span>.</span></a><nav aria-label="Main navigation"><a href="{root}index.html#about">About</a><a href="{root}index.html#projects">Projects</a><a href="{root}index.html#journey">Journey</a><a href="{root}index.html#contact">Contact</a></nav></div></header><main>{body}</main><footer><div class="wrap">© 2026 Najd Alharthi · Industrial Engineering Portfolio</div></footer></body></html>'''
site=read(R/'content/site.json')
projects=[read(p) for p in sorted((R/'content/projects').glob('*.json'))]
articles=[read(p) for p in sorted((R/'content/articles').glob('*.json'))]
projects=[p for p in projects if p.get('published',True)]
articles=[a for a in articles if a.get('published',False)]
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir();shutil.copy(R/'styles.css',OUT/'styles.css');shutil.copytree(R/'media',OUT/'media')
(OUT/'projects').mkdir();(OUT/'articles').mkdir()
seen=set()
for p in projects:
 slug=safe_slug(p.get('slug') or p.get('title'))
 if slug in seen:raise ValueError('Duplicate project slug: '+slug)
 seen.add(slug)
 p['_url']='projects/'+slug+'.html'
 sections=[('The challenge','challenge'),('Approach','approach'),('Tools & methods','tools'),('Results / deliverables','outcome'),('What I learned','learned')]
 details=''.join(f'<section><h2>{e(label)}</h2>{para(" · ".join(p.get(key,[])) if key=="tools" else p.get(key,""))}</section>' for label,key in sections)
 notice='<p class="review">Draft information — verify against original course materials before external publication.</p>' if p.get('needsReview') else ''
 body=f'<div class="detail"><a class="back-link" href="../index.html#projects">← All projects</a><p class="eyebrow">{e(p.get("category"))} / {e(p.get("type"))}</p><h1>{e(p.get("title"))}</h1><p class="lead">{e(p.get("summary"))}</p>{img(p.get("image"),prefix='../')}{notice}{details}</div>'
 (OUT/p['_url']).write_text(layout(p['title'],body,'../'),encoding='utf-8')
for a in articles:
 slug=safe_slug(a.get('title'))
 a['_url']='articles/'+slug+'.html'
 body=f'<div class="detail"><a class="back-link" href="../index.html#journey">← Engineering journey</a><p class="eyebrow">ENGINEERING JOURNEY · {e(a.get("date"))}</p><h1>{e(a.get("title"))}</h1><p class="lead">{e(a.get("summary"))}</p>{img(a.get("image"),prefix='../')}<div class="text-body">{para(a.get("body"))}</div></div>'
 (OUT/a['_url']).write_text(layout(a['title'],body,'../'),encoding='utf-8')
categories=['All']+sorted(set(p.get('category','Other') for p in projects))
cards=''.join(f'''<article class="project-card" data-category="{e(p.get('category'))}" data-search="{e(' '.join([p.get('title',''),p.get('summary',''),p.get('category',''),' '.join(p.get('tools',[]))]).lower())}">{img(p.get('image'))}<div class="card-body"><div class="card-top"><span>{e(p.get('category'))} · {e(p.get('type'))}</span>{'<span class="featured">Featured</span>' if p.get('featured') else ''}</div><h3>{e(p.get('title'))}</h3><p>{e(p.get('summary'))}</p><div class="card-bottom"><span>{'Details to verify' if p.get('needsReview') else 'Case study'}</span><a href="{e(p['_url'])}">View project ↗</a></div></div></article>''' for p in sorted(projects,key=lambda p:(not p.get('featured'),p.get('title',''))))
article_cards=''.join(f'<article class="article-card">{img(a.get("image"))}<p class="eyebrow">{e(a.get("date"))}</p><h3>{e(a.get("title"))}</h3><p>{e(a.get("summary"))}</p><a href="{e(a["_url"])}">Read article ↗</a></article>' for a in articles)
contacts=''.join(f'<a class="btn light" href="{e(url)}" {"target=_blank rel=noopener" if name=="LinkedIn" else ""}>{name} ↗</a>' for name,url in [('Email','mailto:'+site['email'] if site.get('email') and re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$',site['email']) else ''),('LinkedIn',site.get('linkedin','') if site.get('linkedin','').startswith('https://') else ''),('Resume',site.get('resume','') if site.get('resume','').startswith(('/media/','https://')) else '')] if url)
body=f'''<section id="home" class="hero"><div class="wrap"><p class="eyebrow">INDUSTRIAL ENGINEER · PORTFOLIO</p><h1>{e(site['headline'])}<br><span>{e(site['tagline'])}</span></h1><p class="lead">{e(site['role'])}</p><p class="intro">{e(site['intro'])}</p><div class="actions"><a class="btn primary" href="#projects">Explore my work ↗</a><a class="btn secondary" href="#contact">Get in touch</a></div><div class="stats"><div><strong>{e(site['gpa'])}</strong><small>University GPA</small></div><div><strong>{e(site['lead_time'])}</strong><small>Lead-time reduction*</small></div><div><strong>{e(site['capacity'])}</strong><small>Capacity increase*</small></div></div><p class="footnote">*Reported graduation project results, not company-wide performance.</p></div></section>
<section id="about" class="section"><div class="wrap narrow"><p class="eyebrow">01 / ABOUT</p><h2>{e(site['about_title'])}</h2>{para(site['about'])}</div></section>
<section id="projects" class="section tint"><div class="wrap"><p class="eyebrow">02 / WORK</p><div class="section-head"><div><h2>Academic projects</h2><p>{len(projects)} projects and studies across manufacturing, systems, quality, and operations.</p></div><label class="search-label">Search projects <input id="search" type="search" placeholder="Try simulation, quality, planning…"></label></div><div class="filters" id="filters">{''.join(f'<button type="button" class="filter {"selected" if c=="All" else ""}" data-filter="{e(c)}">{e(c)}</button>' for c in categories)}</div><div class="project-grid" id="project-grid">{cards}</div><p class="footnote">Some project records are preliminary and marked for verification before public release.</p></div></section>
<section id="journey" class="section"><div class="wrap"><p class="eyebrow">03 / ENGINEERING JOURNEY</p><h2>Learning beyond the classroom.</h2><p>{e(site['journey_intro'])}</p><div class="article-grid">{article_cards or '<p>Articles and learning notes are coming soon.</p>'}</div></div></section>
<section id="contact" class="section dark"><div class="wrap narrow"><p class="eyebrow">04 / CONTACT</p><h2>Let's connect.</h2><p>Interested in production planning, industrial engineering, manufacturing, and continuous improvement.</p><div class="actions">{contacts or '<p>Professional contact details will be added soon.</p>'}</div></div></section>
<script>const q=document.querySelector('#search'),buttons=[...document.querySelectorAll('[data-filter]')],cards=[...document.querySelectorAll('.project-card')];let category='All';function update(){{let term=q.value.trim().toLowerCase();cards.forEach(c=>c.hidden=!(category==='All'||c.dataset.category===category)||!c.dataset.search.includes(term));}}q.addEventListener('input',update);buttons.forEach(b=>b.addEventListener('click',()=>{{category=b.dataset.filter;buttons.forEach(x=>x.classList.toggle('selected',x===b));update();}}));</script>'''
(OUT/'index.html').write_text(layout('Industrial Engineer',body),encoding='utf-8')
(OUT/'.nojekyll').touch()
print(f'Built {len(projects)} project pages and {len(articles)} published article pages in dist/')
