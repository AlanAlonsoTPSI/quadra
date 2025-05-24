import tkinter as tk
from tkinter import ttk

class HomeUser:
    def __init__(self, parent, username, on_logout):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        label = ttk.Label(
            self.frame, 
            text=f"Bienvenido, {username}!\nExplora puestos de comida.", 
            font=('Arial', 14)
        )
        label.pack(pady=20)
        
        btn_logout = ttk.Button(self.frame, text="Cerrar Sesión", command=on_logout)
        btn_logout.pack(pady=10)
        
        self.frame.pack()

    def destroy(self):
        self.frame.destroy()