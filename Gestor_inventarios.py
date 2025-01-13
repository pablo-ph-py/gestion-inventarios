import sqlite3
from datetime import datetime

# Crear la conexión con la base de datos
def conectar_db():
    return sqlite3.connect("database.db")

# Crear las tablas (solo la primera vez)
def crear_tablas():
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')

    # Tabla de ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    ''')

    conexion.commit()
    conexion.close()

crear_tablas()

# Funciones CRUD
def agregar_producto(nombre, descripcion, cantidad, precio):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio)
        VALUES (?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio))
    conexion.commit()
    conexion.close()
    print(f"Producto '{nombre}' agregado correctamente.")

def listar_productos():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    if productos:
        print("\nInventario:")
        print("-" * 40)
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: {producto[4]:.2f}")
    else:
        print("No hay productos en el inventario.")

def buscar_producto(nombre):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def actualizar_producto(id_producto, campo, nuevo_valor):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(f"UPDATE productos SET {campo} = ? WHERE id = ?", (nuevo_valor, id_producto))
    conexion.commit()
    conexion.close()
    print("Producto actualizado correctamente.")

def eliminar_producto(id_producto):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conexion.commit()
    conexion.close()
    print("Producto eliminado correctamente.")

# Nuevas funciones
def filtrar_productos_por_cantidad(min_cantidad, max_cantidad):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad BETWEEN ? AND ?", (min_cantidad, max_cantidad))
    productos = cursor.fetchall()
    conexion.close()
    if productos:
        print("\nProductos filtrados:")
        print("-" * 40)
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: {producto[4]:.2f}")
    else:
        print("No se encontraron productos en el rango especificado.")

def consultar_estadisticas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*), SUM(cantidad), SUM(cantidad * precio) FROM productos")
    total_productos, total_cantidad, valor_inventario = cursor.fetchone()
    cursor.execute("SELECT nombre, cantidad FROM productos ORDER BY cantidad DESC LIMIT 1")
    producto_mas_stock = cursor.fetchone()
    cursor.execute("SELECT nombre, precio FROM productos ORDER BY precio DESC LIMIT 1")
    producto_mas_caro = cursor.fetchone()
    conexion.close()

    print("\nEstadísticas del inventario:")
    print("-" * 40)
    print(f"Total de productos: {total_productos}")
    print(f"Total de cantidad en stock: {total_cantidad}")
    print(f"Valor total del inventario: {valor_inventario:.2f}")
    if producto_mas_stock:
        print(f"Producto con más stock: {producto_mas_stock[0]} ({producto_mas_stock[1]} unidades)")
    if producto_mas_caro:
        print(f"Producto más caro: {producto_mas_caro[0]} ({producto_mas_caro[1]:.2f} €)")

def realizar_venta(id_producto, cantidad_vendida):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, cantidad, precio FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        print("Producto no encontrado.")
        return

    nombre, cantidad, precio = producto
    if cantidad_vendida > cantidad:
        print(f"No hay suficiente stock. Stock disponible: {cantidad}")
        return

    total = cantidad_vendida * precio
    nueva_cantidad = cantidad - cantidad_vendida

    # Actualizar stock
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))

    # Registrar venta
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO ventas (producto_id, cantidad, total, fecha)
        VALUES (?, ?, ?, ?)
    ''', (id_producto, cantidad_vendida, total, fecha))

    conexion.commit()
    conexion.close()
    print(f"Venta realizada correctamente. Producto: {nombre}, Cantidad: {cantidad_vendida}, Total: {total:.2f} €")

def consultar_historial_ventas():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT v.id, p.nombre, v.cantidad, v.total, v.fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    ''')
    ventas = cursor.fetchall()
    conexion.close()

    if ventas:
        print("\nHistorial de ventas:")
        print("-" * 60)
        for venta in ventas:
            print(f"ID Venta: {venta[0]}, Producto: {venta[1]}, Cantidad: {venta[2]}, Total: {venta[3]:.2f}, Fecha: {venta[4]}")
    else:
        print("No hay ventas registradas.")

