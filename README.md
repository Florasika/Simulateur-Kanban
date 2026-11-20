# Kanban Flow Analytics — Simulateur Lean IT & Agile (cas Pixels & Dragons)

Application de bureau interactive développée en Python (PyQt6 & Matplotlib) pour modéliser, simuler et analyser un flux de travail sous méthode Kanban et Lean IT.

Le simulateur a été adapté au cas d'étude **Pixels & Dragons** : un studio de jeu vidéo en ligne organisé en silos (Développement, Data, Sécurité, Ops/Infra, Support), avec un outil de suivi par département, des données dupliquées, un pic de charge le vendredi soir (20h-minuit) et des accès aux bases de test mal tracés (RGPD). Il permet de comparer la situation actuelle à l'organisation préconisée, de lire des KPIs de fin de sprint avec leur interprétation Lean (muda, mura, muri, 5S) et de tenir une rétrospective qui modifie la suite de la simulation.

Les scénarios génériques d'origine (équipe équilibrée, goulot QA, rush, flux tendu) restent disponibles.

## Table des matières

1. Objectifs pédagogiques et fonctionnels
2. Fonctionnalités principales
3. Logique du moteur de simulation
4. Scénarios intégrés
5. KPIs de fin de sprint et interprétation
6. Rétrospective
7. Graphiques analytiques
8. Bilan exporté en Markdown
9. Installation et exécution
10. Limites du modèle

## 1. Objectifs pédagogiques et fonctionnels

- Visualiser un flux tiré (pull system) : une tâche n'avance que lorsqu'une capacité se libère en aval.
- Identifier les goulots d'étranglement : colonnes saturées, files d'attente, dépendance à un seul spécialiste (la Sécurité dans le cas Pixels & Dragons).
- Mesurer l'effet des leviers Lean sur le débit, les délais, le coût cloud et la charge du vendredi : outil de suivi commun, polyvalence, backlog priorisé, rétrospective.
- Relier les chiffres aux notions du cours : muda (attente, stocks, surproduction), mura (irrégularité), muri (surcharge) et 5S.
- Expérimenter la réorganisation : modifier les colonnes, l'équipe, les plafonds WIP et les tâches.

## 2. Fonctionnalités principales

### Pilotage de la simulation
- Boutons Play, Pause, Stop / Réinitialisation et curseur de vitesse réglable (150 à 1400 ms par jour simulé).
- Suivi par sprint et par jour, avec le jour de la semaine (semaine de 5 jours ouvrés, le vendredi est le jour de pic).
- Bouton « 📄 Bilan .md » pour exporter le bilan à tout moment.

### Tableau Kanban dynamique
- Colonnes du cas Pixels & Dragons : Backlog → Support → Développement → Data → Sécurité → Ops/Infra → Terminé. Les scénarios génériques gardent leurs colonnes d'origine.
- Plafond d'équipiers actifs réglable sur chaque colonne, alertes visuelles en rouge sur les colonnes saturées (GOULOT) ou sans équipier qualifié (0 QUALIFIÉ).
- Trois types de cartes : chantiers d'amélioration, tickets joueurs et alertes sécurité (pastilles distinctes). Un chantier indique son thème et, quand il attend une reprise, « Reprise demain : outil de suivi différent ».
- Chaque carte affiche sa progression, l'équipier assigné et son lead time à la livraison. La colonne Terminé montre les 12 dernières cartes.

### Paramétrage (⚙ Paramètres)
- Nombre de sprints (1 à 10) et durée d'un sprint (5 à 45 jours).
- Équipe : ajout et suppression d'équipiers, avec une spécialité ou le statut Polyvalent.
- Catégories : ajout, suppression et réorganisation des étapes du flux.
- Backlog : volume de tâches, ajout rapide, tâches personnalisées prioritaires.
- Choix des graphiques affichés.

## 3. Logique du moteur de simulation

À chaque journée simulée, le moteur exécute :

1. **Arrivées** : les tickets joueurs arrivent selon un tirage de Poisson, multiplié par un coefficient de pic le vendredi. Des alertes sécurité arrivent aussi. Le volume de données augmente légèrement chaque jour.
2. **Avancement du travail** : chaque tâche active progresse selon les équipiers assignés. À la fin d'une étape, la tâche passe à la colonne suivante. Si les outils de suivi diffèrent, la reprise se fait le jour suivant. Une étape sans effort est sautée (par exemple, un chantier ne passe pas par le Support).
3. **Allocation en flux tiré (de droite à gauche)** : les équipiers libres sont affectés en priorité aux étapes les plus proches de la livraison, dans la limite du plafond de chaque colonne. Les spécialistes passent avant les polyvalents, et les tickets et alertes avant les chantiers. Le backlog n'est sollicité que si la première étape utile a de la capacité.
4. **Effet des chantiers livrés** : chaque chantier livré améliore le système selon son thème.

