# -*- coding: utf-8 -*-
"""Générateur du site leadr.ch v2. Lancer : python3 build.py  -> dossier dist/"""
import os, shutil, html, json, re

OUT = 'dist'
EMAIL = 'lrohmer@leadr.ch'
LINKEDIN = 'https://www.linkedin.com/in/lucrohmer/'
WA = 'https://wa.me/41766504264?text=Bonjour%20Luc%2C%20je%20viens%20du%20site%20leadr.ch.'
_IC = json.load(open('parts/icons.json'))
WA_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="' + _IC['wa'] + '"/></svg>'
LI_ICON = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="' + _IC['li'] + '"/></svg>'
def SOCIAL(cls=''):
    return (f'<div class="social {cls}"><a class="soc soc-li" href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn">{LI_ICON}</a>'
            f'<a class="soc soc-wa" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp" title="WhatsApp">{WA_ICON}</a></div>')
BOOK = 'https://cal.com/lrohmer/meeting'      # Agenda en ligne de Luc
FORM_URL = 'https://formsubmit.co/ajax/' + EMAIL   # FormSubmit : envoi des messages vers la boîte de Luc
LOGO, LOGO_W = 'logo.png', 'logo-blanc.png'     # Remplaçables par les vrais fichiers

NAV = [('vers-la-suisse.html', 'Vers la Suisse'), ('vers-la-france.html', 'Vers la France'),
       ('entre-regions-suisses.html', 'Entre régions suisses')]
SERVICES = [('methode.html', 'Notre méthode'), ('premier-rendez-vous.html', 'Premier rendez-vous'),
            ('implantation.html', 'Implantation'), ('relocalisation.html', 'Relocalisation'),
            ('management-transition.html', 'Management de transition')]
CHEV = '<svg class="chev" viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

e = lambda s: s  # textes déjà maîtrisés (HTML autorisé dans les contenus)

# ------------------------------------------------------------------ gabarit
ORG_LD = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Leadr GmbH", "url": "https://www.leadr.ch/",
  "logo": "https://www.leadr.ch/logo.png", "email": EMAIL, "telephone": "+41 76 650 42 64",
  "address": {"@type": "PostalAddress", "streetAddress": "Sternengasse 6", "postalCode": "4051", "addressLocality": "Bâle", "addressCountry": "CH"},
  "employee": {"@type": "Person", "name": "Luc Rohmer", "jobTitle": "CEO", "sameAs": [LINKEDIN]}, "areaServed": ["CH", "FR"],
  "knowsAbout": ["Prospection commerciale externalisée", "Implantation en Suisse", "Développement commercial en France", "Management de transition", "Relocalisation d'entreprise"],
  "description": "Société suisse, antenne des entreprises françaises et suisses sur leur nouveau marché : renseignement, adaptation de l'offre, mise en relation ciblée."}, ensure_ascii=False)

def head(title, desc, slug):
    return f'''<!doctype html>
<html lang="fr" translate="no" class="notranslate">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google" content="notranslate">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.leadr.ch/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="627">
<meta property="og:locale" content="fr_CH">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1D1D1F">
<script type="application/ld+json">{ORG_LD}</script>
<meta property="og:url" content="https://www.leadr.ch/{'' if slug=='index.html' else slug}">
<link rel="canonical" href="https://www.leadr.ch/{'' if slug=='index.html' else slug}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/style.css">
<script src="js/main.js" defer></script>
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''

def header(slug):
    cur = ' aria-current="page"'
    links = ''.join(f'<li><a href="{h}"{cur if h==slug else ""}>{l}</a></li>' for h, l in NAV)
    in_srv = any(h == slug for h, _ in SERVICES)
    sub = ''.join(f'<li><a href="{h}"{cur if h==slug else ""}>{l}</a></li>' for h, l in SERVICES)
    links += (f'<li class="has-dd{" is-cur" if in_srv else ""}"><button class="dd-btn" type="button" aria-expanded="false" aria-controls="dd-services">Services{CHEV}</button>'
              f'<ul class="dd" id="dd-services">{sub}</ul></li>')
    links += f'<li><a href="contact.html"{cur if slug=="contact.html" else ""}>Contact</a></li>'
    links += f'<li class="nav-extra"><a href="leadr.html"{cur if slug=="leadr.html" else ""}>Qui sommes-nous</a></li>'
    return f'''<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="index.html" aria-label="Leadr, accueil"><img src="{LOGO}" alt="Leadr" width="146" height="30"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="nav" class="nav" aria-label="Navigation principale">
      <ul>{links}</ul>
      <!--LANG-->
      <a class="btn btn-red btn-sm" href="contact.html">Prendre rendez-vous</a>
    </nav>
  </div>
</header>
<main id="contenu">
'''

FOOT = f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <img src="{LOGO_W}" alt="Leadr" width="146" height="30">
        <p>Votre antenne entre la France et la Suisse, et d'une région suisse à l'autre.</p>
        <p class="foot-addr">Leadr GmbH, Sternengasse 6, 4051 Bâle, Suisse<br><a href="tel:+41766504264">+41 76 650 42 64</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>{SOCIAL("social-foot")}
      </div>
      <div><h2>Directions</h2><ul>
        <li><a href="vers-la-suisse.html">Vers la Suisse</a></li><li><a href="vers-la-france.html">Vers la France</a></li><li><a href="entre-regions-suisses.html">Entre régions suisses</a></li></ul></div>
      <div><h2>Services</h2><ul>
        <li><a href="methode.html">Méthode</a></li><li><a href="premier-rendez-vous.html">Premier rendez-vous</a></li><li><a href="implantation.html">Implantation</a></li><li><a href="relocalisation.html">Relocalisation</a></li><li><a href="management-transition.html">Management de transition</a></li></ul></div>
      <div><h2>Leadr</h2><ul>
        <li><a href="leadr.html">Qui sommes-nous</a></li><li><a href="cas-clients.html">Cas clients</a></li><li><a href="reperes.html">Repères</a></li><li><a href="contact.html">Prendre rendez-vous</a></li><li><a href="contact.html#formulaire">Nous écrire</a></li></ul></div>
    </div>
    <div class="foot-bottom"><span>© 2026 Leadr GmbH</span><a href="mentions-legales.html">Mentions légales et confidentialité</a></div>
  </div>
</footer>
<div class="mbar" aria-hidden="true"><a class="btn btn-red" href="contact.html" tabindex="-1">Prendre rendez-vous</a><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener" tabindex="-1" aria-label="WhatsApp">{WA_ICON}</a></div>
</body>
</html>
'''

# ------------------------------------------------------------------ blocs
def kicker(k):
    return f'<p class="kicker">{k}</p>' if k else ''

def btns(bs):
    if not bs: return ''
    h = ''
    for i, (href, label) in enumerate(bs):
        ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
        h += f'<a class="btn {"btn-red" if i==0 else "btn-line"}" href="{href}"{ext}>{label}</a>'
    return f'<div class="actions">{h}</div>'

MAP = '''<figure class="map" aria-label="Trois directions : de la France vers la Suisse, de la Suisse vers la France, et entre Suisse romande et Suisse alémanique">
<svg viewBox="0 0 620 430" role="img">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#E8192C"/></marker>
  </defs>
  <path class="land" d="M178 46 L312 104 L332 232 L272 368 L118 382 L36 262 L70 118 Z"/>
  <path class="land ch-w" d="M362 236 L392 196 L440 182 L466 170 L458 236 L452 292 L440 290 L410 296 L376 270 Z"/>
  <path class="land ch-e" d="M466 170 L520 160 L560 168 L604 196 L594 236 L558 250 L542 290 L502 278 L472 300 L452 292 L458 236 Z"/>
  <path class="sarine" d="M466 170 L458 236 L452 292"/>
  <path class="arrow a1" marker-end="url(#ah)" d="M262 112 C 316 60, 386 80, 408 176"/>
  <path class="arrow a2" marker-end="url(#ah)" d="M412 318 C 384 382, 318 380, 300 334"/>
  <path class="arrow a3" marker-start="url(#ah)" marker-end="url(#ah)" d="M446 156 C 478 104, 532 104, 556 146"/>
  <text x="140" y="236" class="lbl">France</text>
  <text x="382" y="238" class="lbl sm">Suisse</text><text x="382" y="256" class="lbl sm">romande</text>
  <text x="484" y="222" class="lbl sm">Suisse</text><text x="484" y="240" class="lbl sm">alémanique</text>
</svg>
</figure>'''

def hero(k, title, text, bs=None, map_=False, small=False):
    cls = 'hero hero-home' if map_ else ('hero hero-sm' if small else 'hero')
    side = MAP if map_ else ''
    return f'''<section class="{cls}"><div class="wrap hero-grid">
  <div class="hero-txt">{kicker(k)}<h1>{title}</h1><p class="lead">{text}</p>{btns(bs)}</div>{side}
</div></section>'''

def rows(k, title, items, intro='', tone='', note=''):
    lis = ''.join(f'<div class="row"><h3>{t}</h3><p>{d}</p></div>' for t, d in items)
    intro_h = f'<p class="intro">{intro}</p>' if intro else ''
    note_h = f'<p class="note">{note}</p>' if note else ''
    return f'''<section class="sec {tone}"><div class="wrap split">
  <div class="split-head">{kicker(k)}<h2>{title}</h2>{intro_h}</div>
  <div class="split-body rows">{lis}{note_h}</div>
</div></section>'''

