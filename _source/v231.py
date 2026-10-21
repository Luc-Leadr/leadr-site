# -*- coding: utf-8 -*-
# ------------------------------------------------------------------ v2.31 : SEO double visibilité France et Suisse (21 oct. 2026)
# Chargé à la fin de build.py (exec). Redéfinit localize, seo_ld, finish, guides et build.
# Contenu : adresses allemandes, guides par direction (dont un guide écrit en allemand),
# cas clients chiffrés, FAQ Méthode et Cas clients, titres H1, descriptions, données Organisation et Service,
# dates réelles dans le sitemap, liens vers les pages distributeur depuis l'accueil.
import hashlib

TODAY = '2026-10-21'
LINKEDIN_CO = 'https://www.linkedin.com/company/leadr-ch/'

# ---------------------------------------------------------------- adresses allemandes (m : adresses traduites)
DE_SLUG = {
    'vers-la-suisse.html': 'in-der-schweiz-verkaufen.html',
    'vers-la-france.html': 'expansion-frankreich.html',
    'entre-regions-suisses.html': 'zwischen-sprachregionen.html',
    'methode.html': 'methode.html',
    'leadr.html': 'ueber-uns.html',
    'premier-rendez-vous.html': 'erstgespraech.html',
    'implantation.html': 'firmengruendung.html',
    'relocalisation.html': 'standortverlagerung.html',
    'management-transition.html': 'interim-management.html',
    'cas-clients.html': 'fallbeispiele.html',
    'reperes.html': 'wissenswertes.html',
    'contact.html': 'kontakt.html',
    'mentions-legales.html': 'impressum.html',
    'formats.html': 'mandatsformen.html',
    'distributeur-suisse.html': 'vertriebspartner-schweiz.html',
    'distributeur-france.html': 'vertriebspartner-frankreich.html',
}

def ps(slug, lg):
    """Nom de fichier publié d'une page dans une langue."""
    if slug == 'index.html': return 'index.html'
    if lg == 'de': return PAGES.get(slug, {}).get('de_slug') or DE_SLUG.get(slug, slug)
    return slug

def avail(slug):
    p = PAGES.get(slug, {})
    if p.get('only'): return [p['only']]
    if p.get('fr_only'): return ['fr']
    return ['fr', 'de', 'en']

def url(slug, lg):
    f = ps(slug, lg)
    return 'https://www.leadr.ch/' + ('' if lg == 'fr' else lg + '/') + ('' if f == 'index.html' else f)

def rel(target, lg, anchor=''):
    """Lien relatif depuis une page en langue lg vers la page target, dans la meilleure langue disponible."""
    av = avail(target)
    tl = lg if lg in av else ('fr' if 'fr' in av else av[0])
    here = '' if lg == 'fr' else '../'
    path = here + ('' if tl == 'fr' else tl + '/') + ps(target, tl)
    if path.startswith(lg + '/') and lg != 'fr':
        path = path[len(lg) + 1:]
    if lg != 'fr' and path.startswith('../' + lg + '/'):
        path = path[len('../' + lg + '/'):]
    extra = '' if tl == lg else f' hreflang="{tl}"'
    return path + anchor, extra

# ---------------------------------------------------------------- traductions ajoutées en v2.31
TR_ADD = {'de': {}, 'en': {}}
def _nb(x):
    for a, b in ((' ?', '\u00a0?'), (' :', '\u00a0:'), (' !', '\u00a0!'), ('« ', '«\u00a0'), (' »', '\u00a0»')):
        x = x.replace(a, b)
    return x
def T(fr, de, en):
    for k in {fr, _nb(fr)}:
        TR_ADD['de'][k] = de; TR_ADD['en'][k] = en
    if fr.rstrip().endswith('?'):   # questions des cas clients, affichées entre guillemets
        TR_ADD['de'][_nb('« ' + fr + ' »')] = '«' + de + '»'; TR_ADD['en'][_nb('« ' + fr + ' »')] = '“' + en + '”'
    return fr

# ---------------------------------------------------------------- m3 : données Organisation
_org = json.loads(ORG_LD)
_org.update({"@id": "https://www.leadr.ch/#organisation", "legalName": "Leadr GmbH", "alternateName": "Leadr",
             "sameAs": [LINKEDIN_CO],
             "identifier": {"@type": "PropertyValue", "propertyID": "UID", "value": "CHE-252.536.958"}})
ORG_LD = json.dumps(_org, ensure_ascii=False)

# ---------------------------------------------------------------- m1 : titres H1 avec le mot-clé
H1_NEW = {
    'implantation.html': ('S\'implanter au bon moment, sur de bonnes bases.',
                          T('Créer sa société en Suisse ou en France, au bon moment et sur de bonnes bases.',
                            'Eine Gesellschaft in der Schweiz oder in Frankreich gründen, zum richtigen Zeitpunkt und auf solider Grundlage.',
                            'Setting up a company in Switzerland or France, at the right time and on solid foundations.')),
    'relocalisation.html': ('Déplacer une activité, sans perdre le fil.',
                            T('Relocaliser une activité en Suisse, sans perdre le fil.',
                              'Eine Tätigkeit in die Schweiz verlagern, ohne den Faden zu verlieren.',
                              'Relocating a business to Switzerland without losing the thread.')),
    'management-transition.html': ('Des dirigeants aguerris, opérationnels dès le premier jour.',
                                   T('Management de transition en Suisse : des dirigeants opérationnels dès le premier jour.',
                                     'Interim Management in der Schweiz: erfahrene Führungskräfte, einsatzbereit ab dem ersten Tag.',
                                     'Interim management in Switzerland: seasoned executives, operational from day one.')),
    'methode.html': ('Une méthode pour ne perdre ni temps, ni argent.',
                     T('Une méthode d\'accompagnement pour ne perdre ni temps, ni argent.',
                       'Eine Begleitmethode, die weder Zeit noch Geld verschwendet.',
                       'A support method that wastes neither time nor money.')),
}
for _s, (_old, _new) in H1_NEW.items():
    _b = PAGES[_s]['body']
    _i = next(k for k, x in enumerate(_b) if _old in x)
    _b[_i] = _b[_i].replace(_old, _new, 1)

# ---------------------------------------------------------------- m2 : descriptions plus courtes (moins de 155 caractères)
PAGES['distributeur-suisse.html']['desc'] = T(
    'Vendre en Suisse sans y créer de société : nous trouvons le distributeur suisse adapté à vos produits et accompagnons son lancement.',
    'In der Schweiz verkaufen ohne Gesellschaft: Wir finden den passenden Schweizer Vertriebspartner und begleiten den Start.',
    'Sell in Switzerland without a local company: we find the right Swiss distributor for your products and support the launch.')
