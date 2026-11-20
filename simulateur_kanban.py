import os
import sys
import math
import copy
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QScrollArea, QFrame,
    QDialog, QListWidget, QListWidgetItem, QMessageBox, QGridLayout,
    QLineEdit, QComboBox, QAbstractItemView, QTextEdit, QCheckBox, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

plt.rcParams["font.sans-serif"] = ["Lato", "Segoe UI", "DejaVu Sans", "Arial"]
plt.rcParams["axes.edgecolor"] = "#E2E8F0"
plt.rcParams["axes.linewidth"] = 0.8

# --- PALETTE HARMONISÉE : BLANC + VERT / JAUNE-AMBRE / ROUGE ---
PALETTE = {
    "bg_page": "#FFFFFF",
    "bg_surface": "#F8FAFC",
    "bg_card": "#FFFFFF",
    "border": "#E2E8F0",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#94A3B8",

    "green": "#16A34A",
    "green_hover": "#15803D",
    "green_soft": "#F0FDF4",
    "green_border": "#BBF7D0",

    "amber": "#D97706",
    "amber_btn": "#EAB308",
    "amber_hover": "#CA8A04",
    "amber_soft": "#FFFBEB",
    "amber_border": "#FDE68A",

    "red": "#DC2626",
    "red_hover": "#B91C1C",
    "red_soft": "#FEF2F2",
    "red_border": "#FECACA",

    "workers": [
        "#15803D",  # Ama
        "#D97706",  # Louis
        "#DC2626",  # Flavia
        "#059669",  # Paul
        "#B45309",  # Bona
        "#4D7C0F",
        "#E11D48",
        "#CA8A04",
    ]
}

DEFAULT_TEAM_SPECS = [
    ("Ama", "Design UI/UX"),
    ("Louis", "Développement"),
    ("Flavia", "Analyse"),
    ("Paul", "QA"),
    ("Bona", "Déploiement"),
]

REAL_TASKS_CATALOG = [
    "Refonte du parcours d'inscription & SSO",
    "Intégration paiement Stripe & Apple Pay",
    "Tableau de bord analytique temps réel",
    "Système de notifications push & email",
    "Optimisation des requêtes SQL catalogue",
    "Mode hors-ligne & synchronisation locale",
    "Génération et export PDF des factures",
    "Gestion des rôles et permissions (RBAC)",
    "Moteur de recherche avec autocomplétion",
    "Audit accessibilité RGAA & contrastes",
    "Tunnel de commande mobile responsive",
    "Création des webhooks API partenaires",
    "Double authentification (2FA) sécurisée",
    "Migration base de données PostgreSQL",
    "Système de parrainage et codes promo",
    "Page interactive de suivi de livraison",
    "Mise en cache Redis des fiches produits",
    "Module de chat support client intégré",
    "Bannière RGPD & gestion des cookies",
    "Tests de charge & montée en scalabilité",
    "Import massif de catalogue via fichier CSV",
    "Refonte du menu de navigation principal",
    "Connexion OAuth2 Google et Microsoft",
    "Historique d'activité et logs d'audit",
    "Système d'avis et notation vérifiés",
    "Optimisation du temps de chargement (LCP)",
    "Envoi automatique des relances impayés",
    "Interface d'administration multi-boutiques",
    "Gestion des stocks et alertes de seuil",
    "Synchronisation calendrier & rappels RDV",
    "Système de messagerie interne temps réel",
    "Export comptable FEC & grand livre",
    "Personnalisation des thèmes marque blanche",
    "Détection automatique de fraude paiement",
    "Onboarding interactif nouveaux clients",
    "API GraphQL pour application mobile",
    "Archivage légal des contrats signés",
    "Tableau de suivi des SLA support",
    "Filtres multicritères avancés sur catalogue",
    "Sauvegarde incrémentale multi-régions",
    "Gestion des avoirs et remboursements",
    "Centre de préférences notifications",
    "Compression et CDN des médias haute déf.",
    "Module de planification des livraisons",
    "Journalisation des erreurs front-end",
    "Design System : composants boutons & modales",
    "Maquettes haute fidélité espace client mobile",
    "Prototypage interactif tunnel de paiement",
    "Refonte ergonomique des tableaux de bord",
    "Tests utilisateurs sur le parcours panier",
    "Micro-interactions & états de chargement UI",
    "Service d'authentification JWT & Refresh Token",
    "File d'attente asynchrone RabbitMQ / Celery",
    "Endpoint REST gestion des abonnements",
    "Moteur de calcul des taxes et TVA multi-pays",
    "Connecteur ERP & synchronisation stocks",
    "Sécurisation contre les injections et XSS",
    "Cahier des charges module facturation B2B",
    "Modélisation des flux de données analytiques",
    "Spécifications fonctionnelles API ouverte",
    "Analyse d'impact migration serveur cloud",
    "Cartographie des parcours utilisateurs clés",
    "Suite de tests automatisés End-to-End Cypress",
    "Tests de non-régression parcours commande",
    "Validation compatibilité Safari, Chrome & Edge",
    "Tests de sécurité & audit des permissions",
    "Pipeline CI/CD déploiement sans interruption",
    "Configuration monitoring Prometheus & alertes",
    "Déploiement conteneurs Docker en production",
    "Plan de reprise d'activité (PRA) & backups"
]

SCENARIOS = {
    "standard": {
        "name": "Équipe Équilibrée (Standard)",
        "desc": "Flux fluide sur 2 sprints de 12j, capacité équilibrée par pôle.",
        "num_sprints": 2,
        "sprint_days": 12,
        "tasks": 38,
        "effort_range": (1, 2),
        "limits": {
            "Design UI/UX": 2,
            "Développement": 3,
            "Analyse": 2,
            "QA": 2,
            "Déploiement": 2
        }
    },
    "qa_bottleneck": {
        "name": "Goulot d'étranglement QA",
        "desc": "Production rapide en amont mais validation QA bloquée à 1 personne.",
        "num_sprints": 2,
        "sprint_days": 12,
        "tasks": 38,
        "effort_range": (1, 3),
        "limits": {
            "Design UI/UX": 3,
            "Développement": 4,
            "Analyse": 2,
            "QA": 1,
            "Déploiement": 1
        }
    },
    "rush_sprint": {
        "name": "Rush Multi-Sprints (Charge forte)",
        "desc": "50 tâches à absorber sur 3 sprints avec forte charge technique.",
        "num_sprints": 3,
        "sprint_days": 10,
        "tasks": 50,
        "effort_range": (2, 3),
        "limits": {
            "Design UI/UX": 2,
            "Développement": 3,
            "Analyse": 2,
            "QA": 2,
            "Déploiement": 2
        }
    },
    "lean_flow": {
        "name": "Flux Tendu Lean (WIP Strict = 1)",
        "desc": "1 personne max par colonne pour minimiser le Lead Time.",
        "num_sprints": 2,
        "sprint_days": 14,
        "tasks": 30,
        "effort_range": (1, 2),
        "limits": {
            "Design UI/UX": 1,
            "Développement": 1,
            "Analyse": 1,
            "QA": 1,
            "Déploiement": 1
        }
    }
}

# =============================================================================
# CAS PIXELS & DRAGONS : MODÈLE ISSU DU SUJET ET DU RENDU
# =============================================================================
# Pôles du cas : Dev, Data engineering, Infrastructure/Ops, Sécurité (RSSI), Support client.
# Les chantiers sont ceux du plan Lean IT du rendu (doublons, scaling, 5S, habilitations/RGPD...).
# Chaque chantier terminé a un effet sur le modèle (voir KanbanSimulatorWindow._apply_chantier_effect).

PD_CHANTIERS = [   # (intitulé, thème) — ordre historique du backlog, non priorisé
    ("Purge des données dupliquées en préproduction", "data"),
    ("Revue des habilitations des administrateurs", "access"),
    ("Dimensionnement nocturne des instances de calcul", "night"),
    ("Réduction de la dette technique du netcode", "debt"),
    ("Tableau de suivi unique des tickets inter-équipes", "tool"),
    ("Archivage des logs de télémétrie vers stockage froid", "data"),
    ("Scaling élastique des serveurs de jeu", "peak"),
    ("Traçabilité des accès aux bases de test", "access"),
    ("Monitoring des latences par région", "debt"),
    ("Suppression des flux de télémétrie en doublon", "data"),
    ("Test de charge du pic du vendredi soir", "peak"),
    ("Anonymisation des données joueurs (RGPD)", "access"),
    ("Extinction nocturne des instances sous-utilisées", "night"),
    ("Plan anti-rollback sur désynchronisation serveurs", "peak"),
    ("Clarification des usages SQL / NoSQL", "debt"),
    ("Nettoyage des environnements de test", "data"),
    ("Alerting proactif avant saturation des pipelines", "peak"),
    ("Rotation des accès et des secrets", "access"),
    ("Politique d'archivage et de purge des données", "data"),
    ("Runbook d'incident du vendredi soir", "peak"),
]

TAG_LABELS = {
    "peak": "PIC VENDREDI",
    "data": "DONNÉES & COÛTS",
    "access": "HABILITATIONS / RGPD",
    "night": "NUIT & ÉNERGIE",
    "debt": "DETTE TECHNIQUE",
    "tool": "OUTIL COMMUN",
}
# Ordre de priorité "flux tiré par la valeur" : d'abord ce qui réduit la cause des tickets et des coûts
PD_PRIORITY_ORDER = ["tool", "peak", "data", "access", "night", "debt"]

WEEKDAYS = ["Lun", "Mar", "Mer", "Jeu", "Ven"]

TICKET_TITLES = [
    "Latence anormale signalée par des joueurs",
    "Progression perdue après désynchronisation (rollback)",
    "Déconnexions pendant le pic de connexions",
    "Transaction de monnaie virtuelle non créditée",
    "Inventaire non synchronisé après reconnexion",
    "Combat figé / serveur de zone saturé",
]
ALERT_TITLES = [
    "Accès anormal à une base de test",
    "Compte administrateur sans traçabilité",
    "Alerte RGPD : données joueurs exposées en préproduction",
    "Pic de requêtes suspect sur la télémétrie",
]

PD_STATES = ["Backlog", "Support", "Développement", "Data", "Sécurité", "Ops/Infra", "Terminé"]

# Situation actuelle : des spécialistes dans des départements cloisonnés
PD_TEAM_SILOS = [
    ("Alix", "Développement"), ("Brune", "Développement"), ("Camille", "Développement"),
    ("Dina", "Data"), ("Elie", "Data"),
    ("Hugo", "Sécurité"),
    ("Farid", "Ops/Infra"), ("Gaëlle", "Ops/Infra"),
    ("Inès", "Support"), ("Jules", "Support"), ("Karim", "Support"),
]
# Organisation préconisée : même effectif, un équipier polyvalent dans chacun des pôles techniques
# (Dev, Data, Ops/Infra). Le Support reste complet : on ne retire pas de capacité à ceux qui répondent aux joueurs.
PD_TEAM_LEAN = [
    ("Alix", "Développement"), ("Brune", "Développement"), ("Camille", "Polyvalent"),
    ("Dina", "Data"), ("Elie", "Polyvalent"),
    ("Hugo", "Sécurité"),
    ("Farid", "Ops/Infra"), ("Gaëlle", "Polyvalent"),
    ("Inès", "Support"), ("Jules", "Support"), ("Karim", "Support"),
]

PD_ENV_BASE = {
    "demand": True,          # des tickets joueurs et des alertes de sécurité arrivent chaque jour
    "base_rate": 1.2,        # tickets joueurs par jour, du lundi au jeudi
    "alert_rate": 0.35,      # alertes de sécurité par jour
    "peak_mult": 4.0,        # multiplicateur de tickets le vendredi soir (20h-minuit)
    "data_volume": 100.0,    # indice du volume de données stockées (doublons inclus), base 100
    "night_waste": 1.0,      # part des instances de calcul sous-utilisées la nuit (1 = situation actuelle)
    "access_gaps": 8,        # failles d'habilitation ouvertes (accès non tracés, droits trop larges)
    "handoff_delay": 1,      # jours perdus à chaque passage entre pôles (un outil de suivi par département)
    "prioritize": False,     # backlog non priorisé
}

SCENARIOS["pd_silos"] = {
    "name": "Pixels & Dragons — Situation actuelle (silos)",
    "desc": "11 spécialistes cloisonnés, un outil par département, tickets avec pic du vendredi.",
    "num_sprints": 4,
    "sprint_days": 10,
    "tasks": 20,
    "effort_range": (1, 3),
    "limits": {"Support": 3, "Développement": 3, "Data": 2, "Sécurité": 1, "Ops/Infra": 2},
    "states": PD_STATES,
    "team": PD_TEAM_SILOS,
    "chantiers": PD_CHANTIERS,
    "env": dict(PD_ENV_BASE),
    "charts": ("cfd", "tickets"),
}

SCENARIOS["pd_lean"] = {
    "name": "Pixels & Dragons — Organisation préconisée (Lean IT)",
    "desc": "Même effectif : outil de suivi commun, 3 polyvalents (Dev, Data, Ops), backlog priorisé par la valeur.",
    "num_sprints": 4,
    "sprint_days": 10,
    "tasks": 20,
    "effort_range": (1, 3),
    "limits": {"Support": 3, "Développement": 3, "Data": 3, "Sécurité": 2, "Ops/Infra": 3},
    "states": PD_STATES,
    "team": PD_TEAM_LEAN,
    "chantiers": PD_CHANTIERS,
    "env": dict(PD_ENV_BASE, handoff_delay=0, prioritize=True),
    "charts": ("cfd", "tickets"),
}


# =============================================================================
# KPIs DE FIN DE SPRINT & INTERPRÉTATION (LEAN : MUDA / MURA / MURI)
# =============================================================================
def interpret_generic(rep: dict, prev: dict | None) -> list[dict]:
    """Transforme les chiffres d'un sprint en lecture Lean : niveau (vert/ambre/rouge) + commentaire."""
    rows = []

    # Débit
    delta_txt = ""
    level = "green"
    if prev is not None:
        diff = rep["delivered"] - prev["delivered"]
        delta_txt = f" ({'+' if diff >= 0 else ''}{diff} vs sprint précédent)"
        if diff < 0:
            level = "amber" if rep["delivered"] > 0 else "red"
    if rep["delivered"] == 0:
        level = "red"
    rows.append({
        "kpi": "Débit", "lean": "Valeur livrée", "level": level,
        "value": f"{rep['delivered']} tâches{delta_txt}",
        "text": ("Aucune valeur livrée : le flux est bloqué quelque part." if rep["delivered"] == 0 else
                 "Le débit recule : chercher ce qui a ralenti le flux (goulot, tâches trop grosses)." if level == "amber" else
                 "Le débit est stable ou en hausse : le flux livre régulièrement."),
    })

    # Lead time
    lt = rep["avg_lead_time"]
    if lt is None:
        rows.append({"kpi": "Lead time moyen", "lean": "Attente (muda)", "level": "amber",
                     "value": "—", "text": "Aucune livraison ce sprint, donc pas de mesure."})
    else:
        level = "green" if lt <= 6 else ("amber" if lt <= 10 else "red")
        rows.append({
            "kpi": "Lead time moyen", "lean": "Attente (muda)", "level": level,
            "value": f"{lt:.1f} jours",
            "text": ("Délai court entre le début et la livraison." if level == "green" else
                     "Les tâches traînent : du temps passe à attendre plutôt qu'à être traité." if level == "amber" else
                     "Délai très long : l'essentiel du lead time est de l'attente, pas du travail."),
        })

    # WIP moyen
    level = "green" if rep["avg_wip"] <= rep["n_workers"] * 1.5 else ("amber" if rep["avg_wip"] <= rep["n_workers"] * 2.5 else "red")
    rows.append({
        "kpi": "WIP moyen", "lean": "Stocks excessifs (muda)", "level": level,
        "value": f"{rep['avg_wip']:.1f} tâches en cours",
        "text": ("Le travail en cours reste proportionné à l'équipe." if level == "green" else
                 "Trop de tâches commencées en même temps : limiter le WIP." if level == "amber" else
                 "Stock de travail en cours très élevé : on commence plus qu'on ne finit."),
    })

    # Part en attente
    wr = rep["waiting_ratio"]
    level = "green" if wr <= 0.25 else ("amber" if wr <= 0.5 else "red")
    rows.append({
        "kpi": "Tâches en attente", "lean": "Attente (muda)", "level": level,
        "value": f"{wr * 100:.0f} % du WIP",
        "text": ("Peu de tâches attendent un équipier." if level == "green" else
                 "Une part notable des tâches attend un équipier disponible." if level == "amber" else
                 f"Plus de la moitié du WIP attend : le goulot « {rep['bottleneck'] or '—'} » étrangle le flux."),
    })

    # Utilisation équipe
    ut = rep["utilisation"]
    if ut > 0.92:
        level, txt = "red", "Équipe saturée en permanence : risque de surcharge (muri) et aucune marge pour l'imprévu."
    elif ut < 0.6:
        level, txt = "amber", "Équipe sous-utilisée : des compétences inactives (muda), souvent faute de tâches dans leur colonne."
    else:
        level, txt = "green", "Charge soutenable : l'équipe travaille sans être saturée."
    rows.append({"kpi": "Utilisation de l'équipe", "lean": "Surcharge (muri)", "level": level,
                 "value": f"{ut * 100:.0f} %", "text": txt})

    # Irrégularité
    idle = rep["zero_delivery_ratio"]
    level = "green" if idle <= 0.4 else ("amber" if idle <= 0.65 else "red")
    rows.append({
        "kpi": "Jours sans livraison", "lean": "Irrégularité (mura)", "level": level,
        "value": f"{idle * 100:.0f} % des jours",
        "text": ("Livraisons régulières." if level == "green" else
                 "Flux par à-coups : le travail s'accumule puis sort d'un coup." if level == "amber" else
                 "Flux très irrégulier : longues périodes sans rien livrer."),
    })
    return rows


