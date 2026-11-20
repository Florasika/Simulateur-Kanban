import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QScrollArea, QFrame,
    QDialog, QListWidget, QListWidgetItem, QMessageBox, QGridLayout,
    QLineEdit, QComboBox, QAbstractItemView
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

CHART_TYPES = {
    "cfd": "Flux Cumulatif (CFD)",
    "wip": "Charge & Goulots par Étape",
    "throughput": "Débit & Livraisons / Jour",
    "leadtime": "Distribution du Lead Time"
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
                 start_state_idx: int = 0, category_tag: str = ""):
        self.id = task_id
        self.title = title
        self.effort_per_stage = {state: random.randint(*effort_range) for state in states[1:-1]}
        self.progress = 0
        self.state_index = start_state_idx
        self.category_tag = category_tag
        self.assigned_workers = []
        self.start_day = 0 if start_state_idx > 0 else None
        self.end_day = None


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
        for t in self.app.tasks[:30]:
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

        self.current_day = 0
        self.is_running = False
        self.tasks: list[Task] = []
        self.workers: list[Worker] = []
        self.history: list[dict] = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

        self._apply_global_stylesheet()
        self._build_ui()
        self.reset_simulation()

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

        self.lbl_scenario_badge = QLabel("Scénario : Équipe Équilibrée (Standard)")
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
                self.active_scenario_key = dlg.selected_scenario
                sc = SCENARIOS[self.active_scenario_key]
                self.effort_range = sc["effort_range"]
                for st, lim in sc["limits"].items():
                    if st in self.col_worker_limits:
                        self.col_worker_limits[st] = lim
                self.lbl_scenario_badge.setText(f"Scénario : {sc['name']}")
                need_reset = True

            self.num_sprints = dlg.new_num_sprints
            self.sprint_duration = dlg.new_sprint_days

            base_task_target = max(1, dlg.new_total_tasks - len(dlg.pending_custom_tasks))
            if base_task_target != self.target_task_count:
                self.target_task_count = base_task_target
                need_reset = True

            self.chart_slot_1 = dlg.selected_chart_1
            self.chart_slot_2 = dlg.selected_chart_2

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

                    new_id = max([t.id for t in self.tasks], default=0) + 1
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

        self.workers = [
            Worker(i + 1, name, spec) for i, (name, spec) in enumerate(self.team_specs)
        ]

        self.tasks = []
        for i in range(self.target_task_count):
            title = self.custom_task_titles[i % len(self.custom_task_titles)]
            if i >= len(self.custom_task_titles):
                title = f"{title} (Lot {i // len(self.custom_task_titles) + 1})"
            self.tasks.append(Task(i + 1, title, self.states, self.effort_range))

        for st in self.states:
            if st not in self.col_worker_limits:
                self.col_worker_limits[st] = 0 if st in (self.states[0], self.states[-1]) else 2

        self._record_history_snapshot(delivered_today=0)
        self._render_all()

    def start_simulation(self):
        if self.is_running:
            return
        done_count = sum(1 for t in self.tasks if t.state_index == len(self.states) - 1)
        if self.current_day >= self.total_simulation_days or done_count == len(self.tasks):
            self.reset_simulation()
        self.is_running = True
        self.timer.start(self.slider_speed.value())

    def pause_simulation(self):
        self.is_running = False
        self.timer.stop()

    def _tick(self):
        done_count = sum(1 for t in self.tasks if t.state_index == len(self.states) - 1)

        if self.current_day >= self.total_simulation_days or done_count == len(self.tasks):
            self.pause_simulation()
            self._render_all()
            msg = (
                "Toutes les tâches ont été livrées !"
                if done_count == len(self.tasks)
                else f"Les {self.num_sprints} sprint(s) ont été exécutés."
            )
            QMessageBox.information(
                self, "Bilan de Simulation",
                f"{msg}\nSprints exécutés : {self.num_sprints} ({self.current_day} / {self.total_simulation_days} jours)\n"
                f"Tâches terminées : {done_count} / {len(self.tasks)}"
            )
            return

        self.current_day += 1
        delivered_today = self._simulate_one_day()
        self._record_history_snapshot(delivered_today=delivered_today)
        self._render_all()

    def _worker_can_work_in(self, worker: Worker, state_name: str) -> bool:
        return worker.specialty == "Polyvalent" or worker.specialty == state_name

    def _simulate_one_day(self) -> int:
        last_idx = len(self.states) - 1
        delivered_today = 0

        # 1. Faire avancer les tâches ayant déjà un équipier assigné
        for task in self.tasks:
            if 0 < task.state_index < last_idx and task.assigned_workers:
                st_name = self.states[task.state_index]
                req_effort = task.effort_per_stage.get(st_name, 1)
                task.progress += len(task.assigned_workers)

                if task.progress >= req_effort:
                    for w in task.assigned_workers:
                        w.assigned_task = None
                    task.assigned_workers.clear()
                    task.state_index += 1
                    task.progress = 0
                    if task.state_index == last_idx:
                        task.end_day = self.current_day
                        delivered_today += 1

        # 2. Affecter les équipiers libres selon leur catégorie (flux tiré de droite à gauche)
        free_workers = [w for w in self.workers if w.assigned_task is None]

        for col_idx in range(last_idx - 1, 0, -1):
            if not free_workers:
                break

            st_name = self.states[col_idx]
            max_w = self.col_worker_limits.get(st_name, 2)
            active_w = sum(len(t.assigned_workers) for t in self.tasks if t.state_index == col_idx)

            waiting_in_col = [t for t in self.tasks if t.state_index == col_idx and not t.assigned_workers]
            for task in waiting_in_col:
                if active_w >= max_w:
                    break
                eligible = [w for w in free_workers if self._worker_can_work_in(w, st_name)]
                if not eligible:
                    break
                eligible.sort(key=lambda w: 0 if w.specialty == st_name else 1)
                worker = eligible[0]
                free_workers.remove(worker)
                worker.assigned_task = task
                task.assigned_workers.append(worker)
                active_w += 1

            # Tirer du Backlog vers la 1ère étape active
            if col_idx == 1:
                backlog_tasks = [t for t in self.tasks if t.state_index == 0]
                for task in backlog_tasks:
                    if active_w >= max_w:
                        break
                    eligible = [w for w in free_workers if self._worker_can_work_in(w, st_name)]
                    if not eligible:
                        break
                    eligible.sort(key=lambda w: 0 if w.specialty == st_name else 1)
                    worker = eligible[0]
                    free_workers.remove(worker)

                    task.state_index = 1
                    task.start_day = self.current_day
                    task.progress = 0
                    worker.assigned_task = task
                    task.assigned_workers.append(worker)
                    active_w += 1

        return delivered_today

    def _record_history_snapshot(self, delivered_today: int = 0):
        snap = {"day": self.current_day, "delivered_today": delivered_today}
        for idx, st in enumerate(self.states):
            snap[st] = sum(1 for t in self.tasks if t.state_index == idx)
        if self.history and self.history[-1]["day"] == self.current_day:
            self.history[-1] = snap
        else:
            self.history.append(snap)

    # --- RENDU GLOBAL ---
    def _render_all(self):
        self._refresh_kpis_and_charts()
        self._render_board()

    def _refresh_kpis_and_charts(self):
        total_t = len(self.tasks)
        last_idx = len(self.states) - 1
        done_tasks = [t for t in self.tasks if t.state_index == last_idx]
        wip_tasks = [t for t in self.tasks if 0 < t.state_index < last_idx]

        cur_sprint = min(self.num_sprints, (self.current_day // max(1, self.sprint_duration)) + 1)
        self.kpi_day_val.setText(f"S{cur_sprint}/{self.num_sprints} — J {self.current_day}/{self.total_simulation_days}")
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
            series = [[h.get(st, 0) for h in self.history] for st in ordered_states]
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

            ax.set_ylim(0, max(1, len(self.tasks)))
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
            cum_deliv = [h.get(self.states[-1], 0) for h in self.history]

            bars = ax.bar(days, daily_deliv, width=0.5, color="#EAB308", alpha=0.85, label="Livrées / jour")
            ax2 = ax.twinx()
            line = ax2.plot(days, cum_deliv, color="#16A34A", linewidth=2, marker="o", markersize=3, label="Cumul livré")
            ax2.set_ylim(0, max(1, len(self.tasks)))
            ax2.tick_params(axis="y", labelsize=7, colors="#16A34A")
            ax2.spines["top"].set_visible(False)

            if len(days) == 1:
                ax.set_xlim(-0.5, max(5, self.total_simulation_days))
            ax.set_ylim(0, max(3, max(daily_deliv, default=0) + 1))

            handles = [bars, line[0]]
            labels = ["Livrées / jour", "Cumul livré"]
            ax.legend(handles, labels, loc="upper left", fontsize=7, frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0")

        elif chart_type == "leadtime":
            done_tasks = [t for t in self.tasks if t.state_index == len(self.states) - 1 and t.start_day is not None]
            if done_tasks:
                lts = [max(1, t.end_day - t.start_day) for t in done_tasks]
                unique_lts = sorted(set(lts))
                counts = [lts.count(v) for v in unique_lts]
                bar_cols = ["#16A34A" if v <= 6 else ("#EAB308" if v <= 10 else "#DC2626") for v in unique_lts]
                ax.bar([f"{v}j" for v in unique_lts], counts, width=0.45, color=bar_cols)
                ax.set_ylim(0, max(counts) + 1)
            else:
                ax.text(0.5, 0.5, "En attente des premières livraisons...", ha="center", va="center",
                        fontsize=8.5, color="#94A3B8", transform=ax.transAxes)
                ax.set_xticks([])
                ax.set_yticks([])

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

            for task in col_tasks:
                cards_vbox.addWidget(self._create_task_card(task, state_name, idx, last_idx, is_bottleneck))

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
        lbl_id = QLabel(f"US-{task.id:02d}")
        lbl_id.setStyleSheet("font-size: 10px; font-weight: 800; color: #64748B; background: transparent;")
        top_row.addWidget(lbl_id)

        if task.category_tag:
            lbl_tag = QLabel(task.category_tag)
            lbl_tag.setStyleSheet("""
                background-color: #FFFBEB;
                color: #B45309;
                border: 1px solid #FDE68A;
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