PAGES['distributeur-france.html']['desc'] = T(
    'Entreprise suisse : vendre en France sans filiale. Nous trouvons le distributeur français adapté à vos produits et accompagnons son lancement.',
    'Schweizer Unternehmen: in Frankreich ohne Tochter verkaufen. Wir finden den passenden Vertriebspartner und begleiten den Start.',
    'Swiss companies: sell in France without a subsidiary. We find the right French distributor for your products and support the launch.')
PAGES['index.html']['desc'] = T(
    'Leadr, société suisse basée à Bâle, accompagne les PME, PMI et ETI en Suisse et en France : prospection ciblée, mise en relation, implantation.',
    'Leadr, Schweizer Unternehmen in Basel, begleitet KMU in der Schweiz und in Frankreich: gezielte Kundengewinnung, Kontakte, Markteintritt.',
    'Leadr, a Swiss company based in Basel, supports SMEs in Switzerland and France: targeted prospecting, introductions and market entry.')
PAGES['vers-la-suisse.html']['desc'] = T(
    'Prospection, mise en relation, normes suisses et implantation : Leadr accompagne les PME, PMI et ETI françaises sur le marché suisse.',
    'Kundengewinnung, Kontakte, Schweizer Normen und Firmengründung: Leadr begleitet französische KMU in den Schweizer Markt.',
    'Prospecting, introductions, Swiss standards and company set-up: Leadr supports French SMEs entering the Swiss market.')
PAGES['formats.html']['desc'] = T(
    'Diagnostic de marché, mission ciblée, antenne permanente, implantation : quatre formats clairs, avec leur durée et leurs livrables, pour la Suisse et la France.',
    'Marktanalyse, gezieltes Mandat, ständige Marktpräsenz, Firmengründung: vier klare Formen mit Dauer und Ergebnissen.',
    'Market diagnosis, targeted assignment, ongoing representation, set-up: four clear formats, each with its duration and deliverables.')

# ---------------------------------------------------------------- cas clients chiffrés (Weinmann, Irola, chantiers, Zest for Work, anonymisés)
CASES = [
    ('Mon produit est-il conforme aux règles du marché suisse ?',
     'Équipement industriel · De la France vers la Suisse',
     T('Un fabricant français d\'équipements industriels, livrés et installés chez ses clients, voulait vendre en Suisse. Son premier projet couvrait les 26 cantons. Avant d\'approcher le moindre acheteur, il fallait savoir quelles normes, prescriptions et exigences cantonales s\'appliquaient à ses installations.',
       'Ein französischer Hersteller von Industrieanlagen, die er bei seinen Kunden liefert und montiert, wollte in der Schweiz verkaufen. Sein erstes Projekt umfasste alle 26 Kantone. Bevor er auch nur einen Einkäufer ansprach, musste klar sein, welche Normen, Vorschriften und kantonalen Anforderungen für seine Anlagen gelten.',
       'A French manufacturer of industrial equipment, delivered and installed on customer sites, wanted to sell in Switzerland. Its first plan covered all 26 cantons. Before approaching a single buyer, it needed to know which standards, regulations and cantonal requirements applied to its installations.'),
     T('Recherche des textes applicables à la source, fédéraux et cantonaux, liste des adaptations à prévoir sur les installations et sur l\'offre, points de TVA et de douane clarifiés, puis recentrage du projet sur les cantons où la demande était la plus forte.',
       'Recherche der geltenden Bestimmungen an der Quelle, auf Bundes- und Kantonsebene, Liste der nötigen Anpassungen an Anlagen und Angebot, Klärung von Mehrwertsteuer und Zoll, dann Fokus auf die Kantone mit der grössten Nachfrage.',
       'Research into the applicable federal and cantonal rules at the source, a list of the changes needed to the installations and the offer, VAT and customs questions clarified, then a sharper focus on the cantons with the strongest demand.'),
     T('Un périmètre ramené de 26 à 4 cantons prioritaires, une offre adaptée en amont et un plan d\'approche canton par canton.',
       'Ein Perimeter, der von 26 auf 4 Schwerpunktkantone reduziert wurde, ein vorab angepasstes Angebot und ein Vorgehensplan Kanton für Kanton.',
       'The scope narrowed from 26 cantons to 4 priority cantons, an offer adapted in advance and an approach plan canton by canton.')),
    ('Qui dois-je rencontrer, et comment les approcher ?',
     T('Environnement et assainissement · De la France vers la Suisse',
       'Umwelt und Abwasser · Von Frankreich in die Schweiz',
       'Environment and sanitation · From France to Switzerland'),
     T('Une entreprise française d\'ingénierie environnementale voulait se développer en Suisse et, depuis la Suisse, à l\'international. Elle ne connaissait personne sur ce marché et refusait une campagne de démarchage à l\'aveugle.',
       'Ein französisches Ingenieurunternehmen im Umweltbereich wollte in der Schweiz und von der Schweiz aus international wachsen. Es kannte niemanden auf diesem Markt und lehnte eine Akquisekampagne ins Blaue ab.',
       'A French environmental engineering firm wanted to grow in Switzerland and, from a Swiss base, internationally. It knew no one in the market and refused any blind cold-calling campaign.'),
     T('Analyse du marché, puis des entreprises et des institutions cibles une par une, pour retenir cinq interlocuteurs prioritaires, avec une approche directe préparée pour chacun. La création d\'une société suisse a été prévue en dernière étape, une fois les premiers signaux du marché obtenus.',
       'Analyse des Marktes, dann der Zielunternehmen und Institutionen, eines nach dem anderen, um fünf vorrangige Ansprechpersonen festzulegen, mit einer vorbereiteten direkten Ansprache für jede. Die Gründung einer Schweizer Gesellschaft wurde als letzter Schritt vorgesehen, sobald erste Signale aus dem Markt vorliegen.',
       'Analysis of the market, then of the target companies and institutions one by one, to select five priority contacts, with a direct approach prepared for each. Setting up a Swiss company was planned as the last step, once the first market signals were in.'),
     T('Cinq décideurs identifiés et approchés directement, plutôt que des centaines d\'appels.',
       'Fünf Entscheidungsträger identifiziert und direkt angesprochen, statt Hunderter Anrufe.',
       'Five decision-makers identified and approached directly, instead of hundreds of calls.')),
    CASES[2],
    (T('Comment trouver des clients en Suisse sans recruter de commercial ?',
       'Wie gewinne ich Kunden in der Schweiz, ohne eine Verkaufsperson einzustellen?',
       'How do I win clients in Switzerland without hiring a salesperson?'),
     T('Formation pour les entreprises · Vers la Suisse',
       'Weiterbildung für Unternehmen · In die Schweiz',
       'Corporate training · Into Switzerland'),
     T('Un cabinet européen de formation, déjà choisi par de grands groupes internationaux, voulait développer sa clientèle en Suisse. Ses ventes reposaient uniquement sur le réseau de ses associées, et il hésitait entre recruter un commercial, rémunérer des agents à la commission ou tout gérer en interne.',
       'Ein europäisches Weiterbildungsunternehmen, das bereits für grosse internationale Konzerne arbeitet, wollte in der Schweiz neue Kunden gewinnen. Der Verkauf lief nur über das Netzwerk der Partnerinnen, und es zögerte zwischen einer Anstellung, Agenten auf Provisionsbasis und dem Verkauf in Eigenregie.',
       'A European training firm, already chosen by large international groups, wanted to build its client base in Switzerland. Its sales relied solely on its partners\' network, and it was torn between hiring a salesperson, paying agents on commission or handling everything in-house.'),
     T('Positionnement de l\'offre revu pour les directions des ressources humaines et de la transformation, sélection des entreprises suisses prioritaires, puis campagne de prospection ciblée, suivie et ajustée chaque mois.',
       'Neue Positionierung des Angebots für Personal- und Transformationsverantwortliche, Auswahl der vorrangigen Schweizer Unternehmen, dann eine gezielte Akquisekampagne, die jeden Monat ausgewertet und angepasst wird.',
       'The offer repositioned for HR and transformation leaders, a selection of priority Swiss companies, then a targeted prospecting campaign, reviewed and adjusted every month.'),
     T('Une présence commerciale en Suisse au mois, sans recrutement ni contrat de travail, ajustable à chaque étape.',
       'Eine monatliche Marktpräsenz in der Schweiz, ohne Anstellung und ohne Arbeitsvertrag, bei jedem Schritt anpassbar.',
       'A monthly commercial presence in Switzerland, with no hiring and no employment contract, adjustable at every stage.')),
]

