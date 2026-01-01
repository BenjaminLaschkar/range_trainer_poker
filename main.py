import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import json
import os
from poker_range_editor import PokerRangeEditor 
from training_table import TrainingTable

# Couleurs modernes du thème poker
POKER_GREEN = "#0D5D37"
POKER_DARK_GREEN = "#0A4028"
POKER_LIGHT_GREEN = "#12804D"
GOLD = "#FFD700"
DARK_GOLD = "#CC9900"
BUTTON_BG = "#1E5A3E"
BUTTON_HOVER = "#2A7550"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#FFA500"

def open_json_range():
    """Ouvre un fichier JSON contenant une range de poker"""
    path = filedialog.askopenfilename(
        title="Sélectionner une range",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        initialdir="./ranges"
    )
    if not path:
        return
    try:
        with open(path, "r", encoding='utf-8') as f:
            data = json.load(f)
        new_window = tk.Toplevel()
        new_window.title(data.get("name", "Range Editor"))
        new_window.configure(bg=POKER_GREEN)
        PokerRangeEditor(new_window, data)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier:\n{str(e)}")

def create_new_range():
    """Crée une nouvelle range vide"""
    name = simpledialog.askstring("Nouvelle Range", "Nom de la range :", parent=tk._default_root)
    if not name:
        return
    data = {"name": name, "labels": {}, "range_data": {}}
    new_window = tk.Toplevel()
    new_window.title(f"Éditeur - {name}")
    new_window.configure(bg=POKER_GREEN)
    PokerRangeEditor(new_window, data)

def train_preflop():
    """Lance le mode entraînement"""
    TrainingTable(tk._default_root)

class HoverButton(tk.Button):
    """Bouton avec effet de survol amélioré"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = BUTTON_HOVER

    def on_leave(self, e):
        self['background'] = self.defaultBackground

def launch_main_app():
    """Lance l'application principale avec interface modernisée"""
    root = tk.Tk()
    root.title("♠️ Poker Range Trainer Pro ♠️")
    root.geometry("600x500")
    root.configure(bg=POKER_GREEN)
    root.resizable(False, False)

    # En-tête stylisé
    header_frame = tk.Frame(root, bg=POKER_DARK_GREEN, height=100)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = tk.Label(
        header_frame,
        text="♠️♥️ POKER RANGE TRAINER ♣️♦️",
        font=("Arial Black", 24, "bold"),
        bg=POKER_DARK_GREEN,
        fg=GOLD
    )
    title_label.pack(pady=20)
    
    subtitle_label = tk.Label(
        header_frame,
        text="Maîtrisez vos ranges preflop comme un pro",
        font=("Arial", 12, "italic"),
        bg=POKER_DARK_GREEN,
        fg=TEXT_COLOR
    )
    subtitle_label.pack()

    # Frame principal pour les boutons
    main_frame = tk.Frame(root, bg=POKER_GREEN)
    main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

    # Boutons d'action stylisés
    buttons_data = [
        ("🎓 S'entraîner au Préflop", train_preflop, "Testez vos connaissances avec des mains aléatoires"),
        ("📊 Créer une Nouvelle Range", create_new_range, "Créez et personnalisez vos propres ranges"),
        ("📂 Ouvrir une Range Existante", open_json_range, "Éditez une range depuis un fichier JSON"),
    ]

    for text, command, tooltip in buttons_data:
        btn_frame = tk.Frame(main_frame, bg=POKER_GREEN)
        btn_frame.pack(pady=12, fill=tk.X)
        
        btn = HoverButton(
            btn_frame,
            text=text,
            command=command,
            font=("Arial", 14, "bold"),
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_COLOR,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            height=2
        )
        btn.pack(fill=tk.X, ipady=5)
        
        # Tooltip
        tooltip_label = tk.Label(
            btn_frame,
            text=tooltip,
            font=("Arial", 9, "italic"),
            bg=POKER_GREEN,
            fg=GOLD
        )
        tooltip_label.pack()

    # Séparateur
    separator = tk.Frame(main_frame, height=2, bg=GOLD)
    separator.pack(fill=tk.X, pady=20)

    # Bouton quitter
    quit_btn = HoverButton(
        main_frame,
        text="❌ Quitter",
        command=root.quit,
        font=("Arial", 12, "bold"),
        bg=POKER_DARK_GREEN,
        fg=TEXT_COLOR,
        activebackground="#8B0000",
        activeforeground=TEXT_COLOR,
        relief=tk.RAISED,
        bd=2,
        cursor="hand2"
    )
    quit_btn.pack(pady=10, ipady=5, ipadx=20)

    # Footer
    footer_label = tk.Label(
        root,
        text="© 2026 Poker Range Trainer | v2.0",
        font=("Arial", 9),
        bg=POKER_GREEN,
        fg=GOLD
    )
    footer_label.pack(side=tk.BOTTOM, pady=10)

    # Centrer la fenêtre
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()

if __name__ == "__main__":
    launch_main_app()