import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

class AddFoodStandWindow:
    def __init__(self, parent, conn, app):
        self.parent = parent
        self.conn = conn
        self.app = app
        
        self.window = tk.Toplevel(parent)
        self.window.title("Agregar Puesto de Comida")
        
        # Campos del formulario
        ttk.Label(self.window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self.window)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.window, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(self.window)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.window, text="Ubicación (Lat, Long):").grid(row=2, column=0, padx=5, pady=5)
        self.lat_entry = ttk.Entry(self.window, width=10)
        self.lat_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.long_entry = ttk.Entry(self.window, width=10)
        self.long_entry.grid(row=2, column=1, padx=5, pady=5, sticky='e')
        
        ttk.Label(self.window, text="Foto:").grid(row=3, column=0, padx=5, pady=5)
        self.photo_path = ""
        self.photo_button = ttk.Button(self.window, text="Seleccionar Foto", command=self.select_photo)
        self.photo_button.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.window, text="Usuario:").grid(row=4, column=0, padx=5, pady=5)
        self.user_entry = ttk.Entry(self.window)
        self.user_entry.grid(row=4, column=1, padx=5, pady=5)
        
        self.submit_button = ttk.Button(self.window, text="Guardar", command=self.save_food_stand)
        self.submit_button.grid(row=5, column=1, pady=10)
    
    def select_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.photo_path = file_path
    
    def save_food_stand(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        lat = self.lat_entry.get()
        long = self.long_entry.get()
        user = self.user_entry.get()
        
        if not all([name, desc, lat, long, user]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO food_stands (name, description, latitude, longitude, photo_path, user_creator)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, desc, lat, long, self.photo_path, user))
        self.conn.commit()
        
        messagebox.showinfo("Éxito", "Puesto agregado correctamente.")
        self.app.load_food_stands()  # Actualizar lista
        self.window.destroy()