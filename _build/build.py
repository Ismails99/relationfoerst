"""Bygger RelationFørst-siderne ud fra _build/kilde.html.

Ret indhold i kilde.html (én lang side med sektioner) og kør:
    python3 _build/build.py
Så genereres index.html (én lang side med alle sektioner), sitemap.xml og llms.txt.
De gamle undersider sendes videre til ankre på forsiden via vercel.json.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "_build" / "kilde.html").read_text()
BASE = "https://www.relationfoerst.dk"
TODAY = "2026-11-20"
NAME = "RelationFørst"


def section(sid):
    m = re.search(r'(<section id="%s"[^>]*>.*?</section>)' % sid, SRC, re.S)
    return m.group(1)


def hero():
    return re.search(r'(<section class="hero">.*?</section>)', SRC, re.S).group(1)


def script():
    return re.search(r"(<script>\s*\(function\(\)\{.*?</script>)", SRC, re.S).group(1)


def promote(html):
    """Første h2 bliver sidens h1, og interne ankre peger på undersider."""
    html = html.replace('style="padding-top:0"', "", 1)
    html = re.sub(r"<h2>(.*?)</h2>", r'<h1 class="h2">\1</h1>', html, count=1)
    return html


def fix_links(html):
    return html



NAV = [("#forloeb", "Forløb"), ("#erfaring", "Erfaring"), ("#tilgang", "Tilgang"),
       ("#om-os", "Om os"), ("#kontakt", "Kontakt")]

DESC_HOME = ("RelationFørst (relationfoerst.dk) tilbyder pædagogiske forløb, mentor- og "
             "kontaktpersonforløb til børn og unge i udsatte positioner på Sjælland.")

ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": BASE + "/#organisation",
    "name": NAME,
    "alternateName": ["Relation Først", "RelationFoerst", "relationfoerst.dk"],
    "url": BASE + "/",
    "logo": BASE + "/apple-touch-icon.png",
    "email": "kontakt@relationfoerst.dk",
    "description": DESC_HOME,
    "areaServed": {"@type": "AdministrativeArea", "name": "Sjælland"},
    "knowsAbout": ["Pædagogiske forløb", "Mentorforløb", "Kontaktpersonforløb", "Udsatte unge",
                   "Unge i krise", "ADHD", "Low arousal", "Relationsarbejde"],
    "founder": [{"@type": "Person", "name": "Ismail Selek"},
                {"@type": "Person", "name": "Joshua Kabagarama"}],
}
WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": NAME,
    "alternateName": ["Relation Først", "relationfoerst.dk"],
    "url": BASE + "/",
}



def jsonld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=2)


def breadcrumb(path, label):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Forside", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": BASE + path},
        ],
    }


def page(path, title, desc, body, extra_ld=(), with_script=False):
    url = BASE + path
    nav = "\n".join(
        '      <li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == path else "", t)
        for h, t in NAV)
    foot_nav = "\n".join('        <li><a href="%s">%s</a></li>' % (h, t) for h, t in [("#top", "Til toppen")] + NAV)
    ld = "\n".join(jsonld(x) for x in extra_ld)
    return f"""<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#1d6b62">
<meta property="og:type" content="website">
<meta property="og:locale" content="da_DK">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{ld}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/styles.css">
</head>
<body>

<header>
  <div class="wrap nav">
    <a class="logo" href="/" aria-label="{NAME}, forside">
      <svg width="34" height="22" viewBox="0 0 34 22" aria-hidden="true"><circle cx="11" cy="11" r="8" fill="none" stroke="var(--primary)" stroke-width="3"/><circle cx="23" cy="11" r="8" fill="none" stroke="var(--sun)" stroke-width="3"/></svg>
      <span>relation<b>først</b></span>
    </a>
    <nav aria-label="Hovedmenu"><ul>
{nav}
    </ul></nav>
  </div>
</header>

<main id="top">
{body}
</main>

<footer>
  <div class="wrap">
    <nav aria-label="Sidefod"><ul class="foot-nav">
{foot_nav}
    </ul></nav>
    <div class="foot-row">
      <span><strong>{NAME}</strong> · relationfoerst.dk · kontakt@relationfoerst.dk · Pædagogiske forløb på Sjælland</span>
      <span>CVR <span class="ph">indsættes</span></span>
    </div>
  </div>
</footer>
{script() if with_script else ""}
</body>
</html>
"""


def write(path, html):
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)


# ---------- Én lang side ----------
om_os = section("om-os").replace("<h2>Relation Først</h2>", "<h2>Om RelationFørst</h2>")
om_os = re.sub(r'(<div class="about-text">.*?<h2>.*?</h2>).*?(</div>)', lambda m: m.group(1) + """
        <p>RelationFørst er en pædagogisk organisation på Sjælland, stiftet af Ismail Selek og Joshua Kabagarama. Vi tilbyder forløb til børn, unge og voksne i udsatte positioner, blandt andet mentorforløb, kontaktpersonforløb, 1:1- og 2:1-indsatser og hjælp til unge i krise.</p>
        <p>Vi samarbejder med kommuner, sagsbehandlere og organisationer, og vi inddrager familien, når det giver mening. Vi løser også vikaropgaver efter aftale, men vores fokus er forløb.</p>
      """ + m.group(2), om_os, count=1, flags=re.S)

body = "\n\n".join([hero(), section("forloeb"), section("erfaring"), section("tilgang"),
                      om_os, section("kontakt")])
write("/", page("/", "RelationFørst - Pædagogiske forløb", DESC_HOME, body,
                extra_ld=[ORG, WEBSITE], with_script=True))

# ---------- sitemap.xml ----------
urls = ["/"]
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n" % (BASE, u, TODAY) for u in urls)
    + "</urlset>\n")

# ---------- llms.txt ----------
(ROOT / "llms.txt").write_text(f"""# RelationFørst

> RelationFørst (relationfoerst.dk) er en pædagogisk organisation på Sjælland, stiftet af Ismail Selek og Joshua Kabagarama. Vi tilbyder pædagogiske forløb til børn, unge og voksne i udsatte positioner og samarbejder med kommuner og organisationer.

RelationFørst må ikke forveksles med RelationerFørst (relationerfoerst.dk) i Randers, som er en anden organisation.

- Område: Sjælland
- Kontakt: kontakt@relationfoerst.dk
- Tilgang: low arousal og relationsarbejde
- Vikaropgaver løses efter aftale, men hovedfokus er forløb

## Indhold på {BASE}/

- [Forløb]({BASE}/#forloeb): Mentorforløb, kontaktpersonforløb, 1:1- og 2:1-indsatser, unge i krise, ADHD, familier der ikke taler dansk
- [Erfaring]({BASE}/#erfaring): Sikrede institutioner, gadeplan, folkeskole, bosteder
- [Tilgang]({BASE}/#tilgang): Low arousal, relationsarbejde, at møde unge på bølgelængde
- [Om os]({BASE}/#om-os): Hvem vi er og stifterne
- [Kontakt]({BASE}/#kontakt): Kontaktformular og mail
""")

print("Bygget:", ", ".join(urls))
