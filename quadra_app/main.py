import tkinter as tk
from tkinter import ttk, messagebox
from add_food_stand import AddFoodStandWindow
from review_window import ReviewWindow
from database import create_connection, create_tables
from auth.login import LoginWindow
from auth.register import RegisterWindow
from views.home_guest import HomeGuest
from views.home_user import HomeUser

class QuadraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadra - Puestos de Comida Callejera")
        self.current_user = None  # Usuario actual (None = invitado)
        
        # Conectar a la base de datos
        self.conn = create_connection()
        if self.conn:
            create_tables(self.conn)
        
        # Mostrar pantalla inicial (invitado)
        self.show_guest_home()

    def show_guest_home(self):
        """Muestra la interfaz para usuarios no logueados"""
        self._clear_window()
        self.current_user = None
        
        # Widgets para invitados
        HomeGuest(
            self.root,
            show_login=self.show_login,
            show_register=self.show_register
        )

    def show_user_home(self, username):
        """Muestra la interfaz para usuarios logueados"""
        self._clear_window()
        self.current_user = username
        
        # Widgets principales (heredados de tu versión original)
        self.label = ttk.Label(self.root, text=f"Bienvenido, {username}", font=('Arial', 14))
        self.label.pack(pady=10)
        
        self.tree = ttk.Treeview(self.root, columns=('Nombre', 'Descripción', 'Creador'), show='headings')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.heading('Creador', text='Creador')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.add_button = ttk.Button(self.root, text="Agregar Puesto", command=self.open_add_window)
        self.add_button.pack(pady=5)
        
        self.review_button = ttk.Button(self.root, text="Ver Reseñas", command=self.open_review_window)
        self.review_button.pack(pady=5)
        
        self.logout_button = ttk.Button(self.root, text="Cerrar Sesión", command=self.logout)
        self.logout_button.pack(pady=10)
        
        self.load_food_stands()

    def _clear_window(self):
        """Elimina todos los widgets de la ventana principal"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_food_stands(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, description, user_creator FROM food_stands')
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert('', tk.END, values=row)
    
    def open_add_window(self):
        if self.current_user:
            AddFoodStandWindow(self.root, self.conn, self)
        else:
            messagebox.showerror("Error", "Debe iniciar sesión para agregar puestos")

    def open_review_window(self):
        ReviewWindow(self.root, self.conn)

    def show_login(self):
        LoginWindow(self.root, on_success=self.show_user_home)

    def show_register(self):
        RegisterWindow(self.root, on_success=lambda: messagebox.showinfo("Éxito", "¡Registro completado! Ahora inicie sesión."))

    def logout(self):
        self.show_guest_home()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraApp(root)
    root.mainloop()