def suggest_generic(rep: dict, rows: list[dict]) -> dict[str, list[str]]:
    """Propose des points Start / Stop / Continue à partir des KPIs du sprint."""
    start, stop, cont = [], [], []
    bn = rep["bottleneck"]
    by_kpi = {r["kpi"]: r for r in rows}

    if bn and by_kpi["Tâches en attente"]["level"] != "green":
        start.append(f"Renforcer la colonne « {bn} » avec un équipier polyvalent (compétences croisées).")
        stop.append(f"Pousser de nouvelles tâches vers « {bn} » tant qu'elle est saturée (respecter la limite).")
    if by_kpi["WIP moyen"]["level"] != "green":
        stop.append("Démarrer de nouvelles tâches avant d'avoir fini celles en cours.")
    if by_kpi["Utilisation de l'équipe"]["level"] == "amber":
        start.append("Rééquilibrer l'équipe : déplacer les équipiers inactifs vers les colonnes qui attendent.")
    if by_kpi["Utilisation de l'équipe"]["level"] == "red":
        start.append("Prévoir une marge de capacité (≈ 20 %) pour absorber les imprévus.")
    if by_kpi["Jours sans livraison"]["level"] != "green":
        start.append("Découper les tâches en morceaux plus petits pour livrer plus souvent.")
    for r in rows:
        if r["level"] == "green":
            cont.append(f"{r['kpi']} : {r['value']} — à maintenir.")
    if not start:
        start.append("Tester une amélioration Kaizen par sprint, mesurée par les mêmes KPIs.")
    if not stop:
        stop.append("Rien de bloquant ce sprint : surveiller les tâches qui attendent.")
    return {"start": start, "stop": stop, "continue": cont[:3]}


# --- Lecture Pixels & Dragons : chaque KPI est rattaché à un concept du rendu (muda / mura / muri / 5S)
def interpret_pd(rep: dict, prev: dict | None) -> list[dict]:
    pd = rep["pd"]
    rows = []

    def row(kpi, lean, level, value, text):
        rows.append({"kpi": kpi, "lean": lean, "level": level, "value": value, "text": text})

    # 1. Débit de chantiers
    level, delta = "green", ""
    if prev is not None:
        diff = rep["delivered"] - prev["delivered"]
        delta = f" ({'+' if diff >= 0 else ''}{diff} vs sprint précédent)"
        if diff < 0:
            level = "amber"
    if rep["delivered"] == 0:
        level = "amber" if rep["sprint"] == 1 else "red"
    row("Chantiers d'amélioration livrés", "Kaizen / valeur livrée", level,
        f"{rep['delivered']} chantiers{delta}",
        "Premier sprint : les chantiers traversent encore les pôles, la mesure sera plus parlante au sprint 2." if (rep["delivered"] == 0 and rep["sprint"] == 1) else
        "Aucun chantier livré : l'équipe n'a pas de temps pour améliorer, elle éteint des incendies." if level == "red" else
        "Le rythme d'amélioration recule : les tickets ou un goulot prennent la capacité." if level == "amber" else
        "L'équipe améliore le système en continu, pas seulement en réparant.")

    # 2. Lead time chantiers
    lt, sd = rep["avg_lead_time"], rep["sprint_days"]
    if lt is None:
        row("Lead time des chantiers", "Attente (muda)", "amber", "—", "Aucun chantier terminé ce sprint : pas de mesure.")
    else:
        level = "green" if lt <= sd else ("amber" if lt <= 1.5 * sd else "red")
        row("Lead time des chantiers", "Attente (muda)", level, f"{lt:.1f} jours",
            "Un chantier sort en moins d'un sprint." if level == "green" else
            "Les chantiers dépassent un sprint : du temps passe entre les pôles plutôt qu'à travailler." if level == "amber" else
            "Les chantiers traînent plus d'un sprint et demi : le travail attend, il n'avance pas.")

    # 3. Part en attente
    wr = rep["waiting_ratio"]
    level = "green" if wr <= 0.25 else ("amber" if wr <= 0.5 else "red")
    row("Travail en attente (% du WIP)", "Attente (muda)", level, f"{wr * 100:.0f} %",
        "Peu de travail attend une personne ou une reprise." if level == "green" else
        "Une part notable du travail attend : reprise entre pôles ou équipier indisponible." if level == "amber" else
        f"Plus de la moitié du travail attend : « {rep['bottleneck'] or '—'} » étrangle le flux.")

    # 4. Volume de données
    dv = pd["data_volume"]
    level = "green" if dv <= 97 else ("amber" if dv <= 103 else "red")
    row("Volume de données stockées (indice, base 100)", "Stocks excessifs (muda) — Seiri / Seiso", level,
        f"{dv:.0f}",
        "Les doublons et logs inutiles diminuent." if level == "green" else
        "Le volume stagne : les purges n'ont pas encore d'effet." if level == "amber" else
        "Le volume continue de croître : la télémétrie reste dupliquée entre test et production.")

    # 5. Coût cloud
    cc = pd["cloud_cost"]
    level = "green" if cc <= 90 else ("amber" if cc <= 100 else "red")
    row("Coût cloud (indice, base 100)", "Surproduction (muda)", level, f"{cc:.0f}",
        "La facture baisse : moins de stockage et moins d'instances inutiles la nuit." if level == "green" else
        "Le coût est stable : à surveiller." if level == "amber" else
        "Le coût dépasse la base de départ : les doublons et les instances de nuit pèsent sur le budget.")

    # 6. Pic du vendredi
    ratio = pd["peak_ratio"]
    level = "green" if ratio <= 2 else ("amber" if ratio <= 3 else "red")
    row("Pic du vendredi (tickets reçus / jour de semaine)", "Irrégularité (mura)", level,
        f"× {ratio:.1f}  ({pd['fri_tickets']:.1f} le vendredi contre {pd['other_tickets']:.1f})",
        "La charge est lissée sur la semaine." if level == "green" else
        "Le vendredi soir reste nettement plus chargé que le reste de la semaine." if level == "amber" else
        "Le vendredi 20h-minuit déborde : latences et rollbacks se transforment en afflux de tickets.")

    # 7. Tickets ouverts le vendredi soir
    of = pd["open_friday"]
    level = "green" if of <= 3 else ("amber" if of <= 8 else "red")
    row("Tickets ouverts le vendredi soir", "Surcharge (muri) — Support", level, f"{of:.1f} en moyenne",
        "Le Support finit la semaine sans file d'attente." if level == "green" else
        "Une file de tickets reste ouverte pour le week-end." if level == "amber" else
        "Le Support est submergé : une file importante reste ouverte jusqu'au lundi.")

    # 8. Délai de traitement d'un ticket
    tl = pd["ticket_lead_time"]
    if tl is None:
        row("Délai moyen d'un ticket joueur", "Attente (muda)", "amber", "—", "Aucun ticket clôturé ce sprint.")
    else:
        level = "green" if tl <= 1.5 else ("amber" if tl <= 3 else "red")
        row("Délai moyen d'un ticket joueur", "Attente (muda)", level, f"{tl:.1f} jours",
            "Les joueurs obtiennent une réponse rapide." if level == "green" else
            "Les joueurs attendent plusieurs jours : risque de perte de joueurs." if level == "amber" else
            "Délai trop long : les joueurs mécontents quittent le jeu.")

    # 9. Équilibre de charge entre pôles
    g, u, gi, ui = pd["busiest_group"], pd["busiest_util"], pd["idlest_group"], pd["idlest_util"]
    spread = u - ui
    if u > 0.92 and spread > 0.4:
        level, txt = "red", f"« {g} » est saturé pendant que « {gi} » manque de travail : charge mal répartie (muri et talents inutilisés)."
    elif u > 0.92:
        level, txt = "amber", "Tous les pôles sont proches de la saturation : aucune marge pour un incident ou le pic du vendredi."
    elif spread > 0.4:
        level, txt = "amber", f"Charge inégale entre « {g} » et « {gi} » : le travail n'est pas lissé (mura)."
    else:
        level, txt = "green", "Charge répartie et soutenable entre les pôles."
    row("Charge des pôles (plus / moins chargé)", "Surcharge (muri) et irrégularité (mura)", level,
        f"{g} {u * 100:.0f} %  /  {gi} {ui * 100:.0f} %", txt)

    # 10. Failles d'habilitation
    gaps = pd["access_gaps"]
    level = "green" if gaps == 0 else ("amber" if gaps <= 4 else "red")
    row("Failles d'habilitation ouvertes", "Seiketsu — accès BDD, RGPD", level, f"{gaps}",
        "Accès tracés et droits maîtrisés." if level == "green" else
        "Des accès restent à régulariser avant un contrôle RGPD." if level == "amber" else
        "Accès aux bases de test porteurs de risque : exposition RGPD tant que ces failles restent ouvertes.")

    # 11. Rituel inter-équipes
    held = pd["retros_held"]
    level = "green" if held >= rep["sprint"] - 1 else "amber"
    row("Rétrospectives inter-équipes tenues", "Shitsuke — réunions inter-équipes", level,
        f"{held} sur {rep['sprint'] - 1} sprint(s) précédent(s)" if rep["sprint"] > 1 else "à tenir à la fin de ce sprint",
        "Le premier sprint se termine par la première rétrospective inter-équipes." if rep["sprint"] == 1 else
        "Le rituel d'amélioration continue est installé." if level == "green" else
        "Des sprints passent sans rétrospective : les actions Kaizen ne sont plus suivies.")
    return rows


def suggest_pd(rep: dict, rows: list[dict]) -> dict[str, list[str]]:
    by = {r["kpi"]: r for r in rows}
    start, stop, cont = [], [], []

    peak = by["Pic du vendredi (tickets reçus / jour de semaine)"]
    open_f = by["Tickets ouverts le vendredi soir"]
    data = by["Volume de données stockées (indice, base 100)"]
    cost = by["Coût cloud (indice, base 100)"]
    wait = by["Travail en attente (% du WIP)"]
    busy = by["Charge des pôles (plus / moins chargé)"]
    gaps = by["Failles d'habilitation ouvertes"]

    if peak["level"] != "green" or open_f["level"] != "green":
        start.append("Prioriser les chantiers « Pic vendredi » (scaling élastique, test de charge, anti-rollback) : ils suppriment la cause des tickets.")
        start.append("Revue de charge le jeudi et montée en capacité avant 20h le vendredi.")
        stop.append("Traiter le vendredi soir en mode pompier, sans runbook ni alerting proactif.")
    if data["level"] != "green" or cost["level"] != "green":
        start.append("Purge et archivage des doublons de télémétrie (Seiri / Seiso), puis extinction nocturne des instances inutiles.")
        stop.append("Dupliquer les flux de télémétrie dans les environnements de test sans nettoyage.")
    if wait["level"] != "green":
        start.append("Un seul tableau de suivi pour tous les pôles et un point inter-équipes court.")
        if rep["bottleneck"]:
            start.append(f"Équipier polyvalent en renfort sur « {rep['bottleneck']} » (compétences croisées).")
        stop.append("Un outil de suivi par département : chaque changement de pôle fait perdre du temps.")
    if busy["level"] == "red":
        start.append("Rééquilibrer : former des équipiers des pôles peu chargés pour renforcer le pôle saturé.")
        stop.append("Empiler les demandes sur le même pôle sans arbitrage.")
    if busy["level"] == "amber":
        start.append("Garder environ 20 % de capacité libre et une astreinte tournante pour absorber les imprévus.")
    if gaps["level"] != "green":
        start.append("Revue des habilitations et traçabilité des accès aux bases de test avec le RSSI (RGPD).")
        stop.append("Donner des accès larges aux bases de test sans traçabilité.")
    for r in rows:
        if r["level"] == "green" and not r["kpi"].startswith("Rétrospectives"):
            cont.append(f"{r['kpi']} : {r['value']}.")
    if not start:
        start.append("Choisir une amélioration Kaizen pour le prochain sprint et la mesurer avec les mêmes KPIs.")
    if not stop:
        stop.append("Rien de bloquant ce sprint : surveiller les tickets du vendredi.")
    return {"start": start[:5], "stop": stop[:4], "continue": cont[:4]}


def interpret_report(rep: dict, prev: dict | None) -> list[dict]:
    return interpret_pd(rep, prev) if rep.get("pd") else interpret_generic(rep, prev)


def suggest_retro_items(rep: dict, rows: list[dict]) -> dict[str, list[str]]:
    return suggest_pd(rep, rows) if rep.get("pd") else suggest_generic(rep, rows)


CHART_TYPES = {
    "cfd": "Flux Cumulatif (CFD)",
    "wip": "Charge & Goulots par Étape",
    "throughput": "Débit & Livraisons / Jour",
    "leadtime": "Distribution du Lead Time",
    "tickets": "Pic du vendredi : tickets reçus / ouverts",
    "cost": "Indice données & coût cloud"
}


# =============================================================================
# COMPOSANTS UI ÉPURÉS (SANS FLÈCHES ▲▼)
# =============================================================================
class CleanStepper(QWidget):
    def __init__(self, value: int, min_val: int, max_val: int, on_change, compact: bool = False, parent=None):
        super().__init__(parent)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.on_change = on_change

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4 if not compact else 2)

        btn_size = 22 if compact else 28
        font_sz = "11px" if compact else "13px"

        self.btn_minus = QPushButton("−")
        self.btn_minus.setFixedSize(btn_size, btn_size)
        self.btn_minus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minus.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 5px;
                font-size: {font_sz};
                font-weight: 800;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: #FEF2F2;
                border-color: #FCA5A5;
                color: #DC2626;
            }}
        """)
        self.btn_minus.clicked.connect(self.decrement)

        self.lbl_val = QLabel(str(self.value))
        self.lbl_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_val.setMinimumWidth(24 if compact else 34)
        self.lbl_val.setStyleSheet(f"""
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1px solid #E2E8F0;
            border-radius: 5px;
            padding: 2px 4px;
            font-size: {font_sz};
            font-weight: 800;
        """)

        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedSize(btn_size, btn_size)
        self.btn_plus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_plus.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
                border-radius: 5px;
                font-size: {font_sz};
                font-weight: 800;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: #F0FDF4;
                border-color: #86EFAC;
                color: #16A34A;
            }}
        """)
        self.btn_plus.clicked.connect(self.increment)

        layout.addWidget(self.btn_minus)
        layout.addWidget(self.lbl_val)
        layout.addWidget(self.btn_plus)

    def set_value(self, val: int):
        self.value = max(self.min_val, min(self.max_val, val))
        self.lbl_val.setText(str(self.value))

    def decrement(self):
        if self.value > self.min_val:
            self.value -= 1
            self.lbl_val.setText(str(self.value))
            if self.on_change:
                self.on_change(self.value)

    def increment(self):
        if self.value < self.max_val:
            self.value += 1
            self.lbl_val.setText(str(self.value))
            if self.on_change:
                self.on_change(self.value)