def steps(k, title, items, intro='', tone=''):
    lis = ''.join(f'<li><span class="n">{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items))
    intro_h = f'<p class="intro">{intro}</p>' if intro else ''
    return f'''<section class="sec {tone}"><div class="wrap">
  {kicker(k)}<h2 class="w-narrow">{title}</h2>{intro_h}<ol class="steps">{lis}</ol>
</div></section>'''

def statement(text, sub='', who='', cls=''):
    s = f'<p class="st-sub">{sub}</p>' if sub else ''
    w = f'<p class="st-who">{who}</p>' if who else ''
    return f'''<section class="sec statement{' ' + cls if cls else ''}"><div class="wrap"><p class="st">{text}</p>{s}{w}</div></section>'''

def cols(k, title, items, intro='', tone=''):
    cs = ''
    for it in items:
        t, d = it[0], it[1]
        link = it[2] if len(it) > 2 else None
        if link:
            cs += f'<a class="col col-link" href="{link}"><h3>{t}</h3><p>{d}</p><span class="more">{it[3] if len(it)>3 else "En savoir plus"}</span></a>'
        else:
            cs += f'<div class="col"><h3>{t}</h3><p>{d}</p></div>'
    intro_h = f'<p class="intro">{intro}</p>' if intro else ''
    return f'''<section class="sec {tone}"><div class="wrap">
  {kicker(k)}<h2 class="w-narrow">{title}</h2>{intro_h}<div class="cols n{len(items)}">{cs}</div>
</div></section>'''

def directions():
    items = [
        ('vers-la-suisse.html', 'De la France vers la Suisse', 'Vous dirigez une entreprise française et la Suisse fait partie de vos ambitions. Nous identifions les bons cantons, les bons interlocuteurs et la bonne façon de les approcher.', 'fr-ch'),
        ('vers-la-france.html', 'De la Suisse vers la France', 'Vous dirigez une entreprise suisse et le marché français vous attire. Nous vous aidons à lire un pays centralisé dans ses textes, mais très régional dans ses réseaux.', 'ch-fr'),
        ('entre-regions-suisses.html', 'Entre Suisse romande et Suisse alémanique', 'La frontière linguistique reste une vraie frontière commerciale. Nous vous aidons à la franchir, dans un sens comme dans l\'autre.', 'ch-ch'),
    ]
    glyph = {
        'fr-ch': '<svg viewBox="0 0 120 28" aria-hidden="true"><rect x="1" y="6" width="34" height="16" class="g-a"/><rect x="85" y="6" width="34" height="16" class="g-b"/><path d="M40 14 H78" class="g-l" marker-end="url(#gh)"/></svg>',
        'ch-fr': '<svg viewBox="0 0 120 28" aria-hidden="true"><rect x="1" y="6" width="34" height="16" class="g-b"/><rect x="85" y="6" width="34" height="16" class="g-a"/><path d="M40 14 H78" class="g-l" marker-end="url(#gh)"/></svg>',
        'ch-ch': '<svg viewBox="0 0 120 28" aria-hidden="true"><rect x="1" y="6" width="34" height="16" class="g-b"/><rect x="85" y="6" width="34" height="16" class="g-b"/><path d="M42 14 H78" class="g-l" marker-start="url(#gh)" marker-end="url(#gh)"/></svg>',
    }
    cs = ''.join(f'<a class="dir" href="{h}">{glyph[g]}<h3>{t}</h3><p>{d}</p><span class="more">Voir cette direction</span></a>' for h, t, d, g in items)
    return f'''<section class="sec sec-white"><div class="wrap">
  <svg width="0" height="0" style="position:absolute"><defs><marker id="gh" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#E8192C"/></marker></defs></svg>
  <p class="kicker">Trois directions</p><h2 class="w-narrow">Un marché voisin n'est jamais un marché proche.</h2>
  <p class="intro">La langue, les usages, la façon de décider : ce qui fonctionne à Lyon ne fonctionne pas forcément à Lausanne, et ce qui convainc à Genève laisse souvent Zurich indifférent.</p>
  <div class="dirs">{cs}</div>
</div></section>'''

CASES = [
    ('Mon produit est-il conforme aux règles du marché suisse ?',
     'Équipement industriel · De la France vers la Suisse',
     'Un fabricant français d\'équipements industriels voulait vendre en Suisse. Avant de démarcher qui que ce soit, il fallait savoir précisément quelles normes, prescriptions de sécurité et exigences cantonales s\'appliquaient à ses produits.',
     'Recherche à la source des textes et prescriptions applicables, identification des points à adapter sur le produit et sur l\'offre, recentrage sur quatre cantons prioritaires avant d\'approcher les acheteurs industriels.',
     'Une offre adaptée en amont, conforme dès le premier rendez-vous, et un plan d\'approche canton par canton.'),
    ('Qui dois-je rencontrer, et comment les approcher ?',
     'Services aux entreprises · Nouveau marché',
     'Une entreprise ne connaissait personne sur le marché visé et ne voulait pas d\'une campagne de démarchage à l\'aveugle.',
     'Analyse du marché, puis analyse des entreprises cibles une par une, pour aboutir à cinq interlocuteurs prioritaires parfaitement identifiés, avec une approche directe préparée pour chacun.',
     'Cinq contacts justes plutôt que des centaines d\'appels, et des premières rencontres avec de vrais décideurs.'),
    ('Faut-il vraiment créer une société en Suisse ?',
     'Travaux et chantiers · De la France vers la Suisse',
     'Une entreprise française intervenait déjà régulièrement sur des chantiers suisses. Entre la limite des jours de prestation autorisés pour une entreprise étrangère et le coût d\'une structure locale, elle hésitait depuis longtemps.',
     'Clarification des règles applicables aux prestataires étrangers, comparaison des options possibles (optimiser le fonctionnement actuel, s\'associer à un partenaire local ou créer une structure), puis recommandation argumentée.',
     'Une décision prise sur des faits, au bon moment, sans créer de structure avant que l\'activité ne la justifie.'),
]

def cases(k, title, items, intro='', tone=''):
    cs = ''
    for q, sect, defi, did, res in items:
        cs += f'''<article class="case">
  <div class="case-head"><h3 class="case-q">« {q} »</h3><p class="case-sect">{sect}</p></div>
  <dl>
    <div><dt>La situation</dt><dd>{defi}</dd></div>
    <div><dt>Ce que nous avons fait</dt><dd>{did}</dd></div>
    <div><dt>Le résultat</dt><dd>{res}</dd></div>
  </dl>
</article>'''
    intro_h = f'<p class="intro">{intro}</p>' if intro else ''
    return f'''<section class="sec {tone}"><div class="wrap">
  {kicker(k)}<h2 class="w-narrow">{title}</h2>{intro_h}<div class="cases">{cs}</div>
</div></section>'''

def text(k, title, paras, tone='', aside=''):
    ps = ''.join(f'<p>{p}</p>' for p in paras)
    a = f'<aside class="aside">{aside}</aside>' if aside else ''
    return f'''<section class="sec {tone}"><div class="wrap split">
  <div class="split-head">{kicker(k)}<h2>{title}</h2></div>
  <div class="split-body prose">{ps}{a}</div>
</div></section>'''

def faq(title, items, tone=''):
    qs = ''.join(f'<details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>' for q, a in items)
    return f'''<section class="sec {tone}"><div class="wrap split">
  <div class="split-head"><p class="kicker">Questions fréquentes</p><h2>{title}</h2></div>
  <div class="split-body faq">{qs}</div>
</div></section>'''

def person(full=False):
    bio = ('Luc Rohmer est CEO de Leadr. Chef d\'entreprise lui-même, il connaît de l\'intérieur les décisions qu\'un dirigeant prend chaque jour : où investir, qui recruter, à qui faire confiance. C\'est ce qui lui permet de parler d\'égal à égal avec ses interlocuteurs, des deux côtés de la frontière, et de mettre en relation des dirigeants qui ont de vraies raisons de se rencontrer.'
           if full else
           'Chez Leadr, votre projet est suivi par la même personne, du premier échange jusqu\'à vos premiers clients. Elle connaît votre dossier, vos contraintes et vos interlocuteurs, et reste joignable dès qu\'une question se pose.')
    title = 'Luc Rohmer' if full else 'Un interlocuteur privilégié.'
    k = 'CEO' if full else 'Luc Rohmer, CEO de Leadr'
    return f'''<section class="sec person"><div class="wrap person-grid">
  <div class="portrait"><img src="img/luc-rohmer.jpg" alt="Luc Rohmer, CEO de Leadr" onerror="this.remove()"><span class="ph" aria-hidden="true">LR</span></div>
  <div class="person-txt"><p class="kicker">{k}</p><h2>{title}</h2><p>{bio}</p>
  <div class="actions actions-soc"><a class="btn btn-red" href="contact.html">Prendre rendez-vous</a>{SOCIAL()}</div>{'' if full else '<p class="link-line person-more"><a href="leadr.html">Qui sommes-nous : le parcours de Luc Rohmer</a></p>'}</div>
</div></section>'''

def cta(title, txt=''):
    t = f'<p>{txt}</p>' if txt else ''
    return f'''<section class="cta"><div class="wrap cta-in"><div><h2>{title}</h2>{t}</div><div class="cta-act"><a class="btn btn-red btn-lg" href="contact.html">Prendre rendez-vous</a><p class="micro">Appel de prise de contact, sans engagement. Vous choisissez votre créneau.</p></div></div></section>'''

# ------------------------------------------------------------------ pages
FAQ_HOME = [
    ('Combien de temps faut-il pour s\'installer sur un nouveau marché ?', 'En général 18 à 24 mois pour une présence durable. Nous ne promettons pas d\'aller plus vite : nous faisons en sorte que chaque mois serve à quelque chose.'),
    ('Faut-il créer une société pour commencer ?', 'Rarement. Notre principe est simple : les revenus d\'abord, la structure ensuite. La société locale se crée quand l\'activité la justifie, pas avant.'),
    ('La mise en relation, c\'est du démarchage téléphonique ?', 'Non. Nous analysons le marché et les entreprises cibles pour identifier les quelques interlocuteurs qui comptent vraiment, puis nous les approchons directement grâce à notre réseau. Chaque contact est préparé.'),
    ('Avec quelles entreprises travaillez-vous ?', 'Principalement des PME, des PMI et des ETI bien installées sur leur marché d\'origine, dans l\'industrie, les technologies et les services aux entreprises. Le critère décisif est l\'exportabilité de votre offre, que nous vérifions dès le premier rendez-vous.'),
    ('Combien coûte une mission ?', 'Chaque mission est dimensionnée selon votre projet, la direction visée et le niveau de présence dont vous avez besoin. Le premier rendez-vous permet d\'en définir le périmètre avant toute proposition.'),
    ('Comment se passe le premier rendez-vous ?', 'Nous parlons de votre offre, du marché visé, de vos ressources et de votre calendrier. Vous repartez avec un avis franc sur le potentiel de votre projet et les prochaines étapes possibles.'),
]

PAGES = {}

PAGES['index.html'] = dict(
    title='Leadr · Développer votre activité entre la France et la Suisse',
    desc='Leadr est votre antenne sur le marché visé : entreprises françaises en Suisse, entreprises suisses en France, et d\'une région linguistique suisse à l\'autre.',
    body=[
        hero('France, Suisse romande, Suisse alémanique', 'Vos prochains clients sont de l\'autre côté de la frontière.',
             'Leadr est une société suisse qui devient votre antenne sur le marché visé. Nous vous renseignons, nous vous aidons à adapter votre offre aux règles locales et nous vous mettons en relation avec les bonnes personnes, jusqu\'à vos premiers clients.',
             [('contact.html', 'Prendre rendez-vous'), ('methode.html', 'Découvrir la méthode')], map_=True),
        directions(),
        rows('Votre antenne sur le marché', 'Une présence permanente de l\'autre côté de la frontière.', [
            ('Renseigner', 'Normes techniques, textes applicables, exigences cantonales, usages d\'achat. Les informations précises dont vous avez besoin pour décider, trouvées à la source.'),
            ('Anticiper', 'Adapter votre produit ou votre offre aux exigences du marché visé avant de vendre, plutôt que découvrir l\'obstacle chez le client.'),
            ('Mettre en relation', 'Identifier, par l\'analyse du marché et des entreprises, les quelques interlocuteurs qui comptent vraiment, puis vous les présenter directement grâce à notre réseau.'),
            ('Installer quand il le faut', 'Société, banque, conformité, coordonnées avec un réseau de spécialistes locaux.'),
        ], intro='Nous ne passons pas une fois pour livrer un rapport. Nous devenons votre équipe externalisée sur le marché visé : vous nous posez vos questions, nous allons chercher les réponses, et nous restons présents aussi longtemps que votre projet en a besoin.',
           tone='sec-dark sec-alps', note='Quelques contacts justes valent mieux que des centaines d\'appels. Nous ne faisons pas de démarchage de masse : chaque mise en relation est préparée.'),
        cases('Exemples de missions', 'Les questions que nos clients nous posent.', CASES,
              intro='Trois situations types, tirées de projets réels. Les noms et les chiffres restent confidentiels.'),
        statement('Les revenus d\'abord, la structure ensuite.',
                  'Beaucoup d\'entreprises commencent par créer une filiale, louer des bureaux et recruter, puis cherchent leurs clients. Nous faisons l\'inverse : valider le marché et générer une activité réelle avant d\'engager des coûts fixes.', cls='st-graph'),
        steps('Méthode Leadr', 'Quatre temps, un seul objectif : une activité réelle.', [
            ('Cadrer', 'Votre offre, vos ambitions, vos contraintes. Et une question franche : votre offre est-elle exportable ?'),
            ('Valider', 'Les normes à respecter et l\'avis de vrais acheteurs, avant tout investissement lourd.'),
            ('Construire', 'La feuille de route commerciale, région par région, et la structure si elle devient nécessaire.'),
            ('Activer', 'Mises en relation, rendez-vous, premiers clients. Sur le terrain.'),
        ]) .replace('</ol>', '</ol><p class="link-line"><a href="methode.html">Voir la méthode en détail</a></p>'),
        text('Pour qui', 'Des entreprises qui ont déjà fait leurs preuves chez elles.', [
            'Nous travaillons avec des dirigeants de PME, de PMI et d\'ETI solidement installées sur leur marché d\'origine, dans l\'industrie, les technologies et les services aux entreprises, qui veulent ouvrir un nouveau marché avec méthode plutôt qu\'au hasard des contacts.'],
            tone='sec-white', aside='<strong>Notre premier critère : l\'exportabilité.</strong> Une offre qui repose sur un produit, une technologie ou un savoir-faire technique voyage bien. Une activité encadrée par une réglementation nationale demande d\'abord une étude, et parfois un autre chemin. Nous vous le disons dès le premier rendez-vous.'),
        person(),
        cols('Quand il faut aller plus loin', 'Implanter, relocaliser, diriger sur place.', [
            ('Implantation', 'Créer la structure locale au bon moment, sur de bonnes bases.', 'implantation.html'),
            ('Relocalisation', 'Déplacer un centre de décision ou une activité, sans perdre le fil.', 'relocalisation.html'),
            ('Management de transition', 'Une direction sur place, le temps de construire l\'équipe.', 'management-transition.html'),
        ], intro='Certains projets dépassent la conquête commerciale. Pour une implantation durable, le transfert d\'une activité ou une direction locale de transition, nous réunissons les bons partenaires sous une coordination unique.', tone='sec-white'),
        faq('Ce que les dirigeants nous demandent.', FAQ_HOME),
        cta('Parlons de votre prochain marché.', 'Un premier rendez-vous pour comprendre votre projet et vous dire franchement s\'il a sa place de l\'autre côté de la frontière.'),
    ])

PAGES['vers-la-suisse.html'] = dict(
    title='Se développer en Suisse · Leadr',
    desc='Entreprises françaises : trouvez vos premiers clients en Suisse avec les codes du marché local, canton par canton.',
    body=[
        hero('De la France vers la Suisse', 'La Suisse ne s\'aborde pas comme une région française de plus.',
             '26 cantons, quatre langues nationales, des acheteurs exigeants qui choisissent lentement et restent fidèles longtemps. Leadr est votre antenne sur le marché suisse : les codes, les règles et les bonnes portes.',
             [('contact.html', 'Prendre rendez-vous')]),
        rows('Les codes du marché', 'Ce qui surprend les entreprises françaises.', [
            ('La décision prend du temps', 'Un acheteur suisse teste, compare et vérifie avant de s\'engager. Une fois convaincu, il s\'engage dans la durée.'),
            ('Le canton compte', 'Fiscalité, autorisations, réseaux d\'affaires : une grande partie se joue au niveau cantonal, pas seulement fédéral.'),
            ('Parler français ne suffit pas', 'En Suisse romande, partager la langue ne fait pas de vous un acteur local. Les usages, eux, sont suisses.'),
            ('La qualité est un prérequis', 'Prix, délais, service après vente : votre offre sera comparée à des fournisseurs suisses déjà en place.'),
            ('Les règles ne sont pas toujours les mêmes', 'Normes techniques, prescriptions de sécurité, exigences cantonales : un produit conforme en France ne l\'est pas forcément en Suisse. Mieux vaut le savoir avant de vendre.'),
        ], tone='sec-white'),
        steps('Notre rôle', 'De la première question au premier client.', [
            ('Choisir où commencer', 'Les cantons et les secteurs où votre offre a le plus de chances, plutôt que toute la Suisse d\'un coup.'),
            ('Vérifier les règles du jeu', 'Nous recherchons les normes et les textes qui s\'appliquent à votre produit, et vous aidons à adapter votre offre en amont.'),
            ('Valider avant d\'investir', 'Des échanges avec de vrais acheteurs pour mesurer l\'intérêt réel de votre offre.'),
            ('Mettre en relation', 'Une approche directe des bons décideurs, identifiés par l\'analyse du marché et des entreprises.'),
            ('Structurer au bon moment', 'Quand l\'activité le justifie : société suisse, banque, conformité, avec notre réseau de spécialistes.'),
        ]),
        cases('Exemples de missions', 'Deux questions fréquentes d\'entreprises françaises.', [CASES[0], CASES[2]], tone='sec-white'),
        statement('Une filiale ne vend rien toute seule. Commencez par vos clients, la structure suivra.', who='Luc Rohmer, CEO de Leadr'),
        cta('Votre offre a-t-elle sa place en Suisse ?', 'Un premier rendez-vous permet de le vérifier, franchement.'),
    ])

PAGES['vers-la-france.html'] = dict(
    title='Se développer en France · Leadr',
    desc='Entreprises suisses : trouvez vos premiers clients en France avec les bons interlocuteurs, région par région.',
    body=[
        hero('De la Suisse vers la France', 'La France est un grand marché. C\'est aussi un marché de réseaux.',
             'Un pays centralisé dans ses textes, mais très régional dans sa façon de faire des affaires. Leadr aide les entreprises suisses à y trouver les bons interlocuteurs, et le bon ton.',
             [('contact.html', 'Prendre rendez-vous')]),
        rows('Les codes du marché', 'Ce qui surprend les entreprises suisses.', [
            ('La taille du marché', '13 régions métropolitaines et des bassins économiques très différents. Viser toute la France d\'emblée, c\'est souvent ne réussir nulle part.'),
            ('Le poids de la relation', 'Le réseau et la recommandation ouvrent souvent plus de portes que la qualité de l\'offre seule.'),
            ('Le circuit de décision', 'Des organisations parfois plus hiérarchiques, avec plusieurs interlocuteurs à convaincre.'),
            ('Les usages commerciaux', 'Négociation, délais de paiement, formalisme des échanges : tout se lit différemment.'),
            ('Les normes du marché', 'Normes françaises et européennes, certifications, réglementations sectorielles : à vérifier produit par produit.'),
        ], tone='sec-white'),
        steps('Notre rôle', 'Le bon marché, les bons interlocuteurs.', [
            ('Choisir la bonne région', 'Celle où votre offre répond à une demande réelle et où les réseaux sont accessibles.'),
            ('Vérifier les règles du jeu', 'Les normes et textes applicables à votre produit en France, pour adapter votre offre en amont.'),
            ('Tester votre offre', 'Auprès d\'acheteurs français, avant tout investissement lourd.'),
            ('Mettre en relation', 'Une approche directe des bons décideurs, identifiés par l\'analyse du marché et des entreprises.'),
            ('Mobiliser les relais locaux', 'Chambres consulaires, collectivités, réseaux d\'affaires : les partenaires qui comptent dans chaque région.'),
        ]),
        cases('Exemple de mission', 'La question que se posent les entreprises qui arrivent en France.', [CASES[1]], tone='sec-white'),
        cta('Votre entreprise est prête pour la France ?', 'Parlons de votre projet et des régions où il a le plus de chances.'),
    ])

PAGES['entre-regions-suisses.html'] = dict(
    title='Suisse romande et Suisse alémanique · Leadr',
    desc='Entreprises suisses : développez votre activité de l\'autre côté de la frontière linguistique, de la Suisse romande à la Suisse alémanique et inversement.',
    body=[
        hero('Suisse romande, Suisse alémanique', 'La frontière la plus difficile à franchir est parfois à l\'intérieur du pays.',
             'Entre Genève et Zurich, la langue change, mais aussi la façon de décider, de négocier et de construire la confiance. Leadr aide les entreprises suisses à se développer de l\'autre côté de la frontière linguistique.',
             [('contact.html', 'Prendre rendez-vous')]),
        rows('Deux cultures d\'affaires', 'Un même pays, deux marchés.', [
            ('La langue de travail', 'Un interlocuteur alémanique attend un premier échange en allemand, un interlocuteur romand en français. C\'est souvent là que tout commence, ou que tout s\'arrête.'),
            ('Les réseaux', 'Associations professionnelles, chambres de commerce et cercles d\'affaires sont largement organisés par région linguistique.'),
            ('Les références', 'Une référence client à Lausanne pèse peu à Saint-Gall. La crédibilité se reconstruit localement.'),
            ('Les usages', 'Forme des échanges, rythme de décision, manière de présenter une offre : les attentes diffèrent.'),
        ], tone='sec-white'),
        cols('Notre rôle', 'Passer la Sarine, dans un sens comme dans l\'autre.', [
            ('Cibler', 'Les cantons et les secteurs les plus porteurs de l\'autre côté de la frontière linguistique.'),
            ('Adapter votre discours', 'Présentation, arguments et supports pensés pour le marché visé, pas simplement traduits.'),
            ('Mettre en relation', 'Les décideurs et les réseaux de la région visée, approchés directement.'),
        ]),
        cta('Prêt à passer la Sarine ?', 'Un premier rendez-vous pour identifier par où commencer.'),
    ])

PAGES['methode.html'] = dict(
    title='Notre méthode · Leadr',
    desc='Cadrer, valider, construire, activer : la méthode Leadr pour ouvrir un nouveau marché sans perdre de temps ni d\'argent.',
    body=[
        hero('Méthode Leadr', 'Une méthode pour ne perdre ni temps, ni argent.',
             'Un point de départ honnête, quatre étapes et un seul objectif : une activité réelle sur le marché visé.'),
        text('Avant tout', 'Votre offre est-elle exportable ?', [
            'Une offre qui repose sur un produit, une technologie ou un savoir-faire technique se transpose bien d\'un pays à l\'autre. Une activité encadrée par une réglementation nationale, comme certaines professions de santé, de droit ou du bâtiment, demande d\'abord une étude spécifique.',
            'Nous le vérifions dès le premier rendez-vous, et nous vous le disons franchement.'], tone='sec-white'),
        steps('Le déroulé', 'Quatre étapes, chacune avec un résultat concret.', [
            ('Cadrer', 'Nous analysons votre offre, vos objectifs, vos ressources et vos contraintes.<br><strong>Ce que vous obtenez :</strong> un diagnostic clair et une décision éclairée sur la suite.'),
            ('Valider', 'Nous recherchons les normes et textes applicables à votre produit et confrontons votre offre à de vrais acheteurs du marché visé.<br><strong>Ce que vous obtenez :</strong> des retours terrain et la liste précise de ce qu\'il faut adapter.'),
            ('Construire', 'Nous définissons la feuille de route : régions prioritaires, cibles, discours, et structure si nécessaire.<br><strong>Ce que vous obtenez :</strong> un plan d\'action concret et priorisé.'),
            ('Activer', 'Nous identifions les bons interlocuteurs par l\'analyse du marché et des entreprises, puis nous les approchons directement et vous les présentons.<br><strong>Ce que vous obtenez :</strong> des rendez-vous qualifiés et vos premiers clients.'),
        ]),
        statement('Les quatre étapes ne s\'arrêtent pas au premier client.',
                  'Une nouvelle question réglementaire, un nouveau segment à ouvrir, un partenaire à trouver : nous restons votre antenne sur le marché, disponible quand le besoin se présente.'),
        text('Dans la durée', '18 à 24 mois : le temps réel d\'un marché.', [
            'S\'installer durablement sur un nouveau marché prend en général 18 à 24 mois. Nous ne promettons pas d\'aller plus vite. Nous faisons en sorte que chaque mois compte.'], tone='sec-white'),
        cta('Commençons par l\'étape 1.', 'Le premier rendez-vous est le début du cadrage.'),
    ])

PAGES['leadr.html'] = dict(
    title='Qui sommes-nous · Leadr GmbH',
    desc='Leadr GmbH, société suisse basée à Bâle, est l\'antenne des entreprises françaises et suisses sur leur nouveau marché.',
    body=[
        hero('Qui sommes-nous', 'Une société suisse, deux cultures d\'affaires.',
             'Leadr GmbH est basée à Bâle. Nous aidons les entreprises françaises et suisses à se développer sur un nouveau marché, avec une conviction : une présence commerciale se construit par les résultats, pas par les promesses.'),
        person(full=True),
        rows('Parcours', 'Une expérience forgée entre la France et la Suisse.', [
            ('Chef d\'entreprise et connecteur de dirigeants', 'Plusieurs entreprises dirigées en France et en Suisse, dans différents secteurs d\'activité. Diriger ses propres sociétés donne une lecture de dirigeant à dirigeant : les mêmes arbitrages, les mêmes contraintes, le même temps compté. Au fil des années, Luc est devenu pour son entourage professionnel celui qui sait qui présenter à qui. C\'est aujourd\'hui le cœur du métier de Leadr.'),
            ('CCI France Suisse, business center de Bâle', 'Un an au sein de la CCI France Suisse pour la mise en place et l\'ouverture de son business center à Bâle : un lieu où les entreprises françaises qui s\'implantent en Suisse peuvent se domicilier, travailler et rencontrer le réseau économique lors d\'événements. Une expérience qui a permis de tisser un réseau dans toute la Suisse.'),
            ('EuroAirport Bâle-Mulhouse, sales manager', 'Deux ans pour redynamiser l\'activité commerciale de l\'aéroport binational : trouver des clients en Suisse, en France et en Allemagne, et remplir salles, espaces et conférences avec des événements institutionnels comme privés.'),
            ('Création de contenu et marketing', 'Des années à construire des marques et des audiences, qui ont forgé une conviction : sur un nouveau marché, la première chose à gagner, c\'est la confiance.'),
        ], intro='Pourquoi Leadr ? Parce que les bonnes entreprises échouent souvent de l\'autre côté de la frontière pour de mauvaises raisons : une norme ignorée, un mauvais interlocuteur, un usage mal compris. Leadr existe pour leur éviter ces erreurs.', tone='sec-white'),
        text('Notre rôle', 'Votre équipe sur place, sans avoir à la recruter.', [
            'Pour nos clients, Leadr est un interlocuteur permanent sur le marché visé. Une question sur une norme, un texte, un interlocuteur à identifier : vous nous la posez, nous revenons avec une réponse précise.',
            'Et quand il faut rencontrer les bonnes personnes, notre réseau fait la différence.'], tone='sec-white'),
        text('Notre réseau', 'Les bons spécialistes, au bon moment.', [
            'Fiduciaires et notaires, banques, avocats, spécialistes des ressources humaines et du recrutement, chambres de commerce et agences de promotion économique.',
            'Pour le management de transition, Leadr s\'appuie en outre sur un partenariat stratégique avec un cabinet spécialisé, implanté en Suisse.',
            'Nous ne les nommons pas ici : nous vous les présentons quand votre projet en a besoin.']),
        cols('Nos engagements', 'Trois choses sur lesquelles nous ne transigeons pas.', [
            ('La franchise', 'Si votre projet n\'a pas sa place sur le marché visé, nous vous le disons dès le premier rendez-vous.'),
            ('La précision', 'Des informations vérifiées à la source et des contacts choisis un par un, jamais de démarchage de masse.'),
            ('La discrétion', 'Vos projets sont stratégiques. Ils restent confidentiels, avant, pendant et après.'),
        ], tone='sec-white'),
        cta('Faisons connaissance.', 'Le plus simple reste d\'en parler de vive voix.'),
    ])

PAGES['premier-rendez-vous.html'] = dict(
    title='Premier rendez-vous · Leadr',
    desc='Un premier rendez-vous pour comprendre votre projet et vous donner un avis franc sur son potentiel.',
    body=[
        hero('Premier rendez-vous', 'Un premier rendez-vous pour savoir où vous en êtes.',
             'Avant toute proposition, nous prenons le temps de comprendre votre projet. Vous repartez avec un avis franc sur son potentiel et sur les prochaines étapes possibles.',
             [('contact.html', 'Prendre rendez-vous')]),
        rows('Au programme', 'Quatre questions, des réponses claires.', [
            ('Votre offre', 'Ce qui la rend exportable, ou pas.'),
            ('Le marché visé', 'Vos ambitions, vos premières pistes, la concurrence que vous connaissez.'),
            ('Vos ressources', 'Qui porte le projet chez vous, avec quel calendrier.'),
            ('La suite', 'Les étapes possibles, et si Leadr est le bon partenaire pour les mener.'),
        ], tone='sec-white'),
        text('En pratique', 'Simple et sans engagement.', [
            'Un appel de prise de contact, sans engagement. Vous choisissez directement le créneau qui vous convient dans l\'agenda de Luc Rohmer.']),
        cta('Prêt pour un premier échange ?'),
    ])

PAGES['implantation.html'] = dict(
    title='Implantation en Suisse ou en France · Leadr',
    desc='Créer votre structure locale au bon moment : société, banque, conformité, coordonnées par un interlocuteur unique.',
    body=[
        hero('Quand l\'activité le justifie', 'S\'implanter au bon moment, sur de bonnes bases.',
             'Créer une société, ouvrir un compte bancaire, se mettre en conformité : quand votre activité justifie une présence locale, nous coordonnons chaque étape avec un réseau de spécialistes locaux.',
             [('contact.html', 'Prendre rendez-vous')]),
        steps('Les étapes', 'Tout ce qu\'il faut, rien de superflu.', [
            ('Le choix de la structure', 'La forme juridique et la localisation adaptées à votre activité et à vos ambitions.'),
            ('La création de la société', 'Les démarches de constitution, avec les fiduciaires et notaires de notre réseau.'),
            ('La banque et les assurances', 'L\'ouverture des comptes et les couvertures nécessaires à l\'activité.'),
            ('La conformité', 'Les obligations sociales, fiscales et réglementaires du pays et, en Suisse, du canton.'),
        ], tone='sec-white'),
        statement('Vous n\'avez pas à coordonner cinq prestataires.', 'Fiduciaire, notaire, banque, avocat, assureur : nous orchestrons l\'ensemble et vous gardez un seul interlocuteur du début à la fin.'),
        cta('Le moment de vous installer est venu ?'),
    ])

PAGES['relocalisation.html'] = dict(
    title='Relocalisation en Suisse · Leadr',
    desc='Transférer un centre de décision ou une activité en Suisse : coordination des équipes et des partenaires spécialisés.',
    body=[
        hero('Projets d\'envergure', 'Déplacer une activité, sans perdre le fil.',
             'Transférer un siège, un centre de décision ou une activité industrielle en Suisse est un projet stratégique. Nous le menons avec des partenaires spécialisés, de la décision jusqu\'à l\'installation des équipes.',
             [('contact.html', 'Prendre rendez-vous')]),
        text('Après le schéma, l\'exécution', 'La structure est dessinée. Reste à la faire vivre.', [
            'Les cabinets de conseil conçoivent la structure, la fiscalité et la substance. Ce qui reste souvent sans pilote, c\'est la mise en œuvre humaine : choisir le site, recruter, installer les équipes, faire tourner l\'activité.',
            'C\'est là que nous intervenons.'], tone='sec-white'),
        rows('Ce que couvre une relocalisation', 'Du choix du site à l\'ancrage local.', [
            ('Le choix du site', 'Canton, ville, bassin d\'emploi, en fonction de votre activité.'),
            ('Les équipes locales', 'Recrutement des profils clés et organisation de l\'entité.'),
            ('La direction de transition', 'Un dirigeant expérimenté sur place pendant la mise en route, grâce à notre partenariat stratégique en management de transition.'),
            ('L\'ancrage local', 'Relations avec les autorités, les réseaux économiques et les premiers partenaires.'),
        ]),
        cta('Un projet de relocalisation à l\'étude ?', 'Parlons-en en toute confidentialité.'),
    ])

PAGES['management-transition.html'] = dict(
    title='Management de transition en Suisse · Leadr',
    desc='Des dirigeants de transition expérimentés en Suisse, grâce à un partenariat stratégique : démarrage, continuité, transformation.',
    body=[
        hero('Management de transition', 'Des dirigeants aguerris, opérationnels dès le premier jour.',
             'Implantation, relocalisation, départ imprévu ou transformation : un dirigeant de transition prend les commandes de votre activité en Suisse, le temps nécessaire. Un profil suisse, une expérience démontrée, un interlocuteur privilégié.',
             [('contact.html', 'Prendre rendez-vous')]),
        text('Un partenariat stratégique', 'Une expérience démontrée, mise à votre disposition.', [
            'Leadr s\'appuie sur un partenariat stratégique avec un cabinet spécialisé du management de transition, implanté en Suisse.',
            'Ce partenariat donne accès à des dirigeants dont les compétences ont été démontrées au fil de longues années de missions, dans des contextes exigeants : direction d\'entité, réorganisation, redressement, croissance.',
            'Leadr reste votre interlocuteur privilégié tout au long de la mission, de sa définition jusqu\'à la passation.'],
            tone='sec-dark', aside='<strong>Toujours un profil suisse.</strong> Le dirigeant qui prend les commandes de votre activité en Suisse connaît le pays de l\'intérieur : ses usages, ses réseaux, ses attentes.'),
        cols('Trois situations', 'Quand faire appel à un dirigeant de transition.', [
            ('Démarrer', 'Lancer l\'entité suisse et la faire tourner avant le recrutement définitif.'),
            ('Assurer la continuité', 'Remplacer un dirigeant absent ou parti, sans laisser l\'activité sans pilote.'),
            ('Transformer', 'Piloter une réorganisation, un transfert d\'activité ou un redressement.'),
        ], tone='sec-white'),
        rows('Fonctions couvertes', 'De la stratégie aux opérations.', [
            ('Direction générale', 'Piloter l\'entité locale et représenter l\'entreprise en Suisse.'),
            ('Direction commerciale', 'Construire et animer l\'équipe de vente, ouvrir les premiers comptes.'),
            ('Direction financière', 'Tenir les comptes, la trésorerie et les relations bancaires.'),
            ('Direction industrielle et des opérations', 'Lancer ou réorganiser la production, la logistique et les achats.'),
            ('Ressources humaines', 'Recruter les profils clés et poser les bases de l\'organisation.'),
        ]),
        steps('Déroulement', 'Une mission en quatre temps.', [
            ('Cadrer', 'Le périmètre, les objectifs et la durée de la mission.'),
            ('Choisir le profil', 'Un dirigeant dont le parcours correspond à votre situation, présenté avant tout engagement.'),
            ('Suivre', 'Des points réguliers tout au long de la mission, avec Leadr comme interlocuteur privilégié.'),
            ('Transmettre', 'Une passation préparée, pour que votre successeur reprenne une organisation qui fonctionne.'),
        ], tone='sec-white'),
        cta('Besoin d\'une direction locale ?', 'Parlons-en en toute confidentialité.'),
    ])

PAGES['cas-clients.html'] = dict(
    title='Cas clients · Leadr',
    desc='Des situations réelles de développement entre la France et la Suisse, présentées de façon anonyme.',
    body=[
        hero('Cas clients', 'Des projets réels, présentés en toute discrétion.',
             'Nos clients nous confient des projets stratégiques. Aucun nom d\'entreprise ni aucun chiffre n\'est publié : chaque situation est présentée par secteur, à partir de la question qui a tout déclenché.'),
        cases('', 'Trois questions, trois réponses.', CASES, tone='sec-white'),
        cta('Votre question pourrait être la prochaine.'),
    ])

PAGES['reperes.html'] = dict(
    title='Repères France et Suisse · Leadr',
    desc='Les repères essentiels pour aborder le marché suisse, le marché français et la frontière linguistique suisse.',
    body=[
        hero('Repères', 'Ce qu\'il faut savoir avant de se lancer.',
             'Les points essentiels pour aborder le marché suisse, le marché français et la frontière linguistique.'),
        rows('Côté suisse', 'Un pays fédéral et multilingue.', [
            ('26 cantons', 'Chacun dispose de compétences fiscales, administratives et parfois réglementaires propres.'),
            ('Quatre langues nationales', 'Allemand, français, italien et romanche. Trois grandes régions linguistiques, trois façons de faire des affaires.'),
            ('Le canton avant tout', 'Beaucoup de démarches et d\'autorisations dépendent du canton d\'implantation autant que du cadre fédéral.'),
        ], tone='sec-white'),
        rows('Côté français', 'Un pays centralisé, des marchés régionaux.', [
            ('13 régions métropolitaines', 'Des bassins économiques et des réseaux professionnels très différents d\'une région à l\'autre.'),
            ('Des relais locaux', 'Chambres consulaires, collectivités et réseaux d\'affaires jouent un rôle concret dans un développement commercial.'),
        ]),
        faq('Les questions qui reviennent souvent.', FAQ_HOME[:3], tone='sec-white'),
        cta('Une question sur votre situation ?'),
    ])

FORM = f'''<section class="sec sec-white"><div class="wrap split">
  <div class="split-head"><p class="kicker">Votre demande</p><h2>Quelques lignes suffisent.</h2>
    <p class="intro">Nous revenons vers vous rapidement pour fixer un premier rendez-vous.</p>
    <p class="contact-direct">Vous préférez écrire directement ?<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>{SOCIAL()}</div>
  <div class="split-body">
  <form class="form" action="{FORM_URL}" method="POST" novalidate>
    <input type="hidden" name="_subject" value="Nouvelle demande depuis leadr.ch"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
    <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="f2"><label>Nom et prénom<input name="nom" autocomplete="name" required></label>
    <label>Fonction<input name="fonction" autocomplete="organization-title" required></label></div>
    <div class="f2"><label>Entreprise<input name="entreprise" autocomplete="organization" required></label>
    <label>Email professionnel<input type="email" name="email" autocomplete="email" required></label></div>
    <label>Téléphone <span class="opt">(facultatif)</span><input type="tel" name="telephone" autocomplete="tel"></label>
    <fieldset><legend>Votre projet</legend><div class="chips">
      <label class="chip"><input type="radio" name="projet" value="France vers Suisse" required><span>De la France vers la Suisse</span></label>
      <label class="chip"><input type="radio" name="projet" value="Suisse vers France"><span>De la Suisse vers la France</span></label>
      <label class="chip"><input type="radio" name="projet" value="Entre régions suisses"><span>Entre Suisse romande et Suisse alémanique</span></label>
      <label class="chip"><input type="radio" name="projet" value="Implantation ou relocalisation"><span>Implantation ou relocalisation</span></label>
      <label class="chip"><input type="radio" name="projet" value="Autre"><span>Autre</span></label></div></fieldset>
    <label>Taille de l'entreprise<select name="taille" required><option value="">Choisir</option><option>Moins de 50 salariés</option><option>50 à 250 salariés</option><option>250 à 5 000 salariés</option><option>Plus de 5 000 salariés</option></select></label>
    <label>Votre message<textarea name="message" rows="5" required></textarea></label>
    <label class="consent"><input type="checkbox" name="consentement" required><span>J'accepte que ces informations soient utilisées par Leadr pour répondre à ma demande. <a href="mentions-legales.html">En savoir plus</a></span></label>
    <button class="btn btn-red btn-lg" type="submit">Envoyer ma demande</button>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form></div>
</div></section>'''

PAGES['contact.html'] = dict(
    title='Prendre rendez-vous · Leadr',
    desc='Réservez un appel de prise de contact avec Luc Rohmer, CEO de Leadr, ou présentez votre projet par écrit.',
    body=[hero('Contact', 'Prenons rendez-vous.', 'Le plus simple : réservez directement un appel de prise de contact dans l\'agenda de Luc Rohmer, CEO de Leadr. Vous préférez écrire ? Le formulaire est juste en dessous.', [(BOOK, 'Choisir un créneau'), ('#formulaire', 'Écrire un message')], small=True), FORM.replace('<section class="sec sec-white">', '<section class="sec sec-white" id="formulaire">', 1)])

PAGES['mentions-legales.html'] = dict(
    title='Mentions légales et confidentialité · Leadr',
    desc='Mentions légales et politique de confidentialité du site leadr.ch.',
    body=[
        hero('Informations légales', 'Mentions légales et confidentialité.', 'Les informations utiles sur l\'éditeur du site et sur l\'usage de vos données.', small=True),
        text('Éditeur', 'Leadr GmbH', [
            'Leadr GmbH, Sternengasse 6, 4051 Bâle, Suisse. Numéro IDE : CHE-252.536.958.',
            f'Responsable de la publication : Luc Rohmer. Contact : <a href="mailto:{EMAIL}">{EMAIL}</a>.',
            'Hébergement : Vercel Inc., 440 N Barranca Ave #4133, Covina, CA 91723, États-Unis.'], tone='sec-white'),
        text('Vos données', 'Confidentialité.', [
            'Les informations transmises par le formulaire de contact servent uniquement à répondre à votre demande et à organiser un éventuel rendez-vous. Elles ne sont ni vendues ni cédées à des tiers.',
            'Le formulaire est opéré par le service FormSubmit, qui transmet votre message par email à Leadr. Vos données sont conservées le temps nécessaire au traitement de votre demande et à la relation commerciale qui peut en découler.',
            f'Conformément à la loi fédérale suisse sur la protection des données et, le cas échéant, au règlement européen sur la protection des données, vous pouvez demander l\'accès, la rectification ou la suppression de vos données en écrivant à <a href="mailto:{EMAIL}">{EMAIL}</a>.',
            'Ce site n\'utilise pas de cookies publicitaires ni d\'outil de suivi.']),
    ])

REDIRECTS = {
    'developpement-commercial.html': 'methode.html', 'validation-marche.html': 'methode.html',
    'offre-pme-pmi.html': 'implantation.html', 'offre-eti-grands-comptes.html': 'implantation.html',
    'partenaires.html': 'leadr.html', 'session-cadrage.html': 'premier-rendez-vous.html', 'ressources.html': 'reperes.html',
}

# ------------------------------------------------------------------ accueil optimisé (v2.1)
MAP2 = open('parts/map.svg', encoding='utf-8').read()

def hero_home():
    return f"""<section class="hero hero-home"><div class="wrap hero-grid">
  <div class="hero-txt"><p class="kicker">France, Suisse romande, Suisse alémanique</p>
    <h1>Vos prochains clients sont de l'autre côté de la frontière.</h1>
    <p class="lead">Leadr est votre antenne sur le marché visé. Nous vous renseignons, nous vous aidons à adapter votre offre aux règles locales et nous vous présentons aux bonnes personnes.</p>
    <div class="actions"><a class="btn btn-red btn-lg" href="contact.html">Prendre rendez-vous</a><a class="btn btn-line btn-lg" href="#exemples">Voir des exemples</a></div>
    <p class="micro">Appel de prise de contact sans engagement, réservé en deux clics.</p>
  </div>{MAP2}
</div></section>"""

def proof_strip():
    items = [('Société suisse', 'Leadr GmbH, basée à Bâle'),
             ('Trois directions', 'Vers la Suisse, vers la France, entre régions linguistiques'),
             ('PME, PMI et ETI', 'Industrie, technologies, transport, services aux entreprises'),
             ('Un réseau dans toute la Suisse', 'Construit sur le terrain, en Suisse romande et alémanique')]
    cs = ''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in items)
    return f'<section class="proof" aria-label="Leadr en bref"><div class="wrap proof-in">{cs}</div></section>'

