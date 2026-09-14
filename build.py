#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur statique du site Leadr — nav/footer partagés, contenu par page."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

PRIMARY_NAV = [
    ("implantation.html", "S'implanter"),
    ("developpement-commercial.html", "Se développer"),
    ("methode.html", "Méthode"),
    ("ressources.html", "Ressources"),
    ("leadr.html", "LEADR"),
]

FOOTER_GROUPS = [
    ("Votre projet", [
        ("implantation.html", "S'implanter"),
        ("developpement-commercial.html", "Se développer"),
        ("validation-marche.html", "Valider un marché"),
        ("relocalisation.html", "Relocalisation"),
    ]),
    ("Approche", [
        ("methode.html", "Méthode"),
        ("session-cadrage.html", "Session de cadrage"),
        ("management-transition.html", "Management de transition"),
        ("partenaires.html", "Partenaires"),
    ]),
    ("Leadr", [
        ("offre-pme-pmi.html", "Offre PME/PMI"),
        ("offre-eti-grands-comptes.html", "Offre ETI & Grands comptes"),
        ("cas-clients.html", "Cas clients"),
        ("ressources.html", "Ressources"),
        ("leadr.html", "LEADR"),
        ("contact.html", "Contact"),
        ("https://www.linkedin.com", "LinkedIn"),
    ]),
]

def render_nav(current):
    items = []
    for href, label in PRIMARY_NAV:
        cur = ' aria-current="page"' if href == current else ''
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    cta_cur = ' aria-current="page"' if current == "contact.html" else ''
    items.append(f'<li class="nav-cta"><a href="contact.html" class="btn btn-primary"{cta_cur}>Parler de votre projet</a></li>')
    return "\n      ".join(items)

def render_footer():
    cols = []
    logo_col = '''<div>
        <a href="index.html" class="logo footer-logo"><span class="lead">Lead</span><span class="r">r</span></a>
        <p style="margin-top:14px; font-size:14px; color:#cfcac0;">Développer et structurer une présence entre la France et la Suisse.</p>
        <p style="font-size:13.5px; color:#9b968c; margin-bottom:4px;">Bâle, Suisse</p>
        <p style="font-size:13.5px; color:#9b968c;"><a href="mailto:lrohmer@leadr.ch">lrohmer@leadr.ch</a></p>
      </div>'''
    cols.append(logo_col)
    for title, links in FOOTER_GROUPS:
        li_items = []
        for href, label in links:
            extra_attr = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            li_items.append(f'<li><a href="{href}"{extra_attr}>{label}</a></li>')
        lis = "\n          ".join(li_items)
        cols.append(f'''<div>
        <h4>{title}</h4>
        <ul>
          {lis}
        </ul>
      </div>''')
    return "\n      ".join(cols)

PAGE_SHELL = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://leadr.ch/{slug}">
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<header class="site-header">
  <nav class="nav-bar">
    <a href="index.html" class="logo"><span class="lead">Lead</span><span class="r">r</span></a>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks">Menu</button>
    <ul class="nav-links" id="navLinks">
      {nav}
    </ul>
  </nav>
</header>

<main>
{content}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      {footer}
    </div>
    <div class="footer-bottom">
      <span>© 2026 Leadr GmbH. Tous droits réservés.</span>
      <span>Bâle, Suisse</span>
    </div>
  </div>
</footer>

<script>
  var navToggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');
  navToggle.addEventListener('click', function () {{
    var open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }});
</script>