def style_clean_combobox(combo: QComboBox):
    combo.setStyleSheet("""
        QComboBox {
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 11.5px;
            font-weight: 700;
        }
        QComboBox:focus {
            border: 1px solid #16A34A;
        }
        QComboBox::drop-down {
            border: none;
            width: 22px;
        }
        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            selection-background-color: #F0FDF4;
            selection-color: #15803D;
        }
    """)


# =============================================================================
# COMPOSANT RÉUTILISABLE : ÉDITEUR DES CATÉGORIES (DÉPLACER / AVANT / APRÈS / SUPPRIMER)
# =============================================================================
class CategoryFlowEditor(QWidget):
    """Permet de réordonner (↑ Avant / ↓ Après / glisser-déposer), ajouter avant/après une catégorie, ou supprimer."""
    def __init__(self, states: list[str], limits: dict[str, int], on_updated=None, list_height: int = 135, parent=None):
        super().__init__(parent)
        self.states = list(states)
        self.limits = dict(limits)
        self.on_updated = on_updated

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)

        add_grid = QGridLayout()
        add_grid.setSpacing(6)

        self.input_new_cat = QLineEdit()
        self.input_new_cat.setPlaceholderText("Nom nouvelle catégorie (ex: Infra, Revue Code)...")
        self.input_new_cat.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 6px 9px;
                font-size: 11.5px;
                background: #FFFFFF;
            }
            QLineEdit:focus { border: 1px solid #16A34A; }
        """)
        self.input_new_cat.returnPressed.connect(self.add_category)

        self.combo_position = QComboBox()
        style_clean_combobox(self.combo_position)

        btn_add = QPushButton("+ Ajouter")
        btn_add.setObjectName("btnGreen")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.add_category)

        add_grid.addWidget(self.input_new_cat, 0, 0, 1, 2)
        add_grid.addWidget(self.combo_position, 1, 0)
        add_grid.addWidget(btn_add, 1, 1)
        layout.addLayout(add_grid)

        self.list_widget = QListWidget()
        self.list_widget.setFixedHeight(list_height)
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.list_widget.model().rowsMoved.connect(lambda *args: QTimer.singleShot(0, self._on_rows_dragged))
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 3px;
                background: #FFFFFF;
                font-size: 11.5px;
                font-weight: 700;
                color: #0F172A;
            }
            QListWidget::item {
                padding: 5px 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: #F0FDF4;
                color: #15803D;
                border: 1px solid #86EFAC;
            }
        """)
        layout.addWidget(self.list_widget)

        actions_row = QHBoxLayout()
        actions_row.setSpacing(6)

        btn_move_before = QPushButton("↑ Avant")
        btn_move_before.setObjectName("btnOutline")
        btn_move_before.setToolTip("Déplacer la catégorie sélectionnée plus tôt dans le flux")
        btn_move_before.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_move_before.clicked.connect(lambda: self.move_selected(-1))

        btn_move_after = QPushButton("↓ Après")
        btn_move_after.setObjectName("btnOutline")
        btn_move_after.setToolTip("Déplacer la catégorie sélectionnée plus tard dans le flux")
        btn_move_after.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_move_after.clicked.connect(lambda: self.move_selected(1))

        btn_delete = QPushButton("Supprimer")
        btn_delete.setObjectName("btnRed")
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.clicked.connect(self.delete_selected)

        actions_row.addWidget(btn_move_before)
        actions_row.addWidget(btn_move_after)
        actions_row.addStretch()
        actions_row.addWidget(btn_delete)
        layout.addLayout(actions_row)

        self.refresh_ui()

    def _active_stages(self) -> list[str]:
        return self.states[1:-1]

    def refresh_ui(self, select_name: str | None = None):
        active = self._active_stages()

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        target_row = 0
        for idx, stage in enumerate(active):
            item = QListWidgetItem(f"{idx + 1}.  {stage}")
            item.setData(Qt.ItemDataRole.UserRole, stage)
            self.list_widget.addItem(item)
            if select_name and stage == select_name:
                target_row = idx
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(target_row)
        self.list_widget.blockSignals(False)

        prev_data = self.combo_position.currentData()
        self.combo_position.clear()
        self.combo_position.addItem("Position : À la fin (avant Terminé)", "END")
        self.combo_position.addItem("Position : Au début (après Backlog)", "START")
        for stage in active:
            self.combo_position.addItem(f"Avant : {stage}", f"BEFORE:{stage}")
            self.combo_position.addItem(f"Après : {stage}", f"AFTER:{stage}")

        if prev_data:
            idx_found = self.combo_position.findData(prev_data)
            if idx_found >= 0:
                self.combo_position.setCurrentIndex(idx_found)

    def _on_rows_dragged(self):
        reordered = []
        for i in range(self.list_widget.count()):
            stage_name = self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            reordered.append(stage_name)
        current_sel = self.list_widget.currentItem().data(Qt.ItemDataRole.UserRole) if self.list_widget.currentItem() else None
        self.states = [self.states[0]] + reordered + [self.states[-1]]
        self.refresh_ui(select_name=current_sel)
        if self.on_updated:
            self.on_updated()

    def move_selected(self, delta: int):
        row = self.list_widget.currentRow()
        active = self._active_stages()
        if row < 0 or row >= len(active):
            return
        new_row = row + delta
        if new_row < 0 or new_row >= len(active):
            return

        moved_name = active.pop(row)
        active.insert(new_row, moved_name)
        self.states = [self.states[0]] + active + [self.states[-1]]
        self.refresh_ui(select_name=moved_name)
        if self.on_updated:
            self.on_updated()

    def delete_selected(self):
        row = self.list_widget.currentRow()
        active = self._active_stages()
        if row < 0 or row >= len(active):
            return
        if len(active) <= 1:
            QMessageBox.information(self, "Action impossible", "Il faut conserver au moins une catégorie entre Backlog et Terminé.")
            return
        removed = active.pop(row)
        self.limits.pop(removed, None)
        self.states = [self.states[0]] + active + [self.states[-1]]
        next_sel = active[min(row, len(active) - 1)] if active else None
        self.refresh_ui(select_name=next_sel)
        if self.on_updated:
            self.on_updated()

    def add_category(self):
        name = self.input_new_cat.text().strip()
        if not name:
            return
        if any(s.lower() == name.lower() for s in self.states):
            QMessageBox.warning(self, "Doublon", f"La catégorie « {name} » existe déjà.")
            return

        active = self._active_stages()
        pos_code = self.combo_position.currentData()

        if pos_code == "START":
            insert_idx = 0
        elif pos_code and pos_code.startswith("BEFORE:"):
            target = pos_code.split(":", 1)[1]
            insert_idx = active.index(target) if target in active else len(active)
        elif pos_code and pos_code.startswith("AFTER:"):
            target = pos_code.split(":", 1)[1]
            insert_idx = (active.index(target) + 1) if target in active else len(active)
        else:
            insert_idx = len(active)

        active.insert(insert_idx, name)
        self.states = [self.states[0]] + active + [self.states[-1]]
        self.limits[name] = 2
        self.input_new_cat.clear()
        self.refresh_ui(select_name=name)
        if self.on_updated:
            self.on_updated()


# =============================================================================
# MODÈLES MÉTIER
# =============================================================================
class Task:
    def __init__(self, task_id: int, title: str, states: list[str], effort_range=(1, 2),
                 start_state_idx: int = 0, category_tag: str = "", kind: str = "chantier",
                 tag: str = "", efforts: dict | None = None):
        self.id = task_id
        self.title = title
        self.kind = kind                  # "chantier" (planifié) | "ticket" (joueur) | "alerte" (sécurité)
        self.tag = tag                    # thème du chantier (peak, data, access, night, debt, tool)
        self.label = f"US-{task_id:02d}"
        if efforts is not None:
            self.effort_per_stage = {state: efforts.get(state, 0) for state in states[1:-1]}
        else:
            self.effort_per_stage = {state: random.randint(*effort_range) for state in states[1:-1]}
        self.progress = 0
        self.state_index = start_state_idx
        self.category_tag = category_tag
        self.assigned_workers = []
        self.start_day = 0 if start_state_idx > 0 else None
        self.end_day = None
        self.ready_day = 0                # jour à partir duquel un équipier peut reprendre la tâche


class Worker:
    def __init__(self, worker_id: int, name: str, specialty: str):
        self.id = worker_id
        self.name = name
        self.specialty = specialty
        self.color = PALETTE["workers"][(worker_id - 1) % len(PALETTE["workers"])]
        self.assigned_task = None