def directions2():
    items = [
        ('vers-la-suisse.html', 'FR', 'CH', '→', 'De la France vers la Suisse', 'Les bons cantons, les bons interlocuteurs et la bonne façon de les approcher.'),
        ('vers-la-france.html', 'CH', 'FR', '→', 'De la Suisse vers la France', 'Un pays centralisé dans ses textes, mais très régional dans ses réseaux.'),
        ('entre-regions-suisses.html', 'Romandie', 'Deutschschweiz', '↔', 'Entre régions suisses', 'La frontière linguistique reste une vraie frontière commerciale. Nous vous aidons à la franchir.'),
    ]
    cs = ''.join(f'<a class="dir2" href="{h}"><span class="route"><b>{a}</b><i aria-hidden="true">{ar}</i><b>{b}</b></span><h3>{t}</h3><p>{d}</p><span class="more">Voir cette direction</span></a>' for h, a, b, ar, t, d in items)
    return f"""<section class="sec sec-white"><div class="wrap">
  <p class="kicker">Trois directions</p><h2 class="w-narrow">Un marché voisin n'est jamais un marché proche.</h2>
  <p class="intro">Ce qui fonctionne à Lyon ne fonctionne pas forcément à Lausanne, et ce qui convainc à Genève laisse souvent Zurich indifférent.</p>
  <div class="dirs2">{cs}</div>
</div></section>"""