</body>
</html>
'''

def page(slug, title, description, content):
    filename = slug if slug.endswith(".html") else slug + ".html"
    html = PAGE_SHELL.format(
        title=title,
        description=description,
        slug=filename,
        nav=render_nav(filename),
        content=content,
        footer=render_footer(),
    )
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


# ============================================================
# INDEX — HOMEPAGE (7 sections)
# ============================================================
index_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">France ↔ Suisse</p>
      <h1>Développer votre activité entre la France et la Suisse. Avec une stratégie adaptée à chaque marché.</h1>
      <p class="lede">Leadr aide les entreprises françaises et suisses à valider leur marché, développer leur activité et structurer leur présence de l'autre côté de la frontière.</p>
      <div class="btn-row">
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
        <a href="methode.html" class="btn btn-outline">Découvrir notre approche</a>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Où en êtes-vous ?</p>
        <h2>Où en êtes-vous dans votre projet ?</h2>
      </div>
      <div class="grid-4">
        <a href="validation-marche.html" class="card" style="text-decoration:none;">
          <h3>Tester un nouveau marché</h3>
          <p>Évaluer si une offre a un potentiel réaliste avant d'engager des ressources.</p>
        </a>
        <a href="developpement-commercial.html" class="card" style="text-decoration:none;">
          <h3>Trouver ses premiers clients</h3>
          <p>Construire une traction commerciale réelle sur le marché visé.</p>
        </a>
        <a href="implantation.html" class="card" style="text-decoration:none;">
          <h3>S'implanter localement</h3>
          <p>Structurer une présence locale, lorsque cela devient nécessaire.</p>
        </a>
        <a href="relocalisation.html" class="card" style="text-decoration:none;">
          <h3>Développer ou relocaliser une activité</h3>
          <p>Piloter des projets stratégiques, industriels ou organisationnels plus larges.</p>
        </a>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Deux marchés, plusieurs réalités locales</p>
        <h2>Ni la France ni la Suisse ne sont des marchés uniformes</h2>
        <p class="lede">Fédérale, cantonale et multilingue côté suisse, régionale et sectorielle côté français : une stratégie pertinente à Genève n'est pas automatiquement celle qui fonctionnera à Bâle, Lyon ou Paris.</p>
      </div>
      <div class="tag-row">
        <span class="region-tag">26 cantons suisses</span>
        <span class="region-tag">Régions linguistiques</span>
        <span class="region-tag">Bassins économiques français</span>
        <span class="region-tag">Réseaux locaux</span>
      </div>
    </div>
  </section>

  <section class="section-border-top section-dark">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Méthode Leadr</p>
        <h2>Quatre étapes, dans l'ordre</h2>
      </div>
      <div class="grid-4">
        <div><h3>Cadrer</h3><p style="color:#d8d4cb;">Comprendre l'entreprise, l'offre, les objectifs et les contraintes.</p></div>
        <div><h3>Valider</h3><p style="color:#d8d4cb;">Confronter les hypothèses à la réalité du marché visé.</p></div>
        <div><h3>Construire</h3><p style="color:#d8d4cb;">Définir la feuille de route commerciale et opérationnelle adaptée.</p></div>
        <div><h3>Activer</h3><p style="color:#d8d4cb;">Passer de la recommandation à l'action commerciale concrète.</p></div>
      </div>
      <div class="btn-row"><a href="methode.html" class="btn btn-outline-light">Voir la méthode en détail</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">La différence Leadr</p>
        <h2>Le conseil ne suffit pas lorsqu'il faut entrer sur un nouveau marché</h2>
      </div>
      <div class="grid-3">
        <div class="card">
          <h3>Terrain</h3>
          <p>Confronter les hypothèses à la réalité du marché, région par région, secteur par secteur.</p>
        </div>
        <div class="card">
          <h3>Accès</h3>
          <p>Mobiliser les relations et les ressources spécialisées pertinentes, quand elles sont utiles au projet.</p>
        </div>
        <div class="card">
          <h3>Exécution</h3>
          <p>Passer de la recommandation à la mise en œuvre concrète, sur le terrain.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">

      <div class="confidential-banner">
        <p class="eyebrow">Confidentialité</p>
        <p>Pour des raisons de secret professionnel, aucun nom d'entreprise ni chiffre d'affaires nominatif n'est diffusé publiquement. Les cas ci-dessous sont présentés par secteur, de façon anonymisée.</p>
      </div>

      <div class="grid-2">
        <div class="card">
          <h3>Industrie de précision & manufacturier</h3>
          <p><strong>Objectif :</strong> s'implanter en respectant les spécificités de la main-d'œuvre locale et des process de production.</p>
          <p><strong>Actions réalisées :</strong> coordination de l'implantation locale, mise en conformité réglementaire, activation des premiers contacts industriels.</p>
        </div>
        <div class="card">
          <h3>Technologies de l'information</h3>
          <p><strong>Objectif :</strong> assurer la conformité aux exigences locales de protection des données.</p>
          <p><strong>Actions réalisées :</strong> structuration d'une filiale technologique, coordination d'un hébergement conforme.</p>
        </div>
      </div>
      <div class="btn-row"><a href="cas-clients.html" class="btn btn-outline">Voir tous les cas clients</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div>
          <h2>Vous avez un projet entre la France et la Suisse ?</h2>
          <p>Avant de parler de structure, de prospection ou de partenaires, commençons par comprendre votre projet.</p>
        </div>
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
      </div>
    </div>
  </section>
'''

