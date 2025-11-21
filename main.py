import streamlit as st
from jinja2 import Template
from PIL import Image
import io, zipfile, os, uuid

st.set_page_config(page_title="Portfolio Maker Demo", layout="wide")

# ------------------------
# Templates (simple demo)
# ------------------------

GLASS_CSS = """
/* glassmorphism theme - demo */
:root{
  --bg: linear-gradient(135deg,#f6f9ff 0%, #eef2ff 100%);
  --glass: rgba(255,255,255,0.55);
  --accent: linear-gradient(90deg,#7aa2ff,#b98bff);
  --text: #0b1226;
}
*{box-sizing:border-box}
body{font-family:Inter,system-ui,Arial;background:var(--bg);color:var(--text);margin:0;padding:0}
.container{max-width:1000px;margin:32px auto;padding:32px}
.hero{backdrop-filter: blur(8px); background: var(--glass); border-radius:16px; padding:28px; box-shadow:0 8px 30px rgba(16,24,40,0.08); display:flex; gap:20px; align-items:center}
.profile-pic{width:120px;height:120px;border-radius:16px;object-fit:cover;border:3px solid rgba(255,255,255,0.6)}
.title{font-size:28px;margin:0}
.tagline{color:#334155;margin-top:8px}
.section{margin-top:22px;padding:18px;background:rgba(255,255,255,0.35);border-radius:12px}
.projects{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:12px}
.card{padding:14px;border-radius:12px;background:linear-gradient(180deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15));box-shadow: inset 0 1px 0 rgba(255,255,255,0.6); min-height:130px}
.kpi{display:inline-block;padding:8px 12px;border-radius:999px;background:linear-gradient(90deg,#ffffff88, #ffffff66);font-weight:600}
.footer{margin-top:24px;color:#475569;font-size:14px}
"""

GLASS_JS = """
// small JS for demo - typewriter effect
document.addEventListener('DOMContentLoaded', function(){
  const el = document.querySelector('.typed');
  if(!el) return;
  const txt = el.dataset.text || '';
  let i=0;
  function step(){
    el.innerText = txt.slice(0,i);
    i++;
    if(i<=txt.length) setTimeout(step, 30);
  }
  step();
});
"""

DARK_CSS = """
/* dark theme - demo */
:root{--bg:#0f1724;--card:#0b1226;--accent:#5eead4;--muted:#94a3b8;--text:#e6eef8}
body{font-family:Inter, system-ui, Arial;margin:0;background:var(--bg);color:var(--text)}
.container{max-width:1000px;margin:32px auto;padding:32px}
.hero{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); padding:28px;border-radius:12px;display:flex;gap:18px;align-items:center;box-shadow:0 6px 18px rgba(2,6,23,0.6)}
.profile-pic{width:110px;height:110px;border-radius:12px;object-fit:cover;border:2px solid rgba(255,255,255,0.04)}
.title{font-size:26px;margin:0}
.tagline{color:var(--muted);margin-top:8px}
.section{margin-top:18px;padding:18px;background:transparent;border:1px solid rgba(255,255,255,0.03);border-radius:10px}
.projects{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:12px}
.card{padding:12px;border-radius:10px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));min-height:120px}
.footer{margin-top:20px;color:var(--muted);font-size:13px}
"""

DARK_JS = """
// tiny interaction for dark theme
document.addEventListener('click', function(e){
  if(e.target.matches('.card a')) alert('This is a demo exported portfolio (link placeholder)');
});
"""

TEMPLATE_HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{{ name }} — Portfolio</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
{{ css }}
</style>
</head>
<body>
  <div class="container">
    <header class="hero">
      {% if photo %}<img class="profile-pic" src="assets/{{ photo }}" alt="photo" />{% endif %}
      <div>
        <h1 class="title">{{ name }}</h1>
        <div class="tagline"><span class="typed" data-text="{{ headline }}">{{ headline }}</span></div>
        <div style="margin-top:10px">
          <span class="kpi">Email: {{ email }}</span>
          {% if website %} <span class="kpi">Website: {{ website }}</span>{% endif %}
        </div>
      </div>
    </header>

    <section class="section about">
      <h2>About</h2>
      <p>{{ bio }}</p>
    </section>

    <section class="section projects">
      <h2>Projects</h2>
      <div class="projects">
        {% for p in projects %}
        <article class="card">
          <h3><a href="{{ p.url }}" target="_blank">{{ p.title }}</a></h3>
          <p>{{ p.description }}</p>
        </article>
        {% endfor %}
      </div>
    </section>

    <footer class="footer">
      Generated with Portfolio Maker Demo
    </footer>
  </div>