# =============================================================================
# FENÊTRE MODALE : GESTION DE L'ÉQUIPE (OUVERTE DEPUIS LES PARAMÈTRES)
# =============================================================================
class TeamManagerDialog(QDialog):
    def __init__(self, team_specs: list[tuple[str, str]], active_categories: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestion de l'Équipe & Rôles")
        self.setFixedSize(490, 470)
        self.team_specs = list(team_specs)
        self.categories = list(active_categories) + ["Polyvalent (Toutes)"]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Équipiers & Affectation par Catégorie")
        title.setStyleSheet("font-size: 15px; font-weight: 800; color: #0F172A;")
        layout.addWidget(title)

        sub = QLabel("Chaque équipier intervient dans sa catégorie assignée (ou partout si Polyvalent).")
        sub.setStyleSheet("font-size: 11px; color: #64748B;")
        layout.addWidget(sub)

        add_row = QHBoxLayout()
        add_row.setSpacing(6)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Prénom (ex: Clara, Youssef...)")
        self.input_name.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 7px 10px;
                font-size: 12px;
                background: #FFFFFF;
            }
            QLineEdit:focus { border: 1px solid #16A34A; }
        """)
        self.input_name.returnPressed.connect(self.add_member)

        self.combo_cat = QComboBox()
        self.combo_cat.addItems(self.categories)
        style_clean_combobox(self.combo_cat)

        btn_add = QPushButton("+ Ajouter")
        btn_add.setObjectName("btnGreen")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(self.add_member)

        add_row.addWidget(self.input_name, stretch=2)
        add_row.addWidget(self.combo_cat, stretch=2)
        add_row.addWidget(btn_add)
        layout.addLayout(add_row)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 4px;
                background: #F8FAFC;
                font-size: 12px;
                font-weight: 700;
                color: #0F172A;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: #FEF3C7;
                color: #92400E;
            }
        """)
        self._refresh_list()
        layout.addWidget(self.list_widget)

        bottom_row = QHBoxLayout()
        btn_remove = QPushButton("Retirer la sélection")
        btn_remove.setObjectName("btnRed")
        btn_remove.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_remove.clicked.connect(self.remove_member)

        btn_apply = QPushButton("Valider l'équipe")
        btn_apply.setObjectName("btnAmber")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.clicked.connect(self.accept)

        bottom_row.addWidget(btn_remove)
        bottom_row.addStretch()
        bottom_row.addWidget(btn_apply)
        layout.addLayout(bottom_row)

    def _refresh_list(self):
        self.list_widget.clear()
        for idx, (name, cat) in enumerate(self.team_specs, start=1):
            self.list_widget.addItem(f"#{idx}   {name}   —   [{cat}]")

    def add_member(self):
        raw = self.input_name.text().strip()
        if not raw:
            raw = f"Équipier {len(self.team_specs) + 1}"
        if any(n.lower() == raw.lower() for n, _ in self.team_specs):
            QMessageBox.warning(self, "Doublon", f"{raw} fait déjà partie de l'équipe.")
            return
        chosen_cat = self.combo_cat.currentText()
        if chosen_cat.startswith("Polyvalent"):
            chosen_cat = "Polyvalent"
        self.team_specs.append((raw, chosen_cat))
        self.input_name.clear()
        self._refresh_list()

    def remove_member(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        if len(self.team_specs) <= 1:
            QMessageBox.information(self, "Action impossible", "Il faut conserver au moins 1 équipier.")
            return
        self.team_specs.pop(row)
        self._refresh_list()


# =============================================================================
# FENÊTRE MODALE : PARAMÈTRES COMPLETS
# =============================================================================
class SettingsDialog(QDialog):
    def __init__(self, app_ref, parent=None):
        super().__init__(parent)
        self.app = app_ref
        self.setWindowTitle("Paramètres de Simulation, Catégories, Équipe, Tâches & Graphiques")
        self.resize(900, 710)

        self.working_team_specs = list(self.app.team_specs)

        self.selected_scenario = self.app.active_scenario_key
        self.selected_chart_1 = self.app.chart_slot_1
        self.selected_chart_2 = self.app.chart_slot_2

        self.new_num_sprints = self.app.num_sprints
        self.new_sprint_days = self.app.sprint_duration
        self.new_total_tasks = len(self.app.tasks)
        self.scenario_applied = False

        self.pending_custom_tasks: list[dict] = []

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 16, 20, 16)
        root_layout.setSpacing(12)

        hdr = QLabel("PARAMÈTRES GÉNÉRAUX DU SIMULATEUR")
        hdr.setStyleSheet("font-size: 16px; font-weight: 900; color: #0F172A; letter-spacing: 0.4px;")
        root_layout.addWidget(hdr)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_body = QWidget()
        grid = QGridLayout(scroll_body)
        grid.setContentsMargins(0, 0, 6, 0)
        grid.setSpacing(14)

        # 1. SPRINTS & ÉQUIPE
        card_sprint = self._make_section_card("1. SPRINTS & ÉQUIPE")
        cs_lay = card_sprint.layout()

        row_ns = QHBoxLayout()
        lbl_ns = QLabel("Nombre de sprints à exécuter :")
        lbl_ns.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
        self.stepper_num_sprints = CleanStepper(self.new_num_sprints, 1, 10, self._on_num_sprints_changed)
        row_ns.addWidget(lbl_ns)
        row_ns.addStretch()
        row_ns.addWidget(self.stepper_num_sprints)
        cs_lay.addLayout(row_ns)

        row_sp = QHBoxLayout()
        lbl_sp = QLabel("Durée d'un sprint (jours) :")
        lbl_sp.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
        self.stepper_sprint_days = CleanStepper(self.new_sprint_days, 5, 45, self._on_sprint_days_changed)
        row_sp.addWidget(lbl_sp)
        row_sp.addStretch()
        row_sp.addWidget(self.stepper_sprint_days)
        cs_lay.addLayout(row_sp)

        self.lbl_horizon_info = QLabel(f"Horizon total : {self.new_num_sprints * self.new_sprint_days} jours")
        self.lbl_horizon_info.setStyleSheet("font-size: 11px; font-weight: 800; color: #16A34A;")
        cs_lay.addWidget(self.lbl_horizon_info)

        row_eq = QHBoxLayout()
        self.lbl_eq_ref = QLabel(f"Équipe ({len(self.working_team_specs)} équipiers) :")
        self.lbl_eq_ref.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
        btn_open_team = QPushButton("+ Équipiers / Rôles")
        btn_open_team.setObjectName("btnOutline")
        btn_open_team.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open_team.clicked.connect(self._open_team_from_settings)
        row_eq.addWidget(self.lbl_eq_ref)
        row_eq.addStretch()
        row_eq.addWidget(btn_open_team)
        cs_lay.addLayout(row_eq)
        cs_lay.addStretch()

        grid.addWidget(card_sprint, 0, 0)

        # 2. CATÉGORIES DU FLUX
        card_cats = self._make_section_card("2. CATÉGORIES DU FLUX (ORDRE, AJOUT, SUPPRESSION)")
        cc_lay = card_cats.layout()

        self.cat_editor = CategoryFlowEditor(
            self.app.states,
            self.app.col_worker_limits,
            on_updated=self._on_categories_changed,
            list_height=130
        )
        cc_lay.addWidget(self.cat_editor)

        grid.addWidget(card_cats, 0, 1)

        # 3. GESTION DES TÂCHES
        card_tasks = self._make_section_card("3. GESTION DU BACKLOG & + TÂCHES")
        ct_lay = card_tasks.layout()

        row_tc = QHBoxLayout()
        lbl_tc = QLabel("Nombre total de tâches :")
        lbl_tc.setStyleSheet("font-size: 12px; font-weight: 700; color: #334155;")
        self.stepper_tasks = CleanStepper(self.new_total_tasks, 5, 100, self._on_task_count_changed)
        btn_bulk_10 = QPushButton("+10 tâches")
        btn_bulk_10.setObjectName("btnOutline")
        btn_bulk_10.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_bulk_10.clicked.connect(self._add_ten_tasks)

        row_tc.addWidget(lbl_tc)
        row_tc.addStretch()
        row_tc.addWidget(btn_bulk_10)
        row_tc.addWidget(self.stepper_tasks)
        ct_lay.addLayout(row_tc)

        lbl_form = QLabel("Créer une tâche spécifique :")
        lbl_form.setStyleSheet("font-size: 11px; font-weight: 800; color: #0F172A; margin-top: 4px;")
        ct_lay.addWidget(lbl_form)

        self.input_task_title = QLineEdit()
        self.input_task_title.setPlaceholderText("Intitulé de la tâche (ex: Refonte écran panier)...")
        self.input_task_title.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CBD5E1; border-radius: 5px;
                padding: 6px 8px; font-size: 11.5px; background: #FFFFFF;
            }
        """)
        ct_lay.addWidget(self.input_task_title)

        row_t_cat = QHBoxLayout()
        lbl_t_cat = QLabel("Appliquer à la catégorie :")
        lbl_t_cat.setStyleSheet("font-size: 11px; font-weight: 700; color: #475569;")
        self.combo_task_cat = QComboBox()
        style_clean_combobox(self.combo_task_cat)
        row_t_cat.addWidget(lbl_t_cat)
        row_t_cat.addWidget(self.combo_task_cat, stretch=1)
        ct_lay.addLayout(row_t_cat)

        row_t_pos = QHBoxLayout()
        lbl_t_pos = QLabel("Ordre de passage :")
        lbl_t_pos.setStyleSheet("font-size: 11px; font-weight: 700; color: #475569;")
        self.combo_task_order = QComboBox()
        style_clean_combobox(self.combo_task_order)
        self._populate_task_order_combo()
        row_t_pos.addWidget(lbl_t_pos)
        row_t_pos.addWidget(self.combo_task_order, stretch=1)
        ct_lay.addLayout(row_t_pos)

        btn_create_task = QPushButton("+ Tâches (Ajouter au tableau)")
        btn_create_task.setObjectName("btnGreen")
        btn_create_task.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_create_task.clicked.connect(self._create_targeted_task)
        ct_lay.addWidget(btn_create_task)

        grid.addWidget(card_tasks, 1, 0)

        # 4. SCÉNARIOS & CHOIX DES GRAPHIQUES
        right_col_vbox = QVBoxLayout()
        right_col_vbox.setSpacing(12)

        card_scen = self._make_section_card("4. SCÉNARIOS DE FLUX")
        sc_lay = card_scen.layout()
        self.scen_buttons: dict[str, QPushButton] = {}
        for key, data in SCENARIOS.items():
            btn = QPushButton(f"{data['name']} — {data['desc']}")
            btn.setCheckable(True)
            btn.setChecked(key == self.selected_scenario)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, k=key: self._select_scenario(k))
            self._style_scenario_btn(btn, key == self.selected_scenario)
            sc_lay.addWidget(btn)
            self.scen_buttons[key] = btn
        right_col_vbox.addWidget(card_scen)

        card_charts = self._make_section_card("5. GRAPHIQUES AFFICHÉS EN HAUT")
        ch_lay = card_charts.layout()

        lbl_g1 = QLabel("Graphique de gauche :")
        lbl_g1.setStyleSheet("font-size: 11px; font-weight: 800; color: #475569;")
        ch_lay.addWidget(lbl_g1)

        self.g1_btns: dict[str, QPushButton] = {}
        g1_grid = QGridLayout()
        g1_grid.setSpacing(5)
        for idx, (ckey, clabel) in enumerate(CHART_TYPES.items()):
            b = QPushButton(clabel)
            b.setCheckable(True)
            b.setChecked(ckey == self.selected_chart_1)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda checked, k=ckey: self._select_chart(1, k))
            self._style_pill_btn(b, ckey == self.selected_chart_1, "#16A34A")
            g1_grid.addWidget(b, idx // 2, idx % 2)
            self.g1_btns[ckey] = b
        ch_lay.addLayout(g1_grid)

        lbl_g2 = QLabel("Graphique de droite :")
        lbl_g2.setStyleSheet("font-size: 11px; font-weight: 800; color: #475569; margin-top: 4px;")
        ch_lay.addWidget(lbl_g2)

        self.g2_btns: dict[str, QPushButton] = {}
        g2_grid = QGridLayout()
        g2_grid.setSpacing(5)
        for idx, (ckey, clabel) in enumerate(CHART_TYPES.items()):
            b = QPushButton(clabel)
            b.setCheckable(True)
            b.setChecked(ckey == self.selected_chart_2)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda checked, k=ckey: self._select_chart(2, k))
            self._style_pill_btn(b, ckey == self.selected_chart_2, "#D97706")
            g2_grid.addWidget(b, idx // 2, idx % 2)
            self.g2_btns[ckey] = b
        ch_lay.addLayout(g2_grid)

        right_col_vbox.addWidget(card_charts)
        grid.addLayout(right_col_vbox, 1, 1)

        scroll.setWidget(scroll_body)
        root_layout.addWidget(scroll)

        self._on_categories_changed()

        footer = QHBoxLayout()
        btn_cancel = QPushButton("Annuler")
        btn_cancel.setObjectName("btnOutline")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Appliquer et mettre à jour")
        btn_save.setObjectName("btnGreen")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.accept)

        footer.addStretch()
        footer.addWidget(btn_cancel)
        footer.addWidget(btn_save)
        root_layout.addLayout(footer)

    @property
    def working_states(self) -> list[str]:
        return self.cat_editor.states

    @property
    def working_limits(self) -> dict[str, int]:
        return self.cat_editor.limits

    def _make_section_card(self, title_text: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
        """)
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(12, 10, 12, 12)
        vbox.setSpacing(8)
        lbl = QLabel(title_text)
        lbl.setStyleSheet("font-size: 10px; font-weight: 900; color: #0F172A; letter-spacing: 0.5px; border: none;")
        vbox.addWidget(lbl)
        return card

    def _style_scenario_btn(self, btn: QPushButton, active: bool):
        if active:
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    background-color: #F0FDF4;
                    color: #14532D;
                    border: 1px solid #16A34A;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 10.5px;
                    font-weight: 700;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    background-color: #FFFFFF;
                    color: #334155;
                    border: 1px solid #E2E8F0;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 10.5px;
                    font-weight: 600;
                }
                QPushButton:hover { border-color: #94A3B8; }
            """)

    def _style_pill_btn(self, btn: QPushButton, active: bool, accent_hex: str):
        if active:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {accent_hex};
                    color: #FFFFFF;
                    border: none;
                    border-radius: 5px;
                    padding: 6px 6px;
                    font-size: 10px;
                    font-weight: 800;
                }}
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    color: #475569;
                    border: 1px solid #CBD5E1;
                    border-radius: 5px;
                    padding: 6px 6px;
                    font-size: 10px;
                    font-weight: 700;
                }
                QPushButton:hover { background-color: #F1F5F9; }
            """)

    def _on_categories_changed(self):
        active_cats = self.working_states[1:-1]
        prev_sel = self.combo_task_cat.currentText()
        self.combo_task_cat.clear()
        self.combo_task_cat.addItem("Backlog (Parcours complet)")
        for c in active_cats:
            self.combo_task_cat.addItem(c)
        idx = self.combo_task_cat.findText(prev_sel)
        if idx >= 0:
            self.combo_task_cat.setCurrentIndex(idx)

    def _populate_task_order_combo(self):
        self.combo_task_order.clear()
        self.combo_task_order.addItem("En premier (Prioritaire — avant toutes les tâches)", "FIRST")
        self.combo_task_order.addItem("En fin de file (Après les tâches existantes)", "LAST")
        for t in [x for x in self.app.tasks if x.kind == "chantier"][:30]:
            short_t = t.title[:34] + "..." if len(t.title) > 34 else t.title
            self.combo_task_order.addItem(f"Avant US-{t.id:02d} : {short_t}", f"BEFORE:{t.id}")

    def _on_num_sprints_changed(self, val: int):
        self.new_num_sprints = val
        self.lbl_horizon_info.setText(f"Horizon total : {self.new_num_sprints * self.new_sprint_days} jours")

    def _on_sprint_days_changed(self, val: int):
        self.new_sprint_days = val
        self.lbl_horizon_info.setText(f"Horizon total : {self.new_num_sprints * self.new_sprint_days} jours")

    def _on_task_count_changed(self, val: int):
        self.new_total_tasks = val

    def _add_ten_tasks(self):
        self.new_total_tasks = min(100, self.new_total_tasks + 10)
        self.stepper_tasks.set_value(self.new_total_tasks)

    def _open_team_from_settings(self):
        dlg = TeamManagerDialog(self.working_team_specs, self.working_states[1:-1], self)
        if dlg.exec():
            self.working_team_specs = dlg.team_specs
            self.lbl_eq_ref.setText(f"Équipe ({len(self.working_team_specs)} équipiers) :")

    def _create_targeted_task(self):
        title = self.input_task_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Champ vide", "Veuillez saisir un intitulé pour la tâche.")
            return

        chosen_cat = self.combo_task_cat.currentText()
        order_code = self.combo_task_order.currentData()

        self.pending_custom_tasks.append({
            "title": title,
            "category": chosen_cat,
            "order": order_code
        })
        self.input_task_title.clear()
        self.new_total_tasks = min(100, self.new_total_tasks + 1)
        self.stepper_tasks.set_value(self.new_total_tasks)

        pos_label = self.combo_task_order.currentText()
        QMessageBox.information(
            self,
            "Tâche programmée",
            f"Tâche : « {title} »\nCatégorie : {chosen_cat}\nPosition : {pos_label}"
        )

    def _select_scenario(self, key: str):
        self.selected_scenario = key
        self.scenario_applied = True
        sc = SCENARIOS[key]
        self.new_num_sprints = sc["num_sprints"]
        self.new_sprint_days = sc["sprint_days"]
        self.new_total_tasks = sc["tasks"] + len(self.pending_custom_tasks)

        self.stepper_num_sprints.set_value(self.new_num_sprints)
        self.stepper_sprint_days.set_value(self.new_sprint_days)
        self.stepper_tasks.set_value(self.new_total_tasks)
        self.lbl_horizon_info.setText(f"Horizon total : {self.new_num_sprints * self.new_sprint_days} jours")

        for k, b in self.scen_buttons.items():
            b.setChecked(k == key)
            self._style_scenario_btn(b, k == key)

    def _select_chart(self, slot: int, key: str):
        if slot == 1:
            self.selected_chart_1 = key
            for k, b in self.g1_btns.items():
                b.setChecked(k == key)
                self._style_pill_btn(b, k == key, "#16A34A")
        else:
            self.selected_chart_2 = key
            for k, b in self.g2_btns.items():
                b.setChecked(k == key)
                self._style_pill_btn(b, k == key, "#D97706")


# =============================================================================
# FENÊTRE MODALE : BILAN DE FIN DE SPRINT (KPIs + INTERPRÉTATION)
# =============================================================================
LEVEL_COLORS = {
    "green": ("#16A34A", "#F0FDF4", "#BBF7D0"),
    "amber": ("#D97706", "#FFFBEB", "#FDE68A"),
    "red": ("#DC2626", "#FEF2F2", "#FECACA"),
}


class SprintReportDialog(QDialog):
    def __init__(self, rep: dict, rows: list[dict], total_sprints: int, parent=None):
        super().__init__(parent)
        self.open_retro = False
        self.setWindowTitle(f"Bilan de fin de sprint {rep['sprint']}/{total_sprints}")
        self.setMinimumWidth(980)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(10)

        title = QLabel(f"SPRINT {rep['sprint']} / {total_sprints} — KPIs ET INTERPRÉTATION")
        title.setStyleSheet("font-size: 15px; font-weight: 900; color: #0F172A; letter-spacing: 0.4px;")
        layout.addWidget(title)

        sub = QLabel(f"Jours {rep['start_day'] + 1} à {rep['end_day']} — équipe de {rep['n_workers']} personnes")
        sub.setStyleSheet("font-size: 11px; color: #64748B;")
        layout.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(470)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        body = QWidget()
        rows_layout = QVBoxLayout(body)
        rows_layout.setContentsMargins(0, 0, 6, 0)
        rows_layout.setSpacing(6)
        scroll.setWidget(body)
        layout.addWidget(scroll)

        for r in rows:
            fg, bg, border = LEVEL_COLORS[r["level"]]
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background-color: {bg}; border: 1px solid {border}; border-left: 4px solid {fg}; border-radius: 6px; }}")
            h = QHBoxLayout(card)
            h.setContentsMargins(10, 6, 10, 6)
            h.setSpacing(12)

            left = QVBoxLayout()
            left.setSpacing(1)
            lbl_k = QLabel(r["kpi"])
            lbl_k.setWordWrap(True)
            lbl_k.setStyleSheet("font-size: 11.5px; font-weight: 800; color: #0F172A; border: none;")
            lbl_l = QLabel(r["lean"])
            lbl_l.setStyleSheet("font-size: 9.5px; font-weight: 700; color: #64748B; border: none;")
            left.addWidget(lbl_k)
            left.addWidget(lbl_l)
            wl = QWidget()
            wl.setLayout(left)
            wl.setFixedWidth(250)
            wl.setStyleSheet("border: none; background: transparent;")

            lbl_v = QLabel(r["value"])
            lbl_v.setStyleSheet(f"font-size: 12px; font-weight: 900; color: {fg}; border: none;")
            lbl_v.setFixedWidth(230)
            lbl_v.setWordWrap(True)

            lbl_t = QLabel(r["text"])
            lbl_t.setWordWrap(True)
            lbl_t.setStyleSheet("font-size: 11px; color: #334155; border: none;")

            h.addWidget(wl)
            h.addWidget(lbl_v)
            h.addWidget(lbl_t, stretch=1)
            rows_layout.addWidget(card)
        rows_layout.addStretch()

        bn = rep["bottleneck"]
        lbl_bn = QLabel(f"Goulot principal du sprint : {bn}" if bn else "Aucun goulot marqué sur ce sprint.")
        lbl_bn.setStyleSheet("font-size: 12px; font-weight: 800; color: #B91C1C;" if bn else "font-size: 12px; font-weight: 700; color: #15803D;")
        layout.addWidget(lbl_bn)

        footer = QHBoxLayout()
        footer.addStretch()
        btn_next = QPushButton("Continuer la simulation")
        btn_next.setObjectName("btnOutline")
        btn_next.clicked.connect(self.accept)
        btn_retro = QPushButton("Ouvrir la rétrospective ▸")
        btn_retro.setObjectName("btnGreen")
        btn_retro.clicked.connect(self._go_retro)
        footer.addWidget(btn_next)
        footer.addWidget(btn_retro)
        layout.addLayout(footer)

    def _go_retro(self):
        self.open_retro = True
        self.accept()


