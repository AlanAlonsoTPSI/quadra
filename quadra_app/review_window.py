import tkinter as tk
from tkinter import ttk, messagebox

class ReviewWindow:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn
        
        self.window = tk.Toplevel(parent)
        self.window.title("Reseñas de Puestos")
        
        # Lista de puestos
        ttk.Label(self.window, text="Selecciona un puesto:").pack(pady=5)
        self.stand_combobox = ttk.Combobox(self.window, state="readonly")
        self.stand_combobox.pack(pady=5)
        self.load_stands()
        
        # Reseñas
        self.review_tree = ttk.Treeview(self.window, columns=('Usuario', 'Calificación', 'Comentario'), show='headings')
        self.review_tree.heading('Usuario', text='Usuario')
        self.review_tree.heading('Calificación', text='Calificación (1-5)')
        self.review_tree.heading('Comentario', text='Comentario')
        self.review_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Nueva reseña
        ttk.Label(self.window, text="Agregar Reseña:").pack(pady=5)
        
        ttk.Label(self.window, text="Usuario:").pack()
        self.user_entry = ttk.Entry(self.window)
        self.user_entry.pack()
        
        ttk.Label(self.window, text="Calificación (1-5):").pack()
        self.rating_entry = ttk.Entry(self.window)
        self.rating_entry.pack()
        
        ttk.Label(self.window, text="Comentario:").pack()
        self.comment_entry = ttk.Entry(self.window)
        self.comment_entry.pack()
        
        self.add_review_button = ttk.Button(self.window, text="Agregar Reseña", command=self.add_review)
        self.add_review_button.pack(pady=10)
        
        self.stand_combobox.bind('<<ComboboxSelected>>', self.load_reviews)
    
    def load_stands(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name FROM food_stands')
        stands = cursor.fetchall()
        self.stand_combobox['values'] = [f"{stand[0]} - {stand[1]}" for stand in stands]
    
    def load_reviews(self, event):
        stand_id = int(self.stand_combobox.get().split(' - ')[0])
        cursor = self.conn.cursor()
        cursor.execute('SELECT user, rating, comment FROM reviews WHERE stand_id = ?', (stand_id,))
        reviews = cursor.fetchall()
        
        for row in self.review_tree.get_children():
            self.review_tree.delete(row)
        
        for review in reviews:
            self.review_tree.insert('', tk.END, values=review)
    
    def add_review(self):
        stand_id = int(self.stand_combobox.get().split(' - ')[0])
        user = self.user_entry.get()
        rating = self.rating_entry.get()
        comment = self.comment_entry.get()
        
        if not all([user, rating, comment]):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (stand_id, user, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (stand_id, user, rating, comment))
        self.conn.commit()
        
        messagebox.showinfo("Éxito", "Reseña agregada correctamente.")
        self.load_reviews(None)  # Actualizar lista