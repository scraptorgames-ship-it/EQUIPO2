
import tkinter as tk
from tkinter import messagebox
import mysql.connector

#luis manuel emba falcón: sube el codigo inicial

# CONEXION A LA BASE DE DATOS
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cuadrados_equipo2"
    )


# GUARDAR LOS CUADRADOS
def guardar_cuadrados():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        for numero in range(1, 21):
            resultado = numero ** 2

            cursor.execute(
                "SELECT id FROM cuadrados WHERE numero = %s",
                (numero,)
            )

            existe = cursor.fetchone()

            if not existe:
                cursor.execute(
                    "INSERT INTO cuadrados (numero, resultado) VALUES (%s, %s)",
                    (numero, resultado)
                )

        conexion.commit()
        cursor.close()
        conexion.close()

        messagebox.showinfo(
            "Guardado",
            "Los cuadrados se guardaron correctamente."
        )

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))


# CONSULTAR LOS CUADRADOS
def consultar_cuadrados():
    lista.delete(0, tk.END)

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id, numero, resultado FROM cuadrados ORDER BY numero"
        )

        registros = cursor.fetchall()

        for registro in registros:
            id_registro, numero, resultado = registro

            lista.insert(
                tk.END,
                f"ID: {id_registro} | {numero} al cuadrado es {resultado}"
            )

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))


# ACTUALIZAR UN REGISTRO
def actualizar_cuadrado():
    seleccion = lista.curselection()

    if not seleccion:
        messagebox.showwarning(
            "Aviso",
            "Selecciona un registro para actualizar."
        )
        return

    texto = lista.get(seleccion[0])
    id_registro = int(texto.split("|")[0].replace("ID:", "").strip())

    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Actualizar cuadrado")
    ventana.geometry("300x180")

    tk.Label(ventana, text="Nuevo número:").pack(pady=10)

    entrada = tk.Entry(ventana)
    entrada.pack()

    def guardar_cambio():
        try:
            numero = int(entrada.get())

            if numero < 1 or numero > 20:
                messagebox.showwarning(
                    "Aviso",
                    "Escribe un número del 1 al 20."
                )
                return

            resultado = numero ** 2

            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "UPDATE cuadrados SET numero=%s, resultado=%s WHERE id=%s",
                (numero, resultado, id_registro)
            )

            conexion.commit()
            cursor.close()
            conexion.close()

            ventana.destroy()
            consultar_cuadrados()

            messagebox.showinfo("Actualizado", "Registro actualizado.")

        except ValueError:
            messagebox.showwarning("Aviso", "Escribe un número válido.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", str(error))

    tk.Button(
        ventana,
        text="Guardar cambios",
        command=guardar_cambio
    ).pack(pady=15)


# ELIMINAR UN REGISTRO
def eliminar_cuadrado():
    seleccion = lista.curselection()

    if not seleccion:
        messagebox.showwarning(
            "Aviso",
            "Selecciona un registro para eliminar."
        )
        return

    texto = lista.get(seleccion[0])
    id_registro = int(texto.split("|")[0].replace("ID:", "").strip())

    confirmar = messagebox.askyesno(
        "Eliminar",
        "¿Deseas eliminar este registro?"
    )

    if confirmar:
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "DELETE FROM cuadrados WHERE id=%s",
                (id_registro,)
            )

            conexion.commit()
            cursor.close()
            conexion.close()

            consultar_cuadrados()

            messagebox.showinfo("Eliminado", "Registro eliminado.")

        except mysql.connector.Error as error:
            messagebox.showerror("Error", str(error))


# VENTANA PRINCIPAL
ventana_principal = tk.Tk()
ventana_principal.title("Cuadrados")
ventana_principal.geometry("650x550")
ventana_principal.resizable(False, False)
ventana_principal.configure(bg="#EAF2F8")

# TITULO
titulo = tk.Label(
    ventana_principal,
    text="Cuadrados del 1 al 20",
    font=("Arial", 20, "bold"),
    bg="#EAF2F8",
    fg="#19324D"
)
titulo.pack(pady=20)

# BOTON MOSTRAR
tk.Button(
    ventana_principal,
    text="Mostrar cuadrados",
    font=("Arial", 12, "bold"),
    bg="#167D8D",
    fg="white",
    command=consultar_cuadrados
).pack(pady=10)

# LISTA DE RESULTADOS
lista = tk.Listbox(
    ventana_principal,
    width=65,
    height=15,
    font=("Arial", 11),
    bg="white"
)
lista.pack(pady=10)

# BOTONES CRUD
botones = tk.Frame(ventana_principal, bg="#EAF2F8")
botones.pack(pady=15)

tk.Button(
    botones,
    text="Guardar",
    width=12,
    command=guardar_cuadrados
).grid(row=0, column=0, padx=5)

tk.Button(
    botones,
    text="Actualizar",
    width=12,
    command=actualizar_cuadrado
).grid(row=0, column=1, padx=5)

tk.Button(
    botones,
    text="Eliminar",
    width=12,
    command=eliminar_cuadrado
).grid(row=0, column=2, padx=5)

ventana_principal.mainloop()