<script>
{{ js }}
</script>
</body>
</html>
"""

# ------------------------
# Helper functions
# ------------------------

def render_html(name, headline, bio, email, website, projects, photo_filename, theme):
    css = GLASS_CSS if theme == "Glassmorphism" else DARK_CSS
    js = GLASS_JS if theme == "Glassmorphism" else DARK_JS
    tmpl = Template(TEMPLATE_HTML)
    return tmpl.render(
        name=name,
        headline=headline,
        bio=bio,
        email=email,
        website=website,
        projects=projects,
        photo=photo_filename,
        css=css,
        js=js
    )

def make_zip_bytes(site_name, index_html, css_text, js_text, assets):
    """
    assets: list of tuples (filename, bytes)
    returns BytesIO of zip
    """
    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        # index.html
        z.writestr(f"{site_name}/index.html", index_html)
        # css & js
        z.writestr(f"{site_name}/style.css", css_text)
        z.writestr(f"{site_name}/script.js", js_text)
        # assets folder
        for fname, b in assets:
            z.writestr(f"{site_name}/assets/{fname}", b)
        # simple README
        readme = f"# {site_name}\n\nExported from Portfolio Maker Demo.\n\nTo deploy: push this folder to GitHub and enable GitHub Pages, or upload to Netlify/Vercel."
        z.writestr(f"{site_name}/README.md", readme)
    mem.seek(0)
    return mem

# ------------------------
# Streamlit UI
# ------------------------

st.title("Portfolio Maker — Demo (Glassmorphism & Dark)")

col1, col2 = st.columns([2,1])
with col1:
    st.subheader("Profile info")
    name = st.text_input("Full name", value="Swagato Bhattacharya")
    headline = st.text_input("Headline / Tagline", value="Product engineer • Portfolio maker demo")
    email = st.text_input("Email", value="you@example.com")
    website = st.text_input("Website (optional)", value="")
    bio = st.text_area("Short bio", value="I build clean frontend experiences and data products. This demo exports a ready-to-deploy static portfolio site.")
    st.markdown("**Projects (add up to 4)**")
    projects = []
    for i in range(1,5):
        t = st.text_input(f"Project {i} title", key=f"pt{i}")
        d = st.text_area(f"Project {i} description", key=f"pd{i}", height=60)
        u = st.text_input(f"Project {i} url", key=f"pu{i}")
        if t:
            projects.append({"title": t, "description": d, "url": u or "#"})
    st.markdown("---")
    uploaded_photo = st.file_uploader("Profile photo (optional)", type=["png","jpg","jpeg"])
    theme = st.selectbox("Choose theme", ["Glassmorphism", "Dark"])
    if st.button("Generate & Preview"):
        # Save uploaded photo to memory with a deterministic filename
        assets = []
        photo_filename = ""
        if uploaded_photo:
            ext = uploaded_photo.name.split(".")[-1]
            photo_filename = f"profile_{uuid.uuid4().hex[:6]}.{ext}"
            img_bytes = uploaded_photo.read()
            assets.append((photo_filename, img_bytes))
        # render HTML
        html = render_html(name=name, headline=headline, bio=bio, email=email, website=website, projects=projects, photo_filename=photo_filename, theme=theme)
        # show preview using components.html
        st.subheader("Live preview")
        st.components.v1.html(html, height=700, scrolling=True)

        # Create zip for download
        css_text = GLASS_CSS if theme == "Glassmorphism" else DARK_CSS
        js_text = GLASS_JS if theme == "Glassmorphism" else DARK_JS
        zip_name = f"{name.lower().replace(' ','_')}_portfolio_demo"
        mem = make_zip_bytes(zip_name, html, css_text, js_text, assets)
        st.markdown("### Downloadable export")
        st.download_button("Download ZIP (exported site)", data=mem, file_name=f"{zip_name}.zip", mime="application/zip")

with col2:
    st.subheader("Quick instructions")
    st.markdown("""
- Fill name, bio, and projects.
- Choose **Glassmorphism** or **Dark** theme and click **Generate & Preview**.
- Click **Download ZIP** to get the ready-to-deploy website folder.
- Deployment options:
  - GitHub Pages (push folder to repo → enable Pages)
  - Netlify / Vercel (drag-and-drop or connect repo)
""")
    st.markdown("### What this demo includes")
    st.markdown("- Generates static `index.html`, `style.css`, `script.js`, and assets")
    st.markdown("- Glassmorphism theme with blur and frosted cards")
    st.markdown("- Dark theme with subtle animations (demo)")
    st.markdown("---")
    st.info("This is a minimal demo. For production features you can add: theme editor, multiple pages, custom fonts, contact form integration, and SQLite/profile saving.")

st.markdown("---")
st.caption("Demo app — Portfolio Maker. This is a compact proof-of-concept to check generated HTML/CSS/JS output.")