# Menú principal
def menu():
    while True:
        print("\nGestión de Inventarios")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Filtrar productos por cantidad")
        print("7. Consultar estadísticas")
        print("8. Realizar venta")
        print("9. Consultar historial de ventas")
        print("10. Salir")

        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            # Validar entrada del nombre
            while True:
                nombre = input("Nombre del producto: ").strip()
                if nombre:
                    break
                print("El nombre no puede estar vacío. Por favor, intenta de nuevo.")

            # Validar entrada de la descripción (opcional)
            descripcion = input("Descripción (puede dejarse en blanco): ").strip()

            # Validar entrada de la cantidad
            while True:
                try:
                    cantidad = int(input("Cantidad: ").strip())
                    if cantidad >= 0:
                        break
                    print("La cantidad debe ser un número entero positivo.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número entero.")

            # Validar entrada del precio
            while True:
                try:
                    precio = float(input("Precio: ").strip())
                    if precio > 0:
                        break
                    print("El precio debe ser un número positivo.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número válido.")

            # Agregar el producto al inventario
            agregar_producto(nombre, descripcion, cantidad, precio)
            input("Pulsa Enter para continuar.")
        elif opcion == "2":
            listar_productos()

            input("Pulsa Enter para continuar.")
        elif opcion == "3":
            nombre = input("Nombre del producto a buscar: ")
            productos = buscar_producto(nombre)
            if productos:
                for producto in productos:
                    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[3]}, Precio: {producto[4]:.2f}")
            else:
                print("No se encontraron productos.")

            input("Pulsa Enter para continuar.")
        elif opcion == "4":
        # Validar el ID del producto
            while True:
                try:
                    id_producto = int(input("ID del producto a actualizar: "))
                    conexion = conectar_db()
                    cursor = conexion.cursor()
                    cursor.execute("SELECT COUNT(*) FROM productos WHERE id = ?", (id_producto,))
                    existe = cursor.fetchone()[0]
                    conexion.close()
                    if existe:
                        break  # Salir del bucle si el ID existe
                    else:
                        print("El producto con ese ID no existe. Inténtalo de nuevo.")
                except ValueError:
                    print("Debes introducir un número válido para el ID. Inténtalo de nuevo.")

            # Validar el campo a actualizar
            while True:
                campo = input("Campo a actualizar (nombre, descripcion, cantidad, precio): ").lower().strip()
                if campo in ["nombre", "descripcion", "cantidad", "precio"]:
                    break  # Salir del bucle si el campo es válido
                else:
                    print("El campo no es válido. Debes elegir entre: nombre, descripcion, cantidad o precio.")

            # Validar el nuevo valor según el tipo del campo
            while True:
                nuevo_valor = input(f"Introduce el nuevo valor para {campo}: ").strip()

                if campo == "precio":
                    try:
                        nuevo_valor = float(nuevo_valor)
                        if nuevo_valor > 0:  # Validar que el precio sea positivo
                            break
                        else:
                            print("El precio debe ser un valor positivo.")
                    except ValueError:
                        print("Debes introducir un valor numérico para el precio.")
                elif campo == "cantidad":
                    try:
                        nuevo_valor = int(nuevo_valor)
                        if nuevo_valor >= 0:  # Validar que la cantidad no sea negativa
                            break
                        else:
                            print("La cantidad no puede ser un número negativo.")
                    except ValueError:
                        print("Debes introducir un número entero para la cantidad.")
                elif campo in ["nombre", "descripcion"]:
                    if nuevo_valor:  # Validar que no esté vacío
                        break
                    else:
                        print(f"El campo {campo} no puede estar vacío.")

            # Llamar a la función de actualización
            actualizar_producto(id_producto, campo, nuevo_valor)
            input("Pulsa Enter para continuar.")


        elif opcion == "5":
            while True:
                try:
                    id_producto = int(input("ID del producto a eliminar: "))
                    conexion = conectar_db()
                    cursor = conexion.cursor()
                    cursor.execute("SELECT COUNT(*) FROM productos WHERE id = ?", (id_producto,))
                    existe = cursor.fetchone()[0]
                    conexion.close()
                    if existe:
                        break  # Salir del bucle si el ID existe
                    else:
                        print("El producto con ese ID no existe. Inténtalo de nuevo.")
                except ValueError:
                    print("Debes introducir un número válido para el ID. Inténtalo de nuevo.")
            eliminar_producto(id_producto)

            input("Pulsa Enter para continuar.")
        elif opcion == "6":
            while True:
                try:
                    min_cantidad = int(input("Cantidad mínima: ").strip())
                    if min_cantidad > 0:
                        break
                    print("La cantidad debe ser un número positivo.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número válido.")

            while True:
                try:
                    max_cantidad = int(input("Cantidad máxima: ").strip())
                    if max_cantidad > 0:
                        break
                    print("La cantidad debe ser un número positivo.")
                except ValueError:
                    print("Entrada no válida. Por favor, introduce un número válido.")

            filtrar_productos_por_cantidad(min_cantidad, max_cantidad)

            input("Pulsa Enter para continuar.")
        elif opcion == "7":
            consultar_estadisticas()

            input("Pulsa Enter para continuar.")
        elif opcion == "8":
            while True:
                try:
                    id_producto = int(input("ID del producto a vender: "))
                    break  # Salir del bucle si la entrada es válida
                except ValueError:
                    print("Debes introducir un número válido para el ID.")

            while True:
                try:
                    cantidad_vendida = int(input("Cantidad a vender: "))
                    if cantidad_vendida > 0:
                        break  # Salir del bucle si la cantidad es válida
                    else:
                        print("La cantidad debe ser un número positivo.")
                except ValueError:
                    print("Debes introducir un número válido para la cantidad.")

            realizar_venta(id_producto, cantidad_vendida)

            input("Pulsa Enter para continuar.")
        elif opcion == "9":
            consultar_historial_ventas()

            input("Pulsa Enter para continuar.")
        elif opcion == "10":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