SHORT_CASES[0] = (SHORT_CASES[0][0], SHORT_CASES[0][1], SHORT_CASES[0][2],
                  T('Recherche des textes à la source, liste des adaptations à faire, TVA et douane clarifiées.',
                    'Recherche der Bestimmungen an der Quelle, Liste der Anpassungen, Mehrwertsteuer und Zoll geklärt.',
                    'Rules researched at the source, list of changes to make, VAT and customs clarified.'),
                  T('Un périmètre ramené de 26 à 4 cantons, et une offre conforme dès le premier rendez-vous.',
                    'Ein Perimeter von 26 auf 4 Kantone reduziert, und ein konformes Angebot ab dem ersten Termin.',
                    'Scope narrowed from 26 to 4 cantons, and a compliant offer from the very first meeting.'))
SHORT_CASES[1] = (SHORT_CASES[1][0], T('Environnement et assainissement, France vers Suisse',
                                       'Umwelt und Abwasser, Frankreich in die Schweiz',
                                       'Environment and sanitation, France to Switzerland'),
                  SHORT_CASES[1][2], SHORT_CASES[1][3], SHORT_CASES[1][4])

FAQ_CASES = [
    (T('Les cas présentés sont-ils réels ?', 'Sind die Fallbeispiele echt?', 'Are these case studies real?'),
     T('Oui. Chaque cas est tiré d\'une mission réelle. Le nom de l\'entreprise n\'est jamais publié, et les détails qui permettraient de la reconnaître sont retirés.',
       'Ja. Jedes Beispiel stammt aus einem echten Mandat. Der Name des Unternehmens wird nie veröffentlicht, und Angaben, die es erkennbar machen würden, werden weggelassen.',
       'Yes. Each case comes from a real assignment. The company name is never published, and any detail that could identify it is removed.')),
    (T('Pourquoi aucun nom de client n\'est-il cité ?', 'Warum werden keine Kundennamen genannt?', 'Why are no client names given?'),
     T('Parce que nos clients nous confient des projets stratégiques, souvent avant que leurs concurrents ou même leurs équipes ne soient au courant. La discrétion fait partie de notre travail.',
       'Weil uns unsere Kunden strategische Projekte anvertrauen, oft bevor ihre Konkurrenz oder sogar ihre eigenen Teams davon wissen. Diskretion gehört zu unserer Arbeit.',
       'Because our clients entrust us with strategic projects, often before their competitors or even their own teams know about them. Discretion is part of our work.')),
    (T('Pouvez-vous m\'indiquer un client à contacter ?', 'Können Sie mir einen Kunden als Referenz nennen?', 'Can you put me in touch with a client?'),
     T('Oui, lorsque le client l\'accepte. Nous pouvons vous mettre en relation avec un dirigeant que nous avons accompagné, sur un projet comparable au vôtre.',
       'Ja, wenn der Kunde einverstanden ist. Wir können Sie mit einer Führungsperson in Kontakt bringen, die wir bei einem vergleichbaren Projekt begleitet haben.',
       'Yes, when the client agrees. We can introduce you to a business leader we have supported on a project similar to yours.')),
    (T('Ces situations ressemblent à la mienne. Par où commencer ?', 'Diese Situationen ähneln meiner. Wo fange ich an?', 'These situations look like mine. Where do I start?'),
     T('Par un premier rendez-vous. Nous parlons de votre offre et du marché visé, et nous vous disons franchement quelle première étape a du sens.',
       'Mit einem Erstgespräch. Wir sprechen über Ihr Angebot und den Zielmarkt und sagen Ihnen ehrlich, welcher erste Schritt sinnvoll ist.',
       'With a first meeting. We discuss your offer and the target market, and tell you candidly which first step makes sense.')),
]

_cc = PAGES['cas-clients.html']['body']
_cc[0] = hero('Cas clients', 'Des projets réels, présentés en toute discrétion.',
              T('Nos clients nous confient des projets stratégiques. Aucun nom d\'entreprise n\'est publié : chaque situation est présentée par secteur, à partir de la question qui a tout déclenché, avec les résultats obtenus.',
                'Unsere Kunden vertrauen uns strategische Projekte an. Wir veröffentlichen keine Firmennamen: Jede Situation wird nach Branche vorgestellt, ausgehend von der Frage, die alles ausgelöst hat, mit den erzielten Ergebnissen.',
                'Our clients entrust us with strategic projects. No company names are published: each situation is presented by sector, starting from the question that set everything in motion, with the results achieved.'))
_cc[1] = cases('', T('Quatre questions, quatre réponses.', 'Vier Fragen, vier Antworten.', 'Four questions, four answers.'), CASES, tone='sec-white')
_cc.insert(2, faq(T('Cas clients : vos questions.', 'Fallbeispiele: Ihre Fragen.', 'Case studies: your questions.'), FAQ_CASES))
_cc.insert(3, faq_ld(FAQ_CASES))

# accueil : grille des exemples
_h = PAGES['index.html']['body']
for _k, _x in enumerate(_h):
    if 'id="exemples"' in _x:
        _h[_k] = cases_grid().replace('Trois situations types, tirées de projets réels. Les noms et les chiffres restent confidentiels.',
                                      T('Trois situations types, tirées de projets réels. Les noms restent confidentiels.',
                                        'Drei typische Situationen aus echten Projekten. Die Namen bleiben vertraulich.',
                                        'Three typical situations drawn from real projects. Names remain confidential.'))

