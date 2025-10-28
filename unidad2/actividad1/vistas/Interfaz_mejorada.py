import tkinter as tk
import re
from tkinter.messagebox import askyesno, showerror, showinfo
from datetime import datetime

root = tk.Tk()
root.title("Software")
root.geometry("420x380")
root.resizable(0,0)
root.config(padx=20, pady=20)

def el_usuario_quiere_salir():
    if askyesno("Salir de la aplicacion", "Estas seguro de querer cerrar la aplicacion"):
        root.destroy()

VAL_VERSION = re.compile(r"^[0-9.]*$")
VAL_TIPO = re.compile(r"^[A-Za-z .]*$")



def limpiar_campos_texto():
    for var, err in [
        (var_version, err_version),
        (var_tipo, err_tipo),
        (var_fecha_publicacion, err_fecha_publicacion),
        (var_firewall, err_firewall)
    ]:
        var.set("")
        err.set("")

def val_version() -> bool:
    txt = var_version.get()
    if txt == "":
        err_version.set("")
        return True
    if VAL_VERSION.match(txt):
        err_version.set("")
        return True
    err_version.set("Solo números y puntos")
    return False

def val_tipo() -> bool:
    txt = var_tipo.get()
    if txt == "":
        err_tipo.set("")
        return True
    if VAL_TIPO.match(txt):
        err_tipo.set("")
        return True
    err_tipo.set("Solo letras y espacios")
    return False

def val_fecha_publicacion() -> bool:
    txt = var_fecha_publicacion.get().strip()
    if txt == "":
        err_fecha_publicacion.set("")
        return True
    try:
        datetime.strptime(txt, "%Y-%m-%d")
        err_fecha_publicacion.set("")
        return True
    except ValueError:
        err_fecha_publicacion.set("Formato: YYYY-MM-DD")
        return False

def val_firewall() -> bool:
    txt = var_firewall.get()
    if txt == "":
        err_firewall.set("")
        return True
    err_firewall.set("")
    return True

def enviar():
    ok = all([
        val_version(),
        val_tipo(),
        val_fecha_publicacion(),
        val_firewall(),
    ])
    obligatorios = [
        (var_version.get().strip() != "", err_version, "La versión es obligatoria."),
        (var_tipo.get().strip() != "", err_tipo, "El tipo es obligatorio."),
        (var_fecha_publicacion.get().strip() != "", err_fecha_publicacion, "La fecha de publicación es obligatoria."),
        (var_firewall.get().strip() != "", err_firewall, "El firewall es obligatorio."),
    ]
    for lleno, err_var, msg in obligatorios:
        if not lleno and err_var.get() == "":
            err_var.set(msg)
            ok = False

    if not ok:
        showerror("Errores de validación", "Por favor complete los campos marcados en rojo.")
        return

    showinfo("OK", "Formulario válido. ¡Datos guardados!")

# Variables de entrada
var_version = tk.StringVar()
var_tipo = tk.StringVar()
var_fecha_publicacion = tk.StringVar()
var_firewall = tk.StringVar()

# Variables de error
err_version = tk.StringVar()
err_tipo = tk.StringVar()
err_fecha_publicacion = tk.StringVar()
err_firewall = tk.StringVar()

# Etiquetas y campos
label_opts = dict(sticky="e", padx=(0,10), pady=(0,8))
entry_opts = dict(sticky="w", padx=(0,10), pady=(0,8))

tk.Label(root, text="Versión").grid(row=0, column=0, **label_opts)
entry_version = tk.Entry(root, textvariable=var_version, width=25)
entry_version.grid(row=0, column=1, **entry_opts)
tk.Label(root, textvariable=err_version, fg="#c1121f").grid(row=1, column=1, sticky="w", pady=(0,8))

tk.Label(root, text="Tipo").grid(row=2, column=0, **label_opts)
entry_tipo = tk.Entry(root, textvariable=var_tipo, width=25)
entry_tipo.grid(row=2, column=1, **entry_opts)
tk.Label(root, textvariable=err_tipo, fg="#c1121f").grid(row=3, column=1, sticky="w", pady=(0,8))

tk.Label(root, text="Fecha de publicación").grid(row=4, column=0, **label_opts)
entry_fecha_publicacion = tk.Entry(root, textvariable=var_fecha_publicacion, width=25)
entry_fecha_publicacion.grid(row=4, column=1, **entry_opts)
tk.Label(root, textvariable=err_fecha_publicacion, fg="#c1121f").grid(row=5, column=1, sticky="w", pady=(0,8))

tk.Label(root, text="Firewall").grid(row=6, column=0, **label_opts)
entry_firewall = tk.Entry(root, textvariable=var_firewall, width=25)
entry_firewall.grid(row=6, column=1, **entry_opts)
tk.Label(root, textvariable=err_firewall, fg="#c1121f").grid(row=7, column=1, sticky="w", pady=(0,8))

# Frame para los botones
boton_frame = tk.Frame(root)
boton_frame.grid(row=8, column=0, columnspan=2, pady=(18,0))

tk.Button(boton_frame, text="Validar Información", command=enviar, width=18).pack(side="left", padx=10)
tk.Button(boton_frame, text="Limpiar", command=limpiar_campos_texto, width=12).pack(side="left", padx=10)

# Eventos de validación en vivo
entry_version.bind("<KeyRelease>", lambda e: val_version())
entry_tipo.bind("<KeyRelease>", lambda e: val_tipo())
entry_fecha_publicacion.bind("<KeyRelease>", lambda e: val_fecha_publicacion())
entry_firewall.bind("<KeyRelease>", lambda e: val_firewall())

root.protocol("WM_DELETE_WINDOW", el_usuario_quiere_salir)
root.mainloop()