page("index.html", "Leadr · Développer votre activité entre la France et la Suisse",
     "Leadr aide les entreprises françaises et suisses à valider leur marché, développer leur activité et structurer leur présence de l'autre côté de la frontière.",
     index_content)


# ============================================================
# S'IMPLANTER
# ============================================================
implantation_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Structurer une présence locale</p>
      <h1>S'implanter</h1>
      <p class="lede">Lorsqu'une présence locale devient nécessaire, structurer une implantation en France ou en Suisse suppose une entité adaptée, une conformité rigoureuse et une gouvernance pensée pour durer.</p>
      <div class="btn-row"><a href="contact.html" class="btn btn-primary">Parler de votre projet</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Ce que couvre une implantation</p>
        <h2>Trois volets à sécuriser</h2>
      </div>
      <div class="grid-3">
        <div class="card"><h3>Structure légale</h3><p>Choix et constitution de l'entité adaptée au projet et à la localisation visée.</p></div>
        <div class="card"><h3>Conformité</h3><p>Alignement sur les obligations réglementaires et sociales du pays d'arrivée.</p></div>
        <div class="card"><h3>Gouvernance locale</h3><p>Organisation pensée pour durer, y compris lorsqu'une direction temporaire est nécessaire le temps du recrutement définitif.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Deux formats</p>
        <h2>Un format calibré à la taille du projet</h2>
        <p class="lede">Le format retenu dépend de la taille de la structure et de l'ampleur du projet : plus léger pour une PME ou une PMI, plus structuré pour une ETI ou un grand compte.</p>
      </div>
      <div class="grid-2">
        <div class="card"><h3>PME & PMI</h3><p>Un format léger, une à deux personnes mobilisées.</p><div class="btn-row"><a href="offre-pme-pmi.html" class="btn btn-outline">Voir le format PME/PMI</a></div></div>
        <div class="card"><h3>ETI & Grands comptes</h3><p>Une feuille de route de phasage complète et une gouvernance locale pérenne.</p><div class="btn-row"><a href="offre-eti-grands-comptes.html" class="btn btn-outline">Voir le format ETI</a></div></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Cadrer votre projet d'implantation</h2><p>Un premier échange pour vérifier la faisabilité.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("implantation.html", "S'implanter · Leadr",
     "Structurer une présence locale en France ou en Suisse : entité, conformité et gouvernance, dans un format calibré à la taille du projet.",
     implantation_content)


# ============================================================
# SE DÉVELOPPER COMMERCIALEMENT
# ============================================================
developpement_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Construire une traction commerciale</p>
      <h1>Se développer commercialement</h1>
      <p class="lede">Trouver ses premiers clients de l'autre côté de la frontière, activer un réseau pertinent et construire une traction commerciale réelle, avant ou en parallèle de toute structuration.</p>
      <div class="btn-row"><a href="contact.html" class="btn btn-primary">Parler de votre projet</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Une approche calibrée</p>
        <h2>Un développement pensé par région et par secteur</h2>
        <p class="lede">Le canal d'accès pertinent, le cycle de vente et les décideurs à identifier varient selon le pays, la région et le secteur d'activité. Le développement commercial se construit sur cette réalité, pas sur une approche uniforme du marché visé.</p>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Pour aller plus loin</p>
        <h2>Selon la maturité du projet</h2>
      </div>
      <div class="grid-2">
        <div class="card"><h3>Le marché n'est pas encore validé</h3><p>Une première étape de validation permet de vérifier le potentiel avant d'investir davantage.</p><div class="btn-row"><a href="validation-marche.html" class="btn btn-outline">Valider un marché</a></div></div>
        <div class="card"><h3>Une présence locale devient nécessaire</h3><p>La structuration s'engage une fois la dynamique commerciale enclenchée.</p><div class="btn-row"><a href="implantation.html" class="btn btn-outline">S'implanter</a></div></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Parlons de votre développement commercial</h2><p>Un premier échange pour cadrer les prochaines étapes.</p></div>
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
      </div>
    </div>
  </section>