# ---------------------------------------------------------------- m7 : FAQ Méthode
FAQ_METH = [
    (T('Combien de temps dure chaque étape ?', 'Wie lange dauert jeder Schritt?', 'How long does each stage take?'),
     T('Le cadrage et la validation prennent en général quelques semaines. La construction et l\'activation s\'inscrivent dans la durée, au rythme du marché visé. Le calendrier est fixé avec vous dès le départ.',
       'Klären und Prüfen dauern in der Regel einige Wochen. Aufbauen und Umsetzen erfolgen über einen längeren Zeitraum, im Rhythmus des Zielmarktes. Den Zeitplan legen wir zu Beginn gemeinsam fest.',
       'Scoping and validation usually take a few weeks. Building and activation run over a longer period, at the pace of the target market. The timetable is set with you from the start.')),
    (T('Peut-on commencer directement par l\'activation ?', 'Kann man direkt mit der Umsetzung beginnen?', 'Can we start directly with activation?'),
     T('Oui, si votre offre est déjà adaptée au marché visé et que vous savez qui cibler. Nous le vérifions au premier rendez-vous, et le premier mois sert alors à préparer les mises en relation.',
       'Ja, wenn Ihr Angebot bereits auf den Zielmarkt zugeschnitten ist und Sie wissen, wen Sie ansprechen wollen. Wir prüfen das im Erstgespräch, und der erste Monat dient dann der Vorbereitung der Kontakte.',
       'Yes, if your offer is already adapted to the target market and you know whom to target. We check this at the first meeting, and the first month is then used to prepare the introductions.')),
    (T('Que se passe-t-il si votre conclusion est négative ?', 'Was passiert, wenn Ihr Fazit negativ ausfällt?', 'What happens if your conclusion is negative?'),
     T('Nous vous le disons, avec nos raisons : une adaptation à prévoir, un autre marché à privilégier ou un moment plus favorable. Une décision de ne pas y aller, prise sur des faits, vous fait aussi gagner du temps et de l\'argent.',
       'Wir sagen es Ihnen, mit unseren Gründen: eine nötige Anpassung, ein anderer Markt oder ein besserer Zeitpunkt. Auch ein faktenbasierter Entscheid, nicht zu starten, spart Zeit und Geld.',
       'We tell you, with our reasons: a change to make, another market to prioritise or a better moment. A fact-based decision not to go ahead also saves you time and money.')),
    (T('La méthode est-elle la même pour la France et pour la Suisse ?', 'Gilt die Methode für Frankreich und die Schweiz gleichermassen?', 'Is the method the same for France and Switzerland?'),
     T('Oui, les quatre étapes sont les mêmes dans les trois directions. Ce qui change, ce sont les règles à vérifier, les réseaux à mobiliser et la façon d\'approcher les décideurs.',
       'Ja, die vier Schritte sind in allen drei Richtungen dieselben. Was sich ändert, sind die zu prüfenden Regeln, die Netzwerke und die Art, Entscheidungsträger anzusprechen.',
       'Yes, the four stages are the same in all three directions. What changes are the rules to check, the networks to draw on and the way to approach decision-makers.')),
]
_insert_before_cta('methode.html', [faq(T('Notre méthode : vos questions.', 'Unsere Methode: Ihre Fragen.', 'Our method: your questions.'), FAQ_METH), faq_ld(FAQ_METH)])

# ---------------------------------------------------------------- m6 : pages distributeur reliées depuis les trois directions de l'accueil
_h = PAGES['index.html']['body']
for _k, _x in enumerate(_h):
    if 'class="dirs2"' in _x:
        _h[_k] = _x.replace('</div>\n</div></section>',
            '</div>\n  <p class="link-line dist-links">' + T('Vendre par des distributeurs :', 'Über Vertriebspartner verkaufen:', 'Selling through distributors:') + ' '
            '<a href="distributeur-suisse.html">' + T('trouver un distributeur en Suisse', 'Vertriebspartner in der Schweiz finden', 'find a distributor in Switzerland') + '</a> · '
            '<a href="distributeur-france.html">' + T('trouver un distributeur en France', 'Vertriebspartner in Frankreich finden', 'find a distributor in France') + '</a></p>\n</div></section>', 1)

