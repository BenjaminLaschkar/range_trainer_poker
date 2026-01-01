# ♠️♥️ Poker Range Trainer Pro ♣️♦️

<div align="center">

![Poker](https://img.shields.io/badge/Poker-Range_Trainer-success?style=for-the-badge&logo=spades)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Maîtrisez vos ranges preflop comme un pro !**

Un outil d'entraînement et de gestion de ranges poker avec interface graphique moderne.

</div>

---

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Captures d'écran](#-captures-décran)
- [Structure du Projet](#-structure-du-projet)
- [Ranges GTO Incluses](#-ranges-gto-incluses)
- [Contribuer](#-contribuer)
- [License](#-license)

---

## ✨ Fonctionnalités

### 🎯 Mode Entraînement
- **Entraînement interactif** avec des mains aléatoires
- **Statistiques détaillées** : précision, série, temps écoulé
- **Visualisation de la table** avec positions et cartes
- **Feedback immédiat** sur vos réponses
- **Système de séries** pour suivre votre progression

### 📊 Éditeur de Ranges
- **Interface visuelle intuitive** avec grille 13x13
- **Création d'étiquettes personnalisées** avec couleurs
- **Support multi-étiquettes** pour stratégies complexes
- **Undo/Redo** pour annuler/refaire vos modifications
- **Statistiques en temps réel** : combos, pourcentages
- **Raccourcis clavier** : Ctrl+S (sauvegarder), Ctrl+Z (undo), Ctrl+Y (redo)
- **Double-clic** pour voir tous les combos d'une main
- **Export/Import JSON** pour partager vos ranges

### 🎨 Interface Moderne
- **Design professionnel** aux couleurs poker
- **Animations fluides** et effets de survol
- **Tooltips informatifs** sur tous les boutons
- **Theme vert poker** apaisant pour les yeux

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/BenjaminLaschkar/range_trainer_poker.git
cd range_trainer_poker
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
python main.py
```

Ou sous Windows, double-cliquez sur `start.bat`

---

## 📖 Utilisation

### Démarrage Rapide

1. **Lancez l'application** avec `python main.py`
2. Choisissez une option :
   - 🎓 **S'entraîner au Préflop** : Testez vos connaissances
   - 📊 **Créer une Range** : Créez votre propre range
   - 📂 **Ouvrir une Range** : Éditez une range existante

### Mode Entraînement

1. Une main et une position vous sont présentées
2. Choisissez l'action optimale parmi les boutons
3. Recevez un feedback immédiat
4. Consultez vos statistiques en temps réel
5. Après 3 erreurs, le score se réinitialise

**Raccourcis** :
- Cliquez sur un bouton d'action pour répondre
- 📊 **Voir Statistiques** : Affiche vos stats détaillées
- 🔄 **Réinitialiser** : Recommence à zéro

### Éditeur de Ranges

1. **Créer des Étiquettes** : Cliquez sur "➕ Créer Étiquette"
   - Donnez un nom (ex: "Open", "Fold", "3-Bet")
   - Choisissez une couleur

2. **Assigner des Mains** :
   - Sélectionnez une étiquette dans le menu déroulant
   - Clic gauche sur une main pour l'ajouter
   - Clic droit pour supprimer toutes les étiquettes
   - Double-clic pour voir les combos

3. **Sauvegarder** : Ctrl+S ou bouton "💾 Sauvegarder"

**Astuces** :
- Les paires sont en **rouge** sur la diagonale
- Les mains **suited** sont en **bleu** (au-dessus de la diagonale)
- Les mains **offsuit** sont en **noir** (en-dessous)
- Le compteur affiche le % de votre range en temps réel

---

## 📸 Captures d'écran

### Menu Principal
```
┌─────────────────────────────────────┐
│  ♠️♥️ POKER RANGE TRAINER ♣️♦️     │
│  Maîtrisez vos ranges preflop     │
├─────────────────────────────────────┤
│  🎓 S'entraîner au Préflop        │
│  📊 Créer une Nouvelle Range       │
│  📂 Ouvrir une Range Existante     │
│  ❌ Quitter                         │
└─────────────────────────────────────┘
```

### Mode Entraînement
- Table de poker avec positions animées
- Cartes affichées à la position du joueur
- Statistiques en temps réel (score, série, précision)
- Boutons d'action colorés selon la stratégie

### Éditeur de Ranges
- Grille 13x13 interactive
- Légende avec toutes vos étiquettes
- Statistiques : nombre de mains, combos, pourcentage
- Instructions d'utilisation en bas

---

## 📁 Structure du Projet

```
range_trainer_poker/
├── main.py                 # Point d'entrée de l'application
├── poker_range_editor.py   # Éditeur de ranges
├── training_table.py       # Mode entraînement
├── fix_ranges.py          # Script de correction des ranges
├── requirements.txt        # Dépendances Python
├── README.md              # Ce fichier
├── ranges/                # Fichiers de ranges GTO
│   ├── open_LJ_40BB.json
│   ├── open_HJ_40BB.json
│   ├── open_CO_40BB.json
│   ├── open_BTN_40BB.json
│   └── open_SB_40BB.json
└── cards_images/          # Images des cartes (52 cartes)
    ├── 2c.png ... As.png
    └── ...
```

---

## 🎲 Ranges GTO Incluses

Le projet inclut 5 ranges d'ouverture optimisées pour 40BB :

| Position | Range | Tightness | Combos approx. |
|----------|-------|-----------|----------------|
| **LJ** (Lojack) | 15-17% | Serré | ~200 combos |
| **HJ** (Hijack) | 18-20% | Moyen-Serré | ~240 combos |
| **CO** (Cutoff) | 24-26% | Moyen | ~320 combos |
| **BTN** (Button) | 45-48% | Large | ~600 combos |
| **SB** (Small Blind) | Mixte RFI/Limp | Complexe | Variable |

### Caractéristiques des Ranges

- **Basées sur la théorie GTO moderne** (2025-2026)
- **Optimisées pour 40BB** de profondeur de tapis
- **Catégories** :
  - `Open` : Mains à ouvrir systématiquement
  - `Open (Mix)` : Mains à mixer (randomiser)
  - `Fold` : Mains à folder
  - SB spécial : `RFI`, `Limp`, et variantes

---

## 🛠️ Technologies Utilisées

- **Python 3.8+** : Langage principal
- **Tkinter** : Interface graphique
- **Pillow (PIL)** : Traitement d'images pour les cartes
- **JSON** : Stockage des ranges

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Idées de Fonctionnalités

- [ ] Support des ranges postflop
- [ ] Mode multijoueur en ligne
- [ ] Import de ranges depuis des solvers (PioSolver, GTO+)
- [ ] Graphiques de progression
- [ ] Support de différentes profondeurs de tapis (20BB, 100BB, etc.)
- [ ] Traduction multilingue

---

## 📝 License

Distribué sous license MIT. Voir `LICENSE` pour plus d'informations.

---

## 👤 Auteur

**Benjamin Laschkar**
- GitHub: [@BenjaminLaschkar](https://github.com/BenjaminLaschkar)

---

## 🙏 Remerciements

- Communauté poker pour les stratégies GTO
- Contributeurs du projet
- Tous les joueurs de poker qui utilisent cet outil

---

<div align="center">

**Fait avec ❤️ pour la communauté poker**

⭐ N'oubliez pas de star le projet si vous le trouvez utile !

</div>
