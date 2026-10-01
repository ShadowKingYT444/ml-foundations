#!/usr/bin/env python3
"""Build a static GitHub-Pages-ready site from _concepts/*.md.

Output: index.html + concepts/<id>.html, one concept per day starting 2026-10-01,
ordered by relevance (how directly the idea powers modern harness work).
"""
import os, re, html, json
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "_concepts")
OUT = ROOT
CONCEPTS_OUT = os.path.join(OUT, "concepts")
START = date(2026, 10, 1)

def md_inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s

def md_block(text):
    out, para, in_list = [], [], False
    def flush_para():
        if para:
            out.append("<p>" + " ".join(md_inline(l) for l in para) + "</p>")
            para.clear()
    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False
    for line in text.split("\n"):
        line = line.rstrip()
        if not line.strip():
            flush_para(); close_list(); continue
        m = re.match(r"^#{2,3}\s+(.*)", line)
        if m:
            flush_para(); close_list()
            lvl = 2 if line.startswith("## ") else 3
            out.append(f"<h{lvl}>{md_inline(m.group(1))}</h{lvl}>")
            continue
        if re.match(r"^[-*]\s+", line):
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append("<li>" + md_inline(re.sub(r"^[-*]\s+", "", line)) + "</li>")
            continue
        if re.match(r"^\d+\.\s+", line):
            flush_para()
            out.append("<p class='num'>" + md_inline(line) + "</p>")
            continue
        para.append(line)
    flush_para(); close_list()
    return "\n".join(out)

def parse(path):
    raw = open(path, encoding="utf-8").read()
    fm, body = {}, raw
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        body = m.group(2)
    return fm, body

concepts = []
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".md"):
        continue
    fm, body = parse(os.path.join(SRC, fn))
    concepts.append({
        "id": fm.get("concept_id", fn[:-3]),
        "title": fm.get("title", fn[:-3]),
        "origin": fm.get("origin", ""),
        "field": fm.get("field", ""),
        "adaptation": fm.get("modern_adaptation", ""),
        "url": fm.get("source_url", ""),
        "relevance": int(fm.get("relevance", "1")),
        "body": body,
    })

SCHED_PATH = os.path.join(OUT, "schedule.json")
sched = {}
if os.path.exists(SCHED_PATH):
    try:
        sched = json.load(open(SCHED_PATH))
    except Exception:
        sched = {}
known = {c["id"] for c in concepts}
sched = {k: v for k, v in sched.items() if k in known}
next_day = max(sched.values()) + 1 if sched else 1
new_ones = sorted([c for c in concepts if c["id"] not in sched],
                  key=lambda c: (-c["relevance"], c["title"]))
for c in new_ones:
    sched[c["id"]] = next_day
    next_day += 1
json.dump(sched, open(SCHED_PATH, "w"), indent=1)
concepts.sort(key=lambda c: sched[c["id"]])
for c in concepts:
    c["day"] = sched[c["id"]]
    c["date"] = START + timedelta(days=c["day"] - 1)

os.makedirs(CONCEPTS_OUT, exist_ok=True)

STYLE = """
:root { --bg:#0d1117; --panel:#161b22; --border:#30363d; --fg:#e6edf3; --muted:#8b949e;
        --accent:#58a6ff; --accent2:#3fb950; --warn:#d29922; }
* { box-sizing:border-box; }
body { background:var(--bg); color:var(--fg); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
       margin:0; line-height:1.65; }
a { color:var(--accent); text-decoration:none; } a:hover { text-decoration:underline; }
.wrap { max-width:860px; margin:0 auto; padding:0 20px 60px; }
header.site { border-bottom:1px solid var(--border); padding:28px 0 18px; margin-bottom:28px; }
header.site .brand { font-size:15px; color:var(--muted); letter-spacing:.12em; text-transform:uppercase; }
header.site h1 { margin:8px 0 4px; font-size:30px; }
header.site p { color:var(--muted); margin:6px 0 0; max-width:640px; }
.card { background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:20px 22px; margin:16px 0; }
.card.today { border-color:var(--accent2); }
.badge { display:inline-block; font-size:12px; font-weight:600; padding:2px 10px; border-radius:20px;
         border:1px solid var(--border); color:var(--muted); margin-right:8px; }
.badge.rel5 { color:#f778ba; border-color:#f778ba55; } .badge.rel4 { color:#ffa657; border-color:#ffa65755; }
.badge.rel3 { color:var(--accent); border-color:#58a6ff55; } .badge.rel2,.badge.rel1 { color:var(--muted); }
.meta { color:var(--muted); font-size:14px; }
h2 { margin-top:34px; font-size:22px; border-bottom:1px solid var(--border); padding-bottom:8px; }
h3 { font-size:17px; margin-top:26px; color:var(--accent); }
code { background:#0d1117; border:1px solid var(--border); border-radius:6px; padding:1px 6px; font-size:13px; }
pre code { display:block; padding:14px; overflow-x:auto; }
table.sched { width:100%; border-collapse:collapse; font-size:14px; }
table.sched th, table.sched td { text-align:left; padding:9px 10px; border-bottom:1px solid var(--border); }
table.sched tr.today td { background:#3fb95014; }
table.sched tr.past td { color:var(--muted); }
.nav { display:flex; justify-content:space-between; margin-top:34px; padding-top:18px; border-top:1px solid var(--border); }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:12px; }
.grid .card { margin:0; padding:14px 16px; } .grid .card h4 { margin:0 0 6px; font-size:15px; }
.grid .card .meta { font-size:12.5px; }
footer { margin-top:50px; color:var(--muted); font-size:13px; border-top:1px solid var(--border); padding-top:16px; }
.kicker { color:var(--accent2); font-size:13px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }
"""