'''
page("developpement-commercial.html", "Se développer commercialement · Leadr",
     "Trouver ses premiers clients de l'autre côté de la frontière et construire une traction commerciale réelle, avec une approche calibrée par région et par secteur.",
     developpement_content)


# ============================================================
# VALIDER UN MARCHÉ
# ============================================================
validation_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Avant d'engager des ressources</p>
      <h1>Valider un marché</h1>
      <p class="lede">Vérifier si une offre a un potentiel réaliste sur un nouveau marché avant d'engager des ressources significatives : réceptivité du marché, positionnement face à la concurrence locale, premiers signaux commerciaux.</p>
      <div class="btn-row"><a href="contact.html" class="btn btn-primary">Parler de votre projet</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Le principe</p>
        <h2>Valider avant de structurer, chaque fois que possible</h2>
        <p class="lede">Dans la mesure du possible, la réalité commerciale du marché visé est vérifiée avant d'engager des coûts fixes importants. Certaines activités, certaines réglementations ou certains modèles économiques peuvent toutefois demander une structuration locale plus tôt : dans ce cas, la structuration fait partie de la feuille de route dès le départ.</p>
      </div>
      <div class="grid-3">
        <div class="card"><h3>Réceptivité du marché</h3><p>Premiers retours sur l'offre auprès d'interlocuteurs locaux pertinents.</p></div>
        <div class="card"><h3>Positionnement local</h3><p>Lecture de l'offre face à la concurrence déjà présente sur le marché visé.</p></div>
        <div class="card"><h3>Canaux d'accès</h3><p>Identification des canaux pertinents selon la région et le secteur concernés.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Vérifier le potentiel de votre offre</h2><p>Ce sujet se cadre dès le premier échange.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("validation-marche.html", "Valider un marché · Leadr",
     "Vérifier le potentiel réaliste d'une offre sur un nouveau marché avant d'engager des ressources significatives.",
     validation_content)


# ============================================================
# RELOCALISATION ET IMPLANTATION STRATÉGIQUE
# ============================================================
relocalisation_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Projets d'envergure</p>
      <h1>Développer ou relocaliser une activité</h1>
      <p class="lede">Pour les projets plus substantiels, avec des enjeux organisationnels, industriels ou stratégiques plus larges, une implantation ou une relocalisation entre la France et la Suisse se prépare avec une feuille de route dédiée.</p>
      <div class="btn-row"><a href="contact.html" class="btn btn-primary">Parler de votre projet</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Pour qui</p>
        <h2>Des projets à enjeux organisationnels</h2>
        <p class="lede">Ce type de projet concerne des entreprises qui évaluent une implantation, une relocalisation ou un développement stratégique de plus grande ampleur, au-delà d'une simple ouverture commerciale.</p>
      </div>
      <div class="btn-row"><a href="offre-eti-grands-comptes.html" class="btn btn-outline">Voir le format ETI & Grands comptes</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Continuité opérationnelle</p>
        <h2>Un dispositif de management de transition, si nécessaire</h2>
        <p class="lede">Pour éviter toute vacance sur un poste critique le temps du recrutement définitif, un dispositif de direction locale temporaire peut être mobilisé.</p>
      </div>
      <div class="btn-row"><a href="management-transition.html" class="btn btn-outline">Voir le management de transition</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Cadrer un projet d'envergure</h2><p>Chaque projet de cette nature se cadre individuellement.</p></div>
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
      </div>
    </div>
  </section>
'''
page("relocalisation.html", "Relocalisation et implantation stratégique · Leadr",
     "Des projets d'implantation ou de relocalisation plus substantiels entre la France et la Suisse, avec une feuille de route dédiée.",
     relocalisation_content)


