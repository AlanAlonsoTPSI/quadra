import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection

class RegisterWindow:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Registro de Usuario")
        
        # Campos: Usuario, Email, Contraseña, Confirmar Contraseña
        fields = ["Usuario", "Email", "Contraseña", "Confirmar Contraseña"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(self.window, text=f"{field}:").grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.window, show="*" if "Contraseña" in field else "")
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        btn_register = ttk.Button(self.window, text="Registrarse", command=self.register)
        btn_register.grid(row=len(fields), column=1, pady=10)

    def register(self):
        # Validaciones básicas
        if self.entries["Contraseña"].get() != self.entries["Confirmar Contraseña"].get():
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (
                        self.entries["Usuario"].get(),
                        self.entries["Contraseña"].get(),  # ¡Encriptar en producción!
                        self.entries["Email"].get()
                    )
                )
                conn.commit()
                messagebox.showinfo("Éxito", "¡Registro completado! Ahora inicia sesión.")
                self.window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "El usuario o email ya existen")
            finally:
                conn.close()