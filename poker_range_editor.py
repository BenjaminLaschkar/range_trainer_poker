
import tkinter as tk
from tkinter import filedialog, Menu, simpledialog, colorchooser, messagebox
import json

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# Couleurs du thème
POKER_GREEN = "#0D5D37"
POKER_DARK_GREEN = "#0A4028"
GOLD = "#FFD700"
TEXT_COLOR = "#FFFFFF"

class PokerRangeEditor:
    def __init__(self, root, data=None):
        self.root = root
        self.root.title("Éditeur de Range Poker")
        self.root.configure(bg=POKER_GREEN)
        self.data = data or {"name": "Nouvelle range", "labels": {}, "range_data": {}}

        self.labels = self.data["labels"]
        self.range_data = {hand: list(lbls) for hand, lbls in self.data["range_data"].items()}
        self.current_label = None
        self.history = []  # Pour undo/redo
        self.history_index = -1

        # En-tête
        top_frame = tk.Frame(root, bg=POKER_DARK_GREEN)
        top_frame.pack(pady=10, fill=tk.X)

        self.title_label = tk.Label(
            top_frame, 
            text=self.data["name"], 
            font=("Arial Black", 16, "bold"),
            bg=POKER_DARK_GREEN,
            fg=GOLD
        )
        self.title_label.pack(pady=5)

        # Frame de contrôle
        control_frame = tk.Frame(root, bg=POKER_GREEN)
        control_frame.pack(pady=10, fill=tk.X, padx=10)

        # Sélection d'étiquette
        label_frame = tk.LabelFrame(
            control_frame,
            text="Étiquette Actuelle",
            font=("Arial", 10, "bold"),
            bg=POKER_GREEN,
            fg=GOLD,
            bd=2
        )
        label_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.label_var = tk.StringVar()
        initial_label = next(iter(self.labels), "")
        self.label_var.set(initial_label)
        self.label_menu = tk.OptionMenu(label_frame, self.label_var, initial_label, *self.labels.keys())
        self.label_menu.config(bg=POKER_DARK_GREEN, fg=TEXT_COLOR, font=("Arial", 10))
        self.label_menu.pack(padx=5, pady=5)

        # Max étiquettes
        max_frame = tk.LabelFrame(
            control_frame,
            text="Max Étiquettes/Main",
            font=("Arial", 10, "bold"),
            bg=POKER_GREEN,
            fg=GOLD,
            bd=2
        )
        max_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.max_label_var = tk.IntVar(value=2)
        tk.OptionMenu(max_frame, self.max_label_var, 1, 2, 3, 4, 5).pack(padx=5, pady=5)

        # Boutons d'action
        action_frame = tk.Frame(control_frame, bg=POKER_GREEN)
        action_frame.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        tk.Button(
            action_frame,
            text="➕ Créer Étiquette",
            command=self.create_label,
            bg=POKER_DARK_GREEN,
            fg=TEXT_COLOR,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            action_frame,
            text="💾 Sauvegarder",
            command=self.save_range,
            bg=POKER_DARK_GREEN,
            fg=GOLD,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        ).pack(side=tk.LEFT, padx=3)

        tk.Button(
            action_frame,
            text="🔄 Réinitialiser",
            command=self.clear_all,
            bg=POKER_DARK_GREEN,
            fg="#FF6B6B",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        ).pack(side=tk.LEFT, padx=3)

        # Statistiques
        stats_frame = tk.Frame(control_frame, bg=POKER_GREEN)
        stats_frame.pack(side=tk.RIGHT, padx=10)

        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg=POKER_GREEN,
            fg=GOLD
        )
        self.stats_label.pack()

        # Frame principal avec canvas et légende
        content_frame = tk.Frame(root, bg=POKER_GREEN)
        content_frame.pack(padx=10, pady=10)

        # Canvas pour la grille
        canvas_frame = tk.LabelFrame(
            content_frame,
            text="Grille des Mains Preflop",
            font=("Arial", 11, "bold"),
            bg=POKER_GREEN,
            fg=GOLD,
            bd=3
        )
        canvas_frame.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=670,
            height=670,
            bg="#1a5c3f",
            highlightthickness=2,
            highlightbackground=GOLD
        )
        self.canvas.pack(padx=5, pady=5)

        # Légende
        legend_outer = tk.LabelFrame(
            content_frame,
            text="Légende des Étiquettes",
            font=("Arial", 11, "bold"),
            bg=POKER_GREEN,
            fg=GOLD,
            bd=3
        )
        legend_outer.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH)

        self.legend_frame = tk.Frame(legend_outer, bg=POKER_GREEN)
        self.legend_frame.pack(padx=10, pady=10, anchor='n')

        # Instructions
        info_frame = tk.Frame(root, bg=POKER_DARK_GREEN, relief=tk.RIDGE, bd=2)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        instructions = tk.Label(
            info_frame,
            text="🖱️ Clic gauche: Ajouter l'étiquette | Clic droit: Supprimer | Double-clic: Voir les combos",
            font=("Arial", 9, "italic"),
            bg=POKER_DARK_GREEN,
            fg=TEXT_COLOR
        )
        instructions.pack(pady=5)

        self.grid = {}
        self.draw_grid()
        self.update_legend()
        self.update_stats()

        # Bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)

        # Raccourcis clavier
        self.root.bind("<Control-s>", lambda e: self.save_range())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())


    def get_hand_label(self, r1, r2, suited):
        """Génère le label d'une main (ex: AKs, 77, QJo)"""
        r1_index = RANKS.index(r1)
        r2_index = RANKS.index(r2)
        if r1_index < r2_index:
            r1, r2 = r2, r1
        if r1 == r2:
            return f"{r1}{r2}"
        return f"{r1}{r2}{suited}" if suited else f"{r1}{r2}"

    def draw_grid(self):
        """Dessine la grille de range 13x13"""
        size = 50
        padding = 5
        
        # En-têtes des colonnes (suited)
        for j, rank in enumerate(RANKS):
            x = j * size + padding + size/2
            self.canvas.create_text(
                x, padding - 2,
                text=rank,
                font=("Arial Black", 10, "bold"),
                fill=GOLD
            )
        
        # En-têtes des lignes (offsuit)
        for i, rank in enumerate(RANKS):
            y = i * size + padding + size/2
            self.canvas.create_text(
                padding - 2, y,
                text=rank,
                font=("Arial Black", 10, "bold"),
                fill=GOLD
            )
        
        for i, r1 in enumerate(RANKS):
            for j, r2 in enumerate(RANKS):
                if i == j:
                    hand = f"{r1}{r2}"  # paires
                elif i < j:
                    hand = f"{r1}{r2}s"  # suited
                else:
                    hand = f"{r2}{r1}o"  # offsuit
                
                x = j * size + padding
                y = i * size + padding
                
                # Bordure plus marquée
                rect = self.canvas.create_rectangle(
                    x, y, x+size, y+size,
                    fill='white',
                    outline='#2d2d2d',
                    width=1,
                    tags=hand
                )
                
                # Texte avec couleur selon le type
                text_color = "red" if i == j else "blue" if i < j else "black"
                text = self.canvas.create_text(
                    x+size/2, y+size/2,
                    text=hand,
                    font=("Arial", 9, "bold"),
                    fill=text_color,
                    tags=hand
                )
                
                self.grid[hand] = (rect, text, x, y)
        
        self.update_grid_display()

    def update_grid_display(self):
        """Met à jour l'affichage de la grille selon les étiquettes"""
        for hand, (rect, text, x, y) in self.grid.items():
            labels = self.range_data.get(hand, [])
            self.canvas.delete("overlay_" + hand)
            self.canvas.itemconfig(text, state='normal')
            
            if len(labels) == 0:
                self.canvas.itemconfig(rect, fill="white")
            elif len(labels) == 1:
                color = self.labels.get(labels[0], "grey")
                self.canvas.itemconfig(rect, fill=color)
            elif len(labels) >= 2:
                self.canvas.itemconfig(rect, fill="white")
                size = 50
                section_width = size / len(labels)
                for idx, lbl in enumerate(labels):
                    color = self.labels.get(lbl, "grey")
                    self.canvas.create_rectangle(
                        x + idx * section_width, y,
                        x + (idx + 1) * section_width, y + size,
                        fill=color,
                        outline='',
                        tags=("overlay_" + hand)
                    )
            
            if labels:
                self.canvas.tag_raise(text)
        
        self.update_stats()

    def update_stats(self):
        """Met à jour les statistiques de la range"""
        total_hands = sum(len(self.range_data.get(hand, [])) > 0 for hand in self.range_data)
        total_combos = self.count_combos()
        percentage = (total_combos / 1326) * 100 if total_combos > 0 else 0
        
        self.stats_label.config(
            text=f"📊 Mains: {total_hands} | Combos: {total_combos}/1326 ({percentage:.1f}%)"
        )

    def count_combos(self):
        """Compte le nombre total de combinaisons dans la range"""
        total = 0
        for hand in self.range_data:
            if self.range_data[hand]:  # Si la main a au moins une étiquette
                if len(hand) == 2:  # Paire (ex: AA)
                    total += 6
                elif hand.endswith('s'):  # Suited
                    total += 4
                elif hand.endswith('o'):  # Offsuit
                    total += 12
        return total

    def create_label(self):
        """Crée une nouvelle étiquette avec nom et couleur"""
        name = simpledialog.askstring("Nouvelle Étiquette", "Nom de l'étiquette :", parent=self.root)
        if not name:
            return
        if name in self.labels:
            messagebox.showwarning("Attention", f"L'étiquette '{name}' existe déjà!")
            return
        
        color = colorchooser.askcolor(title="Choisissez une couleur", parent=self.root)[1]
        if not color:
            return
        
        self.labels[name] = color
        self.update_label_menu()
        self.update_legend()
        self.save_state()

    def update_label_menu(self):
        """Met à jour le menu déroulant des étiquettes"""
        menu = self.label_menu["menu"]
        menu.delete(0, "end")
        for label in self.labels:
            menu.add_command(label=label, command=lambda l=label: self.label_var.set(l))

    def update_legend(self):
        """Actualise la légende des étiquettes"""
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        
        if not self.labels:
            tk.Label(
                self.legend_frame,
                text="Aucune étiquette",
                font=("Arial", 10, "italic"),
                bg=POKER_GREEN,
                fg=TEXT_COLOR
            ).pack()
            return
        
        for label, color in self.labels.items():
            frame = tk.Frame(self.legend_frame, bg=POKER_GREEN)
            frame.pack(anchor='w', pady=3, fill=tk.X)
            
            color_box = tk.Label(
                frame,
                text=label,
                bg=color,
                fg="black" if self._is_light_color(color) else "white",
                width=15,
                font=("Arial", 9, "bold"),
                relief=tk.RAISED,
                bd=2
            )
            color_box.pack(side=tk.LEFT, padx=2)
            
            tk.Button(
                frame,
                text="✏️",
                command=lambda l=label: self.rename_label(l),
                bg=POKER_DARK_GREEN,
                fg=GOLD,
                cursor="hand2",
                width=2
            ).pack(side=tk.LEFT, padx=1)
            
            tk.Button(
                frame,
                text="🗑️",
                command=lambda l=label: self.delete_label(l),
                bg=POKER_DARK_GREEN,
                fg="#FF6B6B",
                cursor="hand2",
                width=2
            ).pack(side=tk.LEFT, padx=1)

    def _is_light_color(self, color):
        """Détermine si une couleur est claire ou foncée"""
        try:
            color = color.lstrip('#')
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b)
            return luminance > 128
        except:
            return False

    def rename_label(self, label):
        """Renomme une étiquette existante"""
        new_name = simpledialog.askstring(
            "Renommer",
            f"Nouveau nom pour '{label}' :",
            parent=self.root
        )
        if not new_name or new_name == label:
            return
        if new_name in self.labels:
            messagebox.showwarning("Attention", f"L'étiquette '{new_name}' existe déjà!")
            return
        
        self.labels[new_name] = self.labels.pop(label)
        for hand in self.range_data:
            self.range_data[hand] = [new_name if l == label else l for l in self.range_data[hand]]
        
        self.update_label_menu()
        self.update_legend()
        self.update_grid_display()
        self.save_state()

    def delete_label(self, label):
        """Supprime une étiquette et toutes ses occurrences"""
        confirm = messagebox.askyesno(
            "Confirmation",
            f"Supprimer l'étiquette '{label}' ?\nToutes les mains associées seront affectées.",
            parent=self.root
        )
        if not confirm:
            return
        
        if label in self.labels:
            del self.labels[label]
        
        for hand in list(self.range_data):
            if label in self.range_data[hand]:
                self.range_data[hand].remove(label)
            if not self.range_data[hand]:
                del self.range_data[hand]
        
        self.update_label_menu()
        self.update_legend()
        self.update_grid_display()
        self.save_state()

    def on_click(self, event):
        """Gère le clic gauche pour ajouter une étiquette"""
        if not self.label_var.get():
            messagebox.showinfo("Info", "Veuillez d'abord créer et sélectionner une étiquette!")
            return
        
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)
        if items:
            tags = self.canvas.gettags(items[0])
            if not tags:
                return
            hand = tags[0]
            if hand.startswith("overlay"):
                return
                
            labels = self.range_data.get(hand, [])
            label_to_add = self.label_var.get()
            
            if label_to_add not in labels:
                max_labels = self.max_label_var.get()
                if len(labels) >= max_labels:
                    labels.pop(0)
                labels.append(label_to_add)
                self.range_data[hand] = labels
                self.save_state()
            
            self.update_grid_display()

    def on_right_click(self, event):
        """Gère le clic droit pour supprimer toutes les étiquettes d'une main"""
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)
        if items:
            tags = self.canvas.gettags(items[0])
            if not tags:
                return
            hand = tags[0]
            if hand.startswith("overlay"):
                return
                
            if hand in self.range_data:
                self.range_data[hand].clear()
                self.update_grid_display()
                self.save_state()

    def on_double_click(self, event):
        """Gère le double-clic pour afficher les combos d'une main"""
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)
        if items:
            tags = self.canvas.gettags(items[0])
            if not tags:
                return
            hand = tags[0]
            if hand.startswith("overlay"):
                return
            
            combos = self.get_hand_combos(hand)
            labels = self.range_data.get(hand, [])
            
            info = f"Main: {hand}\n"
            info += f"Combinaisons: {len(combos)}\n"
            info += f"Étiquettes: {', '.join(labels) if labels else 'Aucune'}\n\n"
            info += "Combos:\n" + ", ".join(combos)
            
            messagebox.showinfo(f"Détails: {hand}", info, parent=self.root)

    def get_hand_combos(self, hand):
        """Retourne toutes les combinaisons possibles pour une main"""
        suits = ['c', 'd', 'h', 's']
        combos = []
        
        if len(hand) == 2:  # Paire (ex: AA)
            rank = hand[0]
            for i, suit1 in enumerate(suits):
                for suit2 in suits[i+1:]:
                    combos.append(f"{rank}{suit1}{rank}{suit2}")
        elif hand.endswith('s'):  # Suited
            r1, r2 = hand[0], hand[1]
            for suit in suits:
                combos.append(f"{r1}{suit}{r2}{suit}")
        elif hand.endswith('o'):  # Offsuit
            r1, r2 = hand[0], hand[1]
            for suit1 in suits:
                for suit2 in suits:
                    if suit1 != suit2:
                        combos.append(f"{r1}{suit1}{r2}{suit2}")
        
        return combos

    def clear_all(self):
        """Réinitialise toutes les mains"""
        confirm = messagebox.askyesno(
            "Confirmation",
            "Supprimer toutes les mains de la range ?",
            parent=self.root
        )
        if confirm:
            self.range_data.clear()
            self.update_grid_display()
            self.save_state()

    def save_state(self):
        """Sauvegarde l'état actuel pour undo/redo"""
        state = {
            'labels': dict(self.labels),
            'range_data': {k: list(v) for k, v in self.range_data.items()}
        }
        # Supprimer les états futurs si on modifie après un undo
        self.history = self.history[:self.history_index + 1]
        self.history.append(state)
        self.history_index += 1
        
        # Limiter l'historique à 50 états
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_index -= 1

    def undo(self):
        """Annuler la dernière action"""
        if self.history_index > 0:
            self.history_index -= 1
            state = self.history[self.history_index]
            self.labels = dict(state['labels'])
            self.range_data = {k: list(v) for k, v in state['range_data'].items()}
            self.update_label_menu()
            self.update_legend()
            self.update_grid_display()

    def redo(self):
        """Refaire l'action annulée"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            state = self.history[self.history_index]
            self.labels = dict(state['labels'])
            self.range_data = {k: list(v) for k, v in state['range_data'].items()}
            self.update_label_menu()
            self.update_legend()
            self.update_grid_display()

    def save_range(self):
        """Sauvegarde la range dans un fichier JSON"""
        data = {
            "name": self.title_label.cget("text"),
            "labels": self.labels,
            "range_data": {k: v for k, v in self.range_data.items() if v}
        }
        
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialdir="./ranges",
            title="Sauvegarder la range"
        )
        
        if path:
            try:
                with open(path, "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Succès", f"Range sauvegardée:\n{path}", parent=self.root)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder:\n{str(e)}", parent=self.root)