# ============================================================
# MÉTHODE
# ============================================================
methode_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Comment Leadr travaille</p>
      <h1>La méthode Leadr</h1>
      <p class="lede">Un filtre d'entrée, puis un déroulé en quatre étapes : cadrer, valider, construire, activer. Chaque étape a un objectif clair.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Avant tout</p>
        <h2>Une question de faisabilité</h2>
        <p class="lede">Leadr travaille en priorité avec des offres dont la valeur peut raisonnablement se commercialiser en dehors de leur cadre national d'origine. Certaines activités, comme celles soumises à une licence locale, une autorisation, une qualification reconnue ou une réglementation sectorielle spécifique, demandent une évaluation de faisabilité complémentaire avant toute chose. Ce point se vérifie au cas par cas, sans conclusion juridique ou réglementaire présumée.</p>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Le déroulé</p>
        <h2>Quatre étapes, dans l'ordre</h2>
      </div>

      <div class="jalon">
        <div class="jalon-num">01</div>
        <div><h3>Cadrer</h3><p>Comprendre l'entreprise, l'offre, les objectifs et les contraintes du projet.</p></div>
      </div>
      <div class="jalon">
        <div class="jalon-num">02</div>
        <div><h3>Valider</h3><p>Confronter les hypothèses à la réalité du marché visé : réceptivité, positionnement, premiers signaux.</p></div>
      </div>
      <div class="jalon">
        <div class="jalon-num">03</div>
        <div><h3>Construire</h3><p>Définir la feuille de route commerciale et opérationnelle adaptée au projet, structuration comprise si nécessaire.</p></div>
      </div>
      <div class="jalon">
        <div class="jalon-num">04</div>
        <div><h3>Activer</h3><p>Passer de la recommandation à l'action commerciale concrète, sur le terrain.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Un horizon indicatif</p>
        <h2>Pas de promesse de calendrier</h2>
        <p class="lede">Construire une présence durable sur un nouveau marché demande souvent une perspective de long terme, de l'ordre de 18 à 24 mois selon les projets. Ce n'est ni un minimum légal, ni une durée garantie, ni une règle universelle : chaque projet a son propre calendrier.</p>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Votre projet correspond-il à cette approche ?</h2><p>La session de cadrage permet de le vérifier.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("methode.html", "Méthode Leadr",
     "La méthode Leadr en quatre étapes : cadrer, valider, construire, activer, et le principe de validation avant structuration.",
     methode_content)


# ============================================================
# RESSOURCES
# ============================================================
ressources_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Repères sur les deux marchés</p>
      <h1>Ressources</h1>
      <p class="lede">Quelques repères de base pour structurer une réflexion sur le marché suisse et le marché français, avant d'aller plus loin. Cette section s'enrichira progressivement.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Côté suisse</p>
        <h2>Un pays fédéral et multilingue</h2>
      </div>
      <div class="grid-3">
        <div class="card">
          <h3>Un pays fédéral</h3>
          <p>La Suisse compte 26 cantons, chacun disposant de compétences fiscales, administratives et parfois réglementaires propres. Une approche nationale uniforme ignore souvent cette réalité.</p>
        </div>
        <div class="card">
          <h3>Plusieurs régions linguistiques</h3>
          <p>Suisse romande, Suisse alémanique, Tessin : la langue de travail, les usages commerciaux et les réseaux professionnels diffèrent d'une région à l'autre.</p>
        </div>
        <div class="card">
          <h3>Un cadre réglementaire cantonal</h3>
          <p>Certaines démarches, autorisations ou obligations dépendent du canton d'implantation autant que du cadre fédéral.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Côté français</p>
        <h2>Un marché régionalisé</h2>
      </div>
      <div class="grid-2">
        <div class="card">
          <h3>Des bassins économiques distincts</h3>
          <p>Les dynamiques commerciales, industrielles et les réseaux professionnels varient sensiblement d'une région française à l'autre, et d'une métropole à l'autre.</p>
        </div>
        <div class="card">
          <h3>Un cadre national décliné localement</h3>
          <p>Chambres consulaires, collectivités et administrations régionales jouent un rôle concret dans une implantation, en complément du cadre national.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Une question sur votre situation précise ?</h2><p>Chaque projet a ses propres spécificités.</p></div>
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
      </div>
    </div>
  </section>
'''
page("ressources.html", "Ressources · Leadr",
     "Quelques repères de base pour structurer une réflexion sur le marché suisse et le marché français.",
     ressources_content)


# ============================================================
# LEADR (à propos)
# ============================================================
leadr_content = '''
  <section class="hero">
    <div class="container hero-split">
      <div>
        <p class="eyebrow">Leadr</p>
        <h1>Comprendre le terrain avant d'agir</h1>
        <p class="lede">Leadr aide les entreprises françaises et suisses à valider leur marché, développer leur activité et structurer leur présence de l'autre côté de la frontière, avec une lecture directe des différences réglementaires, culturelles et commerciales entre les deux marchés.</p>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Fondateur</p>
        <h2>Luc Rohmer</h2>
        <p class="lede">Basé à Strasbourg, Luc Rohmer vient du monde de la création de contenu et du marketing avant de fonder Leadr, avec une conviction simple : une présence commerciale se construit par les résultats, pas par la promesse.</p>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Échanger directement</h2><p>Une question, un projet à cadrer : le contact se fait simplement.</p></div>
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
      </div>
    </div>
  </section>
