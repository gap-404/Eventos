import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno
import urllib.request, urllib.error, json

API_URL = 'http://127.0.0.1:8000/api/software/'

class InterfazSoftware:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestión de Software")
        self.root.geometry("680x620")
        self.root.resizable(0, 0)

        self.var_tipo = tk.StringVar()
        self.var_version = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_firewall = tk.StringVar()

        tk.Label(self.root, text="Tipo de software:").pack(pady=(18, 2))
        self.entry_tipo = tk.Entry(self.root, textvariable=self.var_tipo, width=40)
        self.entry_tipo.pack()

        tk.Label(self.root, text="Versión:").pack(pady=(12, 2))
        self.entry_version = tk.Entry(self.root, textvariable=self.var_version, width=40)
        self.entry_version.pack()

        tk.Label(self.root, text="Fecha publicación (YYYY-MM-DD):").pack(pady=(12, 2))
        self.entry_fecha = tk.Entry(self.root, textvariable=self.var_fecha, width=40)
        self.entry_fecha.pack()

        tk.Label(self.root, text="Firewall:").pack(pady=(12, 2))
        self.entry_firewall = tk.Entry(self.root, textvariable=self.var_firewall, width=40)
        self.entry_firewall.pack()

        tk.Button(self.root, text="Guardar", command=self.guardar, width=18).pack(pady=8)
        tk.Button(self.root, text="Actualizar", command=self.actualizar, width=18).pack(pady=4)
        tk.Button(self.root, text="Borrar", command=self.borrar, width=18).pack(pady=4)
        tk.Button(self.root, text="Consultar uno", command=self.consultar_uno, width=18).pack(pady=4)
        tk.Button(self.root, text="Consultar todos", command=self.cargar_tabla, width=18).pack(pady=4)
        tk.Button(self.root, text="Limpiar", command=self.limpiar, width=18).pack(pady=10)

        columnas = ["id", "tipo", "version", "fecha_publicacion", "firewall"]
        titulos = ["ID", "Tipo", "Versión", "Fecha", "Firewall"]

        self.tabla = ttk.Treeview(self.root, columns=columnas, show="headings", height=12)
        for i in range(len(columnas)):
            self.tabla.heading(columnas[i], text=titulos[i])
            self.tabla.column(columnas[i], width=120)
        self.tabla.pack(pady=6)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)
        self.tabla.bind("<Delete>", self.borrar_fila)

        self.cargar_tabla()
        self.root.mainloop()

    def limpiar(self):
        self.var_tipo.set("")
        self.var_version.set("")
        self.var_fecha.set("")
        self.var_firewall.set("")

    def pedir_id(self, msg):
        win = tk.Toplevel(self.root)
        win.title(msg)
        win.geometry('220x100')
        var = tk.StringVar()
        tk.Label(win, text=msg).pack(pady=8)
        entry = tk.Entry(win, textvariable=var)
        entry.pack(pady=4)
        result = {'value': None}

        def ok():
            result['value'] = var.get().strip()
            win.destroy()

        tk.Button(win, text='OK', command=ok).pack(pady=8)
        win.wait_window()
        return result['value']

    def guardar(self):
        tipo = self.var_tipo.get().strip()
        version = self.var_version.get().strip()
        fecha = self.var_fecha.get().strip()
        firewall = self.var_firewall.get().strip()

        data = json.dumps({
            "tipo": tipo,
            "version": version,
            "fecha_publicacion": fecha,
            "firewall": firewall
        }).encode()

        try:
            req = urllib.request.Request(API_URL, data=data, headers={'Content-Type': 'application/json'}, method='POST')
            urllib.request.urlopen(req, timeout=5)
            showinfo("Éxito", "Software guardado.")
            self.limpiar()
            self.cargar_tabla()
        except Exception as e:
            showerror("Error", f"No se pudo guardar: {e}")

    def cargar_tabla(self):
        try:
            req = urllib.request.Request(API_URL)
            with urllib.request.urlopen(req) as resp:
                datos = json.loads(resp.read().decode())

            self.tabla.delete(*self.tabla.get_children())
            for s in datos:
                self.tabla.insert("", "end", values=(
                    s.get("id", ""),
                    s.get("tipo", ""),
                    s.get("version", ""),
                    s.get("fecha_publicacion", ""),
                    s.get("firewall", "")
                ))
        except Exception as e:
            showerror("Error", f"No se pudo cargar la tabla: {e}")

    def seleccionar_fila(self, _):
        for fila in self.tabla.selection():
            valores = self.tabla.item(fila)["values"]
            self.var_tipo.set(valores[1])
            self.var_version.set(valores[2])
            self.var_fecha.set(valores[3])
            self.var_firewall.set(valores[4])

    def borrar_fila(self, _):
        for fila in self.tabla.selection():
            id_ = self.tabla.item(fila)["values"][0]
            self.borrar_id(id_)
        self.cargar_tabla()

    def consultar_uno(self):
        id_ = self.pedir_id("ID a consultar")
        if not id_:
            return
        try:
            req = urllib.request.Request(f"{API_URL}{id_}/")
            with urllib.request.urlopen(req) as resp:
                s = json.loads(resp.read().decode())
            msg = f"ID: {s.get('id')}\nTipo: {s.get('tipo')}\nVersión: {s.get('version')}\nFecha: {s.get('fecha_publicacion')}\nFirewall: {s.get('firewall')}"
            showinfo("Detalle", msg)
        except Exception as e:
            showerror("Error", f"No se pudo consultar: {e}")

    def actualizar(self):
        id_ = self.pedir_id("ID a actualizar")
        if not id_:
            return

        data = json.dumps({
            "tipo": self.var_tipo.get().strip(),
            "version": self.var_version.get().strip(),
            "fecha_publicacion": self.var_fecha.get().strip(),
            "firewall": self.var_firewall.get().strip()
        }).encode()

        try:
            req = urllib.request.Request(f"{API_URL}{id_}/", data=data, headers={'Content-Type': 'application/json'}, method='PUT')
            urllib.request.urlopen(req)
            showinfo("Éxito", "Software actualizado.")
            self.cargar_tabla()
        except Exception as e:
            showerror("Error", f"No se pudo actualizar: {e}")

    def borrar(self):
        id_ = self.pedir_id("ID a borrar")
        if not id_:
            return
        self.borrar_id(id_)
        self.cargar_tabla()

    def borrar_id(self, id_):
        try:
            req = urllib.request.Request(f"{API_URL}{id_}/", method='DELETE')
            urllib.request.urlopen(req)
            showinfo("Éxito", "Eliminado.")
        except Exception as e:
            showerror("Error", f"No se pudo borrar: {e}")


InterfazSoftware()