SHORT_CASES = [
    ('Mon produit est-il conforme aux règles du marché suisse ?', 'Équipement industriel, France vers Suisse',
     'Vendre en Suisse sans savoir précisément quelles normes et prescriptions s\'appliquent aux produits.',
     'Recherche des textes à la source, liste des adaptations à faire, quatre cantons prioritaires.',
     'Une offre conforme dès le premier rendez-vous.'),
    ('Qui dois-je rencontrer, et comment les approcher ?', 'Services aux entreprises, nouveau marché',
     'Aucun contact sur le marché visé, et pas question de démarcher à l\'aveugle.',
     'Analyse du marché, puis des entreprises cibles, une par une.',
     'Cinq décideurs identifiés et approchés directement.'),
    ('Faut-il vraiment créer une société en Suisse ?', 'Travaux et chantiers, France vers Suisse',
     'Des chantiers suisses réguliers, freinés par la limite des jours de prestation pour une entreprise étrangère.',
     'Règles clarifiées, options comparées : optimiser, s\'associer, créer une structure.',
     'Une décision prise sur des faits, au bon moment.'),
]

def cases_grid():
    cs = ''.join(f"""<article class="qcard"><p class="qcard-sect">{sect}</p><h3>« {q} »</h3>
  <dl><div><dt>Situation</dt><dd>{a}</dd></div><div><dt>Ce que nous avons fait</dt><dd>{b}</dd></div></dl>
  <p class="qcard-res"><span>Résultat</span>{c}</p></article>""" for q, sect, a, b, c in SHORT_CASES)
    return f"""<section class="sec" id="exemples"><div class="wrap">
  <p class="kicker">Exemples de missions</p><h2 class="w-narrow">Les questions que nos clients nous posent.</h2>
  <p class="intro">Trois situations types, tirées de projets réels. Les noms et les chiffres restent confidentiels.</p>
  <div class="qgrid">{cs}</div>
  <p class="link-line"><a href="cas-clients.html">Lire les cas en détail</a></p>
</div></section>"""