'''
page("leadr.html", "LEADR",
     "Leadr est fondé par Luc Rohmer, basé à Strasbourg, venu du monde de la création de contenu et du marketing.",
     leadr_content)


# ============================================================
# CAS CLIENTS
# ============================================================
cas_clients_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Secteurs d'intervention</p>
      <h1>Cas clients</h1>
      <p class="lede">Un relevé factuel de projets menés par secteur, sans hypothèse théorique.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">

      <div class="confidential-banner">
        <p class="eyebrow">Confidentialité</p>
        <p>Pour des raisons de secret professionnel, aucun nom d'entreprise, aucun chiffre d'affaires nominatif ni aucun partenaire n'est diffusé publiquement sur cette page. Les cas ci-dessous sont présentés par secteur, de façon anonymisée.</p>
      </div>

      <div class="grid-2">
        <div class="card">
          <h3>Industrie de précision & manufacturier</h3>
          <p><strong>Objectif :</strong> s'implanter en respectant les spécificités de la main-d'œuvre locale et des process de production.</p>
          <p><strong>Actions réalisées :</strong> coordination de l'implantation locale, mise en conformité réglementaire, activation des premiers contacts industriels.</p>
        </div>
        <div class="card">
          <h3>Technologies de l'information (IT & SaaS)</h3>
          <p><strong>Objectif :</strong> assurer la conformité aux exigences locales de protection des données pour une activité numérique.</p>
          <p><strong>Actions réalisées :</strong> structuration d'une filiale technologique, détachement de profils commerciaux, coordination d'un hébergement conforme.</p>
        </div>
        <div class="card">
          <h3>Ingénierie & R&D</h3>
          <p><strong>Objectif :</strong> établir une collaboration de recherche transfrontalière sans friction de double imposition ni risque sur le savoir-faire.</p>
          <p><strong>Actions réalisées :</strong> mise en place d'une gouvernance bilatérale cohérente et organisation du transfert de compétences.</p>
        </div>
        <div class="card">
          <h3>Logistique & négoce B2B</h3>
          <p><strong>Objectif :</strong> fluidifier l'acheminement transfrontalier de marchandises techniques.</p>
          <p><strong>Actions réalisées :</strong> définition d'une architecture d'implantation douanière et jalonnement des flux d'approvisionnement.</p>
        </div>
      </div>

    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Votre secteur n'est pas listé ?</h2><p>La faisabilité se vérifie au cas par cas, en session de cadrage.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("cas-clients.html", "Cas clients · Leadr",
     "Des exemples anonymisés de projets menés par Leadr entre la France et la Suisse, par secteur d'activité, dans le respect de la confidentialité des projets.",
     cas_clients_content)


# ============================================================
# SESSION DE CADRAGE
# ============================================================
session_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Premier échange</p>
      <h1>La session de cadrage</h1>
      <p class="lede">Avant toute chose, un échange direct pour comprendre votre projet : objectifs commerciaux, maturité du marché, priorités géographiques, points réglementaires à vérifier, ressources disponibles, voie d'entrée envisageable.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Ce qui est examiné</p>
        <h2>Ce que couvre l'échange</h2>
      </div>
      <div class="grid-3">
        <div class="card"><h3>Le projet</h3><p>Objectifs commerciaux, priorités géographiques et calendrier envisagé.</p></div>
        <div class="card"><h3>La faisabilité</h3><p>Points réglementaires à vérifier et ressources déjà disponibles.</p></div>
        <div class="card"><h3>La suite</h3><p>La voie d'entrée la plus pertinente : validation, développement commercial, implantation ou relocalisation.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Prêt à en parler ?</h2><p>Un message suffit pour démarrer.</p></div>
        <a href="contact.html" class="btn btn-primary">Parler de votre projet</a>
      </div>
    </div>
  </section>
'''
page("session-cadrage.html", "Session de cadrage · Leadr",
     "La session de cadrage est le premier échange avec Leadr pour comprendre un projet et sa faisabilité entre la France et la Suisse.",
     session_content)


