
import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import re
import time
from PIL import Image, ImageTk

POSITIONS = ["LJ", "HJ", "CO", "BTN", "SB", "BB"]

# Couleurs du thème
POKER_GREEN = "#0D5D37"
POKER_DARK_GREEN = "#0A4028"
GOLD = "#FFD700"
TEXT_COLOR = "#FFFFFF"
BUTTON_BG = "#1E5A3E"

class TrainingTable:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("♠️ Entraînement Préflop ♠️")
        self.root.configure(bg=POKER_GREEN)
        self.root.geometry("900x700")
        
        # Statistiques
        self.score = 0
        self.errors = 0
        self.streak = 0
        self.best_streak = 0
        self.total_questions = 0
        self.start_time = time.time()
        self.question_times = []

        # En-tête avec statistiques
        header_frame = tk.Frame(self.root, bg=POKER_DARK_GREEN, relief=tk.RIDGE, bd=3)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        title = tk.Label(
            header_frame,
            text="🎯 MODE ENTRAÎNEMENT PRÉFLOP 🎯",
            font=("Arial Black", 18, "bold"),
            bg=POKER_DARK_GREEN,
            fg=GOLD
        )
        title.pack(pady=10)

        # Frame des statistiques
        stats_frame = tk.Frame(header_frame, bg=POKER_DARK_GREEN)
        stats_frame.pack(pady=5)

        self.score_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg=POKER_DARK_GREEN,
            fg=TEXT_COLOR
        )
        self.score_label.pack(side=tk.LEFT, padx=15)

        self.streak_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg=POKER_DARK_GREEN,
            fg=GOLD
        )
        self.streak_label.pack(side=tk.LEFT, padx=15)

        self.accuracy_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 12, "bold"),
            bg=POKER_DARK_GREEN,
            fg="#4ECDC4"
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=15)

        # Canvas pour la table de poker
        canvas_frame = tk.Frame(self.root, bg=POKER_GREEN, relief=tk.SUNKEN, bd=3)
        canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=700,
            height=450,
            bg='#1a5c3f',
            highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)

        # Zone de feedback
        self.feedback_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 13, "bold"),
            bg=POKER_GREEN,
            height=2
        )
        self.feedback_label.pack(pady=5)

        # Frame pour les boutons d'action
        self.button_frame = tk.Frame(self.root, bg=POKER_GREEN)
        self.button_frame.pack(pady=15)

        # Boutons utilitaires
        utils_frame = tk.Frame(self.root, bg=POKER_GREEN)
        utils_frame.pack(pady=5)

        tk.Button(
            utils_frame,
            text="📊 Voir Statistiques",
            command=self.show_statistics,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            utils_frame,
            text="🔄 Réinitialiser",
            command=self.reset_stats,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            utils_frame,
            text="❌ Fermer",
            command=self.root.destroy,
            bg=POKER_DARK_GREEN,
            fg="#FF6B6B",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        # Initialisation des données
        self.positions = POSITIONS.copy()
        self.range_files = {
            "LJ": "ranges/open_LJ_40BB.json",
            "HJ": "ranges/open_HJ_40BB.json",
            "CO": "ranges/open_CO_40BB.json",
            "BTN": "ranges/open_BTN_40BB.json",
            "SB": "ranges/open_SB_40BB.json"
        }
        
        self.current_data = {}
        self.current_hand = ""
        self.current_hand_image_str = ""
        self.current_position = ""
        self.current_bb = 0
        self.card_images = []
        
        self.update_score_display()
        self.generate_new_hand()

    def draw_table(self):
        """Dessine la table de poker avec positions et cartes"""
        self.canvas.delete("all")
        
        # Table elliptique
        self.canvas.create_oval(
            80, 80, 620, 370,
            outline=GOLD,
            width=4,
            fill='#0a3d25'
        )
        
        # Positions des joueurs sur la table
        pos_coords = {
            "LJ": (190, 130),
            "HJ": (350, 90),
            "CO": (510, 130),
            "BTN": (580, 225),
            "SB": (200, 330),
            "BB": (130, 225),
        }

        pos_order = POSITIONS
        cur_idx = pos_order.index(self.current_position)

        # Dessiner les positions
        for pos, (x, y) in pos_coords.items():
            is_current = (pos == self.current_position)
            has_folded = pos_order.index(pos) < cur_idx
            
            # Cercle de position
            fill_color = GOLD if is_current else "#2d5f3f" if has_folded else "#4a7c59"
            outline_color = "#FFD700" if is_current else "#666"
            
            self.canvas.create_oval(
                x - 30, y - 30, x + 30, y + 30,
                fill=fill_color,
                outline=outline_color,
                width=3 if is_current else 2
            )
            
            # Texte de position
            text_color = "black" if is_current else "white"
            self.canvas.create_text(
                x, y - 5,
                text=pos,
                font=("Arial Black", 12, "bold"),
                fill=text_color
            )
            
            # Indicateur de fold
            if has_folded:
                self.canvas.create_text(
                    x, y + 10,
                    text="FOLD",
                    fill="#999",
                    font=("Arial", 8, "bold")
                )

        # Affichage des cartes
        filenames = self.parse_hand_to_filenames(self.current_hand_image_str)
        self.card_images = []

        offset_xy_from_position = {
            "LJ": (160, 100),
            "HJ": (320, 60),
            "CO": (480, 100),
            "BTN": (550, 195),
            "SB": (170, 300),
            "BB": (100, 195),
        }
        
        offset_x, offset_y = offset_xy_from_position[self.current_position]
        
        for i, filename in enumerate(filenames):
            path = os.path.join("cards_images", filename)
            try:
                pil_image = Image.open(path)
                resized_image = pil_image.resize((55, 85), Image.Resampling.LANCZOS)
                tk_image = ImageTk.PhotoImage(resized_image)
                self.card_images.append(tk_image)
                
                # Rotation légère pour effet dynamique
                self.canvas.create_image(
                    offset_x + i * 58,
                    offset_y,
                    image=tk_image,
                    anchor=tk.NW
                )
            except Exception as e:
                print(f"Erreur chargement image {path} : {e}")

        # Panneau d'informations au centre
        self.canvas.create_rectangle(
            250, 200, 450, 250,
            fill="#1a1a1a",
            outline=GOLD,
            width=2
        )
        
        self.canvas.create_text(
            350, 215,
            text=f"Main: {self.current_hand}",
            fill=GOLD,
            font=("Arial Black", 14, "bold")
        )
        
        self.canvas.create_text(
            350, 235,
            text=f"{self.current_position} - {self.current_bb}BB",
            fill="white",
            font=("Arial", 11, "italic")
        )

    def generate_new_hand(self):
        """Génère une nouvelle main pour l'entraînement"""
        self.current_position = random.choice(POSITIONS[:-1])  # Sans BB
        self.current_data, self.current_position, self.current_bb = self.load_range_for_position(self.current_position)
        self.range_data = self.current_data.get("range_data", {})
        
        if not self.range_data:
            messagebox.showerror("Erreur", f"Aucune donnée trouvée pour {self.current_position}")
            return
            
        range_key = random.choice(list(self.range_data.keys()))
        self.current_hand = range_key
        self.current_hand_image_str = self.convert_range_hand_to_cards(range_key)

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.draw_table()
        self.feedback_label.config(text="Quelle est la meilleure action?", fg=TEXT_COLOR)

        self.current_actions = list(self.current_data.get("labels", {}).keys())

        # Créer les boutons d'action
        for i, action in enumerate(self.current_actions):
            color = self.current_data.get("labels", {}).get(action, BUTTON_BG)
            btn = tk.Button(
                self.button_frame,
                text=action.upper(),
                width=18,
                height=2,
                command=lambda a=action: self.check_answer(a),
                bg=color,
                fg="black" if self._is_light_color(color) else "white",
                font=("Arial", 11, "bold"),
                cursor="hand2",
                relief=tk.RAISED,
                bd=3
            )
            btn.grid(row=i//3, column=i%3, padx=8, pady=5)

    def _is_light_color(self, color):
        """Détermine si une couleur est claire"""
        try:
            color = color.lstrip('#')
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b)
            return luminance > 128
        except:
            return False

    def check_answer(self, response):
        """Vérifie la réponse du joueur"""
        self.total_questions += 1
        current_answer = self.range_data.get(self.current_hand, [])

        correct = response.lower() in [a.lower() for a in current_answer]

        if correct:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            self.feedback_label.config(
                text=f"✅ CORRECT! {response}",
                fg="#2ECC71"
            )
        else:
            self.errors += 1
            self.streak = 0
            correct_actions = ', '.join(current_answer)
            self.feedback_label.config(
                text=f"❌ INCORRECT! La bonne réponse: {correct_actions}",
                fg="#E74C3C"
            )

        self.update_score_display()

        if self.errors >= 3:
            messagebox.showwarning(
                "Attention",
                f"3 erreurs! Score réinitialisé.\n\nDernière série: {self.streak}",
                parent=self.root
            )
            self.score = 0
            self.errors = 0
            self.streak = 0

        self.root.after(1500, self.generate_new_hand)

    def update_score_display(self):
        """Met à jour l'affichage des statistiques"""
        accuracy = (self.score / self.total_questions * 100) if self.total_questions > 0 else 0
        
        self.score_label.config(
            text=f"✓ Score: {self.score} | ✗ Erreurs: {self.errors}"
        )
        
        streak_text = f"🔥 Série: {self.streak}"
        if self.streak >= 5:
            streak_text += " 🏆"
        self.streak_label.config(text=streak_text)
        
        self.accuracy_label.config(
            text=f"📈 Précision: {accuracy:.1f}% ({self.score}/{self.total_questions})"
        )

    def show_statistics(self):
        """Affiche les statistiques détaillées"""
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        stats_text = f"""
═══════════════════════════
    STATISTIQUES DE SESSION
═══════════════════════════

✅ Bonnes réponses: {self.score}
❌ Mauvaises réponses: {self.errors}
📊 Total de questions: {self.total_questions}

🎯 Précision: {(self.score/self.total_questions*100) if self.total_questions > 0 else 0:.1f}%

🔥 Série actuelle: {self.streak}
🏆 Meilleure série: {self.best_streak}

⏱️ Temps écoulé: {minutes}m {seconds}s

═══════════════════════════
        """
        
        messagebox.showinfo("Statistiques", stats_text, parent=self.root)

    def reset_stats(self):
        """Réinitialise les statistiques"""
        confirm = messagebox.askyesno(
            "Confirmation",
            "Réinitialiser toutes les statistiques?",
            parent=self.root
        )
        if confirm:
            self.score = 0
            self.errors = 0
            self.streak = 0
            self.best_streak = 0
            self.total_questions = 0
            self.start_time = time.time()
            self.question_times = []
            self.update_score_display()
            self.generate_new_hand()

    def load_range_for_position(self, position):
        """Charge les données de range pour une position"""
        filename = self.range_files[position]
        path = os.path.join(os.getcwd(), filename)
        try:
            with open(path, "r", encoding='utf-8') as f:
                data = json.load(f)
            bb = self.extract_bb_from_filename(filename)
            return data, position, bb
        except Exception as e:
            print(f"Erreur lors du chargement de {filename}: {e}")
            return {"labels": {}, "range_data": {}}, position, 40

    def extract_bb_from_filename(self, filename):
        """Extrait le nombre de BB du nom de fichier"""
        match = re.search(r'(\d+)bb', filename.lower())
        return int(match.group(1)) if match else 40
    
    def parse_hand_to_filenames(self, hand_str):
        """Transforme une main en noms de fichiers d'images"""
        match = re.findall(r"[AKQJT\d][cdhs]", hand_str, re.IGNORECASE)
        if len(match) != 2:
            return ["2c.png", "2d.png"]  # Fallback
        return [f"{match[0]}.png", f"{match[1]}.png"]
    
    def convert_range_hand_to_cards(self, range_hand):
        """Convertit une main de range en cartes concrètes"""
        suits = ['c', 'd', 'h', 's']
        
        if len(range_hand) == 2:  # Pocket pair
            suit1, suit2 = random.sample(suits, 2)
            return range_hand[0] + suit1 + range_hand[1] + suit2

        if len(range_hand) != 3:
            return "AhKs"  # Fallback

        r1, r2, suited_flag = range_hand[0], range_hand[1], range_hand[2]

        if suited_flag == 's':
            suit = random.choice(suits)
            return r1 + suit + r2 + suit
        elif suited_flag == 'o':
            suit1, suit2 = random.sample(suits, 2)
            return r1 + suit1 + r2 + suit2
        else:
            return "AhKs"  # Fallback
