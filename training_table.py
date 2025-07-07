
import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import re
from PIL import Image, ImageTk

POSITIONS = ["LJ", "HJ", "CO", "BTN", "SB", "BB"]

class TrainingTable:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("S'entraîner au préflop")
        self.score, self.errors = 0, 0

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='darkgreen')
        self.canvas.pack(pady=10)

        self.feedback_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.feedback_label.pack()

        self.score_label = tk.Label(self.root, text="Score: 0 | Erreurs: 0", font=("Helvetica", 12, "bold"))
        self.score_label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

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
        self.generate_new_hand()

    def draw_table(self):
        self.canvas.delete("all")
        self.canvas.create_oval(100, 50, 500, 350, outline="white", width=3)

        pos_coords = {
            "LJ": (170, 90),
            "HJ": (300, 60),
            "CO": (430, 90),
            "BTN": (480, 200),
            "SB": (180, 310),
            "BB": (120, 200),
        }

        pos_order = POSITIONS
        cur_idx = pos_order.index(self.current_position)

        for pos, (x, y) in pos_coords.items():
            fill = "yellow" if pos == self.current_position else "white"
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=fill)
            self.canvas.create_text(x, y, text=pos, font=("Helvetica", 10, "bold"))
            if pos_order.index(pos) < cur_idx:
                self.canvas.create_text(x, y + 25, text="Fold", fill="gray", font=("Helvetica", 8))

        # Affiche les infos textuelles
        self.canvas.create_text(300, 180, text=f"Main: {self.current_hand}", fill="white", font=("Helvetica", 14, "bold"))
        self.canvas.create_text(300, 210, text=f"Position: {self.current_position} | Stack: {self.current_bb}BB", fill="white", font=("Helvetica", 10, "italic"))

        # === Affichage des cartes ===
        filenames = self.parse_hand_to_filenames(self.current_hand_image_str)

        self.card_images = []  # très important pour ne pas que les images soient supprimées !

        x_start = 260  # position de la première carte
        for i, filename in enumerate(filenames):
            path = os.path.join("cards_images", filename)
            try:
                # Ouvre l’image avec PIL
                pil_image = Image.open(path)
                # Redimensionne (par exemple 60x90 pixels)
                resized_image = pil_image.resize((50, 80), Image.Resampling.LANCZOS)
                # Convertit en image Tkinter
                tk_image = ImageTk.PhotoImage(resized_image)
                # Stocke l’image pour ne pas qu’elle soit supprimée
                self.card_images.append(tk_image)
                # Affiche l’image
                offset_xy_from_position = {
                                        "LJ": (-60, -45),
                                        "HJ": (-5, -45),
                                        "CO": (130, -27),
                                        "BTN": (150, 90),
                                        "SB": (-50, 150),
                                        "BB": (100, 100),
                                }
                offset_x, offset_y = offset_xy_from_position[self.current_position]
                print(offset_x, offset_y)
                print(self.current_position)
                self.canvas.create_image(x_start + i * 52 + offset_x, 130 + offset_y, image=tk_image, anchor=tk.NW)
            except Exception as e:
                print(f"Erreur chargement image {path} : {e}")

    def generate_new_hand(self):
        self.current_position = random.choice(POSITIONS[:-1])  # enlève la BB
        self.current_data, self.current_position, self.current_bb = self.load_range_for_position(self.current_position)
        self.range_data = self.current_data.get("range_data", {})
        range_key = random.choice(list(self.range_data.keys()))
        self.current_hand = range_key
        self.current_hand_image_str = self.convert_range_hand_to_cards(range_key)
        # Charger et afficher les cartes au centre
        filenames = self.parse_hand_to_filenames(self.current_hand_image_str)
        print(self.current_hand_image_str)

        self.card_images = []  # stocker les références pour éviter la garbage collection

        x_start = 260  # position de la 1re carte
        for i, filename in enumerate(filenames):
            path = os.path.join("cards_images", filename)
            try:
                image = tk.PhotoImage(file=path)
                self.card_images.append(image)
                self.canvas.create_image(x_start + i * 60, 140, image=image, anchor=tk.NW)
            except Exception as e:
                print(f"Erreur chargement image {path} : {e}")

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.draw_table()
        self.feedback_label.config(text="")

        self.current_actions = list(self.current_data.get("labels", {}).keys())

        for action in self.current_actions:
            btn = tk.Button(self.button_frame, text=action.title(), width=15,
                            command=lambda a=action: self.check_answer(a))
            btn.pack(side=tk.LEFT, padx=5)

    def check_answer(self, response):
        current_answer = self.range_data.get(self.current_hand, [])

        correct = response.lower() in [a.lower() for a in current_answer]

        if correct:
            self.score += 1
            self.feedback_label.config(text="Bravo ! Bonne réponse.", fg="green")
        else:
            self.errors += 1
            self.feedback_label.config(text=f"Non ! L'optimale est : {', '.join(current_answer)}", fg="red")

        self.score_label.config(text=f"Score: {self.score} | Erreurs: {self.errors}")

        if self.errors >= 3:
            messagebox.showinfo("Réinitialisation", "Vous avez fait 3 erreurs. Le score est remis à zéro.")
            self.score = 0
            self.errors = 0
            self.score_label.config(text=f"Score: {self.score} | Erreurs: {self.errors}")

        self.root.after(1000, self.generate_new_hand)

    def load_range_for_position(self, position):
        filename = self.range_files[position]
        path = os.path.join(os.getcwd(), filename)
        with open(path, "r") as f:
            data = json.load(f)
        bb = self.extract_bb_from_filename(filename)
        return data, position, bb

    def extract_bb_from_filename(self, filename):
        match = re.search(r'(\d+)bb', filename.lower())
        return int(match.group(1)) if match else 0
    
    def parse_hand_to_filenames(self, hand_str):
        """
        Transforme une string de main (ex : 'AhKs', '8s2d') en 2 noms de fichiers image ['Ah.png', 'Ks.png']
        """
        match = re.findall(r"[AKQJT\d][cdhs]", hand_str, re.IGNORECASE)
        if len(match) != 2:
            print(f"Format de main invalide : {hand_str}")
            return ["back.png", "back.png"]  # fallback si problème
        return [f"{match[0]}.png", f"{match[1]}.png"]
    
    def convert_range_hand_to_cards(self, range_hand):
        """
        Convertit une main style 'K3s' ou 'QJo' en deux cartes concrètes avec couleurs, ex : 'Kh3h' ou 'QsJd'
        """
        ranks = "AKQJT98765432"
        suits = ['c', 'd', 'h', 's']
        
        if len(range_hand) == 2:
            print(f"Pocket pair : {range_hand}")
            suit1, suit2 = random.sample(suits, 2)
            return range_hand[0]+ suit1 + range_hand[1]+ suit2

        if len(range_hand) != 3:
            print(f"Format incorrect : {range_hand}")
            return "AhKs"  # fallback

        r1, r2, suited_flag = range_hand[0], range_hand[1], range_hand[2]

        if suited_flag == 's':
            suit = random.choice(suits)
            card1 = r1 + suit
            card2 = r2 + suit
        elif suited_flag == 'o':
            suit1, suit2 = random.sample(suits, 2)  # deux couleurs différentes
            card1 = r1 + suit1
            card2 = r2 + suit2
        else:
            print(f"Symbole de suited inconnu : {range_hand}")
            return "AhKs"  # fallback

        return card1 + card2  # format ex: "Kh3h"