# ============================================================
# MANAGEMENT DE TRANSITION
# ============================================================
management_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Continuité opérationnelle</p>
      <h1>Management de transition</h1>
      <p class="lede">Pour éviter toute vacance sur un poste critique en phase de lancement, une direction locale temporaire peut être mobilisée le temps que le recrutement définitif suive son cours.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Le principe</p>
        <h2>Une continuité assurée entre deux étapes</h2>
        <p class="lede">Entre la création de la structure et l'arrivée d'un dirigeant permanent, une direction locale temporaire prend en charge la continuité opérationnelle : gouvernance, décisions courantes, pilotage de l'activité commerciale.</p>
      </div>
      <div class="grid-3">
        <div class="card"><h3>Ressources</h3><p>Sélection d'un profil local pertinent pour la mission.</p></div>
        <div class="card"><h3>Continuité</h3><p>Gestion des postes de direction sans rupture de rythme sur l'activité.</p></div>
        <div class="card"><h3>Transition</h3><p>Un dispositif souple jusqu'au recrutement définitif, puis passage de témoin organisé.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Le réseau</p>
        <h2>Un dispositif adossé à un réseau de partenaires suisses</h2>
        <p class="lede">Ce dispositif s'appuie aujourd'hui sur un réseau de partenaires suisses spécialisés dans la transition opérationnelle. Leadr reste l'interlocuteur unique du projet et pilote l'ensemble, en toute indépendance.</p>
        <div class="btn-row"><a href="partenaires.html" class="btn btn-outline">Voir les partenaires</a></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Un poste critique à sécuriser ?</h2><p>Ce sujet se cadre dès le premier échange.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("management-transition.html", "Management de transition · Leadr",
     "Le dispositif de direction locale temporaire de Leadr, le temps que le recrutement définitif suive son cours.",
     management_content)


# ============================================================
# PARTENAIRES
# ============================================================
partenaires_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Un acteur indépendant</p>
      <h1>Partenaires</h1>
      <p class="lede">Leadr reste indépendant sur chaque projet, et mobilise, selon les besoins réels, un réseau de partenaires spécialisés.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Les domaines mobilisés</p>
        <h2>Un seul interlocuteur, plusieurs domaines de compétence</h2>
      </div>
      <div class="grid-4">
        <div class="card"><h3>Juridique</h3><p>Structuration légale et mise en conformité.</p></div>
        <div class="card"><h3>Fiduciaire</h3><p>Comptabilité et obligations fiscales locales.</p></div>
        <div class="card"><h3>Bancaire</h3><p>Ouverture et gestion des comptes nécessaires à l'activité.</p></div>
        <div class="card"><h3>Recrutement</h3><p>Profils locaux, y compris en management de transition.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Un projet en tête ?</h2><p>La session de cadrage est le point de départ.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("partenaires.html", "Partenaires · Leadr",
     "Leadr s'appuie sur un réseau de partenaires spécialisés (juridique, fiduciaire, bancaire, recrutement) tout en restant un acteur indépendant.",
     partenaires_content)


# ============================================================
# OFFRE PME & PMI
# ============================================================
pme_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Structures agiles</p>
      <h1>Offre PME & PMI</h1>
      <p class="lede">Un format léger pour les entreprises industrielles et de sous-traitance qui veulent ouvrir un nouveau marché sans engager, dès le départ, une structure lourde.</p>
      <div class="btn-row"><a href="contact.html" class="btn btn-primary">Parler de votre projet</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Pour qui</p>
        <h2>Une équipe restreinte, un projet ciblé</h2>
        <p class="lede">Ce format s'adresse aux PME et PMI qui souhaitent tester puis développer une activité entre la France et la Suisse, quel que soit le sens du projet, avec une à deux personnes mobilisées.</p>
      </div>
      <div class="grid-4">
        <div class="card"><h3>Création d'entité</h3><p>Constitution de la structure légale adaptée.</p></div>
        <div class="card"><h3>Ouverture bancaire</h3><p>Mise en place des comptes nécessaires à l'activité.</p></div>
        <div class="card"><h3>Mise en conformité</h3><p>Alignement sur les obligations réglementaires et sociales.</p></div>
        <div class="card"><h3>Premiers contacts</h3><p>Activation du réseau pour générer les premiers contacts commerciaux réels.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Votre projet correspond à ce format ?</h2><p>La session de cadrage permet de le vérifier.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("offre-pme-pmi.html", "Offre PME & PMI · Leadr",
     "Le format léger de Leadr pour les PME et PMI qui veulent ouvrir un nouveau marché entre la France et la Suisse sans lourde structure.",
     pme_content)


