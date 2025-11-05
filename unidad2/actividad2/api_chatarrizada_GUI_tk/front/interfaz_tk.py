import tkinter as tk
from tkinter.messagebox import showinfo, showerror, askyesno
import urllib.request, urllib.error, json

API_URL = 'http://127.0.0.1:8000/api/software/'

root = tk.Tk()
root.title("Gestión de Software")
root.geometry("420x520")
root.resizable(0, 0)

# --- VARIABLES ---
var_tipo = tk.StringVar()
var_version = tk.StringVar()
var_fecha = tk.StringVar()
var_firewall = tk.StringVar()

# --- CAMPOS ---
tk.Label(root, text="Tipo de software:").pack(pady=(18, 2))
tk.Entry(root, textvariable=var_tipo, width=30).pack(pady=2)
tk.Label(root, text="Versión:").pack(pady=(12, 2))
tk.Entry(root, textvariable=var_version, width=30).pack(pady=2)
tk.Label(root, text="Fecha de publicación (YYYY-MM-DD):").pack(pady=(12, 2))
tk.Entry(root, textvariable=var_fecha, width=30).pack(pady=2)
tk.Label(root, text="Firewall:").pack(pady=(12, 2))
tk.Entry(root, textvariable=var_firewall, width=30).pack(pady=2)

# --- FUNCIONES ---
def limpiar():
    var_tipo.set("")
    var_version.set("")
    var_fecha.set("")
    var_firewall.set("")

def pedir_id(msg):
    win = tk.Toplevel(root)
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

# --- GUARDAR ---
def guardar():
    tipo = var_tipo.get().strip()
    version = var_version.get().strip()
    fecha = var_fecha.get().strip()
    firewall = var_firewall.get().strip()

    if not tipo or not version:
        showerror("Error", "Completa los campos obligatorios: Tipo y Versión.")
        return

    data = json.dumps({
        "tipo": tipo,
        "version": version,
        "fecha_publicacion": fecha,
        "firewall": firewall
    }).encode('utf-8')

    headers = {'Content-Type': 'application/json', 'User-Agent': 'Tkinter-Client'}

    try:
        req = urllib.request.Request(API_URL, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"HTTP error {resp.status}")
        showinfo("Éxito", "Software guardado correctamente.")
        limpiar()
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode())
            msg = "\n".join([f"{k}: {v}" for k, v in err_data.items()])
        except Exception:
            msg = e.reason
        showerror("Error HTTP", f"No se pudo guardar:\n{msg}")
    except Exception as e:
        showerror("Error", f"No se pudo guardar: {e}")

# --- CONSULTAR TODOS ---
def consultar_todos():
    try:
        req = urllib.request.Request(API_URL, headers={'User-Agent': 'Tkinter-Client'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        msg = '\n'.join([f"{s.get('id', '')} - {s.get('tipo', '')} (v{s.get('version', '')})" for s in data]) or 'Sin datos.'
        showinfo('Todos los software', msg)
    except Exception as e:
        showerror('Error', f'No se pudo consultar: {e}')

# --- CONSULTAR UNO ---
def consultar_uno():
    id_ = pedir_id('ID a consultar')
    if not id_:
        return
    try:
        req = urllib.request.Request(f'{API_URL}{id_}/', headers={'User-Agent': 'Tkinter-Client'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        msg = f"ID: {data.get('id', '')}\nTipo: {data.get('tipo', '')}\nVersión: {data.get('version', '')}\nFecha: {data.get('fecha_publicacion', '')}\nFirewall: {data.get('firewall', '')}"
        showinfo('Detalle', msg)
    except Exception as e:
        showerror('Error', f'No se pudo consultar: {e}')

# --- ACTUALIZAR ---
def actualizar():
    id_ = pedir_id('ID a actualizar')
    if not id_:
        return

    tipo = var_tipo.get().strip()
    version = var_version.get().strip()
    fecha = var_fecha.get().strip()
    firewall = var_firewall.get().strip()

    if not tipo or not version:
        showerror("Error", "Completa los campos obligatorios: Tipo, Versión, Fecha y Firewall.")
        return

    data = json.dumps({
        "tipo": tipo,
        "version": version,
        "fecha_publicacion": fecha,
        "firewall": firewall
    }).encode('utf-8')

    headers = {'Content-Type': 'application/json', 'User-Agent': 'Tkinter-Client'}

    try:
        req = urllib.request.Request(f'{API_URL}{id_}/', data=data, headers=headers, method='PUT')
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"HTTP error {resp.status}")
        showinfo("Éxito", "Software actualizado correctamente.")
        limpiar()
    except urllib.error.HTTPError as e:
        try:
            err_data = json.loads(e.read().decode())
            msg = "\n".join([f"{k}: {v}" for k, v in err_data.items()])
        except Exception:
            msg = e.reason
        showerror("Error HTTP", f"No se pudo actualizar:\n{msg}")
    except Exception as e:
        showerror("Error", f"No se pudo actualizar: {e}")

# --- BORRAR ---
def borrar():
    id_ = pedir_id('ID a borrar')
    if not id_:
        return
    if not askyesno('Confirmar', f'¿Seguro que quieres borrar el software ID {id_}?'):
        return
    try:
        req = urllib.request.Request(f'{API_URL}{id_}/', headers={'User-Agent': 'Tkinter-Client'}, method='DELETE')
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status not in (204, 200):
                raise RuntimeError(f'HTTP error {resp.status}')
        showinfo('Éxito', 'Software borrado correctamente.')
    except Exception as e:
        showerror('Error', f'No se pudo borrar: {e}')

# --- BOTONES ---
tk.Button(root, text="Guardar", command=guardar, width=14, bg="#e0e7ff").pack(pady=10)
tk.Button(root, text="Consultar todos", command=consultar_todos, width=14, bg="#e0e7ff").pack(pady=2)
tk.Button(root, text="Consultar uno", command=consultar_uno, width=14, bg="#e0e7ff").pack(pady=2)
tk.Button(root, text="Actualizar", command=actualizar, width=14, bg="#e0e7ff").pack(pady=2)
tk.Button(root, text="Borrar", command=borrar, width=14, bg="#e0e7ff").pack(pady=2)
tk.Button(root, text="Limpiar", command=limpiar, width=14, bg="#f7f7f7").pack(pady=10)

root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
root.mainloop()