# ---------------------------------------------------------------- guides par direction (dont un guide écrit en allemand)
ARTICLES = [
    dict(slug='implantation-suisse-pme-francaises.html', md='implantation-suisse-pme-francaises.md', lang='fr', dir='ch',
         title='Implantation en Suisse pour PME françaises : guide 2026 · Leadr',
         h1='Implantation en Suisse pour PME françaises : comment choisir le bon partenaire',
         desc='Implantation en Suisse pour PME françaises en 2026 : modalités, coûts, erreurs à éviter et critères pour choisir le bon partenaire. Guide par Leadr.',
         card={'fr': 'Implantation en Suisse', 'de': 'Markteintritt in der Schweiz', 'en': 'Setting up in Switzerland'},
         short={'fr': 'Modalités, structures juridiques, erreurs à éviter et critères pour choisir le bon partenaire.',
                'de': 'Möglichkeiten, Rechtsformen, typische Fehler und Kriterien für die Wahl des richtigen Partners.',
                'en': 'Options, legal structures, mistakes to avoid and how to choose the right partner.'},
         pub='2026-09-09', mod='2026-10-02', date='2 octobre 2026', og='og-guide-implantation.png'),
    dict(slug='vendre-en-suisse-tva-douane.html', md='vendre-en-suisse-tva-douane.md', lang='fr', dir='ch',
         title='Vendre en Suisse depuis la France : TVA et douane, guide 2026 · Leadr',
         h1='Vendre en Suisse depuis la France : TVA, douane et assujettissement',
         desc='Vendre en Suisse depuis la France en 2026 : droits de douane, TVA suisse à l\'importation, seuil d\'inscription et représentant fiscal. Guide par Leadr.',
         card={'fr': 'TVA et douane en Suisse', 'de': 'Mehrwertsteuer und Zoll in der Schweiz', 'en': 'Swiss VAT and customs'},
         short={'fr': 'Douane, TVA à l\'importation, inscription à la TVA suisse et représentant fiscal : ce qu\'il faut régler avant la première offre.',
                'de': 'Zoll, Einfuhrsteuer, Schweizer Mehrwertsteuerpflicht und Fiskalvertreter: was vor dem ersten Angebot geklärt sein muss.',
                'en': 'Customs, import VAT, Swiss VAT registration and tax representative: what to settle before the first quote.'},
         pub=TODAY, mod=TODAY, date='21 octobre 2026', og='og-guide-tva-douane.png'),
    dict(slug='prospection-externalisee-suisse.html', md='prospection-externalisee-suisse.md', lang='fr', dir='ch',
         title='Prospection externalisée en Suisse : guide 2026 · Leadr',
         h1='Prospection externalisée en Suisse : comment choisir le bon prestataire',
         desc='Prospection commerciale externalisée pour vendre en Suisse depuis la France en 2026 : quand la choisir, combien elle coûte, comment choisir le bon prestataire.',
         card={'fr': 'Prospection externalisée', 'de': 'Ausgelagerte Kundengewinnung', 'en': 'Outsourced prospecting'},
         short={'fr': 'Quand la choisir, combien elle coûte, et comment choisir le bon prestataire.',
                'de': 'Wann sie sinnvoll ist, was sie kostet und wie Sie den richtigen Anbieter wählen.',
                'en': 'When to choose it, what it costs and how to pick the right provider.'},
         pub='2026-09-10', mod='2026-10-02', date='2 octobre 2026', og='og-guide-prospection.png'),
    dict(slug='marketing-externalise-suisse.html', md='marketing-externalise-suisse.md', lang='fr', dir='ch',
         title='Marketing externalisé pour la Suisse : guide 2026 · Leadr',
         h1='Marketing externalisé : comment adapter sa marque au marché suisse',
         desc='Marketing externalisé pour se développer en Suisse en 2026 : comment adapter sa marque, son site et son discours au marché suisse. Guide par Leadr.',
         card={'fr': 'Marketing externalisé', 'de': 'Ausgelagertes Marketing', 'en': 'Outsourced marketing'},
         short={'fr': 'Adapter sa marque, son site et son discours au marché suisse, sans simple traduction.',
                'de': 'Marke, Website und Argumentation an den Schweizer Markt anpassen, nicht nur übersetzen.',
                'en': 'Adapting your brand, website and message to the Swiss market, beyond translation.'},
         pub='2026-10-01', mod='2026-10-02', date='2 octobre 2026', og='og-guide-marketing.png'),
    dict(slug='entreprise-suisse-s-implanter-en-france.html', md='entreprise-suisse-s-implanter-en-france.md', lang='fr', dir='fr',
         title='Entreprise suisse : s\'implanter en France, guide 2026 · Leadr',
         h1='S\'implanter en France : guide 2026 pour les entreprises suisses',
         desc='Entreprise suisse : vendre et s\'implanter en France en 2026. Douane, TVA et représentant fiscal, détachement, filiale ou succursale. Guide par Leadr.',
         card={'fr': 'S\'implanter en France', 'de': 'In Frankreich Fuss fassen', 'en': 'Setting up in France'},
         short={'fr': 'Pour les entreprises suisses : vendre sans filiale, douane, TVA, détachement, puis succursale ou SAS.',
                'de': 'Für Schweizer Unternehmen: Verkauf ohne Tochter, Zoll, Mehrwertsteuer, Entsendung, dann Zweigniederlassung oder SAS.',
                'en': 'For Swiss companies: selling without a subsidiary, customs, VAT, posting staff, then branch or SAS.'},
         pub=TODAY, mod=TODAY, date='21 octobre 2026', og='og-guide-france.png'),
    dict(slug='markteintritt-frankreich.html', md='markteintritt-frankreich.md', lang='de', dir='fr',
         title='Markteintritt Frankreich: Leitfaden 2026 für Schweizer KMU · Leadr',
         h1='Markteintritt Frankreich: Leitfaden 2026 für Schweizer KMU',
         desc='Markteintritt Frankreich 2026 für Schweizer KMU: Vertriebswege, Zoll, Mehrwertsteuer und Fiskalvertreter, Entsendung, SAS gründen. Leitfaden von Leadr.',
         card={'fr': 'Markteintritt Frankreich', 'de': 'Markteintritt Frankreich', 'en': 'Markteintritt Frankreich'},
         short={'fr': 'Le guide écrit pour les entreprises de Suisse alémanique qui visent la France.',
                'de': 'Vertriebswege, Zoll, Mehrwertsteuer, Entsendung und Gesellschaftsgründung: der Leitfaden für Schweizer KMU.',
                'en': 'Our guide for German-speaking Swiss companies targeting France.'},
         pub=TODAY, mod=TODAY, date='21. Oktober 2026', og='og-guide-markteintritt.png'),
]
ART = {a['slug']: a for a in ARTICLES}
FR_ONLY = {a['slug'] for a in ARTICLES if a['lang'] == 'fr'}
LANG_NOTE = {'fr': {'de': ' (en allemand)'}, 'de': {'fr': ' (auf Französisch)'}, 'en': {'fr': ' (in French)', 'de': ' (in German)'}}
MORE = {'fr': 'Lire le guide', 'de': 'Leitfaden lesen', 'en': 'Read the guide'}

def _guide_items(lg, dirs, exclude=None):
    items = [a for a in ARTICLES if a['dir'] in dirs and a['slug'] != exclude]
    items.sort(key=lambda a: (a['lang'] != lg, ARTICLES.index(a)))
    return items

GUIDE_CTX = {
    # contexte : (directions, surtitre, titre, intro) par langue
    'all': (('ch', 'fr'),
            {'fr': ('Guides 2026', 'Nos guides pour aller plus loin.', 'Des guides détaillés, mis à jour régulièrement, pour chacune de nos directions.'),
             'de': ('Leitfäden 2026', 'Unsere Leitfäden für den nächsten Schritt.', 'Ausführliche, regelmässig aktualisierte Leitfäden für jede unserer Richtungen.'),
             'en': ('2026 guides', 'Our guides to go further.', 'Detailed, regularly updated guides for each of our directions.')}),
    'ch': (('ch',),
           {'fr': ('Guides 2026', 'Vendre et s\'implanter en Suisse : nos guides.', 'Pour approfondir, nos guides détaillés.'),
            'de': ('Leitfäden 2026', 'In der Schweiz verkaufen: unsere Leitfäden.', 'Zur Vertiefung: unsere ausführlichen Leitfäden (auf Französisch).'),
            'en': ('2026 guides', 'Selling in Switzerland: our guides.', 'For more detail: our in-depth guides (in French).')}),
    'fr': (('fr',),
           {'fr': ('Guides 2026', 'Se développer en France : nos guides.', 'Pour approfondir, nos guides détaillés.'),
            'de': ('Leitfäden 2026', 'In Frankreich wachsen: unsere Leitfäden.', 'Zur Vertiefung, unsere ausführlichen Leitfäden.'),
            'en': ('2026 guides', 'Growing in France: our guides.', 'To go further, our detailed guides.')}),
}
READ_ALSO = {'fr': ('À lire aussi', 'Les autres guides.'), 'de': ('Ebenfalls lesenswert', 'Weitere Leitfäden.'), 'en': ('Also worth reading', 'Our other guides.')}

def tt(fr, own):
    """Texte dans la langue lg : traduction existante (relue en v2.30) si elle existe, sinon la nôtre."""
    lg, mine = own
    if lg == 'fr': return fr
    return TR[lg].get(_nb(fr)) or TR[lg].get(fr) or mine

