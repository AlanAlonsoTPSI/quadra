import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection

class LoginWindow:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Iniciar Sesión")
        
        ttk.Label(self.window, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.window)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.window, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.window, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_login = ttk.Button(self.window, text="Ingresar", command=self.authenticate)
        btn_login.grid(row=2, column=1, pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()  # ¡Encriptar en producción!
        
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username FROM users WHERE username = ? AND password = ?",  # <-- Paréntesis cerrado correctamente
                (username, password)  # <-- Paréntesis cerrado aquí
            )
            user = cursor.fetchone()
            conn.close()
            
            if user:
                self.on_success(username)  # Llama a la función de éxito
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")