| Thème du chantier | Effet une fois livré |
| --- | --- |
| Pic du vendredi (scaling élastique) | Réduit le coefficient de pic |
| Dette technique | Réduit le taux d'arrivée des tickets (environ 12 %) |
| Données (purge des doublons) | Réduit le volume de données (environ 12 %) |
| Nuit (instances nocturnes) | Réduit le gaspillage de la nuit |
| Accès (habilitations) | Ferme des failles d'habilitation |
| Outil de suivi commun | Supprime le délai de reprise entre pôles |

Le coût cloud est calculé à partir du volume de données et du gaspillage de nuit (indice 100 au départ).

## 4. Scénarios intégrés

### Cas Pixels & Dragons

| Scénario | Horizon | Volume | Équipe | Particularités |
| --- | --- | --- | --- | --- |
| Pixels & Dragons — Situation actuelle (silos) | 4 sprints × 10 j (40 j) | 20 chantiers + tickets et alertes | 11 personnes, toutes spécialistes (3 Dev, 2 Data, 1 Sécurité, 2 Ops/Infra, 3 Support) | Plafonds Support 3, Dev 3, Data 2, Sécurité 1, Ops/Infra 2 ; outils de suivi différents (reprise d'un jour) ; backlog dans l'ordre d'arrivée |
| Pixels & Dragons — Organisation préconisée (Lean IT) | 4 sprints × 10 j (40 j) | identique | 11 personnes dont 3 polyvalents (Dev, Data, Ops/Infra) | Plafonds Support 3, Dev 3, Data 3, Sécurité 2, Ops/Infra 3 ; outil commun (pas de délai de reprise) ; backlog priorisé |

### Scénarios génériques d'origine

| Scénario | Horizon | Volume | Objectif d'observation |
| --- | --- | --- | --- |
| Équipe Équilibrée (Standard) | 2 sprints × 12 j | 38 tâches | Flux nominal de référence |
| Goulot d'étranglement QA | 2 sprints × 12 j | 38 tâches | Files d'attente devant la QA |
| Rush Multi-Sprints | 3 sprints × 10 j | 50 tâches | Forte charge technique |
| Flux Tendu Lean (WIP = 1) | 2 sprints × 14 j | 30 tâches | Limitation stricte de l'en-cours |

Les scénarios génériques utilisent leur propre équipe de 5 personnes et leurs colonnes d'origine ; le changement de scénario restaure automatiquement le bon jeu de colonnes et d'équipe.

## 5. KPIs de fin de sprint et interprétation

À la fin de chaque sprint, une fenêtre affiche le rapport de KPIs sous forme de cartes colorées (vert, ambre, rouge), avec une phrase d'interprétation et le goulot principal du sprint. Dans le cas Pixels & Dragons, les 11 KPIs sont :

| KPI | Lecture Lean | Seuils |
| --- | --- | --- |
| Chantiers d'amélioration livrés | Kaizen | Rouge si 0, ambre si recul |
| Lead time des chantiers | Attente (muda) | Vert ≤ 1 sprint, ambre ≤ 1,5 sprint |
| Travail en attente (% du WIP) | Attente (muda) | Vert ≤ 25 %, ambre ≤ 50 % |
| Volume de données stockées (indice 100) | Stocks excessifs, Seiri / Seiso | Vert ≤ 97, ambre ≤ 103 |
| Coût cloud (indice 100) | Surproduction (muda) | Vert ≤ 90, ambre ≤ 100 |
| Pic du vendredi | Irrégularité (mura) | Vert ≤ 2, ambre ≤ 3 |
| Tickets ouverts le vendredi soir | Surcharge (muri) | Vert ≤ 3, ambre ≤ 8 |
| Délai moyen d'un ticket joueur | Attente (muda) | Vert ≤ 1,5 j, ambre ≤ 3 j |
| Charge des pôles (plus / moins chargé) | Muri et mura | Rouge si > 92 % avec un écart > 40 points |
| Failles d'habilitation ouvertes | Seiketsu (accès BDD, RGPD) | Vert 0, ambre ≤ 4 |
| Rétrospectives inter-équipes tenues | Shitsuke | Vert si tenue à chaque sprint |

Les scénarios génériques affichent six KPIs d'origine : débit, lead time, WIP moyen, tâches en attente, utilisation de l'équipe et jours sans livraison.

## 6. Rétrospective

Après le rapport de KPIs, le bouton « Ouvrir la rétrospective ▸ » ouvre une fenêtre au format **Start / Stop / Continue** :

- Trois zones de texte préremplies à partir des KPIs, que l'équipe peut modifier.
- Des actions Kaizen à cocher, appliquées au sprint suivant :
  - ajouter une capacité à la colonne goulot ;
  - former un équipier (hors Support) pour le rendre polyvalent ;
  - passer en tête du backlog un thème de chantiers (pic du vendredi, données, accès, etc.), présélectionné d'après les KPIs ;
  - mettre en place l'outil de suivi commun.

Les décisions sont conservées dans un journal et reprises dans le bilan exporté. Elles modifient réellement la simulation : on peut mesurer au sprint suivant ce qu'elles ont changé.

## 7. Graphiques analytiques

Deux emplacements configurables parmi six vues :

- **Flux Cumulatif (CFD)** : répartition quotidienne des tâches par étape.
- **Charge & Goulots par Étape** : tâches en traitement et tâches en attente d'équipier, par colonne.
- **Débit & Livraisons / Jour** : livraisons quotidiennes et courbe cumulée.
- **Distribution du Lead Time** : répartition des tâches livrées selon leur durée de traversée.
- **Pic du vendredi : tickets reçus / ouverts** : tickets par jour de semaine, pour voir le lissage de la charge.
- **Indice données & coût cloud** : évolution des deux indices (base 100).

Par défaut, les scénarios Pixels & Dragons affichent le CFD et le pic du vendredi ; les scénarios génériques affichent le CFD et la charge par étape.

## 8. Bilan exporté en Markdown

En fin de simulation, le fichier `bilan_simulation.md` est créé dans le **même dossier que le script**, et la fenêtre de fin indique son chemin complet. Le bouton « 📄 Bilan .md » permet aussi de l'exporter à tout moment (après au moins un sprint), à l'emplacement de votre choix.

Contenu du fichier :
- une synthèse (jours simulés, chantiers livrés, lead time, délai des tickets, rétrospectives tenues, actions Kaizen décidées) ;
- pour chaque sprint, le tableau des KPIs avec leur interprétation et le goulot principal ;
- les Start / Stop / Continue saisis lors de chaque rétrospective.

## 9. Installation et exécution

### Prérequis
- Python 3.10+
- Dépendances : `PyQt6` et `matplotlib`

### Étapes

```bash
# 1. Cloner le dépôt GitHub
git clone https://github.com/<votre-identifiant>/<nom-du-depot>.git
cd <nom-du-depot>

# 2. (Optionnel) Créer et activer un environnement virtuel
python -m venv venv
# Sous Windows :
venv\Scripts\activate
# Sous macOS / Linux :
source venv/bin/activate

# 3. Installer les dépendances
pip install PyQt6 matplotlib

# 4. Lancer l'application
python kanban_sim.py
```

Si vous renommez le script en `simulateur_kanban.py`, lancez-le avec ce nom. Le fichier `requirements.txt` doit contenir `PyQt6` et `matplotlib`.

## 10. Limites du modèle

Les résultats du simulateur dépendent d'hypothèses choisies pour le cas : 11 personnes, efforts de 1 à 3 jours par étape, taux d'arrivée des tickets, effet de chaque type de chantier, un seul spécialiste Sécurité, polyvalence supposée acquise par la formation. Les simulations montrent l'effet relatif des leviers (outil commun, polyvalence, backlog priorisé, rétrospective), pas des valeurs réelles du studio.

Sur 100 tirages et 40 jours, les chantiers livrés (sur 20) passent d'environ 8,8 en silos à environ 20 dans l'organisation Lean, la polyvalence étant le levier le plus fort. L'organisation Lean approche de la saturation (98 % de charge au sprint 3) : il faut garder environ 20 % de marge.

## Architecture du code

Le code tient dans un seul fichier, `kanban_sim.py` :

- **Données du cas** : `PD_CHANTIERS`, `PD_TEAM_SILOS`, `PD_TEAM_LEAN`, `PD_ENV_BASE`, `SCENARIOS`.
- **Interprétation** : `interpret_pd` et `suggest_pd` (Pixels & Dragons), `interpret_generic` et `suggest_generic` (scénarios génériques), appelés par `interpret_report` et `suggest_retro_items`.
- **Fenêtres** : `SprintReportDialog` (KPIs), `RetrospectiveDialog` (Start / Stop / Continue et actions Kaizen), fenêtre de paramètres.
- **Moteur** : `KanbanSimulatorWindow`, avec `_simulate_one_day`, `_apply_chantier_effect`, `build_sprint_report`, `apply_retrospective` et `export_bilan_markdown`.