NOTE = {'fr': 'FR', 'de': 'DE', 'en': 'EN'}
def render_guides(ctx, lg, exclude=None, tone='sec-white'):
    if ctx == 'article':
        a = ART[exclude]
        items = _guide_items(lg, (a['dir'],), exclude)
        if len(items) < 2:
            items += [x for x in _guide_items(lg, ('ch', 'fr'), exclude) if x not in items][:3 - len(items)]
        k, t = READ_ALSO[lg]
        k, t = tt(READ_ALSO['fr'][0], (lg, k)), tt(READ_ALSO['fr'][1], (lg, t)); intro = ''
    else:
        dirs, txt = GUIDE_CTX[ctx]
        items = _guide_items(lg, dirs, exclude)
        k, t, intro = (tt(txt['fr'][i], (lg, txt[lg][i])) if i < 2 else txt[lg][i] for i in range(3))
    cs = ''
    for a in items:
        href, extra = rel(a['slug'], lg)
        note = '' if a['lang'] == lg else f' ({NOTE[a["lang"]]})'
        card = re.sub(r' \((FR|DE)\)$', '', tt(a['card']['fr'], (lg, a['card'][lg]))) if a['lang'] == 'fr' else a['card'][lg]
        short = tt(a['short']['fr'], (lg, a['short'][lg])) if a['lang'] == 'fr' else a['short'][lg]
        more = tt('Lire le guide', (lg, MORE[lg]))
        more = re.sub(r' \((FR|DE)\)$', '', more) + note
        cs += f'<a class="col col-link" href="{href}"{extra}><h3>{card}{note}</h3><p>{short}</p><span class="more">{more}</span></a>'
    intro_h = f'<p class="intro">{intro}</p>' if intro else ''
    n = len(items)
    return f'''<section class="sec {tone}"><div class="wrap">
  <p class="kicker">{k}</p><h2 class="w-narrow">{t}</h2>{intro_h}<div class="cols n{n}">{cs}</div>
</div></section>'''

def guides_ph(ctx, exclude='', tone='sec-white'):
    return f'<!--GUIDES:{ctx}:{exclude}:{tone}-->'

# remplace les blocs de guides déjà insérés dans les pages par des emplacements rendus par langue
_GCTX = {'index.html': 'all', 'reperes.html': 'all', 'vers-la-suisse.html': 'ch', 'implantation.html': 'all',
         'distributeur-suisse.html': 'ch'}
for _s, _p in PAGES.items():
    if _p.get('fr_only'): continue
    for _k, _x in enumerate(_p['body']):
        if 'class="cols' in _x and 'implantation-suisse-pme-francaises.html' in _x and 'Lire le guide' in _x:
            _tone = 'sec-white' if 'class="sec sec-white"' in _x[:40] else ''
            _p['body'][_k] = guides_ph(_GCTX.get(_s, 'all'), '', _tone)
_insert_before_cta('vers-la-france.html', [guides_ph('fr', '', '')])
_insert_before_cta('distributeur-france.html', [guides_ph('fr', '', '')])
_insert_before_cta('entre-regions-suisses.html', [guides_ph('all', '', '')])

# pied de page : liens vers les guides selon la langue
FOOT = re.sub(r'<div class="foot-guides">.*?</div>', '<!--FOOTGUIDES-->', FOOT, flags=re.S)
def foot_guides(lg):
    lab = tt('Guides 2026', (lg, {'de': 'Leitfäden 2026', 'en': '2026 guides'}.get(lg, '')))
    out = ''
    for a in _guide_items(lg, ('ch', 'fr')):
        href, extra = rel(a['slug'], lg)
        note = '' if a['lang'] == lg else f' ({NOTE[a["lang"]]})'
        card = re.sub(r' \((FR|DE)\)$', '', tt(a['card']['fr'], (lg, a['card'][lg]))) if a['lang'] == 'fr' else a['card'][lg]
        out += f'<a href="{href}"{extra}>{card}{note}</a>'
    return f'<div class="foot-guides"><span>{lab}</span>{out}</div>'

# ---------------------------------------------------------------- pages des guides
PILLAR = {'ch': 'vers-la-suisse.html', 'fr': 'vers-la-france.html'}
PILLAR_LABEL = {'ch': {'fr': 'Vers la Suisse', 'de': 'In die Schweiz', 'en': 'To Switzerland'},
                'fr': {'fr': 'Vers la France', 'de': 'Expansion Frankreich', 'en': 'To France'}}
ART_TXT = {
    'fr': dict(kind='Guide 2026', by='Par', ceo='CEO de Leadr', upd='Mis à jour le', toc='Sommaire',
               cta=('Votre projet mérite un avis franc ?', 'Un premier rendez-vous pour voir comment ce guide s\'applique à votre situation.')),
    'de': dict(kind='Leitfaden 2026', by='Von', ceo='CEO von Leadr', upd='Aktualisiert am', toc='Inhalt',
               cta=('Ihr Projekt verdient eine ehrliche Einschätzung.', 'Ein Erstgespräch, um zu sehen, wie dieser Leitfaden auf Ihre Situation passt.')),
}

def _article_html(a):
    lg = a['lang']; tx = ART_TXT[lg]
    src = open(os.path.join('articles', a['md']), encoding='utf-8').read()
    faq_part = src.split('## 7.', 1)[1]
    qa = re.findall(r'^### (.+?)\n\n(.+?)(?=\n\n### |\n\n\*Sources|\n\n\*Quellen|\Z)', faq_part, flags=re.S | re.M)
    body = _md.markdown(src, extensions=['tables', 'sane_lists', 'toc'])
    ids = re.findall(r'<h2 id="([^"]+)">\d+\.', body)
    m = re.search(r'(<h2 id="[^"]*">' + tx['toc'] + r'</h2>\s*<ol>)(.*?)(</ol>)', body, flags=re.S)
    if m and ids:
        lis = re.findall(r'<li>(.*?)</li>', m.group(2), flags=re.S)
        new = ''.join(f'<li><a href="#{ids[i]}">{t}</a></li>' if i < len(ids) else f'<li>{t}</li>' for i, t in enumerate(lis))
        body = body[:m.start(2)] + new + body[m.end(2):]
    body = body.replace('<table>', '<div class="table-scroll"><table>').replace('</table>', '</table></div>')
    page_url = url(a['slug'], lg)
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['desc'],
          "datePublished": a['pub'], "dateModified": a['mod'], "inLanguage": lg,
          "author": {"@type": "Person", "name": "Luc Rohmer", "jobTitle": "CEO", "url": url('leadr.html', lg), "sameAs": [LINKEDIN]},
          "publisher": {"@type": "Organization", "@id": "https://www.leadr.ch/#organisation", "name": "Leadr GmbH", "logo": {"@type": "ImageObject", "url": "https://www.leadr.ch/logo.png"}},
          "mainEntityOfPage": page_url, "image": "https://www.leadr.ch/img/" + a['og']}
    pil = PILLAR[a['dir']]
    head_ = f'''<section class="hero hero-small"><div class="wrap"><div class="hero-txt">
  <p class="kicker"><a href="{pil}">{PILLAR_LABEL[a['dir']][lg]}</a> · {tx['kind']}</p><h1>{a['h1']}</h1>
  <p class="art-meta">{tx['by']} <a href="leadr.html">Luc Rohmer</a>, {tx['ceo']} · {tx['upd']} {a['date']}</p></div></div></section>'''
    art = f'<section class="sec sec-white"><div class="wrap"><article class="article-body">{body}</article></div></section>'
    return [head_, art, guides_ph('article', a['slug'], ''),
            '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
            faq_ld([(q.strip(), re.sub(r'\s+', ' ', r.strip())) for q, r in qa]),
            cta(*tx['cta'])]

