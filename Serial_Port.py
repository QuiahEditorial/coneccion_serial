# Conección serial

import tkinter as tk
import threading
import serial
import serial.tools.list_ports

# ======================================================================================== ventana principal

root = tk.Tk()
root.title("OPN Spec")
root.geometry("1150x680")
root.minsize(650, 625)
root.configure(bg="#333333")

# ======================================================================================== icono de aplicación

try:
    root.iconphoto(False, tk.PhotoImage(file="icon.ico"))
except Exception:
    pass

# ======================================================================================== variables globales

ser = None

# ======================================================================================== conección serial

def list_ports():
    puertos = [p.device for p in serial.tools.list_ports.comports()]
    combo_puertos["values"] = puertos
    if puertos:
        combo_puertos.current(0)
    else:
        combo_puertos.set("Conecte ESP32")

def conectar():
    global ser
    puerto = combo_puertos.get()
    if not puerto:
        messagebox.showwarning("Aviso", "Selecciona un puerto.")
        return
    try:
        ser = serial.Serial(puerto, 115200, timeout=1)
        ser.dtr = True
        ser.rts = True
        ser.reset_input_buffer()

        lbl_estado.config(text=f" 📡 Conectado a {puerto}", foreground="green", font=("Arial", 11, "bold") )
        btn_conectar.config(state="disabled")
        btn_desconectar.config(state="normal")

        threading.Thread(target=leer_serial, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar:\n{e}")

def desconectar():
    global ser
    if ser and ser.is_open:
        try:
            ser.write(b"STOP\n")                                 # Se envían los comandos a ESP32
            ser.write(b"LED:OFF\n")
        except Exception:
            pass
        ser.close()
    ser = None
    grabando = False
    lbl_estado.config(text=" 🛸 Desconectado", foreground="red", font=("Arial", 11 , "bold"))
    btn_conectar.config(state="normal")
    btn_desconectar.config(state="disabled")

# ======================================================================================== layout

frame_puertos = ttk.LabelFrame(root, text="Puerto Serial")
frame_puertos.pack(fill="x", padx=(5,5), pady=(5, 5))

combo_puertos = ttk.Combobox(frame_puertos, state="readonly", width=25)
combo_puertos.pack(side="left", padx=4, pady=4)

lbl_estado = ttk.Label(frame_puertos, text=" 🛸 Desconectado", font=("Arial", 11 , "bold"), foreground="red" )
lbl_estado.pack(side="right", padx=4)

# ======================================================================================== botones

ttk.Button(frame_puertos, text="⟳", width=5, command=list_ports).pack(side="left", padx=4)

btn_conectar = ttk.Button(frame_puertos, text="Conectar", command=conectar)
btn_conectar.pack(side="left", padx=4)

btn_desconectar = ttk.Button(frame_puertos, text="Desconectar", command=desconectar, state="disabled")
btn_desconectar.pack(side="left", padx=4)

# ======================================================================================== ejecución de aplicación

list_ports()
root.mainloop()
