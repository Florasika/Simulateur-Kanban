# Kanban Flow Analytics — Simulateur Lean IT & Agile

Application de bureau interactive développée en **Python (PyQt6 & Matplotlib)** permettant de modéliser, simuler et analyser la dynamique d'un flux de production logiciel sous méthode **Kanban** et **Lean IT**.

L'outil met en évidence l'impact des limites de travail en cours (**WIP**), de la spécialisation des rôles, de la charge technique et des goulots d'étranglement sur les indicateurs clés de performance (**Lead Time**, **Débit / Throughput**, **Diagramme de Flux Cumulatif**).

---

## Table des matières
1. [Objectifs pédagogiques et fonctionnels](#1-objectifs-pédagogiques-et-fonctionnels)
2. [Fonctionnalités principales](#2-fonctionnalités-principales)
3. [Logique du moteur de simulation](#3-logique-du-moteur-de-simulation)
4. [Scénarios de flux intégrés](#4-scénarios-de-flux-intégrés)
5. [Indicateurs et graphiques analytiques](#5-indicateurs-et-graphiques-analytiques)
6. [Installation et exécution](#6-installation-et-exécution)
7. [Architecture du code](#7-architecture-du-code)

---

## 1. Objectifs pédagogiques et fonctionnels

* **Visualiser le flux tiré (*Pull System*)** : observer comment les tâches avancent d'étape en étape uniquement lorsqu'une capacité de traitement se libère en aval.
* **Identifier et résoudre les goulots d'étranglement (*Bottlenecks*)** : repérer visuellement les colonnes en surcharge, les files d'attente et le manque de compétences sur une étape donnée.
* **Mesurer l'impact des limites WIP (*Work In Progress*)** : comparer un flux standard, un flux engorgé et un flux tendu Lean (`WIP = 1`) sur le temps de traversée (*Lead Time*).
* **Expérimenter la réorganisation d'équipe et de processus** : ajouter ou déplacer des étapes du cycle de vie (ex. *Infra*, *Revue de code*), recruter des profils spécialisés ou polyvalents et injecter des tâches prioritaires.

---

## 2. Fonctionnalités principales

### Pilotage de la simulation
* Contrôles **Play**, **Pause**, **Stop / Réinitialisation** et **curseur de vitesse** réglable en temps réel (de 150 ms à 1400 ms par jour simulé).
* Suivi de l'avancement par **Sprints** et **Jours** (ex. `S1/2 — J 0/24`).

### Tableau Kanban dynamique
* Colonnes par défaut : `Backlog` → `Design UI/UX` → `Développement` → `Analyse` → `QA` → `Déploiement` → `Terminé`.
* Réglage direct sur chaque colonne du plafond maximal d'équipiers actifs simultanément (`Équipe : X / Max`).
* Alertes visuelles automatiques en rouge sur les colonnes saturées (**`GOULOT`**) ou dépourvues d'équipier qualifié (**`0 QUALIFIÉ`**).
* Cartes tâches détaillées : identifiant (`US-01`), intitulé métier, barre de progression journalière (`1/2 j`), badge d'équipier assigné et *Lead Time* individuel à la livraison (`Livré en Xj`).

### Paramétrage centralisé (`⚙ Paramètres`)
* **Sprints & Horizon** : configuration du nombre de sprints (1 à 10) et de la durée d'un sprint (5 à 45 jours).
* **Gestion de l'équipe et des compétences** : ajout et suppression d'équipiers avec affectation à une catégorie métier spécifique ou au statut **Polyvalent**, avec suivi d'activité en temps réel dans le panneau supérieur.
* **Catégories du flux** : ajout d'étapes avant ou après une colonne existante, réorganisation de l'ordre de passage (`↑ Avant`, `↓ Après` ou glisser-déposer) et suppression d'étapes.
* **Backlog & Tâches ciblées** : ajustement du volume total de tâches (5 à 100), ajout rapide `+10 tâches`, ou création de tâches personnalisées positionnées en priorité (`En premier`), avant une tâche précise, ou injectées directement dans une colonne cible.

---

## 3. Logique du moteur de simulation

À chaque journée simulée (`_simulate_one_day`), le moteur exécute deux phases séquentielles :

1. **Avancement du travail en cours** : chaque tâche occupée progresse en fonction du nombre d'équipiers assignés. Dès que l'effort requis pour l'étape est atteint, les équipiers sont libérés et la tâche passe à la colonne suivante (ou en `Terminé`, enregistrant son jour de fin `end_day`).
2. **Allocation en flux tiré (de droite à gauche)** : les équipiers disponibles sont affectés en priorité aux étapes les plus proches de la livraison (`Déploiement` → `QA` → `Analyse` → `Développement` → `Design UI/UX`), dans la limite du plafond `Max` de chaque colonne et selon leur qualification (les spécialistes de l'étape sont priorisés sur les profils polyvalents). Le `Backlog` n'est sollicité que si la première étape active dispose encore de capacité libre.

---

## 4. Scénarios de flux intégrés

| Scénario | Horizon | Volume | Effort / étape | Plafonds par colonne | Objectif d'observation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Équipe Équilibrée (Standard)** | 2 sprints × 12 j (24 j) | 38 tâches | 1 à 2 j | Design: 2, Dev: 3, Analyse: 2, QA: 2, Dépl.: 2 | Flux nominal de référence, progression régulière. |
| **Goulot d'étranglement QA** | 2 sprints × 12 j (24 j) | 38 tâches | 1 à 3 j | Design: 3, Dev: 4, Analyse: 2, **QA: 1, Dépl.: 1** | Saturation en aval et accumulation des files d'attente devant la QA. |
| **Rush Multi-Sprints** | 3 sprints × 10 j (30 j) | 50 tâches | 2 à 3 j | Design: 2, Dev: 3, Analyse: 2, QA: 2, Dépl.: 2 | Forte charge technique et pression sur la capacité de livraison. |
| **Flux Tendu Lean (WIP = 1)** | 2 sprints × 14 j (28 j) | 30 tâches | 1 à 2 j | **1 sur toutes les colonnes** | Limitation stricte de l'en-cours pour minimiser le *Lead Time*. |

---

## 5. Indicateurs et graphiques analytiques

### KPI temps réel
* **Sprints & Temps** : sprint courant et avancement en jours par rapport à l'horizon total.
* **Tâches livrées** : ratio des tâches ayant atteint la colonne `Terminé`.
* **Lead Time moyen** : durée moyenne (en jours) entre l'entrée d'une tâche dans le flux actif et sa livraison finale.
* **En cours (WIP)** : nombre total de tâches actuellement actives ou en attente entre le `Backlog` et `Terminé`.

### Graphiques dynamiques (2 emplacements configurables parmi 4 vues)
1. **Flux Cumulatif (CFD)** : graphique en aires empilées illustrant la répartition quotidienne des tâches par étape et la stabilité du flux à travers les sprints.
2. **Charge & Goulots par Étape** : histogramme empilé comparant les tâches en cours de traitement (vert) et les tâches en attente d'équipier (jaune/rouge) pour chaque colonne.
3. **Débit & Livraisons / Jour** : double axe combinant les livraisons quotidiennes (barres) et la courbe cumulée des tâches livrées.
4. **Distribution du Lead Time** : répartition des tâches livrées selon leur durée totale de traversée (en jours).

---

## 6. Installation et exécution

### Prérequis
* **Python 3.10+** installé sur le poste.

### Étapes d'installation

```bash
# 1. Cloner le dépôt GitHub
git clone [https://github.com/](https://github.com/)<votre-identifiant>/<nom-du-depot>.git
cd <nom-du-depot>

# 2. (Optionnel) Créer et activer un environnement virtuel
python -m venv venv
# Sous Windows :
venv\Scripts\activate
# Sous macOS / Linux :
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python simulateur_kanban.py