for _a in ARTICLES:
    _d = dict(title=_a['title'], desc=_a['desc'], body=_article_html(_a), og=_a['og'])
    if _a['lang'] == 'fr':
        _d['fr_only'] = True
    else:
        _d['only'] = _a['lang']; _d['de_slug'] = _a['slug']
    PAGES[_a['slug']] = _d
    BC_LABEL[_a['slug']] = _a['card'][_a['lang']]

# l'article allemand pointe vers les pages françaises équivalentes pour le sélecteur de langue
SWITCH = {'markteintritt-frankreich.html': {'fr': 'entreprise-suisse-s-implanter-en-france.html', 'en': 'vers-la-france.html'},
          'entreprise-suisse-s-implanter-en-france.html': {'de': 'markteintritt-frankreich.html', 'en': 'vers-la-france.html'}}

# ---------------------------------------------------------------- m4 : balisage Service
SERVICE_PAGES = {
    'vers-la-suisse.html': ('CH',), 'vers-la-france.html': ('FR',), 'entre-regions-suisses.html': ('CH',),
    'formats.html': ('CH', 'FR'), 'implantation.html': ('CH', 'FR'), 'relocalisation.html': ('CH',),
    'management-transition.html': ('CH',), 'distributeur-suisse.html': ('CH',), 'distributeur-france.html': ('FR',),
    'premier-rendez-vous.html': ('CH', 'FR'),
}
COUNTRY = {'CH': {'fr': 'Suisse', 'de': 'Schweiz', 'en': 'Switzerland'}, 'FR': {'fr': 'France', 'de': 'Frankreich', 'en': 'France'}}
PARENT = {'distributeur-suisse.html': 'vers-la-suisse.html', 'distributeur-france.html': 'vers-la-france.html'}
for _a in ARTICLES: PARENT[_a['slug']] = PILLAR[_a['dir']]

def _lab(slug, lg):
    if slug in ART: return ART[slug]['card'][lg] if lg in ART[slug]['card'] else ART[slug]['card']['fr']
    x = BC_LABEL.get(slug, slug)
    if lg == 'fr': return x
    return TR[lg].get(x, x)

def seo_ld(slug, lg, doc=''):
    out = []
    if slug == 'index.html':
        out.append({"@context": "https://schema.org", "@type": "WebSite", "name": "Leadr", "alternateName": "Leadr GmbH",
                    "url": url('index.html', lg), "inLanguage": lg, "publisher": {"@id": "https://www.leadr.ch/#organisation"}})
    else:
        items = [(HOME[lg], url('index.html', lg))]
        par = PARENT.get(slug)
        if par: items.append((_lab(par, lg), url(par, lg)))
        items.append((_lab(slug, lg), url(slug, lg)))
        out.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]})
    if slug == 'leadr.html':
        out.append({"@context": "https://schema.org", "@type": "Person", "name": "Luc Rohmer", "jobTitle": "CEO",
                    "worksFor": {"@id": "https://www.leadr.ch/#organisation", "@type": "Organization", "name": "Leadr GmbH", "url": "https://www.leadr.ch/"},
                    "image": "https://www.leadr.ch/img/luc-rohmer.jpg", "sameAs": [LINKEDIN]})
    if slug in SERVICE_PAGES:
        m = re.search(r'<meta name="description" content="([^"]*)"', doc)
        out.append({"@context": "https://schema.org", "@type": "Service", "name": _lab(slug, lg), "serviceType": _lab(slug, lg),
                    "description": html.unescape(m.group(1)) if m else '', "url": url(slug, lg),
                    "provider": {"@type": "Organization", "@id": "https://www.leadr.ch/#organisation", "name": "Leadr GmbH", "url": "https://www.leadr.ch/"},
                    "areaServed": [{"@type": "Country", "name": COUNTRY[c][lg]} for c in SERVICE_PAGES[slug]]})
    return ''.join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + '</script>' for o in out)

def finish(doc, slug, lg):
    doc = doc.replace('</head>', seo_ld(slug, lg, doc) + '\n</head>', 1)
    return keep_hyphen_words(doc)

# ---------------------------------------------------------------- langues
for _l in ('de', 'en'):
    TR[_l].update({k: v for k, v in TR_ADD[_l].items() if k not in TR[_l] or True})