# =============================================================================
# FENÊTRE MODALE : RÉTROSPECTIVE (START / STOP / CONTINUE + ACTION KAIZEN)
# =============================================================================
class RetrospectiveDialog(QDialog):
    def __init__(self, rep: dict, rows: list[dict], app_ref, parent=None):
        super().__init__(parent)
        self.rep = rep
        self.app = app_ref
        self.setWindowTitle(f"Rétrospective — sprint {rep['sprint']}")
        self.setMinimumWidth(820)
        self.result_data: dict = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 16)
        layout.setSpacing(10)

        title = QLabel(f"RÉTROSPECTIVE DU SPRINT {rep['sprint']}")
        title.setStyleSheet("font-size: 15px; font-weight: 900; color: #0F172A; letter-spacing: 0.4px;")
        layout.addWidget(title)

        sub = QLabel("Suggestions générées à partir des KPIs : modifiez-les, complétez-les, puis choisissez l'action Kaizen du prochain sprint.")
        sub.setStyleSheet("font-size: 11px; color: #64748B;")
        sub.setWordWrap(True)
        layout.addWidget(sub)

        sugg = suggest_retro_items(rep, rows)
        cols = QHBoxLayout()
        cols.setSpacing(10)
        self.edits: dict[str, QTextEdit] = {}
        for key, label, color in (("start", "START — à commencer", "#16A34A"),
                                  ("stop", "STOP — à arrêter", "#DC2626"),
                                  ("continue", "CONTINUE — à garder", "#D97706")):
            box = QVBoxLayout()
            lbl = QLabel(label)
            lbl.setStyleSheet(f"font-size: 10.5px; font-weight: 900; color: {color}; letter-spacing: 0.4px;")
            ed = QTextEdit()
            ed.setPlainText("\n".join(f"- {s}" for s in sugg[key]))
            ed.setMinimumHeight(150)
            ed.setStyleSheet("QTextEdit { border: 1px solid #CBD5E1; border-radius: 6px; font-size: 11px; padding: 4px; }")
            box.addWidget(lbl)
            box.addWidget(ed)
            cols.addLayout(box)
            self.edits[key] = ed
        layout.addLayout(cols)

        lbl_k = QLabel("ACTION KAIZEN POUR LE PROCHAIN SPRINT (appliquée à la simulation)")
        lbl_k.setStyleSheet("font-size: 10.5px; font-weight: 900; color: #0F172A; letter-spacing: 0.4px; margin-top: 6px;")
        layout.addWidget(lbl_k)

        bn = rep["bottleneck"]
        self.chk_limit = QCheckBox(
            f"Augmenter de 1 la capacité de la colonne « {bn} »" if bn else "Aucune colonne goulot à renforcer")
        self.chk_limit.setEnabled(bool(bn))
        self.chk_limit.setChecked(bool(bn))
        layout.addWidget(self.chk_limit)

        self.donor = self.app.find_cross_training_candidate(bn) if bn else None
        txt = (f"Former {self.donor.name} (colonne « {self.donor.specialty} ») pour qu'il devienne polyvalent et renforce les goulots"
               if self.donor else "Aucun équipier spécialiste disponible pour devenir polyvalent")
        self.chk_poly = QCheckBox(txt)
        self.chk_poly.setEnabled(self.donor is not None)
        by0 = {r["kpi"]: r for r in rows}
        wait_lvl = by0.get("Travail en attente (% du WIP)", by0.get("Tâches en attente", {})).get("level")
        self.chk_poly.setChecked(self.donor is not None and wait_lvl in ("amber", "red"))
        layout.addWidget(self.chk_poly)

        # Actions propres au cas Pixels & Dragons (liées au modèle du simulateur)
        self.combo_prio = QComboBox()
        style_clean_combobox(self.combo_prio)
        self.chk_tool = QCheckBox("Mettre en place un outil de suivi commun à tous les pôles (supprime le délai de reprise entre pôles)")
        by = {r["kpi"]: r for r in rows}
        if self.app.env is not None:
            self.combo_prio.addItem("Backlog : ne pas changer la priorité", None)
            in_backlog = {t.tag for t in self.app.tasks if t.state_index == 0 and t.kind == "chantier"}
            for tag in PD_PRIORITY_ORDER:
                if tag in in_backlog:
                    self.combo_prio.addItem(f"Backlog : passer le thème « {TAG_LABELS[tag]} » en tête", tag)
            pick = None
            if by["Pic du vendredi (tickets reçus / jour de semaine)"]["level"] != "green" and self.combo_prio.findData("peak") >= 0:
                pick = "peak"
            elif by["Volume de données stockées (indice, base 100)"]["level"] != "green" and self.combo_prio.findData("data") >= 0:
                pick = "data"
            elif by["Failles d'habilitation ouvertes"]["level"] != "green" and self.combo_prio.findData("access") >= 0:
                pick = "access"
            if pick:
                self.combo_prio.setCurrentIndex(self.combo_prio.findData(pick))
            layout.addWidget(self.combo_prio)
            self.chk_tool.setEnabled(self.app.env.get("handoff_delay", 0) > 0)
            self.chk_tool.setChecked(self.app.env.get("handoff_delay", 0) > 0 and by["Travail en attente (% du WIP)"]["level"] != "green")
            layout.addWidget(self.chk_tool)

        footer = QHBoxLayout()
        footer.addStretch()
        btn_cancel = QPushButton("Ignorer")
        btn_cancel.setObjectName("btnOutline")
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Valider la rétrospective")
        btn_ok.setObjectName("btnGreen")
        btn_ok.clicked.connect(self._validate)
        footer.addWidget(btn_cancel)
        footer.addWidget(btn_ok)
        layout.addLayout(footer)

    def _validate(self):
        self.result_data = {
            "sprint": self.rep["sprint"],
            "start": self.edits["start"].toPlainText().strip(),
            "stop": self.edits["stop"].toPlainText().strip(),
            "continue": self.edits["continue"].toPlainText().strip(),
            "raise_limit": self.chk_limit.isChecked(),
            "cross_train": self.chk_poly.isChecked(),
            "prioritize_tag": self.combo_prio.currentData() if self.app.env is not None else None,
            "unify_tool": self.chk_tool.isChecked() if self.app.env is not None else False,
        }
        self.accept()