# ============================================================
# OFFRE ETI & GRANDS COMPTES
# ============================================================
eti_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Structures étendues</p>
      <h1>Offre ETI & Grands comptes</h1>
      <p class="lede">Un format structuré pour les ETI et grands comptes qui engagent une implantation d'envergure, avec une gouvernance locale pérenne.</p>
      <div class="btn-row"><a href="contact.html" class="btn btn-primary">Parler de votre projet</a></div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="section-head">
        <p class="eyebrow">Pour qui</p>
        <h2>Une implantation pensée dans la durée</h2>
      </div>
      <div class="grid-3">
        <div class="card"><h3>Feuille de route de phasage</h3><p>Un calendrier complet, étape par étape.</p></div>
        <div class="card"><h3>Management de transition</h3><p>Une direction locale temporaire, le temps du recrutement définitif.</p></div>
        <div class="card"><h3>Gouvernance pérenne</h3><p>Une organisation locale conçue pour durer.</p></div>
      </div>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="cta-band">
        <div><h2>Cadrer votre projet d'implantation</h2><p>Un premier échange pour valider la faisabilité.</p></div>
        <a href="session-cadrage.html" class="btn btn-primary">Réserver une session de cadrage</a>
      </div>
    </div>
  </section>
'''
page("offre-eti-grands-comptes.html", "Offre ETI & Grands comptes · Leadr",
     "Le format structuré de Leadr pour les ETI et grands comptes : feuille de route de phasage et management de transition.",
     eti_content)


# ============================================================
# CONTACT
# ============================================================
contact_content = '''
  <section class="hero">
    <div class="container hero-inner">
      <p class="eyebrow">Prendre contact</p>
      <h1>Parler de votre projet</h1>
      <p class="lede">Un message suffit pour démarrer l'échange. La réponse porte sur la faisabilité de votre projet et les prochaines étapes possibles.</p>
    </div>
  </section>

  <section class="section-border-top">
    <div class="container">
      <div class="grid-2">
        <div>
          <!--
            Formulaire branché sur un service tiers gratuit (Formspree), sans stockage de données côté site.
            À faire avant la mise en ligne : créer un compte sur https://formspree.io, créer un formulaire,
            puis remplacer "VOTRE_ID_FORMSPREE" ci-dessous par l'identifiant fourni.
          -->
          <form action="https://formspree.io/f/VOTRE_ID_FORMSPREE" method="POST">
            <div class="form-row">
              <div><label for="nom">Nom</label><input type="text" id="nom" name="nom" required></div>
              <div><label for="entreprise">Entreprise</label><input type="text" id="entreprise" name="entreprise" required></div>
            </div>
            <div class="form-row">
              <div><label for="email">Email</label><input type="email" id="email" name="email" required></div>
              <div><label for="telephone">Téléphone (facultatif)</label><input type="tel" id="telephone" name="telephone"></div>
            </div>
            <div class="form-row">
              <div>
                <label for="type_projet">Type de projet</label>
                <select id="type_projet" name="type_projet" required>
                  <option value="">Sélectionner</option>
                  <option>Validation de marché</option>
                  <option>Développement commercial</option>
                  <option>Implantation</option>
                  <option>Relocalisation</option>
                  <option>Session de cadrage</option>
                  <option>Autre</option>
                </select>
              </div>
              <div>
                <label for="stade_projet">Stade du projet</label>
                <select id="stade_projet" name="stade_projet" required>
                  <option value="">Sélectionner</option>
                  <option>Réflexion</option>
                  <option>Validation</option>
                  <option>Lancement</option>
                  <option>Déjà présent sur le marché visé</option>
                </select>
              </div>
            </div>
            <div>
              <label for="message">Message</label>
              <textarea id="message" name="message" required placeholder="Quelques lignes sur votre projet."></textarea>
            </div>
            <label style="font-weight:400; font-size:13.5px; display:flex; gap:8px; align-items:flex-start;">
              <input type="checkbox" name="consentement" required style="width:auto; margin-top:3px;">
              <span>J'accepte que ces informations soient utilisées par Leadr pour répondre à ma demande.</span>
            </label>
            <div class="btn-row"><button type="submit" class="btn btn-primary">Envoyer le message</button></div>
          </form>
        </div>

        <div>
          <div class="card-flush">
            <h3>Coordonnées</h3>
            <p style="margin-bottom:6px;"><strong>Leadr GmbH</strong><br>Bâle, Suisse</p>
            <p style="margin-bottom:6px;"><a href="mailto:lrohmer@leadr.ch">lrohmer@leadr.ch</a></p>
            <!-- Remplacer par l'URL réelle de la page LinkedIn Leadr avant mise en ligne -->
            <p><a href="https://www.linkedin.com" target="_blank" rel="noopener">Suivre Leadr sur LinkedIn</a></p>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
page("contact.html", "Contact · Leadr",
     "Prendre contact avec Leadr pour un projet de validation, développement, implantation ou relocalisation entre la France et la Suisse.",
     contact_content)

print("done")