def localize(doc, lg, slug):
    p = PAGES[slug]
    av = avail(slug)
    native = p.get('only')
    # balises hreflang
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{url(slug, l)}">' for l in av)
    alt += f'<link rel="alternate" hreflang="x-default" href="{url(slug, "fr" if "fr" in av else av[0])}">'
    # sélecteur de langue
    def lk(l):
        if l in av: target = slug
        else: target = SWITCH.get(slug, {}).get(l) or PARENT.get(slug) or 'index.html'
        here = '' if lg == 'fr' else '../'
        return here + ('' if l == 'fr' else l + '/') + ps(target, l)
    sw = '<div class="lang" aria-label="' + {'fr': 'Langue', 'de': 'Sprache', 'en': 'Language'}[lg] + '">' + ''.join(
        f'<a href="{lk(l)}" hreflang="{l}" lang="{l}"' + (' aria-current="true"' if l == lg else '') + f'>{l.upper()}</a>' for l in ('fr', 'de', 'en')) + '</div>'
    pub_fr = '' if slug == 'index.html' else slug
    doc = doc.replace(f'href="https://www.leadr.ch/{pub_fr}"', f'href="{url(slug, lg)}"').replace(f'content="https://www.leadr.ch/{pub_fr}"', f'content="{url(slug, lg)}"')
    doc = doc.replace('<!--LANG-->', sw).replace('<link rel="canonical"', alt + '\n<link rel="canonical"', 1)
    doc = doc.replace(WA_TXT['fr'], WA_TXT[lg])
    if lg != 'fr':
        t = TR[lg]
        def tr(s):
            k = s.strip()
            if not k: return s
            if k in t: return s[:len(s) - len(s.lstrip())] + t[k] + s[len(s.rstrip()):]
            if not native and re.search(r'[a-zà-ÿ]{3}', k) and not k.startswith('http') and '@' not in k and k not in ('website', 'summary_large_image', 'width=device-width, initial-scale=1') and k not in ('Leadr', 'Luc Rohmer', 'LinkedIn', 'WhatsApp', 'Leadr GmbH', 'Romandie', 'Deutschschweiz', 'Paris', 'Lyon', 'Lausanne', 'Sprache', 'Language'):
                MISSING.add((lg, k))
            return s
        parts = re.split(r'(<script.*?</script>|<!--GUIDES:[^>]*-->|<!--FOOTGUIDES-->)', doc, flags=re.S)
        out = []
        for part in parts:
            if part.startswith('<script type="application/ld+json">'):
                d = json.loads(part[len('<script type="application/ld+json">'):-len('</script>')])
                if not native and 'description' in d: d['description'] = tr(d['description'])
                if 'address' in d: d['address']['addressLocality'] = 'Basel'
                if not native:
                    for q in d.get('mainEntity', []):
                        q['name'] = tr(q['name']); q['acceptedAnswer']['text'] = tr(q['acceptedAnswer']['text'])
                out.append('<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>')
            elif part.startswith('<script') or part.startswith('<!--'):
                out.append(part)
            else:
                part = re.sub(r'>([^<]+)<', lambda m: '>' + html.escape(tr(html.unescape(m.group(1))), quote=False) + '<', part)
                part = re.sub(r'((?:content|alt|aria-label|title)=")([^"]+)(")', lambda m: m.group(1) + html.escape(tr(html.unescape(m.group(2)))) + m.group(3), part)
                out.append(part)
        doc = ''.join(out)
        doc = doc.replace('<html lang="fr" ', f'<html lang="{lg}" ').replace('content="fr_CH"', f'content="{LOCALE[lg]}"')
        doc = doc.replace('og-image.png', f'og-image-{lg}.png')
        for a in ('href="css/', 'src="js/', 'src="logo', 'src="img/', 'href="favicon', 'href="apple-touch', 'href="fonts/'):
            doc = doc.replace(a, a.replace('="', '="../'))
    # liens internes vers la bonne langue et la bonne adresse
    def fix(m):
        target, anchor = m.group(1), m.group(2) or ''
        if target not in PAGES: return m.group(0)
        href, extra = rel(target, lg, anchor)
        return f'href="{href}"{extra}'
    doc = re.sub(r'href="([a-z0-9-]+\.html)(#[^"]*)?"', fix, doc)
    # blocs de guides et pied de page
    doc = re.sub(r'<!--GUIDES:([a-z]+):([^:]*):([^>]*)-->', lambda m: render_guides(m.group(1), lg, m.group(2) or None, m.group(3)), doc)
    doc = doc.replace('<!--FOOTGUIDES-->', foot_guides(lg))
    # image de partage propre à chaque guide
    if p.get('og'):
        doc = re.sub(r'content="https://www\.leadr\.ch/og-image(?:-[a-z]{2})?\.png"', f'content="https://www.leadr.ch/img/{p["og"]}"', doc)
    return doc

# ---------------------------------------------------------------- redirections des anciennes adresses allemandes
def _clean_url_redirects():
    for _s in list(PAGES):
        if _s == 'index.html': continue
        for lg in avail(_s):
            f = ps(_s, lg); pre = '' if lg == 'fr' else lg + '/'
            REDIRECTS.setdefault(pre + f[:-5], pre + f)
            if lg == 'de' and f != _s and not PAGES[_s].get('only'):
                REDIRECTS[pre + _s] = pre + f          # ancienne adresse /de/vers-la-suisse.html
                REDIRECTS[pre + _s[:-5]] = pre + f     # ancienne adresse sans .html
    for _lg in ('de', 'en'):
        REDIRECTS.setdefault(f'{_lg}/index.html', f'{_lg}/')

# ---------------------------------------------------------------- m5 : dates réelles dans le sitemap
LASTMOD_FILE = 'lastmod.json'

def _main_hash(doc):
    m = re.search(r'<main.*?</main>', doc, flags=re.S)
    txt = re.sub(r'\s+', ' ', m.group(0) if m else doc)
    return hashlib.sha1(txt.encode('utf-8')).hexdigest()[:16]

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree('static', OUT)
    try: lastmod = json.load(open(LASTMOD_FILE, encoding='utf-8'))
    except Exception: lastmod = {}
    newmod, sm = {}, []
    for slug, p in PAGES.items():
        body = '\n'.join(p['body'])
        for a, b in ((' ?', ' ?'), (' :', ' :'), (' !', ' !'), ('« ', '« '), (' »', ' »')):
            body = body.replace(a, b)
        body = re.sub(r'<a ([^>]*?)href="contact.html"([^>]*)>(Prendre rendez-vous|Choisir un créneau)</a>', lambda m: f'<a {m.group(1)}href="{BOOK}" target="_blank" rel="noopener"{m.group(2)}>{m.group(3)}</a>', body)
        doc = head(p['title'], p['desc'].replace('"', '&quot;'), slug) + header(slug) + body + FOOT
        doc = re.sub(r'<a ([^>]*?)href="contact.html"([^>]*)>Prendre rendez-vous</a>', lambda m: f'<a {m.group(1)}href="{BOOK}" target="_blank" rel="noopener"{m.group(2)}>Prendre rendez-vous</a>', doc)
        for lg in avail(slug):
            d = finish(localize(doc, lg, slug), slug, lg)
            folder = OUT if lg == 'fr' else os.path.join(OUT, lg)
            os.makedirs(folder, exist_ok=True)
            open(os.path.join(folder, ps(slug, lg)), 'w', encoding='utf-8').write(d)
            u = url(slug, lg); h = _main_hash(d)
            old = lastmod.get(u)
            date = old['date'] if old and old['hash'] == h else TODAY
            newmod[u] = {'hash': h, 'date': date}
            sm.append(f'<url><loc>{u}</loc><lastmod>{date}</lastmod></url>')
    json.dump(newmod, open(LASTMOD_FILE, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    _clean_url_redirects()
    json.dump({'redirects': [{'source': '/' + a, 'destination': '/' + b, 'permanent': True} for a, b in REDIRECTS.items()],
               'headers': [{'source': '/(.*)', 'has': [{'type': 'host', 'value': 'leadr-site.vercel.app'}],
                            'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex, nofollow'}]}] + VERCEL_HEADERS},
              open(os.path.join(OUT, 'vercel.json'), 'w'), indent=2)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(sm) + '</urlset>')
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(page_404())
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://www.leadr.ch/sitemap.xml\n')
    print('pages:', len(PAGES), '· fichiers:', len(sm))
    for m in sorted(MISSING): print('NON TRADUIT', m)

# ---------------------------------------------------------------- version des fichiers de style, page 404
_head_v230 = head
def head(title, desc, slug):
    return _head_v230(title, desc, slug).replace('?v=2.30', '?v=2.31')
_page_404_v230 = page_404
def page_404():
    global FOOT
    _saved = FOOT
    FOOT = FOOT.replace('<!--FOOTGUIDES-->', foot_guides('fr'))
    try:
        return _page_404_v230()
    finally:
        FOOT = _saved