def further_strip():
    items = [('implantation.html', 'Implantation', 'Créer la structure locale au bon moment.'),
             ('relocalisation.html', 'Relocalisation', 'Déplacer une activité sans perdre le fil.'),
             ('management-transition.html', 'Management de transition', 'Des dirigeants aguerris, grâce à un partenariat stratégique.')]
    cs = ''.join(f'<a href="{h}"><strong>{t}</strong><span>{d}</span></a>' for h, t, d in items)
    return f"""<section class="further"><div class="wrap further-in"><div><p class="kicker">Quand il faut aller plus loin</p>
  <p class="further-t">Pour une implantation durable, le transfert d'une activité ou une direction locale, nous réunissons les bons partenaires sous une coordination unique.</p></div>
  <div class="further-links">{cs}</div></div></section>"""

def cta2(title, txt):
    return f"""<section class="cta"><div class="wrap cta-in"><div><h2>{title}</h2><p>{txt}</p></div>
  <div class="cta-act"><a class="btn btn-red btn-lg" href="contact.html">Prendre rendez-vous</a><p class="micro">Appel de prise de contact, sans engagement. Vous choisissez votre créneau.</p></div></div></section>"""

FAQ_HOME2 = FAQ_HOME[:1] + [
    ('Faites-vous de la prospection commerciale externalisée ?', 'Oui, sous une forme ciblée. Nous agissons comme votre équipe commerciale externalisée sur le marché visé : analyse du marché, identification des décideurs, approche directe et préparation de chaque rendez-vous. Pas de démarchage de masse ni d\'appels à froid en série.'),
    ('Comment se passe l\'accompagnement au quotidien ?', 'Un interlocuteur privilégié suit votre dossier de bout en bout. Il vous renseigne sur les règles et les usages, prépare les mises en relation et fait régulièrement le point avec vous. L\'accompagnement dure aussi longtemps que votre projet en a besoin.'),
] + FAQ_HOME[1:3] + [('Mon activité est-elle exportable ?', 'Une offre qui repose sur un produit, une technologie ou un savoir-faire technique voyage bien. Une activité encadrée par une réglementation nationale demande d\'abord une étude, et parfois un autre chemin. Nous vous le disons dès le premier rendez-vous.')] + FAQ_HOME[3:]
FAQ_LD = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ_HOME2]}, ensure_ascii=False)

