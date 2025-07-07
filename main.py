import tkinter as tk
from tkinter import filedialog, simpledialog, Button
import json
from poker_range_editor import PokerRangeEditor 
from training_table import TrainingTable

def open_json_range():
    path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if not path:
        return
    with open(path, "r") as f:
        data = json.load(f)
    new_window = tk.Toplevel()
    new_window.title(data.get("name", "Range"))
    PokerRangeEditor(new_window, data)

def create_new_range():
    name = simpledialog.askstring("Nom du tableau", "Nom de la range :")
    if not name:
        return
    data = {"name": name, "labels": {}, "range_data": {}}
    new_window = tk.Toplevel()
    new_window.title(name)
    PokerRangeEditor(new_window, data)

def train_preflop():
    TrainingTable(tk._default_root)

def launch_main_app():
    root = tk.Tk()
    root.title("Custom Range Manager & Open Trainer")
    root.geometry("400x300")  # Agrandit la fenêtre

    # Titre de bienvenue
    tk.Label(root, text="Bienvenue dans le gestionnaire de ranges", font=("Helvetica", 14, "bold")).pack(pady=20)

    # Cadre pour les boutons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Boutons d'action
    tk.Button(button_frame, text="Créer un nouveau range", width=25, command=create_new_range).pack(pady=5)
    tk.Button(button_frame, text="Ouvrir un range existant", width=25, command=open_json_range).pack(pady=5)
    tk.Button(button_frame, text="S'entraîner au préflop", width=25, command=train_preflop).pack(pady=5)
    tk.Button(button_frame, text="Quitter", width=25, command=root.quit).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    launch_main_app()