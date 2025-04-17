import tkinter as tk
from tkinter import filedialog, messagebox
import os

ruta_archivo = ""

def buscar_archivo():
    global ruta_archivo

    ruta_base = os.path.join(
        os.environ["USERPROFILE"],
        "AppData", "Local", "VALORANT", "Saved", "Config"
    )

    ruta = filedialog.askopenfilename(
        initialdir=ruta_base,
        title="Selecciona GameUserSettings.ini",
        filetypes=[("INI files", "*.ini")]
    )

    if ruta:
        ruta_archivo = ruta
        nombre_archivo = os.path.basename(ruta_archivo)
        lbl_archivo.config(text=f"Archivo: {nombre_archivo}")
    else:
        lbl_archivo.config(text="Ningún archivo seleccionado")

def aplicar_cambios():
    global ruta_archivo

    if not ruta_archivo or not os.path.isfile(ruta_archivo):
        messagebox.showerror("Error", "Por favor selecciona un archivo válido.")
        return

    x = entry_x.get()
    y = entry_y.get()

    if not (x.isdigit() and y.isdigit()):
        messagebox.showerror("Error", "Resolución no válida. Usa solo números.")
        return

    x = int(x)
    y = int(y)

    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        nuevas_lineas = []
        en_bloque_shooter = False
        fullscreen_ya_existe = False

        # Primero buscamos si ya existe FullscreenMode=
        for i, linea in enumerate(lineas):
            if linea.strip() == "[/Script/ShooterGame.ShooterGameUserSettings]":
                en_bloque_shooter = True
            elif linea.startswith("[") and linea.strip() != "[/Script/ShooterGame.ShooterGameUserSettings]":
                en_bloque_shooter = False

            if en_bloque_shooter and linea.strip().startswith("FullscreenMode="):
                fullscreen_ya_existe = True

        # Insertamos FullscreenMode=2 después de HDRDisplayOutputNits=1000 si no existe
        en_bloque_shooter = False
        for i, linea in enumerate(lineas):
            if linea.strip() == "[/Script/ShooterGame.ShooterGameUserSettings]":
                en_bloque_shooter = True
            elif linea.startswith("[") and linea.strip() != "[/Script/ShooterGame.ShooterGameUserSettings]":
                en_bloque_shooter = False

            nuevas_lineas.append(linea)

            if (
                not fullscreen_ya_existe and
                en_bloque_shooter and
                linea.strip() == "HDRDisplayOutputNits=1000"
            ):
                nuevas_lineas.append("FullscreenMode=2\n")

        # Reemplazar resoluciones
        reemplazos = {
            "ResolutionSizeX=": f"ResolutionSizeX={x}\n",
            "ResolutionSizeY=": f"ResolutionSizeY={y}\n",
            "LastUserConfirmedResolutionSizeX=": f"LastUserConfirmedResolutionSizeX={x}\n",
            "LastUserConfirmedResolutionSizeY=": f"LastUserConfirmedResolutionSizeY={y}\n",
        }

        nuevas_lineas = [
            reemplazos.get(linea.split("=")[0] + "=", linea)
            if linea.split("=")[0] + "=" in reemplazos
            else linea
            for linea in nuevas_lineas
        ]

        with open(ruta_archivo, 'w') as f:
            f.writelines(nuevas_lineas)

        messagebox.showinfo("Hecho", f"Resolución {x}x{y} actualizada.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

# ==== UI ==== 
root = tk.Tk()
root.title("True Stretched")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#191919")

tk.Label(root, text="True Stretched", font=("Segoe UI", 14, "bold"), bg="#191919", fg="white").pack(pady=10)

btn_buscar = tk.Button(root, text="Buscar GameUserSettings.ini", command=buscar_archivo, relief="raised", bg="gray20", fg="white")
btn_buscar.pack(pady=5)

lbl_archivo = tk.Label(root, text="Ningún archivo seleccionado", wraplength=380, fg="white", bg="#191919")
lbl_archivo.pack(pady=5)

frame_inputs = tk.Frame(root, bg="#191919")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Resolución X:", bg="#191919", fg="white").grid(row=0, column=0, padx=10, pady=5)
entry_x = tk.Entry(frame_inputs, width=10, bg="gray20", fg="white", insertbackground="white")
entry_x.grid(row=0, column=1, pady=5)

tk.Label(frame_inputs, text="Resolución Y:", bg="#191919", fg="white").grid(row=1, column=0, padx=10, pady=5)
entry_y = tk.Entry(frame_inputs, width=10, bg="gray20", fg="white", insertbackground="white")
entry_y.grid(row=1, column=1, pady=5)

btn_aplicar = tk.Button(root, text="Aplicar resolución", command=aplicar_cambios, relief="raised", bg="gray20", fg="white")
btn_aplicar.pack(pady=15)

root.mainloop()