PAGES['index.html']['body'] = [
    hero_home(),
    proof_strip(),
    directions2(),
    PAGES['index.html']['body'][2],   # Votre antenne sur le marché
    cases_grid(),
    PAGES['index.html']['body'][4],   # Les revenus d'abord, la structure ensuite
    PAGES['index.html']['body'][5],   # Méthode
    PAGES['index.html']['body'][7],   # Fondateur
    further_strip(),
    faq('Ce que les dirigeants nous demandent.', FAQ_HOME2),
    '<script type="application/ld+json">' + FAQ_LD + '</script>',
    cta2('Parlons de votre prochain marché.', 'Un premier rendez-vous pour comprendre votre projet et vous dire franchement s\'il a sa place de l\'autre côté de la frontière.'),
]

# ------------------------------------------------------------------ langues
def _load(lg):
    return json.load(open(f'i18n/{lg}.json', encoding='utf-8'))
TR = {'de': _load('de'), 'en': _load('en')}
LOCALE = {'fr': 'fr_CH', 'de': 'de_CH', 'en': 'en_GB'}
WA_TXT = {'fr': 'Bonjour%20Luc%2C%20je%20viens%20du%20site%20leadr.ch.', 'de': 'Guten%20Tag%20Luc%2C%20ich%20komme%20von%20der%20Website%20leadr.ch.', 'en': 'Hello%20Luc%2C%20I%20found%20you%20through%20leadr.ch.'}
MISSING = set()