# =============================================================================
# FENÊTRE PRINCIPALE DU SIMULATEUR KANBAN
# =============================================================================
class KanbanSimulatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kanban Flow Analytics — Simulateur Lean & Agile")
        self.resize(1460, 895)

        self.states = [
            "Backlog",
            "Design UI/UX",
            "Développement",
            "Analyse",
            "QA",
            "Déploiement",
            "Terminé"
        ]
        self.col_worker_limits = {
            "Backlog": 0,
            "Design UI/UX": 2,
            "Développement": 3,
            "Analyse": 2,
            "QA": 2,
            "Déploiement": 2,
            "Terminé": 0
        }

        self.team_specs = list(DEFAULT_TEAM_SPECS)
        self.custom_task_titles = list(REAL_TASKS_CATALOG)

        self.active_scenario_key = "standard"
        self.num_sprints = 2
        self.sprint_duration = 12
        self.target_task_count = 38
        self.effort_range = (1, 2)

        self.chart_slot_1 = "cfd"
        self.chart_slot_2 = "wip"

        self.env_cfg = None          # paramètres du cas (demande, coûts, habilitations...) : None = Kanban générique
        self.env = None              # état courant du cas pendant la simulation
        self.task_tags: dict[str, str] = {}
        self.chantier_skip: set[str] = set()
        self.ticket_counter = 0
        self.day_stats = {"arr_t": 0, "arr_a": 0, "closed_t": 0}

        self.current_day = 0
        self.is_running = False
        self.tasks: list[Task] = []
        self.workers: list[Worker] = []
        self.history: list[dict] = []
        self.sprint_reports: list[dict] = []
        self.retro_log: list[dict] = []
        self.show_sprint_dialogs = True   # False en mode sans fenêtre (tests / batch)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

        self._load_scenario("pd_silos", set_durations=True)

        self._apply_global_stylesheet()
        self._build_ui()
        self.reset_simulation()

    def _load_scenario(self, key: str, set_durations: bool = False):
        """Charge un scénario : colonnes, équipe, chantiers, paramètres du cas et graphiques par défaut."""
        sc = SCENARIOS[key]
        self.active_scenario_key = key
        self.effort_range = sc["effort_range"]
        if "states" in sc:
            self.states = list(sc["states"])
            self.col_worker_limits = {s: 0 for s in self.states}
            self.team_specs = list(sc["team"])
            self.custom_task_titles = [t for t, _ in sc["chantiers"]]
            self.task_tags = {t: tag for t, tag in sc["chantiers"]}
            self.chantier_skip = {"Support"}
        else:
            if self.env_cfg is not None:   # retour à un scénario générique après un scénario Pixels & Dragons
                self.states = ["Backlog", "Design UI/UX", "Développement", "Analyse", "QA", "Déploiement", "Terminé"]
                self.col_worker_limits = {"Backlog": 0, "Design UI/UX": 2, "Développement": 3, "Analyse": 2,
                                          "QA": 2, "Déploiement": 2, "Terminé": 0}
                self.team_specs = list(DEFAULT_TEAM_SPECS)
            self.custom_task_titles = list(REAL_TASKS_CATALOG)
            self.task_tags = {}
            self.chantier_skip = set()
        for st, lim in sc["limits"].items():
            if st in self.col_worker_limits:
                self.col_worker_limits[st] = lim
        self.env_cfg = copy.deepcopy(sc.get("env"))
        if set_durations:
            self.num_sprints = sc["num_sprints"]
            self.sprint_duration = sc["sprint_days"]
            self.target_task_count = sc["tasks"]
            if "charts" in sc:
                self.chart_slot_1, self.chart_slot_2 = sc["charts"]
        if hasattr(self, "lbl_scenario_badge"):
            self.lbl_scenario_badge.setText(f"Scénario : {sc['name']}")

    @property
    def total_simulation_days(self) -> int:
        return self.num_sprints * self.sprint_duration

    def _apply_global_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #FFFFFF;
                font-family: 'Lato', 'Segoe UI', sans-serif;
                color: #0F172A;
            }
            QFrame#TopBar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E2E8F0;
            }
            QFrame#AnalyticsPanel {
                background-color: #F8FAFC;
                border-bottom: 1px solid #E2E8F0;
            }
            QFrame#KpiCard, QFrame#ChartCard {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
            QPushButton {
                border-radius: 6px;
                padding: 7px 14px;
                font-weight: 800;
                font-size: 12px;
                border: none;
            }
            QPushButton#btnGreen {
                background-color: #16A34A;
                color: #FFFFFF;
            }
            QPushButton#btnGreen:hover { background-color: #15803D; }
            QPushButton#btnAmber {
                background-color: #EAB308;
                color: #0F172A;
            }
            QPushButton#btnAmber:hover { background-color: #CA8A04; }
            QPushButton#btnRed {
                background-color: #DC2626;
                color: #FFFFFF;
            }
            QPushButton#btnRed:hover { background-color: #B91C1C; }
            QPushButton#btnOutline {
                background-color: #FFFFFF;
                color: #0F172A;
                border: 1px solid #CBD5E1;
            }
            QPushButton#btnOutline:hover {
                background-color: #F8FAFC;
                border-color: #94A3B8;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. BARRE SUPÉRIEURE
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 12, 20, 12)
        top_layout.setSpacing(12)

        brand_box = QVBoxLayout()
        brand_box.setSpacing(3)
        lbl_title = QLabel("KANBAN FLOW ANALYTICS")
        lbl_title.setStyleSheet("font-size: 15px; font-weight: 900; letter-spacing: 0.5px; color: #0F172A;")

        self.lbl_scenario_badge = QLabel(f"Scénario : {SCENARIOS[self.active_scenario_key]['name']}")
        self.lbl_scenario_badge.setStyleSheet("""
            background-color: #F0FDF4;
            color: #15803D;
            border: 1px solid #BBF7D0;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 10.5px;
            font-weight: 700;
        """)
        brand_box.addWidget(lbl_title)
        brand_box.addWidget(self.lbl_scenario_badge)
        top_layout.addLayout(brand_box)

        top_layout.addStretch()

        btn_settings = QPushButton("⚙  Paramètres")
        btn_settings.setObjectName("btnOutline")
        btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_settings.clicked.connect(self.open_settings_dialog)
        top_layout.addWidget(btn_settings)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setStyleSheet("color: #E2E8F0;")
        top_layout.addWidget(sep)

        self.btn_play = QPushButton("▶ Play")
        self.btn_play.setObjectName("btnGreen")
        self.btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_play.clicked.connect(self.start_simulation)
        top_layout.addWidget(self.btn_play)

        self.btn_pause = QPushButton("❚❚ Pause")
        self.btn_pause.setObjectName("btnAmber")
        self.btn_pause.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_pause.clicked.connect(self.pause_simulation)
        top_layout.addWidget(self.btn_pause)

        self.btn_stop = QPushButton("■ Stop")
        self.btn_stop.setObjectName("btnRed")
        self.btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stop.clicked.connect(self.reset_simulation)
        top_layout.addWidget(self.btn_stop)

        self.btn_export = QPushButton("📄 Bilan .md")
        self.btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_export.setToolTip("Exporter le bilan (KPIs, interprétations, rétrospectives) en Markdown")
        self.btn_export.clicked.connect(self.export_bilan_dialog)
        top_layout.addWidget(self.btn_export)

        speed_box = QVBoxLayout()
        speed_box.setSpacing(2)
        lbl_spd = QLabel("VITESSE")
        lbl_spd.setStyleSheet("font-size: 9px; font-weight: 800; color: #64748B; letter-spacing: 0.5px;")
        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setRange(150, 1400)
        self.slider_speed.setValue(700)
        self.slider_speed.setInvertedAppearance(True)
        self.slider_speed.setFixedWidth(85)
        self.slider_speed.valueChanged.connect(self._update_timer_speed)
        speed_box.addWidget(lbl_spd)
        speed_box.addWidget(self.slider_speed)
        top_layout.addLayout(speed_box)

        main_layout.addWidget(top_bar)

        # 2. SECTION ANALYTIQUE EN HAUT
        analytics_panel = QFrame()
        analytics_panel.setObjectName("AnalyticsPanel")
        analytics_panel.setFixedHeight(255)
        analytics_layout = QHBoxLayout(analytics_panel)
        analytics_layout.setContentsMargins(20, 12, 20, 12)
        analytics_layout.setSpacing(14)

        left_kpi_container = QWidget()
        left_kpi_container.setStyleSheet("background: transparent;")
        left_kpi_container.setFixedWidth(405)
        left_vbox = QVBoxLayout(left_kpi_container)
        left_vbox.setContentsMargins(0, 0, 0, 0)
        left_vbox.setSpacing(8)

        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(8)

        self.kpi_day_val = self._create_kpi_card(kpi_grid, 0, 0, "SPRINTS & TEMPS", "S1/2 — J 0/24", "#0F172A")
        self.kpi_done_val = self._create_kpi_card(kpi_grid, 0, 1, "TÂCHES LIVRÉES", "0 / 38", "#16A34A")
        self.kpi_lt_val = self._create_kpi_card(kpi_grid, 1, 0, "LEAD TIME MOYEN", "—", "#D97706")
        self.kpi_wip_val = self._create_kpi_card(kpi_grid, 1, 1, "EN COURS (WIP)", "0 tâches", "#0F172A")

        left_vbox.addLayout(kpi_grid)

        team_card = QFrame()
        team_card.setObjectName("KpiCard")
        team_layout = QVBoxLayout(team_card)
        team_layout.setContentsMargins(10, 7, 10, 7)
        team_layout.setSpacing(5)
        lbl_team_hdr = QLabel("ÉQUIPE & PÔLES ASSIGNÉS")
        lbl_team_hdr.setStyleSheet("font-size: 9px; font-weight: 800; color: #64748B; letter-spacing: 0.5px;")
        team_layout.addWidget(lbl_team_hdr)

        self.team_pills_grid = QGridLayout()
        self.team_pills_grid.setSpacing(4)
        self.team_pills_grid.setContentsMargins(0, 0, 0, 0)
        team_layout.addLayout(self.team_pills_grid)
        left_vbox.addWidget(team_card)

        analytics_layout.addWidget(left_kpi_container)

        # Graphique 1
        chart1_card = QFrame()
        chart1_card.setObjectName("ChartCard")
        c1_layout = QVBoxLayout(chart1_card)
        c1_layout.setContentsMargins(10, 8, 10, 6)
        c1_layout.setSpacing(2)
        self.lbl_chart_1 = QLabel("FLUX CUMULATIF (CFD)")
        self.lbl_chart_1.setStyleSheet("font-size: 10px; font-weight: 800; color: #475569; letter-spacing: 0.5px;")
        c1_layout.addWidget(self.lbl_chart_1)

        self.fig_1 = Figure(figsize=(5.0, 2.0), dpi=100, facecolor="#FFFFFF")
        self.canvas_1 = FigureCanvas(self.fig_1)
        c1_layout.addWidget(self.canvas_1)
        analytics_layout.addWidget(chart1_card, stretch=3)

        # Graphique 2
        chart2_card = QFrame()
        chart2_card.setObjectName("ChartCard")
        c2_layout = QVBoxLayout(chart2_card)
        c2_layout.setContentsMargins(10, 8, 10, 6)
        c2_layout.setSpacing(2)
        self.lbl_chart_2 = QLabel("CHARGE & GOULOTS PAR ÉTAPE")
        self.lbl_chart_2.setStyleSheet("font-size: 10px; font-weight: 800; color: #475569; letter-spacing: 0.5px;")
        c2_layout.addWidget(self.lbl_chart_2)

        self.fig_2 = Figure(figsize=(4.4, 2.0), dpi=100, facecolor="#FFFFFF")
        self.canvas_2 = FigureCanvas(self.fig_2)
        c2_layout.addWidget(self.canvas_2)
        analytics_layout.addWidget(chart2_card, stretch=2)

        main_layout.addWidget(analytics_panel)

        # 3. TABLEAU KANBAN
        self.board_scroll = QScrollArea()
        self.board_scroll.setWidgetResizable(True)
        self.board_scroll.setStyleSheet("background-color: #FFFFFF;")

        self.board_container = QWidget()
        self.board_container.setStyleSheet("background-color: #FFFFFF;")
        self.columns_layout = QHBoxLayout(self.board_container)
        self.columns_layout.setContentsMargins(20, 14, 20, 16)
        self.columns_layout.setSpacing(12)

        self.board_scroll.setWidget(self.board_container)
        main_layout.addWidget(self.board_scroll, stretch=1)

    def _create_kpi_card(self, grid, row, col, title, initial_val, val_color):
        card = QFrame()
        card.setObjectName("KpiCard")
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(10, 7, 10, 7)
        vbox.setSpacing(2)
        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("font-size: 9px; font-weight: 800; color: #64748B; letter-spacing: 0.4px;")
        lbl_v = QLabel(initial_val)
        lbl_v.setStyleSheet(f"font-size: 15px; font-weight: 900; color: {val_color};")
        vbox.addWidget(lbl_t)
        vbox.addWidget(lbl_v)
        grid.addWidget(card, row, col)
        return lbl_v

    # --- OUVERTURE DES PARAMÈTRES ---
    def _update_timer_speed(self):
        if self.is_running:
            self.timer.setInterval(self.slider_speed.value())

    def open_settings_dialog(self):
        self.pause_simulation()
        dlg = SettingsDialog(self, self)
        if dlg.exec():
            need_reset = False

            if self.states != dlg.working_states or self.team_specs != dlg.working_team_specs:
                self.states = dlg.working_states
                self.col_worker_limits = dlg.working_limits
                self.team_specs = dlg.working_team_specs
                need_reset = True

            if dlg.scenario_applied:
                self._load_scenario(dlg.selected_scenario)
                need_reset = True

            self.num_sprints = dlg.new_num_sprints
            self.sprint_duration = dlg.new_sprint_days

            base_task_target = max(1, dlg.new_total_tasks - len(dlg.pending_custom_tasks))
            if base_task_target != self.target_task_count:
                self.target_task_count = base_task_target
                need_reset = True

            charts_unchanged = (dlg.selected_chart_1 == self.chart_slot_1 and dlg.selected_chart_2 == self.chart_slot_2)
            self.chart_slot_1 = dlg.selected_chart_1
            self.chart_slot_2 = dlg.selected_chart_2
            if dlg.scenario_applied and charts_unchanged:
                self.chart_slot_1, self.chart_slot_2 = SCENARIOS[self.active_scenario_key].get("charts", ("cfd", "wip"))

            if need_reset:
                self.reset_simulation()

            if dlg.pending_custom_tasks:
                for item in dlg.pending_custom_tasks:
                    chosen_cat = item["category"]
                    if chosen_cat.startswith("Backlog"):
                        start_idx = 0
                        tag = ""
                    else:
                        start_idx = self.states.index(chosen_cat) if chosen_cat in self.states else 0
                        tag = chosen_cat if start_idx > 0 else ""

                    new_id = max([t.id for t in self.tasks if t.kind == "chantier"], default=0) + 1
                    new_task = Task(
                        task_id=new_id,
                        title=item["title"],
                        states=self.states,
                        effort_range=self.effort_range,
                        start_state_idx=start_idx,
                        category_tag=tag
                    )
                    if start_idx > 0:
                        new_task.start_day = self.current_day
                    self.custom_task_titles.insert(0, item["title"])

                    order = item["order"]
                    if order == "FIRST":
                        self.tasks.insert(0, new_task)
                    elif order.startswith("BEFORE:"):
                        target_id = int(order.split(":")[1])
                        insert_pos = next((i for i, t in enumerate(self.tasks) if t.id == target_id), len(self.tasks))
                        self.tasks.insert(insert_pos, new_task)
                    else:
                        self.tasks.append(new_task)

                self.target_task_count = len(self.tasks)
                self._record_history_snapshot(delivered_today=0)

            self._render_all()

    # --- MOTEUR DE SIMULATION ---
    def reset_simulation(self):
        self.pause_simulation()
        self.current_day = 0
        self.history.clear()
        self.sprint_reports.clear()
        self.retro_log.clear()

        self.workers = [
            Worker(i + 1, name, spec) for i, (name, spec) in enumerate(self.team_specs)
        ]

        self.env = copy.deepcopy(self.env_cfg)
        self.ticket_counter = 0
        self.alert_counter = 0
        self.day_stats = {"arr_t": 0, "arr_a": 0, "closed_t": 0}

        self.tasks = []
        middle = self.states[1:-1]
        for i in range(self.target_task_count):
            base_title = self.custom_task_titles[i % len(self.custom_task_titles)]
            title = base_title
            if i >= len(self.custom_task_titles):
                title = f"{base_title} (Lot {i // len(self.custom_task_titles) + 1})"
            tag = self.task_tags.get(base_title, "")
            efforts = None
            if self.chantier_skip:
                efforts = {st: (0 if st in self.chantier_skip else random.randint(*self.effort_range)) for st in middle}
            self.tasks.append(Task(i + 1, title, self.states, self.effort_range,
                                   category_tag=TAG_LABELS.get(tag, ""), tag=tag, efforts=efforts))
        if self.env and self.env.get("prioritize"):
            self.tasks.sort(key=lambda t: PD_PRIORITY_ORDER.index(t.tag) if t.tag in PD_PRIORITY_ORDER else 99)
            for n, t in enumerate(self.tasks, start=1):
                t.id = n
                t.label = f"US-{n:02d}"

        for st in self.states:
            if st not in self.col_worker_limits:
                self.col_worker_limits[st] = 0 if st in (self.states[0], self.states[-1]) else 2

        self._record_history_snapshot(delivered_today=0)
        self._render_all()

    def start_simulation(self):
        if self.is_running:
            return
        done_count, total_count = self._chantier_counts()
        if self.current_day >= self.total_simulation_days or done_count == total_count:
            self.reset_simulation()
        self.is_running = True
        self.timer.start(self.slider_speed.value())

    def pause_simulation(self):
        self.is_running = False
        self.timer.stop()

    def _tick(self):
        done_count, total_count = self._chantier_counts()

        if self.current_day >= self.total_simulation_days or done_count == total_count:
            self.pause_simulation()
            self._render_all()
            msg = (
                "Tous les chantiers ont été livrés !"
                if done_count == total_count
                else f"Les {self.num_sprints} sprint(s) ont été exécutés."
            )
            export_note = ""
            if self.sprint_reports:
                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilan_simulation.md")
                try:
                    self.export_bilan_markdown(path)
                    export_note = f"\n\nBilan détaillé exporté :\n{path}"
                except OSError:
                    export_note = "\n\nExport automatique impossible : utilisez le bouton « Bilan .md »."

            QMessageBox.information(
                self, "Bilan de Simulation",
                f"{msg}\nSprints exécutés : {self.num_sprints} ({self.current_day} / {self.total_simulation_days} jours)\n"
                f"Chantiers livrés : {done_count} / {total_count}{export_note}"
            )
            return

        self.step_day()
        self._render_all()

        # Fin de sprint : KPIs + interprétation, puis rétrospective optionnelle
        if self.current_day % self.sprint_duration == 0 and self.current_day <= self.total_simulation_days:
            self._on_sprint_end()

    # --- FIN DE SPRINT : KPIs, INTERPRÉTATION, RÉTROSPECTIVE ---
    def build_sprint_report(self, sprint_no: int) -> dict:
        start_day = (sprint_no - 1) * self.sprint_duration
        end_day = sprint_no * self.sprint_duration
        snaps = [h for h in self.history if start_day < h["day"] <= end_day]
        n_days = max(1, len(snaps))
        last_idx = len(self.states) - 1
        middle = self.states[1:-1]

        delivered = sum(h["delivered_today"] for h in snaps)
        lead_times = [max(1, t.end_day - t.start_day) for t in self.tasks
                      if t.kind == "chantier" and t.end_day is not None and t.start_day is not None and start_day < t.end_day <= end_day]
        wip_per_day = [sum(h.get(st, 0) for st in middle) for h in snaps]
        wait_per_day = [sum(h.get(f"wait::{st}", 0) for st in middle) for h in snaps]
        avg_wip = sum(wip_per_day) / n_days
        waiting_ratio = (sum(wait_per_day) / max(1, sum(wip_per_day))) if sum(wip_per_day) else 0.0
        n_workers = max(1, len(self.workers))
        utilisation = sum(h.get("busy_workers", 0) for h in snaps) / (n_days * n_workers)
        zero_days = sum(1 for h in snaps if h["delivered_today"] == 0) / n_days

        avg_wait_by_col = {st: sum(h.get(f"wait::{st}", 0) for h in snaps) / n_days for st in middle}
        bottleneck, bn_val = (max(avg_wait_by_col.items(), key=lambda kv: kv[1]) if avg_wait_by_col else (None, 0))
        if bn_val < 1.0:
            bottleneck = None

        pd = None
        if self.env is not None:
            fridays = [h for h in snaps if h.get("weekday") == 4]
            others = [h for h in snaps if h.get("weekday") != 4]
            fri_t = sum(h.get("arr_tickets", 0) for h in fridays) / max(1, len(fridays))
            oth_t = sum(h.get("arr_tickets", 0) for h in others) / max(1, len(others))
            tk_lts = [max(1, t.end_day - t.start_day) for t in self.tasks
                      if t.kind == "ticket" and t.end_day is not None and start_day < t.end_day <= end_day]
            groups = sorted({w.specialty for w in self.workers})
            util_by_group = {}
            for g in groups:
                busy = sum(h.get("busy::" + g, 0) for h in snaps)
                size = max(1, snaps[0].get("size::" + g, 1)) if snaps else 1
                util_by_group[g] = busy / (n_days * size)
            busiest_group, busiest_util = max(util_by_group.items(), key=lambda kv: kv[1]) if util_by_group else ("—", 0.0)
            idlest_group, idlest_util = min(util_by_group.items(), key=lambda kv: kv[1]) if util_by_group else ("—", 0.0)
            last = snaps[-1] if snaps else {}
            pd = {
                "fri_tickets": fri_t, "other_tickets": oth_t,
                "peak_ratio": fri_t / max(0.1, oth_t),
                "open_friday": (sum(h.get("open_tickets", 0) for h in fridays) / len(fridays)) if fridays else 0.0,
                "ticket_lead_time": (sum(tk_lts) / len(tk_lts)) if tk_lts else None,
                "tickets_received": sum(h.get("arr_tickets", 0) for h in snaps),
                "alerts_received": sum(h.get("arr_alerts", 0) for h in snaps),
                "busiest_group": busiest_group, "busiest_util": busiest_util, "util_by_group": util_by_group,
                "idlest_group": idlest_group, "idlest_util": idlest_util,
                "data_volume": last.get("data_volume", 100.0), "cloud_cost": last.get("cloud_cost", 100.0),
                "access_gaps": last.get("access_gaps", 0), "peak_mult": last.get("peak_mult", 1.0),
                "retros_held": len(self.retro_log),
            }

        return {
            "sprint": sprint_no, "start_day": start_day, "end_day": end_day,
            "delivered": delivered,
            "avg_lead_time": (sum(lead_times) / len(lead_times)) if lead_times else None,
            "avg_wip": avg_wip, "waiting_ratio": waiting_ratio,
            "utilisation": utilisation, "zero_delivery_ratio": zero_days,
            "bottleneck": bottleneck, "avg_wait_by_col": avg_wait_by_col,
            "n_workers": len(self.workers),
            "total_done": sum(1 for t in self.tasks if t.kind == "chantier" and t.state_index == last_idx),
            "sprint_days": self.sprint_duration, "pd": pd,
        }

    def find_cross_training_candidate(self, bottleneck: str | None):
        """Équipier spécialiste le moins sollicité hors goulot : candidat à la polyvalence."""
        if not bottleneck or not self.sprint_reports:
            return None
        waits = self.sprint_reports[-1]["avg_wait_by_col"]
        sizes = {}
        for w in self.workers:
            sizes[w.specialty] = sizes.get(w.specialty, 0) + 1
        candidates = [w for w in self.workers if w.specialty not in ("Polyvalent", bottleneck)]
        if self.env is not None:   # on ne retire pas le dernier spécialiste d'un pôle, ni un équipier du Support
            candidates = [w for w in candidates if w.specialty != "Support" and sizes[w.specialty] > 1]
        if not candidates:
            return None
        return min(candidates, key=lambda w: waits.get(w.specialty, 0))

    def _on_sprint_end(self):
        sprint_no = self.current_day // self.sprint_duration
        rep = self.build_sprint_report(sprint_no)
        self.sprint_reports.append(rep)
        if not self.show_sprint_dialogs:
            return
        was_running = self.is_running
        self.pause_simulation()
        prev = self.sprint_reports[-2] if len(self.sprint_reports) > 1 else None
        rows = interpret_report(rep, prev)
        dlg = SprintReportDialog(rep, rows, self.num_sprints, self)
        dlg.exec()
        if dlg.open_retro:
            retro = RetrospectiveDialog(rep, rows, self, self)
            if retro.exec():
                self.apply_retrospective(retro.result_data)
        if was_running:
            self.is_running = True
            self.timer.start(self.slider_speed.value())

    def apply_retrospective(self, data: dict):
        """Enregistre la rétrospective et applique les actions Kaizen décidées par l'équipe."""
        applied = []
        bn = self.sprint_reports[-1]["bottleneck"] if self.sprint_reports else None
        if data.get("raise_limit") and bn:
            self.col_worker_limits[bn] = self.col_worker_limits.get(bn, 1) + 1
            applied.append(f"capacité de « {bn} » portée à {self.col_worker_limits[bn]}")
        if data.get("cross_train"):
            donor = self.find_cross_training_candidate(bn)
            if donor:
                applied.append(f"{donor.name} (ex-« {donor.specialty} ») devient polyvalent")
                donor.specialty = "Polyvalent"
                self.team_specs = [(w.name, w.specialty) for w in self.workers]
        tag = data.get("prioritize_tag")
        if tag and self.env is not None:
            positions = [i for i, t in enumerate(self.tasks) if t.state_index == 0 and t.kind == "chantier"]
            ordered = sorted((self.tasks[i] for i in positions), key=lambda t: 0 if t.tag == tag else 1)
            for pos, t in zip(positions, ordered):
                self.tasks[pos] = t
            applied.append(f"backlog : thème « {TAG_LABELS.get(tag, tag)} » passé en tête")
        if data.get("unify_tool") and self.env is not None and self.env.get("handoff_delay", 0) > 0:
            self.env["handoff_delay"] = 0
            applied.append("outil de suivi commun : fin du délai de reprise entre pôles")
        data["applied"] = applied
        self.retro_log.append(data)
        self._render_all()

    def export_bilan_dialog(self):
        if not self.sprint_reports:
            QMessageBox.information(self, "Bilan", "Aucun sprint terminé pour l'instant : lancez la simulation d'abord.")
            return
        default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilan_simulation.md")
        path, _ = QFileDialog.getSaveFileName(self, "Exporter le bilan", default, "Markdown (*.md)")
        if not path:
            return
        try:
            self.export_bilan_markdown(path)
            QMessageBox.information(self, "Bilan", f"Bilan exporté :\n{path}")
        except OSError as e:
            QMessageBox.warning(self, "Bilan", f"Export impossible : {e}")

    def export_bilan_markdown(self, path: str):
        lines = [f"# Bilan de simulation — {self.lbl_scenario_badge.text()}", ""]
        done, total = self._chantier_counts()
        lts = [max(1, t.end_day - t.start_day) for t in self.tasks if t.kind == "chantier" and t.end_day is not None]
        tks = [max(1, t.end_day - t.start_day) for t in self.tasks if t.kind == "ticket" and t.end_day is not None]
        lines += ["## Synthèse", "",
                  f"- Jours simulés : {self.current_day} / {self.total_simulation_days} ({len(self.sprint_reports)} sprint(s) terminé(s))",
                  f"- Chantiers livrés : {done} / {total}",
                  f"- Lead time moyen des chantiers : {sum(lts)/len(lts):.1f} j" if lts else "- Lead time moyen des chantiers : —",
                  f"- Délai moyen d'un ticket joueur : {sum(tks)/len(tks):.1f} j" if tks else "- Délai moyen d'un ticket joueur : —",
                  f"- Rétrospectives tenues : {len(self.retro_log)} / {len(self.sprint_reports)}", ""]
        if self.retro_log:
            lines += ["### Actions Kaizen décidées", ""]
            for r in self.retro_log:
                lines.append(f"- Sprint {r['sprint']} : {', '.join(r.get('applied', [])) or 'aucune action'}")
            lines.append("")
        prev = None
        for rep in self.sprint_reports:
            rows = interpret_report(rep, prev)
            lines += [f"## Sprint {rep['sprint']} (jours {rep['start_day'] + 1} à {rep['end_day']})", "",
                      "| KPI | Lecture Lean | Valeur | Interprétation |", "| --- | --- | --- | --- |"]
            for r in rows:
                lines.append(f"| {r['kpi']} | {r['lean']} | {r['value']} | {r['text']} |")
            lines.append(f"\nGoulot principal : {rep['bottleneck'] or 'aucun'}\n")
            for retro in self.retro_log:
                if retro["sprint"] == rep["sprint"]:
                    lines += ["**Rétrospective**", "", "- Start :", retro["start"], "- Stop :", retro["stop"],
                              "- Continue :", retro["continue"],
                              f"- Actions Kaizen appliquées : {', '.join(retro.get('applied', [])) or 'aucune'}", ""]
            prev = rep
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _worker_can_work_in(self, worker: Worker, state_name: str) -> bool:
        return worker.specialty == "Polyvalent" or worker.specialty == state_name

    # --- OUTILS DU MODÈLE ---
    def _chantier_counts(self) -> tuple[int, int]:
        last_idx = len(self.states) - 1
        chantiers = [t for t in self.tasks if t.kind == "chantier"]
        return sum(1 for t in chantiers if t.state_index == last_idx), len(chantiers)

    @staticmethod
    def weekday(day: int) -> int:
        """0 = lundi ... 4 = vendredi (semaine de 5 jours ouvrés)."""
        return (day - 1) % 5 if day >= 1 else 0

    @staticmethod
    def _poisson(lam: float) -> int:
        if lam <= 0:
            return 0
        limit, k, p = math.exp(-lam), 0, 1.0
        while True:
            k += 1
            p *= random.random()
            if p <= limit:
                return k - 1

    @property
    def cloud_cost(self) -> float:
        """Indice de coût cloud (base 100) : stockage, instances de nuit sous-utilisées, reste."""
        if self.env is None:
            return 100.0
        e = self.env
        return 50 * e["data_volume"] / 100 + 30 * (0.6 + 0.4 * e["night_waste"]) + 20

    def _first_stage_idx(self, task: Task) -> int:
        return self._next_stage_idx(task, 0)

    def _next_stage_idx(self, task: Task, from_idx: int) -> int:
        last_idx = len(self.states) - 1
        for i in range(from_idx + 1, last_idx):
            if task.effort_per_stage.get(self.states[i], 0) > 0:
                return i
        return last_idx

    def _make_unplanned(self, kind: str):
        """Crée un ticket joueur ou une alerte de sécurité qui entre directement dans son premier pôle."""
        middle = self.states[1:-1]
        if kind == "ticket":
            route = {"Support": random.choice([1, 1, 1, 2])}
            if random.random() < 0.40:
                route["Ops/Infra"] = random.randint(1, 2)
            if random.random() < 0.15:
                route["Développement"] = random.randint(1, 2)
            title, chip = random.choice(TICKET_TITLES), "TICKET JOUEUR"
            self.ticket_counter += 1
            label, task_id = f"T-{self.ticket_counter:03d}", 1000 + self.ticket_counter
        else:
            route = {"Sécurité": 1}
            if random.random() < 0.30:
                route["Ops/Infra"] = 1
            title, chip = random.choice(ALERT_TITLES), "ALERTE SÉCU"
            self.alert_counter += 1
            label, task_id = f"A-{self.alert_counter:03d}", 2000 + self.alert_counter
        efforts = {st: route.get(st, 0) for st in middle}
        if not any(efforts.values()):
            efforts[middle[0]] = 1
        t = Task(task_id, title, self.states, kind=kind, category_tag=chip, efforts=efforts)
        t.label = label
        t.state_index = self._first_stage_idx(t)
        t.start_day = self.current_day
        t.ready_day = self.current_day
        self.tasks.append(t)

    def _generate_arrivals(self):
        e = self.env
        lam = e["base_rate"] * (e["peak_mult"] if self.weekday(self.current_day) == 4 else 1.0)
        n_t, n_a = self._poisson(lam), self._poisson(e["alert_rate"])
        for _ in range(n_t):
            self._make_unplanned("ticket")
        for _ in range(n_a):
            self._make_unplanned("alerte")
        self.day_stats["arr_t"], self.day_stats["arr_a"] = n_t, n_a

    def _apply_chantier_effect(self, task: Task):
        """Chaque chantier livré modifie le système, selon son thème (plan Lean IT du rendu)."""
        e = self.env
        if e is None:
            return
        if task.tag == "peak":        # scaling, test de charge, anti-rollback : moins de tickets le vendredi
            e["peak_mult"] = max(1.5, e["peak_mult"] - 0.6)
        elif task.tag == "debt":      # dette technique, monitoring : moins d'incidents au quotidien
            e["base_rate"] *= 0.88
        elif task.tag == "data":      # purge, archivage, suppression des doublons : moins de données stockées
            e["data_volume"] *= 0.88
        elif task.tag == "night":     # extinction / dimensionnement nocturne des instances
            e["night_waste"] = max(0.0, e["night_waste"] - 0.5)
        elif task.tag == "access":    # habilitations, traçabilité, RGPD : failles refermées
            e["access_gaps"] = max(0, e["access_gaps"] - 2)
        elif task.tag == "tool":      # tableau de suivi unique : plus de délai de reprise entre pôles
            e["handoff_delay"] = 0

    def step_day(self) -> int:
        self.current_day += 1
        delivered = self._simulate_one_day()
        self._record_history_snapshot(delivered_today=delivered)
        return delivered

    def _simulate_one_day(self) -> int:
        last_idx = len(self.states) - 1
        delivered_today = 0
        e = self.env
        self.day_stats = {"arr_t": 0, "arr_a": 0, "closed_t": 0}

        # 0. Le système évolue et la demande non planifiée arrive (tickets joueurs, alertes de sécurité)
        if e is not None and e.get("demand"):
            e["data_volume"] *= 1.001      # la télémétrie continue de s'accumuler
            self._generate_arrivals()

        # 1. Faire avancer les tâches ayant déjà un équipier assigné
        for task in self.tasks:
            if 0 < task.state_index < last_idx and task.assigned_workers:
                st_name = self.states[task.state_index]
                req_effort = task.effort_per_stage.get(st_name, 1) or 1
                task.progress += len(task.assigned_workers)

                if task.progress >= req_effort:
                    for w in task.assigned_workers:
                        w.assigned_task = None
                    task.assigned_workers.clear()
                    task.state_index = self._next_stage_idx(task, task.state_index)
                    task.progress = 0
                    if task.state_index == last_idx:
                        task.end_day = self.current_day
                        if task.kind == "chantier":
                            delivered_today += 1
                            self._apply_chantier_effect(task)
                        elif task.kind == "ticket":
                            self.day_stats["closed_t"] += 1
                    else:
                        delay = e.get("handoff_delay", 0) if e is not None else 0
                        task.ready_day = self.current_day + delay

        # 2. Affecter les équipiers libres (flux tiré de droite à gauche) : tickets et alertes d'abord
        free_workers = [w for w in self.workers if w.assigned_task is None]

        for col_idx in range(last_idx - 1, 0, -1):
            if not free_workers:
                break

            st_name = self.states[col_idx]
            max_w = self.col_worker_limits.get(st_name, 2)
            active_w = sum(len(t.assigned_workers) for t in self.tasks if t.state_index == col_idx)

            waiting = [t for t in self.tasks
                       if t.state_index == col_idx and not t.assigned_workers and t.ready_day <= self.current_day]
            waiting.sort(key=lambda t: 0 if t.kind != "chantier" else 1)
            from_backlog = [t for t in self.tasks if t.state_index == 0 and self._first_stage_idx(t) == col_idx]

            for task in waiting + from_backlog:
                if active_w >= max_w:
                    break
                eligible = [w for w in free_workers if self._worker_can_work_in(w, st_name)]
                if not eligible:
                    break
                eligible.sort(key=lambda w: 0 if w.specialty == st_name else 1)
                worker = eligible[0]
                free_workers.remove(worker)
                if task.state_index == 0:
                    task.state_index = col_idx
                    task.start_day = self.current_day
                    task.progress = 0
                worker.assigned_task = task
                task.assigned_workers.append(worker)
                active_w += 1

        return delivered_today

    def _record_history_snapshot(self, delivered_today: int = 0):
        snap = {"day": self.current_day, "delivered_today": delivered_today}
        chantiers = [t for t in self.tasks if t.kind == "chantier"]
        for idx, st in enumerate(self.states):
            snap[st] = sum(1 for t in self.tasks if t.state_index == idx)
            snap["ch::" + st] = sum(1 for t in chantiers if t.state_index == idx)
            if 0 < idx < len(self.states) - 1:
                snap[f"wait::{st}"] = sum(1 for t in self.tasks if t.state_index == idx and not t.assigned_workers)
        snap["busy_workers"] = sum(1 for w in self.workers if w.assigned_task is not None)
        snap["n_workers"] = len(self.workers)
        for g in {w.specialty for w in self.workers}:
            snap["busy::" + g] = sum(1 for w in self.workers if w.specialty == g and w.assigned_task is not None)
            snap["size::" + g] = sum(1 for w in self.workers if w.specialty == g)

        last_idx = len(self.states) - 1
        snap["weekday"] = self.weekday(self.current_day)
        snap["arr_tickets"] = self.day_stats["arr_t"]
        snap["arr_alerts"] = self.day_stats["arr_a"]
        snap["closed_tickets"] = self.day_stats["closed_t"]
        snap["open_tickets"] = sum(1 for t in self.tasks if t.kind == "ticket" and t.state_index < last_idx)
        if self.env is not None:
            snap["data_volume"] = self.env["data_volume"]
            snap["cloud_cost"] = self.cloud_cost
            snap["access_gaps"] = self.env["access_gaps"]
            snap["peak_mult"] = self.env["peak_mult"]
        if self.history and self.history[-1]["day"] == self.current_day:
            self.history[-1] = snap
        else:
            self.history.append(snap)

    # --- RENDU GLOBAL ---
    def _render_all(self):
        self._refresh_kpis_and_charts()
        self._render_board()

    def _refresh_kpis_and_charts(self):
        last_idx = len(self.states) - 1
        chantiers = [t for t in self.tasks if t.kind == "chantier"]
        total_t = len(chantiers)
        done_tasks = [t for t in chantiers if t.state_index == last_idx]
        wip_tasks = [t for t in self.tasks if 0 < t.state_index < last_idx]

        cur_sprint = min(self.num_sprints, (self.current_day // max(1, self.sprint_duration)) + 1)
        day_txt = f"S{cur_sprint}/{self.num_sprints} — J {self.current_day}/{self.total_simulation_days}"
        if self.env is not None and self.current_day > 0:
            day_txt += f" · {WEEKDAYS[self.weekday(self.current_day)]}"
        self.kpi_day_val.setText(day_txt)
        self.kpi_done_val.setText(f"{len(done_tasks)} / {total_t}")
        self.kpi_wip_val.setText(f"{len(wip_tasks)} tâche{'s' if len(wip_tasks) > 1 else ''}")

        if done_tasks:
            avg_lt = sum(max(1, t.end_day - t.start_day) for t in done_tasks if t.start_day is not None) / len(done_tasks)
            self.kpi_lt_val.setText(f"{avg_lt:.1f} jours")
        else:
            self.kpi_lt_val.setText("—")

        while self.team_pills_grid.count():
            item = self.team_pills_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        has_overflow = len(self.workers) > 8
        visible_workers = self.workers[:7] if has_overflow else self.workers[:8]
        for idx, w in enumerate(visible_workers):
            busy = w.assigned_task is not None
            short_cat = w.specialty[:4].upper() if w.specialty != "Polyvalent" else "POLY"
            pill = QLabel(f"{w.name} ({short_cat})")
            pill.setToolTip(f"{w.name} — Catégorie : {w.specialty}")
            if busy:
                pill.setStyleSheet(f"""
                    background-color: {w.color};
                    color: #FFFFFF;
                    border-radius: 4px;
                    padding: 2px 5px;
                    font-size: 9px;
                    font-weight: 700;
                """)
            else:
                pill.setStyleSheet("""
                    background-color: #F1F5F9;
                    color: #64748B;
                    border: 1px solid #E2E8F0;
                    border-radius: 4px;
                    padding: 2px 5px;
                    font-size: 9px;
                    font-weight: 600;
                """)
            self.team_pills_grid.addWidget(pill, idx // 4, idx % 4)

        if has_overflow:
            extra = QLabel(f"+{len(self.workers) - 7} autres")
            extra.setStyleSheet("font-size: 9.5px; font-weight: 800; color: #64748B;")
            self.team_pills_grid.addWidget(extra, 1, 3)

        self.lbl_chart_1.setText(CHART_TYPES[self.chart_slot_1].upper())
        self.lbl_chart_2.setText(CHART_TYPES[self.chart_slot_2].upper())
        self._draw_chart_by_type(self.chart_slot_1, self.fig_1, self.canvas_1)
        self._draw_chart_by_type(self.chart_slot_2, self.fig_2, self.canvas_2)

    def _draw_chart_by_type(self, chart_type: str, fig: Figure, canvas: FigureCanvas):
        fig.clear()
        ax = fig.add_subplot(111)

        if chart_type == "cfd":
            days = [h["day"] for h in self.history]
            ordered_states = list(reversed(self.states))
            series = [[h.get("ch::" + st, h.get(st, 0)) for h in self.history] for st in ordered_states]
            cfd_palette = [
                "#16A34A", "#4ADE80", "#86EFAC", "#FACC15", "#F59E0B", "#FB923C", "#E2E8F0"
            ]
            colors = [cfd_palette[i % len(cfd_palette)] for i in range(len(ordered_states))]

            if len(days) == 1:
                bottom = 0
                for idx, st in enumerate(ordered_states):
                    val = series[idx][0]
                    ax.bar([0], [val], bottom=bottom, width=0.4, color=colors[idx], label=st)
                    bottom += val
                ax.set_xlim(-0.5, max(5, self.total_simulation_days))
            else:
                ax.stackplot(days, *series, labels=ordered_states, colors=colors, alpha=0.9)
                ax.set_xlim(0, max(days[-1], 1))

            for s in range(1, self.num_sprints):
                boundary = s * self.sprint_duration
                if boundary <= max(days[-1], self.total_simulation_days):
                    ax.axvline(boundary, color="#0F172A", linestyle=":", linewidth=0.9, alpha=0.6)

            ax.set_ylim(0, max(1, self._chantier_counts()[1]))
            ax.legend(loc="upper left", fontsize=6, frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0", ncol=3)

        elif chart_type == "wip":
            active_stages = self.states[1:-1]
            short_labels = [s[:11] + "." if len(s) > 12 else s for s in active_stages]
            active_counts, waiting_counts = [], []
            for st in active_stages:
                st_idx = self.states.index(st)
                st_tasks = [t for t in self.tasks if t.state_index == st_idx]
                active_counts.append(sum(1 for t in st_tasks if t.assigned_workers))
                waiting_counts.append(sum(1 for t in st_tasks if not t.assigned_workers))

            x = range(len(active_stages))
            ax.bar(x, active_counts, width=0.48, color="#16A34A", label="Actif")
            wait_colors = ["#DC2626" if w >= 2 else "#EAB308" for w in waiting_counts]
            ax.bar(x, waiting_counts, bottom=active_counts, width=0.48, color=wait_colors, label="Attente / Goulot")
            ax.set_xticks(list(x))
            ax.set_xticklabels(short_labels, fontsize=7.5, color="#334155")
            ax.set_ylim(0, max(5, max([a + w for a, w in zip(active_counts, waiting_counts)], default=0) + 1))
            ax.legend(loc="upper right", fontsize=7, frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0")

        elif chart_type == "throughput":
            days = [h["day"] for h in self.history]
            daily_deliv = [h.get("delivered_today", 0) for h in self.history]
            cum_deliv = [h.get("ch::" + self.states[-1], h.get(self.states[-1], 0)) for h in self.history]

            bars = ax.bar(days, daily_deliv, width=0.5, color="#EAB308", alpha=0.85, label="Livrées / jour")
            ax2 = ax.twinx()
            line = ax2.plot(days, cum_deliv, color="#16A34A", linewidth=2, marker="o", markersize=3, label="Cumul livré")
            ax2.set_ylim(0, max(1, self._chantier_counts()[1]))
            ax2.tick_params(axis="y", labelsize=7, colors="#16A34A")
            ax2.spines["top"].set_visible(False)

            if len(days) == 1:
                ax.set_xlim(-0.5, max(5, self.total_simulation_days))
            ax.set_ylim(0, max(3, max(daily_deliv, default=0) + 1))

            handles = [bars, line[0]]
            labels = ["Livrées / jour", "Cumul livré"]
            ax.legend(handles, labels, loc="upper left", fontsize=7, frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0")

        elif chart_type == "leadtime":
            done_tasks = [t for t in self.tasks if t.kind == "chantier" and t.state_index == len(self.states) - 1 and t.start_day is not None]
            if done_tasks:
                lts = [max(1, t.end_day - t.start_day) for t in done_tasks]
                unique_lts = sorted(set(lts))
                counts = [lts.count(v) for v in unique_lts]
                g_lim, a_lim = (self.sprint_duration, 1.5 * self.sprint_duration) if self.env is not None else (6, 10)
                bar_cols = ["#16A34A" if v <= g_lim else ("#EAB308" if v <= a_lim else "#DC2626") for v in unique_lts]
                ax.bar([f"{v}j" for v in unique_lts], counts, width=0.45, color=bar_cols)
                ax.set_ylim(0, max(counts) + 1)
            else:
                ax.text(0.5, 0.5, "En attente des premières livraisons...", ha="center", va="center",
                        fontsize=8.5, color="#94A3B8", transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])

        elif chart_type == "tickets":
            days = [h["day"] for h in self.history]
            arr = [h.get("arr_tickets", 0) for h in self.history]
            opened = [h.get("open_tickets", 0) for h in self.history]
            if self.env is None:
                ax.text(0.5, 0.5, "Pas de tickets dans ce scénario.", ha="center", va="center",
                        fontsize=8.5, color="#94A3B8", transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])
            else:
                cols = ["#DC2626" if (h.get("weekday") == 4 and h["day"] > 0) else "#EAB308" for h in self.history]
                ax.bar(days, arr, width=0.6, color=cols)
                ax2 = ax.twinx()
                ax2.plot(days, opened, color="#0F172A", linewidth=1.6)
                ax2.tick_params(axis="y", labelsize=7, colors="#0F172A")
                ax2.spines["top"].set_visible(False)
                ax2.set_ylim(0, max(5, max(opened, default=0) + 2))
                ax.set_ylim(0, max(5, max(arr, default=0) + 1))
                ax.set_xlim(-0.5, max(self.total_simulation_days, 5) + 0.5)
                for s_i in range(1, self.num_sprints):
                    ax.axvline(s_i * self.sprint_duration + 0.5, color="#0F172A", linestyle=":", linewidth=0.9, alpha=0.5)
                handles = [matplotlib.patches.Patch(color="#DC2626"), matplotlib.patches.Patch(color="#EAB308"),
                           matplotlib.lines.Line2D([0], [0], color="#0F172A", linewidth=1.6)]
                ax.legend(handles, ["Reçus le vendredi", "Reçus lun-jeu", "Ouverts (axe droit)"], loc="upper left",
                          fontsize=6.5, frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0", ncol=3)

        elif chart_type == "cost":
            days = [h["day"] for h in self.history]
            if self.env is None:
                ax.text(0.5, 0.5, "Pas de suivi des coûts dans ce scénario.", ha="center", va="center",
                        fontsize=8.5, color="#94A3B8", transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])
            else:
                dv = [h.get("data_volume", 100) for h in self.history]
                cc = [h.get("cloud_cost", 100) for h in self.history]
                ax.plot(days, dv, color="#D97706", linewidth=1.8, label="Volume de données")
                ax.plot(days, cc, color="#16A34A", linewidth=1.8, label="Coût cloud")
                ax.axhline(100, color="#94A3B8", linestyle=":", linewidth=1)
                ax.set_xlim(0, max(self.total_simulation_days, 5))
                ax.set_ylim(min(dv + cc + [90]) - 5, max(dv + cc + [105]) + 5)
                ax.legend(loc="upper right", fontsize=7, frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0")

        ax.tick_params(axis="both", labelsize=7.5, colors="#64748B")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", linewidth=0.5, color="#E2E8F0")
        fig.tight_layout(pad=0.6)
        canvas.draw()

    # --- RENDU DU TABLEAU KANBAN ---
    def _render_board(self):
        h_val = self.board_scroll.horizontalScrollBar().value()

        while self.columns_layout.count():
            item = self.columns_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        last_idx = len(self.states) - 1

        for idx, state_name in enumerate(self.states):
            col_tasks = [t for t in self.tasks if t.state_index == idx]
            active_workers = sum(len(t.assigned_workers) for t in col_tasks)
            max_w = self.col_worker_limits.get(state_name, 0)
            waiting_tasks = [t for t in col_tasks if not t.assigned_workers]
            qualified_count = sum(1 for w in self.workers if self._worker_can_work_in(w, state_name))

            is_bottleneck = (0 < idx < last_idx) and (len(waiting_tasks) >= 2) and (
                active_workers >= max_w or qualified_count == 0
            )

            if is_bottleneck:
                col_bg = PALETTE["red_soft"]
                border_col = PALETTE["red_border"]
                accent_col = PALETTE["red"]
            elif idx == last_idx:
                col_bg = PALETTE["green_soft"]
                border_col = PALETTE["green_border"]
                accent_col = PALETTE["green"]
            elif idx == 0:
                col_bg = PALETTE["bg_surface"]
                border_col = PALETTE["border"]
                accent_col = PALETTE["amber_btn"]
            else:
                col_bg = PALETTE["bg_surface"]
                border_col = PALETTE["border"]
                accent_col = PALETTE["green"] if active_workers > 0 else PALETTE["amber_btn"]

            col_frame = QFrame()
            col_frame.setMinimumWidth(235)
            col_frame.setObjectName("KanbanCol")
            col_frame.setStyleSheet(f"""
                QFrame#KanbanCol {{
                    background-color: {col_bg};
                    border: 1px solid {border_col};
                    border-top: 3px solid {accent_col};
                    border-radius: 8px;
                }}
            """)

            col_vbox = QVBoxLayout(col_frame)
            col_vbox.setContentsMargins(10, 10, 10, 10)
            col_vbox.setSpacing(8)

            hdr_row = QHBoxLayout()
            lbl_name = QLabel(state_name.upper())
            lbl_name.setStyleSheet("font-size: 10px; font-weight: 800; color: #0F172A; letter-spacing: 0.4px; background: transparent;")
            hdr_row.addWidget(lbl_name)

            badge_cnt = QLabel(str(len(col_tasks)))
            badge_cnt.setStyleSheet("""
                background-color: #FFFFFF;
                color: #334155;
                border: 1px solid #CBD5E1;
                border-radius: 9px;
                padding: 1px 7px;
                font-size: 10px;
                font-weight: 800;
            """)
            hdr_row.addWidget(badge_cnt)
            hdr_row.addStretch()

            if is_bottleneck:
                lbl_bn = QLabel("0 QUALIFIÉ" if qualified_count == 0 else "GOULOT")
                lbl_bn.setStyleSheet("""
                    background-color: #DC2626;
                    color: #FFFFFF;
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-size: 9px;
                    font-weight: 800;
                """)
                hdr_row.addWidget(lbl_bn)

            col_vbox.addLayout(hdr_row)

            if 0 < idx < last_idx:
                cap_row = QHBoxLayout()
                lbl_cap = QLabel(f"Équipe : {active_workers} / Max")
                lbl_cap.setStyleSheet("font-size: 11px; color: #475569; font-weight: 600; background: transparent;")
                cap_row.addWidget(lbl_cap)
                cap_row.addStretch()

                stepper_lim = CleanStepper(
                    max_w, 1, 15,
                    on_change=lambda val, s=state_name: self._on_col_limit_changed(s, val),
                    compact=True
                )
                cap_row.addWidget(stepper_lim)
                col_vbox.addLayout(cap_row)

            cards_scroll = QScrollArea()
            cards_scroll.setWidgetResizable(True)
            cards_scroll.setStyleSheet("background: transparent;")

            cards_widget = QWidget()
            cards_widget.setStyleSheet("background: transparent;")
            cards_vbox = QVBoxLayout(cards_widget)
            cards_vbox.setContentsMargins(0, 2, 2, 2)
            cards_vbox.setSpacing(7)

            shown = col_tasks
            if idx == last_idx and len(col_tasks) > 12:
                shown = sorted(col_tasks, key=lambda t: -(t.end_day or 0))[:12]
            for task in shown:
                cards_vbox.addWidget(self._create_task_card(task, state_name, idx, last_idx, is_bottleneck))
            if len(shown) < len(col_tasks):
                lbl_more = QLabel(f"+ {len(col_tasks) - len(shown)} autres terminées")
                lbl_more.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748B; background: transparent;")
                cards_vbox.addWidget(lbl_more)

            cards_vbox.addStretch()
            cards_scroll.setWidget(cards_widget)
            col_vbox.addWidget(cards_scroll)

            self.columns_layout.addWidget(col_frame)

        QTimer.singleShot(0, lambda: self.board_scroll.horizontalScrollBar().setValue(h_val))

    def _on_col_limit_changed(self, state_name: str, val: int):
        self.col_worker_limits[state_name] = val
        self._render_all()

    def _create_task_card(self, task: Task, state_name: str, col_idx: int, last_idx: int, col_bottleneck: bool) -> QFrame:
        if col_idx == last_idx:
            stripe = PALETTE["green"]
        elif col_idx == 0:
            stripe = PALETTE["amber_btn"]
        elif task.assigned_workers:
            stripe = PALETTE["green"]
        elif col_bottleneck:
            stripe = PALETTE["red"]
        else:
            stripe = PALETTE["amber"]

        card = QFrame()
        card.setObjectName("TaskCard")
        card.setStyleSheet(f"""
            QFrame#TaskCard {{
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-left: 3px solid {stripe};
                border-radius: 6px;
            }}
        """)

        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(9, 8, 9, 8)
        vbox.setSpacing(5)

        top_row = QHBoxLayout()
        lbl_id = QLabel(task.label)
        lbl_id.setStyleSheet("font-size: 10px; font-weight: 800; color: #64748B; background: transparent;")
        top_row.addWidget(lbl_id)

        if task.category_tag:
            lbl_tag = QLabel(task.category_tag)
            tag_fg, tag_bg, tag_bd = {
                "ticket": ("#B91C1C", "#FEF2F2", "#FECACA"),
                "alerte": ("#B45309", "#FFFBEB", "#FDE68A"),
            }.get(task.kind, ("#15803D", "#F0FDF4", "#BBF7D0") if task.tag else ("#B45309", "#FFFBEB", "#FDE68A"))
            lbl_tag.setStyleSheet(f"""
                background-color: {tag_bg};
                color: {tag_fg};
                border: 1px solid {tag_bd};
                border-radius: 4px;
                padding: 1px 5px;
                font-size: 8.5px;
                font-weight: 800;
            """)
            top_row.addWidget(lbl_tag)

        top_row.addStretch()

        if col_idx == last_idx and task.start_day is not None and task.end_day is not None:
            lt = max(1, task.end_day - task.start_day)
            lbl_lt = QLabel(f"Livré en {lt}j")
            lbl_lt.setStyleSheet("""
                background-color: #F0FDF4;
                color: #15803D;
                border: 1px solid #BBF7D0;
                border-radius: 4px;
                padding: 1px 5px;
                font-size: 9px;
                font-weight: 800;
            """)
            top_row.addWidget(lbl_lt)
        elif 0 < col_idx < last_idx:
            req = task.effort_per_stage.get(state_name, 1)
            lbl_prog = QLabel(f"{task.progress}/{req} j")
            lbl_prog.setStyleSheet("""
                background-color: #F8FAFC;
                color: #475569;
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                padding: 1px 5px;
                font-size: 9px;
                font-weight: 700;
            """)
            top_row.addWidget(lbl_prog)

        vbox.addLayout(top_row)

        lbl_title = QLabel(task.title)
        lbl_title.setWordWrap(True)
        lbl_title.setStyleSheet("font-size: 11.5px; font-weight: 700; color: #0F172A; background: transparent;")
        vbox.addWidget(lbl_title)

        if 0 < col_idx < last_idx:
            req = task.effort_per_stage.get(state_name, 1)
            pct = min(1.0, task.progress / req)
            bar_track = QFrame()
            bar_track.setFixedHeight(4)
            bar_track.setStyleSheet("background-color: #E2E8F0; border-radius: 2px;")
            bar_layout = QHBoxLayout(bar_track)
            bar_layout.setContentsMargins(0, 0, 0, 0)
            bar_layout.setSpacing(0)

            if pct > 0:
                bar_fill = QFrame()
                bar_fill.setFixedHeight(4)
                bar_fill.setStyleSheet("background-color: #16A34A; border-radius: 2px;")
                bar_layout.addWidget(bar_fill, int(pct * 100))
            bar_layout.addStretch(max(1, int((1.0 - pct) * 100)))
            vbox.addWidget(bar_track)

        if task.assigned_workers:
            w_row = QHBoxLayout()
            w_row.setSpacing(4)
            for w in task.assigned_workers:
                badge = QLabel(w.name)
                badge.setStyleSheet(f"""
                    background-color: {w.color};
                    color: #FFFFFF;
                    border-radius: 4px;
                    padding: 2px 6px;
                    font-size: 10px;
                    font-weight: 700;
                """)
                w_row.addWidget(badge)
            w_row.addStretch()
            vbox.addLayout(w_row)
        elif 0 < col_idx < last_idx:
            if task.ready_day > self.current_day:
                txt, col_txt = "Reprise demain : outil de suivi différent", "#D97706"
            else:
                txt = "Bloquée (goulot)" if col_bottleneck else "En attente d'équipier"
                col_txt = "#DC2626" if col_bottleneck else "#D97706"
            lbl_wait = QLabel(txt)
            lbl_wait.setStyleSheet(f"font-size: 10px; font-weight: 600; color: {col_txt}; background: transparent;")
            vbox.addWidget(lbl_wait)

        return card


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Lato", 10))
    window = KanbanSimulatorWindow()
    window.show()
    sys.exit(app.exec())