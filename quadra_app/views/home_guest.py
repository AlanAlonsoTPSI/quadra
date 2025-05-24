import tkinter as tk
from tkinter import ttk

class HomeGuest:
    def __init__(self, parent, show_login, show_register):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        label = ttk.Label(self.frame, text="¡Bienvenido a Quadra!", font=('Arial', 16))
        label.pack(pady=20)
        
        btn_login = ttk.Button(self.frame, text="Iniciar Sesión", command=show_login)
        btn_login.pack(pady=10)
        
        btn_register = ttk.Button(self.frame, text="Registrarse", command=show_register)
        btn_register.pack(pady=10)
        
        self.frame.pack()

    def destroy(self):
        self.frame.destroy()