def localize(doc, lg, slug):
    pub = '' if slug == 'index.html' else slug
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="https://www.leadr.ch/{"" if l=="fr" else l+"/"}{pub}">' for l in ('fr', 'de', 'en'))
    alt += f'<link rel="alternate" hreflang="x-default" href="https://www.leadr.ch/{pub}">'
    up = '' if lg == 'fr' else '../'
    def lk(l): return up + ('' if l == 'fr' else l + '/') + slug
    sw = '<div class="lang" aria-label="' + {'fr': 'Langue', 'de': 'Sprache', 'en': 'Language'}[lg] + '">' + ''.join(
        f'<a href="{lk(l)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == lg else '') + f'>{l.upper()}</a>' for l in ('fr', 'de', 'en')) + '</div>'
    doc = doc.replace('<!--LANG-->', sw).replace('<link rel="canonical"', alt + '\n<link rel="canonical"', 1)
    doc = doc.replace(WA_TXT['fr'], WA_TXT[lg])
    if lg == 'fr': return doc
    t = TR[lg]
    def tr(s):
        k = s.strip()
        if not k: return s
        if k in t: return s[:len(s) - len(s.lstrip())] + t[k] + s[len(s.rstrip()):]
        if re.search(r'[a-zà-ÿ]{3}', k) and not k.startswith('http') and '@' not in k and k not in ('website', 'summary_large_image', 'width=device-width, initial-scale=1') and k not in ('Leadr', 'Luc Rohmer', 'LinkedIn', 'WhatsApp', 'Leadr GmbH', 'Romandie', 'Deutschschweiz', 'Paris', 'Lyon', 'Lausanne'):
            MISSING.add((lg, k))
        return s
    parts = re.split(r'(<script.*?</script>)', doc, flags=re.S)
    out = []
    for p in parts:
        if p.startswith('<script type="application/ld+json">'):
            d = json.loads(p[len('<script type="application/ld+json">'):-len('</script>')])
            if 'description' in d: d['description'] = tr(d['description'])
            for q in d.get('mainEntity', []):
                q['name'] = tr(q['name']); q['acceptedAnswer']['text'] = tr(q['acceptedAnswer']['text'])
            out.append('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>')
        elif p.startswith('<script'):
            out.append(p)
        else:
            p = re.sub(r'>([^<]+)<', lambda m: '>' + html.escape(tr(html.unescape(m.group(1))), quote=False) + '<', p)
            p = re.sub(r'((?:content|alt|aria-label|title)=")([^"]+)(")', lambda m: m.group(1) + html.escape(tr(html.unescape(m.group(2)))) + m.group(3), p)
            out.append(p)
    doc = ''.join(out)
    doc = doc.replace('<html lang="fr" ', f'<html lang="{lg}" ').replace('content="fr_CH"', f'content="{LOCALE[lg]}"')
    doc = doc.replace(f'href="https://www.leadr.ch/{pub}"', f'href="https://www.leadr.ch/{lg}/{pub}"').replace(f'content="https://www.leadr.ch/{pub}"', f'content="https://www.leadr.ch/{lg}/{pub}"')
    doc = doc.replace(f'hreflang="x-default" href="https://www.leadr.ch/{lg}/{pub}"', f'hreflang="x-default" href="https://www.leadr.ch/{pub}"').replace(f'hreflang="fr" href="https://www.leadr.ch/{lg}/{pub}"', f'hreflang="fr" href="https://www.leadr.ch/{pub}"')
    doc = doc.replace('og-image.png', f'og-image-{lg}.png')
    for g in FR_ONLY:
        doc = doc.replace(f'href="{g}"', f'href="../{g}" hreflang="fr"')
    for a in ('href="css/', 'src="js/', 'src="logo', 'src="img/', 'href="favicon'):
        doc = doc.replace(a, a.replace('="', '="../'))
    return doc

# ------------------------------------------------------------------ v2.16 : référencement, FAQ, guides
import markdown as _md

TITLES = {
    'index.html': ('Prospection et implantation en Suisse et en France · Leadr',
                   'Leadr, société suisse basée à Bâle, accompagne les PME, PMI et ETI en Suisse et en France : prospection ciblée, mise en relation, implantation.'),
    'vers-la-suisse.html': ('Entreprise française : vendre et s\'implanter en Suisse · Leadr',
                            'Prospection, mise en relation, normes suisses et implantation : Leadr accompagne les PME, PMI et ETI françaises sur le marché suisse.'),
    'vers-la-france.html': ('Entreprise suisse : se développer en France · Leadr',
                            'Prospection ciblée, réseaux régionaux et mise en relation avec les bons décideurs : Leadr accompagne les entreprises suisses en France.'),
    'entre-regions-suisses.html': ('Vendre en Suisse alémanique ou en Suisse romande · Leadr',
                                   'Franchir le Röstigraben : prospection, codes d\'affaires et mise en relation pour les entreprises suisses qui visent l\'autre région linguistique.'),
    'methode.html': ('Notre méthode d\'accompagnement en quatre temps · Leadr',
                     'Cadrer, valider, construire, activer : la méthode Leadr pour ouvrir un nouveau marché en Suisse ou en France, du diagnostic aux premiers clients.'),
    'leadr.html': ('Qui sommes-nous · Leadr GmbH, Bâle',
                   'Leadr GmbH, société suisse basée à Bâle et dirigée par Luc Rohmer : prospection, accompagnement et mise en relation entre la France et la Suisse.'),
    'premier-rendez-vous.html': ('Premier rendez-vous : un avis franc sur votre projet · Leadr',
                                 'Un premier rendez-vous pour comprendre votre projet en Suisse ou en France et vous donner un avis franc sur son potentiel.'),
    'implantation.html': ('Créer sa société en Suisse ou en France · Leadr',
                          'Créer une société en Suisse ou en France au bon moment : choix de la structure, constitution, banque, conformité, avec un seul interlocuteur.'),
    'relocalisation.html': ('Relocalisation d\'activité en Suisse · Leadr',
                            'Transférer un siège, un centre de décision ou une activité en Suisse : accompagnement de la décision jusqu\'à l\'installation des équipes.'),
    'cas-clients.html': ('Cas clients : prospection et implantation en Suisse · Leadr',
                         'Des missions réelles entre la France et la Suisse, présentées de façon anonyme : normes, prospection ciblée, création de société.'),
    'reperes.html': ('Repères et guides pour s\'implanter en Suisse · Leadr',
                     'Guides 2026 pour les PME françaises : implantation en Suisse, prospection externalisée, marketing externalisé, et les repères clés du marché suisse.'),
    'contact.html': ('Contact et prise de rendez-vous · Leadr',
                     'Réservez un appel de prise de contact avec Luc Rohmer, CEO de Leadr, ou présentez votre projet par écrit.'),
}
for _s, (_t, _d) in TITLES.items():
    PAGES[_s]['title'], PAGES[_s]['desc'] = _t, _d

def faq_ld(items):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False) + '</script>'

FAQ_CH = [
    ('Comment une entreprise française peut-elle prospecter en Suisse ?', 'En ciblant d\'abord une région linguistique et quelques cantons, puis en approchant directement les décideurs identifiés, idéalement avec une recommandation. Le démarchage de masse fonctionne mal en Suisse : les acheteurs choisissent lentement, sur la base de la confiance et de références concrètes. Notre prospection est donc ciblée : quelques interlocuteurs justes, approchés un par un.'),
    ('Faut-il créer une société en Suisse pour y vendre ?', 'Pas au début. Une entreprise française peut vendre ses produits depuis la France et fournir des prestations en Suisse jusqu\'à 90 jours par an, après une annonce préalable. Au-delà de 100 000 francs de chiffre d\'affaires mondial avec une activité imposable en Suisse, l\'inscription à la TVA suisse s\'impose, avec un représentant fiscal. La société suisse se justifie quand l\'activité est installée.'),
    ('Par quelle région de Suisse commencer ?', 'Cela dépend de votre secteur et de vos clients cibles. La Suisse romande est plus accessible pour une entreprise française, mais la Suisse alémanique pèse la majorité de l\'économie du pays. Nous recommandons souvent un premier marché test, puis une extension réfléchie de l\'autre côté du Röstigraben.'),
    ('Mes produits doivent-ils être adaptés aux normes suisses ?', 'Souvent, oui. La Suisse reprend une grande partie des normes européennes, mais des prescriptions fédérales ou cantonales s\'ajoutent dans certains domaines, comme la construction ou la sécurité. Nous recherchons les textes applicables à la source avant que vous ne commenciez à vendre.'),
    ('Combien de temps faut-il pour obtenir des résultats en Suisse ?', 'Les premiers rendez-vous qualifiés arrivent dès la phase d\'activation, mais une présence commerciale durable se construit généralement sur 18 à 24 mois. Les acheteurs suisses prennent le temps de décider, et restent fidèles ensuite.'),
]
FAQ_FR = [
    ('Comment une entreprise suisse peut-elle prospecter en France ?', 'En ciblant des régions précises plutôt que « la France » dans son ensemble. Le pays est centralisé dans ses textes mais très régional dans ses réseaux : chaque bassin économique a ses décideurs, ses salons et ses relais. Nous identifions les interlocuteurs qui comptent et vous présentons directement.'),
    ('Faut-il créer une société en France ?', 'Pas forcément au départ. Selon votre activité, vous pouvez vendre depuis la Suisse, travailler avec un agent commercial ou ouvrir un bureau de liaison. Les obligations de TVA et de représentation fiscale sont à vérifier selon votre cas. La filiale française se justifie quand l\'activité est installée.'),
    ('Par quelle région de France commencer ?', 'Par celle où vos clients cibles sont concentrés, pas forcément la plus proche. Chaque filière a ses pôles : l\'industrie, la santé, l\'énergie ou l\'agroalimentaire n\'ont pas la même géographie. Le premier rendez-vous sert aussi à faire ce choix.'),
    ('Quelles différences entre la France et la Suisse dans les affaires ?', 'En France, les décisions remontent souvent plus haut dans la hiérarchie et la relation personnelle pèse beaucoup. Les rendez-vous s\'obtiennent plus facilement avec une recommandation, et les négociations sont souvent plus directes qu\'en Suisse.'),
]
FAQ_RG = [
    ('Qu\'est-ce que le Röstigraben, et pourquoi compte-t-il en affaires ?', 'C\'est la frontière culturelle entre la Suisse romande et la Suisse alémanique. Au-delà de la langue, les habitudes d\'achat, la façon de décider et les réseaux professionnels diffèrent. Une offre qui fonctionne à Lausanne doit souvent être repensée pour Zurich ou Bâle.'),
    ('Est-il possible de prospecter en Suisse alémanique en français ?', 'Pour quelques contacts, parfois. Pour développer une vraie activité, non : les décideurs alémaniques attendent des échanges en allemand et des supports pensés pour leurs codes, pas une simple traduction. Nous préparons l\'approche et vous mettons en relation avec les bons interlocuteurs.'),
    ('Comment une entreprise alémanique peut-elle se développer en Suisse romande ?', 'En adaptant son discours au marché romand, plus proche de la culture française dans le ton et la relation, et en s\'appuyant sur des relais locaux. Nous identifions les décideurs et les réseaux romands qui comptent pour votre secteur.'),
    ('Faut-il une adresse dans l\'autre région linguistique ?', 'Pas au début. Une présence se construit d\'abord par les clients. Une adresse ou une équipe locale se justifie ensuite, quand l\'activité le demande.'),
]

