import tkinter as tk
from tkinter import ttk, messagebox

class FormularioCRUD(tk.Toplevel):
    def __init__(self, parent, titulo, campos, entidades_ejemplo=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("700x500")
        
        self.campos = campos
        self.entradas = {}
        
        self._crear_formulario()
        self._crear_botones()
        self._crear_tabla()
        
        if entidades_ejemplo:
            self._cargar_datos_prueba(entidades_ejemplo)

    def _crear_formulario(self):
        frame_form = ttk.LabelFrame(self, text="Datos de la Entidad", padding=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        for i, campo in enumerate(self.campos):
            lbl = ttk.Label(frame_form, text=f"{campo}:")
            lbl.grid(row=i, column=0, sticky="w", pady=2, padx=5)
            
            entry = ttk.Entry(frame_form)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            self.entradas[campo] = entry
            
        frame_form.columnconfigure(1, weight=1)

    def _crear_botones(self):
        frame_btn = ttk.Frame(self, padding=5)
        frame_btn.pack(fill="x", padx=10)

        ttk.Button(frame_btn, text="Crear", command=self.accion_crear).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Actualizar", command=self.accion_actualizar).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Eliminar", command=self.accion_eliminar).pack(side="left", padx=5)
        ttk.Button(frame_btn, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)

    def _crear_tabla(self):
        frame_tabla = ttk.Frame(self, padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabla = ttk.Treeview(frame_tabla, columns=self.campos, show="headings")
        for campo in self.campos:
            self.tabla.heading(campo, text=campo)
            self.tabla.column(campo, anchor="w", width=120)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_registro)

    def obtener_datos_formulario(self):
        return {campo: entry.get().strip() for campo, entry in self.entradas.items()}

    def limpiar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)

    def _validar_campos(self):
        datos = self.obtener_datos_formulario()
        if any(valor == "" for valor in datos.values()):
            messagebox.showwarning("Error de Validación", "Todos los campos son obligatorios.")
            return None
        return datos

    def accion_crear(self):
        datos = self._validar_campos()
        if datos:
            valores = [datos[campo] for campo in self.campos]
            self.tabla.insert("", tk.END, values=valores)
            self.limpiar_campos()

    def accion_actualizar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error de Selección", "Debe seleccionar un registro de la tabla para actualizar.")
            return
        
        datos = self._validar_campos()
        if datos:
            valores = [datos[campo] for campo in self.campos]
            self.tabla.item(seleccion[0], values=valores)
            self.limpiar_campos()

    def accion_eliminar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error de Selección", "Debe seleccionar un registro de la tabla para eliminar.")
            return
        
        self.tabla.delete(seleccion[0])
        self.limpiar_campos()

    def _al_seleccionar_registro(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            for campo, valor in zip(self.campos, valores):
                self.entradas[campo].delete(0, tk.END)
                self.entradas[campo].insert(0, str(valor))

    def _cargar_datos_prueba(self, datos):
        for fila in datos:
            self.tabla.insert("", tk.END, values=fila)

# hice cambios al llamar a la clase del formulario, ya que antes era una sola ventana para la gestión de vehiculos.
# ahora se llaman dos ventanas, una para gestionar vehiculos y otra para gestionar propietarios.
# 