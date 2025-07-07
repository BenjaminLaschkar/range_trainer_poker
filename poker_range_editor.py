
import tkinter as tk
from tkinter import filedialog, Menu, simpledialog, colorchooser
import json

RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

class PokerRangeEditor:
    def __init__(self, root, data=None):
        self.root = root
        self.root.title("Éditeur de Range")
        self.data = data or {"name": "Nouvelle range", "labels": {}, "range_data": {}}

        self.labels = self.data["labels"]
        self.range_data = {hand: list(lbls) for hand, lbls in self.data["range_data"].items()}
        self.current_label = None

        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        self.title_label = tk.Label(top_frame, text=self.data["name"], font=("Helvetica", 14, "bold"))
        self.title_label.pack()

        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.label_var = tk.StringVar()
        initial_label = next(iter(self.labels), "")
        self.label_var.set(initial_label)
        self.label_menu = tk.OptionMenu(control_frame, self.label_var, initial_label, *self.labels.keys())
        self.label_menu.pack(side=tk.LEFT, padx=5)

        self.max_label_var = tk.IntVar(value=2)
        tk.Label(control_frame, text="Max étiquettes :").pack(side=tk.LEFT)
        tk.OptionMenu(control_frame, self.max_label_var, 1, 2, 3, 4, 5).pack(side=tk.LEFT)

        self.create_label_btn = tk.Button(control_frame, text="Créer une étiquette", command=self.create_label)
        self.create_label_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(control_frame, text="Sauvegarder", command=self.save_range)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        content_frame = tk.Frame(root)
        content_frame.pack()

        self.canvas = tk.Canvas(content_frame, width=800, height=800)
        self.canvas.pack(side=tk.LEFT, padx=10)

        self.legend_frame = tk.Frame(content_frame)
        self.legend_frame.pack(side=tk.RIGHT, padx=10, anchor='n')

        self.grid = {}
        self.draw_grid()
        self.update_legend()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)


    def get_hand_label(self, r1, r2, suited):
        r1_index = RANKS.index(r1)
        r2_index = RANKS.index(r2)
        if r1_index < r2_index:
            r1, r2 = r2, r1
        if r1 == r2:
            return f"{r1}{r2}"
        return f"{r1}{r2}{suited}" if suited else f"{r1}{r2}"

    def draw_grid(self):
        size = 50
        padding = 10
        for i, r1 in enumerate(RANKS):
            for j, r2 in enumerate(RANKS):
                if i == j:
                    hand = f"{r1}{r2}"  # paires
                elif i < j:
                    hand = f"{r1}{r2}s"  # suited (r1 plus fort que r2)
                else:
                    hand = f"{r2}{r1}o"  # offsuit (r1 plus faible que r2, donc inversé)
                x, y = j * size + padding, i * size + padding
                rect = self.canvas.create_rectangle(x, y, x+size, y+size, fill='white', tags=hand)
                text = self.canvas.create_text(x+size/2, y+size/2, text=hand, tags=hand)
                self.grid[hand] = (rect, text, x, y)
        self.update_grid_display()

    def update_grid_display(self):
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
                    self.canvas.create_rectangle(x + idx * section_width, y, x + (idx + 1) * section_width, y + size, fill=color, tags=("overlay_" + hand))
            if labels:
                self.canvas.tag_raise(text)

    def create_label(self):
        name = simpledialog.askstring("Nom de l'étiquette", "Nom :")
        if not name:
            return
        color = colorchooser.askcolor(title="Choisissez une couleur")[1]
        if not color:
            return
        self.labels[name] = color
        self.update_label_menu()
        self.update_legend()

    def update_label_menu(self):
        menu = self.label_menu["menu"]
        menu.delete(0, "end")
        for label in self.labels:
            menu.add_command(label=label, command=lambda l=label: self.label_var.set(l))

    def update_legend(self):
        for widget in self.legend_frame.winfo_children():
            widget.destroy()
        for label, color in self.labels.items():
            frame = tk.Frame(self.legend_frame)
            frame.pack(anchor='w', pady=2)
            tk.Label(frame, text=label, bg=color, width=10).pack(side=tk.LEFT)
            tk.Button(frame, text="✎", command=lambda l=label: self.rename_label(l)).pack(side=tk.LEFT)
            tk.Button(frame, text="✖", command=lambda l=label: self.delete_label(l)).pack(side=tk.LEFT)

    def rename_label(self, label):
        new_name = simpledialog.askstring("Renommer", f"Nouveau nom pour '{label}' :")
        if not new_name:
            return
        if new_name in self.labels:
            return
        self.labels[new_name] = self.labels.pop(label)
        for hand in self.range_data:
            self.range_data[hand] = [new_name if l == label else l for l in self.range_data[hand]]
        self.update_label_menu()
        self.update_legend()
        self.update_grid_display()

    def delete_label(self, label):
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

    def on_click(self, event):
        if not self.label_var.get():
            return
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)
        if items:
            tags = self.canvas.gettags(items[0])
            if not tags:
                return
            hand = tags[0]
            labels = self.range_data.get(hand, [])
            label_to_add = self.label_var.get()
            if label_to_add not in labels:
                max_labels = self.max_label_var.get()
                if len(labels) >= max_labels:
                    labels.pop(0)
                labels.append(label_to_add)
                self.range_data[hand] = labels
            self.update_grid_display()

    def on_right_click(self, event):
        x, y = event.x, event.y
        items = self.canvas.find_closest(x, y)
        if items:
            tags = self.canvas.gettags(items[0])
            if not tags:
                return
            hand = tags[0]
            if hand in self.range_data:
                self.range_data[hand].clear()
                self.update_grid_display()

    def save_range(self):
        data = {
            "name": self.title_label.cget("text"),
            "labels": self.labels,
            "range_data": {k: v for k, v in self.range_data.items() if v}
        }
        path = filedialog.asksaveasfilename(defaultextension=".json")
        if path:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)