def _insert_before_cta(slug, blocks):
    b = PAGES[slug]['body']
    i = max(k for k, x in enumerate(b) if 'class="cta"' in x)
    PAGES[slug]['body'] = b[:i] + blocks + b[i:]

# ---- guides (articles en français uniquement)
ARTICLES = [
    dict(slug='implantation-suisse-pme-francaises.html', md='implantation-suisse-pme-francaises.md',
         title='Implantation en Suisse pour PME françaises : guide 2026 · Leadr',
         h1='Implantation en Suisse pour PME françaises : comment choisir le bon partenaire',
         desc='Implantation en Suisse pour PME françaises en 2026 : modalités, coûts, erreurs à éviter et critères pour choisir le bon partenaire. Guide par Leadr.',
         short='Modalités, structures juridiques, erreurs à éviter et critères pour choisir le bon partenaire.',
         card='Implantation en Suisse', pub='2026-09-09', mod='2026-10-02', date_fr='2 octobre 2026'),
    dict(slug='prospection-externalisee-suisse.html', md='prospection-externalisee-suisse.md',
         title='Prospection externalisée en Suisse : guide 2026 · Leadr',
         h1='Prospection externalisée en Suisse : comment choisir le bon prestataire',
         desc='Prospection commerciale externalisée pour vendre en Suisse depuis la France en 2026 : quand la choisir, combien elle coûte, comment choisir le bon prestataire.',
         short='Quand la choisir, combien elle coûte, et comment choisir le bon prestataire.',
         card='Prospection externalisée', pub='2026-09-10', mod='2026-10-02', date_fr='2 octobre 2026'),
    dict(slug='marketing-externalise-suisse.html', md='marketing-externalise-suisse.md',
         title='Marketing externalisé pour la Suisse : guide 2026 · Leadr',
         h1='Marketing externalisé : comment adapter sa marque au marché suisse',
         desc='Marketing externalisé pour se développer en Suisse en 2026 : comment adapter sa marque, son site et son discours au marché suisse. Guide par Leadr.',
         short='Adapter sa marque, son site et son discours au marché suisse, sans simple traduction.',
         card='Marketing externalisé', pub='2026-10-01', mod='2026-10-02', date_fr='2 octobre 2026'),
]
FR_ONLY = {a['slug'] for a in ARTICLES}

def guides_block(k='Guides 2026', title='Nos guides pour aller plus loin.', exclude=None, tone='sec-white', intro=''):
    items = [(a['card'], a['short'], a['slug'], 'Lire le guide') for a in ARTICLES if a['slug'] != exclude]
    return cols(k, title, items, intro=intro, tone=tone)

def _article_html(a):
    src = open(os.path.join('articles', a['md']), encoding='utf-8').read()
    # FAQ (section 7) pour le balisage
    faq_part = src.split('## 7.', 1)[1]
    qa = re.findall(r'^### (.+?)\n\n(.+?)(?=\n\n### |\n\n\*Sources|\Z)', faq_part, flags=re.S | re.M)
    body = _md.markdown(src, extensions=['tables', 'sane_lists', 'toc'])
    ids = re.findall(r'<h2 id="([^"]+)">\d+\.', body)
    m = re.search(r'(<h2 id="[^"]*">Sommaire</h2>\s*<ol>)(.*?)(</ol>)', body, flags=re.S)
    if m and ids:
        lis = re.findall(r'<li>(.*?)</li>', m.group(2), flags=re.S)
        new = ''.join(f'<li><a href="#{ids[i]}">{t}</a></li>' if i < len(ids) else f'<li>{t}</li>' for i, t in enumerate(lis))
        body = body[:m.start(2)] + new + body[m.end(2):]
    body = body.replace('<table>', '<div class="table-scroll"><table>').replace('</table>', '</table></div>')
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['desc'],
          "datePublished": a['pub'], "dateModified": a['mod'], "inLanguage": "fr",
          "author": {"@type": "Person", "name": "Luc Rohmer", "jobTitle": "CEO", "url": "https://www.leadr.ch/leadr.html"},
          "publisher": {"@type": "Organization", "name": "Leadr GmbH", "logo": {"@type": "ImageObject", "url": "https://www.leadr.ch/logo.png"}},
          "mainEntityOfPage": "https://www.leadr.ch/" + a['slug']}
    head_ = f'''<section class="hero hero-small"><div class="wrap"><div class="hero-txt">
  <p class="kicker"><a href="reperes.html">Repères</a> · Guide 2026</p><h1>{a['h1']}</h1>
  <p class="art-meta">Par Luc Rohmer, CEO de Leadr · Mis à jour le {a['date_fr']}</p></div></div></section>'''
    art = f'<section class="sec sec-white"><div class="wrap"><article class="article-body">{body}</article></div></section>'
    return [head_, art, guides_block('À lire aussi', 'Les autres guides.', exclude=a['slug'], tone=''),
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
            faq_ld([(q.strip(), re.sub(r'\s+', ' ', r.strip())) for q, r in qa]),
            cta('Votre projet mérite un avis franc ?', 'Un premier rendez-vous pour voir comment ce guide s\'applique à votre situation.')]

for _a in ARTICLES:
    PAGES[_a['slug']] = dict(title=_a['title'], desc=_a['desc'], body=_article_html(_a), fr_only=True)

_insert_before_cta('vers-la-suisse.html', [faq('Vendre et s\'implanter en Suisse : vos questions.', FAQ_CH), faq_ld(FAQ_CH),
                                           guides_block(intro='Pour approfondir, nos guides détaillés (en français).')])
_insert_before_cta('vers-la-france.html', [faq('Se développer en France : vos questions.', FAQ_FR, tone='sec-white'), faq_ld(FAQ_FR)])
_insert_before_cta('entre-regions-suisses.html', [faq('Franchir le Röstigraben : vos questions.', FAQ_RG, tone='sec-white'), faq_ld(FAQ_RG)])
_insert_before_cta('reperes.html', [guides_block(intro='Des guides complets, mis à jour régulièrement, pour préparer votre arrivée sur le marché suisse (en français).')])
_insert_before_cta('implantation.html', [guides_block(intro='Pour approfondir, nos guides détaillés (en français).')])

REDIRECTS['delegation-commerciale'] = 'prospection-externalisee-suisse.html'
REDIRECTS['privacy-policy'] = 'mentions-legales.html'

# ------------------------------------------------------------------ build
def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree('static', OUT)
    for slug, p in PAGES.items():
        body = '\n'.join(p['body'])
        for a, b in ((' ?', '\u00a0?'), (' :', '\u00a0:'), (' !', '\u00a0!'), ('« ', '«\u00a0'), (' »', '\u00a0»')):
            body = body.replace(a, b)
        body = re.sub(r'<a ([^>]*?)href="contact.html"([^>]*)>(Prendre rendez-vous|Choisir un créneau)</a>', lambda m: f'<a {m.group(1)}href="{BOOK}" target="_blank" rel="noopener"{m.group(2)}>{m.group(3)}</a>', body)
        doc = head(p['title'], p['desc'].replace('"', '&quot;'), slug) + header(slug) + body + FOOT
        doc = re.sub(r'<a ([^>]*?)href="contact.html"([^>]*)>Prendre rendez-vous</a>', lambda m: f'<a {m.group(1)}href="{BOOK}" target="_blank" rel="noopener"{m.group(2)}>Prendre rendez-vous</a>', doc)
        if p.get('fr_only'):
            d = localize(doc, 'fr', slug)
            d = re.sub(r'<link rel="alternate" hreflang="(de|en)"[^>]*>', '', d)
            d = d.replace(f'href="de/{slug}"', 'href="de/reperes.html"').replace(f'href="en/{slug}"', 'href="en/reperes.html"')
            open(os.path.join(OUT, slug), 'w', encoding='utf-8').write(d)
            continue
        open(os.path.join(OUT, slug), 'w', encoding='utf-8').write(localize(doc, 'fr', slug))
        for lg in ('de', 'en'):
            os.makedirs(os.path.join(OUT, lg), exist_ok=True)
            open(os.path.join(OUT, lg, slug), 'w', encoding='utf-8').write(localize(doc, lg, slug))
    json.dump({'redirects': [{'source': '/' + a, 'destination': '/' + b, 'permanent': True} for a, b in REDIRECTS.items()],
               'headers': [{'source': '/(.*)', 'has': [{'type': 'host', 'value': 'leadr-site.vercel.app'}],
                            'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex, nofollow'}]}]},
              open(os.path.join(OUT, 'vercel.json'), 'w'), indent=2)
    urls = ''.join(f'<url><loc>https://www.leadr.ch/{p}{"" if s=="index.html" else s}</loc><lastmod>2026-10-02</lastmod></url>' for s in PAGES for p in (('',) if PAGES[s].get('fr_only') else ('', 'de/', 'en/')))
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://www.leadr.ch/sitemap.xml\n')
    print('pages:', len(PAGES), 'x3 langues')
    for m in sorted(MISSING): print('NON TRADUIT', m)

if __name__ == '__main__':
    build()
