#!/usr/bin/env python3
"""Wrap an Artifact-format fragment (title + style + body markup + script,
no doctype/html/head/body) into a real standalone HTML document for direct
static hosting. Extracts <title> and <style> into <head>, puts everything
else in <body>. Injects the shared site-nav (Home / Whitepaper / Leaderboard)
right after <body> so all three pages carry the same persistent menu."""
import re
import sys

NAV_CSS = '''<style>
.site-nav {
  position: sticky; top: 0; z-index: 200;
  background: rgba(20,17,15,0.94); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.site-nav-inner {
  max-width: 1080px; margin: 0 auto; padding: 14px 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
}
.site-nav-brand {
  font-family: var(--serif); font-size: 1rem; color: var(--gold);
  text-decoration: none; font-weight: 600; white-space: nowrap;
}
.site-nav-links { display: flex; gap: 24px; }
.site-nav-links a {
  font-family: var(--mono); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.06em;
  color: var(--text-muted); text-decoration: none; transition: color 0.15s; white-space: nowrap;
}
.site-nav-links a:hover { color: var(--gold); }
.site-nav-links a.is-active { color: var(--gold); border-bottom: 1px solid var(--gold); padding-bottom: 2px; }
@media (max-width: 560px) {
  .site-nav-inner { padding: 12px 16px; }
  .site-nav-links { gap: 14px; }
  .site-nav-brand { font-size: 0.88rem; }
  .site-nav-links a { font-size: 0.68rem; }
}
</style>
'''

def nav_html(active):
    def cls(page):
        return ' class="is-active"' if page == active else ""
    return f'''<nav class="site-nav">
    <div class="site-nav-inner">
      <a class="site-nav-brand" href="landing.html">The Eureka Engine</a>
      <div class="site-nav-links">
        <a href="landing.html"{cls("landing")}>Home</a>
        <a href="whitepaper.html"{cls("whitepaper")}>Whitepaper</a>
        <a href="leaderboard.html"{cls("leaderboard")}>Leaderboard</a>
      </div>
    </div>
  </nav>
  '''

def wrap(fragment_path, out_path, nav_active=None, extra_head=""):
    with open(fragment_path, "r", encoding="utf-8") as f:
        content = f.read()

    title_match = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    title = title_match.group(1) if title_match else "Eureka Engine"
    content_no_title = content[:title_match.start()] + content[title_match.end():] if title_match else content

    style_blocks = re.findall(r"<style>.*?</style>", content_no_title, re.DOTALL)
    body_content = re.sub(r"<style>.*?</style>", "", content_no_title, flags=re.DOTALL).strip()

    styles = "\n".join(style_blocks)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<title>{title}</title>
{extra_head}
{styles}
{NAV_CSS if nav_active else ""}
</head>
<body>
{nav_html(nav_active) if nav_active else ""}{body_content}
</body>
</html>
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_path} ({len(html)/1024:.1f} KB), title={title!r}, nav_active={nav_active!r}")

if __name__ == "__main__":
    active = sys.argv[3] if len(sys.argv) > 3 else None
    wrap(sys.argv[1], sys.argv[2], nav_active=active)