def page(title, body_html):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — ML Foundations</title>
<style>{STYLE}</style></head>
<body><div class="wrap">
<header class="site">
<div class="brand"><a href="../index.html" style="color:inherit">ML Foundations</a></div>
<h1>{html.escape(title)}</h1>
</header>
{body_html}
<footer>Study notes on the foundational ideas of statistics and machine learning —
and the modern work (TextGrad, RRSI, PluginRSI, …) that adapts them. Not affiliated
with any authors. Source links point to public references.</footer>
</div></body></html>"""

def rel_badge(r):
    labels = {5: "core idea", 4: "highly relevant", 3: "relevant", 2: "context", 1: "background"}
    return f'<span class="badge rel{r}">{labels.get(r,"")}</span>'

for i, c in enumerate(concepts):
    prev_l = f'<a href="{concepts[i-1]["id"]}.html">← Day {concepts[i-1]["day"]}: {html.escape(concepts[i-1]["title"][:60])}</a>' if i > 0 else ""
    next_l = f'<a href="{concepts[i+1]["id"]}.html">Day {concepts[i+1]["day"]}: {html.escape(concepts[i+1]["title"][:60])} →</a>' if i < len(concepts)-1 else ""
    src_l = f' · <a href="{c["url"]}">reference</a>' if c["url"] else ""
    adapt_l = f'<p><span class="badge">modern adaptation: {html.escape(c["adaptation"])}</span></p>' if c["adaptation"] else ""
    body = f"""
<div class="kicker">Day {c['day']} · {c['date'].strftime('%b %d, %Y')}</div>
<h1 style="margin-top:6px">{html.escape(c['title'])}</h1>
<p class="meta">{html.escape(c['origin'])}{src_l} · {html.escape(c['field'])}</p>
<p>{rel_badge(c['relevance'])}</p>
{adapt_l}
<div class="card">{md_block(c['body'])}</div>
<div class="nav"><span>{prev_l}</span><span><a href="../index.html">All concepts</a></span><span>{next_l}</span></div>
"""
    open(os.path.join(CONCEPTS_OUT, c["id"] + ".html"), "w", encoding="utf-8").write(page(c["title"], body))

sched_rows = []
for c in concepts:
    cls = ""
    if c["date"] == date.today():
        cls = "today"
    elif c["date"] < date.today():
        cls = "past"
    sched_rows.append(
        f'<tr class="{cls}"><td><strong>Day {c["day"]}</strong></td>'
        f'<td>{c["date"].strftime("%a %b %d")}</td>'
        f'<td><a href="concepts/{c["id"]}.html">{html.escape(c["title"])}</a></td>'
        f'<td>{rel_badge(c["relevance"])}</td></tr>')

first = concepts[0]
hero = f"""
<div class="card today">
<div class="kicker">Start here — Day 1 · {first['date'].strftime('%b %d, %Y')}</div>
<h3 style="margin:8px 0"><a href="concepts/{first['id']}.html">{html.escape(first['title'])}</a></h3>
<p class="meta">{html.escape(first['origin'])} · {html.escape(first['field'])}</p>
<p>{rel_badge(first['relevance'])}</p>
</div>"""

grid = "\n".join(
    f'<div class="card"><h4><a href="concepts/{c["id"]}.html">{html.escape(c["title"])}</a></h4>'
    f'<p class="meta">Day {c["day"]} · {html.escape(c["field"])}</p>'
    f'<p>{rel_badge(c["relevance"])}</p></div>' for c in concepts)

index_body = f"""
<p>Foundational ideas from statistics and machine learning — the roots that modern
agent-harness work keeps rediscovering. TextGrad is textual backprop. RRSI is recursion
with a fixed-point flavor. PluginRSI is evolution over modules. VACE is EM alternation.
Each deep-dive explains the original idea from first principles, then shows exactly
which modern technique is its descendant and what got adapted along the way.</p>
{hero}
<h2>Reading schedule</h2>
<table class="sched"><tr><th>Day</th><th>Date</th><th>Concept</th><th>Relevance</th></tr>
{''.join(sched_rows)}
</table>
<h2>Browse all concepts</h2>
<div class="grid">{grid}</div>
"""
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
    page("ML Foundations", index_body).replace('../index.html', 'index.html'))

print(f"built {len(concepts)} concept pages + index -> {OUT}")
