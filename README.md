Gestión de Inventarios con SQLite

Este proyecto es una aplicación en Python para gestionar inventarios de productos. Incluye funciones para agregar, buscar, actualizar y eliminar productos, además de consultar estadísticas, realizar ventas y llevar un historial de transacciones. La base de datos utilizada es SQLite.
Características

    Gestión de productos:
        Agregar nuevos productos con nombre, descripción, cantidad y precio.
        Listar todos los productos en el inventario.
        Buscar productos por nombre.
        Actualizar información de productos existentes.
        Eliminar productos del inventario.
    Funciones avanzadas:
        Filtrar productos según criterios (por cantidad o rango de precio).
        Consultar estadísticas del inventario: cantidad total de productos y valor total.
    Gestión de ventas:
        Registrar ventas con control de stock.
        Consultar el historial de ventas, con detalles de cada transacción.

Requisitos

    Python 3.x
    SQLite3 (se incluye con Python por defecto)

Instalación

    Clona el repositorio:

git clone https://github.com/tuusuario/nombre-del-repositorio.git
cd nombre-del-repositorio

Asegúrate de tener Python instalado y ejecuta el script:

python main.py


Estructura del Proyecto

    main.py: Archivo principal que contiene el menú y las funciones CRUD.
    database.db: Archivo SQLite donde se almacenan los datos del inventario y las ventas (se genera automáticamente).