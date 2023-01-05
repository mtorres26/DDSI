import mysql.connector
from tkinter import messagebox
from datetime import date


conexion =  mysql.connector.connect(
            host='localhost', #contraseña
            port='3306', #puerto 
            user='ddsi', #usuario de mysql al que conectarse
            password='1234', #contraseña
            db='aplicacion' #base de datos a la que conectarse dentro de mysql
            )

cursor = conexion.cursor()
    

#Función que crea la tabla stock
def crear_tabla_stock():
    sql = '''
    CREATE TABLE stock(
        Cproducto INTEGER PRIMARY KEY,
        Cantidad INTEGER NOT NULL
    );    
    ''' #Sentencia sql que vamos a utilizar para ejecutar con el cursor del objeto conexion que hemos creado en el archivo database.py
    
    try:
        cursor.execute(sql)
        conexion.commit()
        titulo = 'Crear tabla stock'
        mensaje = 'Se creo la tabla en la base de datos'
        messagebox.showinfo(titulo, mensaje)

    except:
        titulo = 'Crear tabla stock'
        mensaje = 'La tabla stock ya esta creada'
        messagebox.showinfo(titulo, mensaje)

""""""
#Crea la tabla pedido
def crear_tabla_pedido():
    sql = '''
    CREATE TABLE pedido(
        Cpedido INTEGER PRIMARY KEY AUTO_INCREMENT,
        Ccliente VARCHAR(30) NOT NULL,
        Fecha DATE
    );
    '''
    try:
        cursor.execute(sql)
        conexion.commit()
        titulo = 'Crear tabla pedido'
        mensaje = 'Se creo la tabla en la base de datos'
        messagebox.showinfo(titulo, mensaje)

    except:
        titulo = 'Crear tabla pedido'
        mensaje = 'La tabla ya esta creada'
        messagebox.showinfo(titulo, mensaje)


#Crea la tabla deta-pedido
def crear_tabla_detapedido():
    sql = '''
    CREATE TABLE detallepedido(
        Cproducto INTEGER,
        Cpedido INTEGER, 
        Cantidad INTEGER NOT NULL,
        FOREIGN KEY (Cproducto) REFERENCES stock(Cproducto) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (Cpedido) REFERENCES pedido(Cpedido) ON DELETE CASCADE ON UPDATE CASCADE,
        PRIMARY KEY (Cproducto, Cpedido)
    );
    '''
    try:
        cursor.execute(sql)
        conexion.commit()
        titulo = 'Crear tabla detalle-pedido'
        mensaje = 'Se creo la tabla en la base de datos'
        messagebox.showinfo(titulo, mensaje)

    except:
        titulo = 'Crear tabla detalle-pedido'
        mensaje = 'La tabla ya esta creada'
        messagebox.showinfo(titulo, mensaje)


def borrar_tabla(n_tabla):
    if type(n_tabla) == str:

        try:
            sql = 'DROP TABLE ' + n_tabla
            cursor.execute(sql)
            conexion.commit()
            titulo = 'Borrar tabla ' + n_tabla
            mensaje = 'La tabla se ha borrado'
            messagebox.showinfo(titulo, mensaje)
        except:
            titulo = 'Crear tabla ' + n_tabla
            mensaje = 'La tabla ya esta borrada o borrar primero deta-pedido'
            messagebox.showinfo(titulo, mensaje)
       

borra_stock = lambda: borrar_tabla('stock')
borra_pedido = lambda: borrar_tabla('pedido')
borra_detapedido = lambda: borrar_tabla('detallepedido')

#Clase para obtener los pedidos que ingresa la gente
class Pedido:
    def __init__(self, nombre, cproducto, cantidad):
        self.cpedido = None
        self.nombre = nombre
        self.cproducto = cproducto
        self.cantidad = cantidad

    def __str__(self):
        return 'Pedido[{self.nombre}, {self.cproducto}, {self.cantidad}]'

#Funcion que inserta las 10 tuplas predefinidas de la tabla stock
def insertar_tuplas_tabla_stock():
    try:
        cantidad = int(20)
        
        for i in range(10):

            sql = """INSERT INTO stock(Cproducto,Cantidad) VALUES(%s, %s)"""
            
            cursor.execute(sql, (i, cantidad))
            cantidad= cantidad * 2

        print('Aqui ha llegado')
        conexion.commit()
        titulo = "Inserción de tuplas tabla stock"
        mensaje = "Se han guardado las tuplas"
        messagebox.showinfo(titulo, mensaje) 
    
    except:
        titulo = "Inserción de tuplas tabla stock"
        mensaje = "Las tuplas ya han sido insertadas"
        messagebox.showerror(titulo, mensaje)


#Funcion que se encarga de cuando un usuario le da a guardar se inserte el pedido en la base de datos y los respectivos cambios
def guardar_pedido(pedido):
    comprobacion = False
    savepoint = "SAVEPOINT borrartodo"
    cursor.execute(savepoint)
    try:
        fecha = date.today()
        
        #ALMACENAMOS NUEVO PEDIDO EN TABLA pedido
        sql = """INSERT INTO pedido(Ccliente, Fecha) VALUES(%s, %s)"""
        cursor.execute(sql,(pedido.nombre, fecha))
        
        #CONSULTAMOS LA CANTIDAD QUE HAY DISPONIBLE DEL PRODUCTO SOLICITADO
        sql = """SELECT * FROM stock WHERE Cproducto = %s"""
        cursor.execute(sql, (pedido.cproducto,))
        consulta = cursor.fetchall()
        cantidad_producto = int(consulta[0][1])
        cantidad_total = cantidad_producto - int(pedido.cantidad)

        if cantidad_total< 0:
            titulo = "Guardar pedido"
            mensaje = "No se ha podido relizar el pedido debido a que solo hay " 
            + cantidad_producto + " del producto " + consulta["Cproducto"]
            messagebox.showwarning(titulo, mensaje)
            conexion.rollback()

        else:
            #ACTUALIZAMOS LA NUEVA CANTIDAD DE LA TUPLA CORRESPONDIENTE EN LA TABLA stock
            new_cantidad_producto = cantidad_producto - int(pedido.cantidad)
            sql = """ UPDATE stock SET Cantidad=%s WHERE Cproducto=%s """
            cursor.execute(sql,(new_cantidad_producto, pedido.cproducto))

            #ALMACENAMOS DETALLES DEL PEDIDO
            sql = """SELECT * FROM pedido WHERE (Ccliente=%s) AND (Fecha=%s)"""
            cursor.execute(sql, (pedido.nombre, fecha))
            consulta = cursor.fetchall()

            savepoint = "SAVEPOINT primerpedido"
            cursor.execute(savepoint)

            sql = """INSERT INTO detallepedido(Cproducto, Cpedido, Cantidad) VALUES (%s,%s,%s)"""
            cursor.execute(sql, (pedido.cproducto, consulta[0][0], pedido.cantidad))

            cpedido = consulta[0][0]
            print(cpedido)

            titulo = "Guardar pedido"
            mensaje = "La operacion se ha realizado correctamente"
            messagebox.showinfo(titulo, mensaje)
            comprobacion = True


    except:
        titulo = "Guardar pedido"
        mensaje = "Ha habido algún fallo y no se ha realizado la operacion"
        messagebox.showerror(titulo, mensaje)

    return comprobacion

#Funcion que se encarga de mostrar el contenido de las tablas
def listar(tabla):
    lista_tabla = []
    sql = 'SELECT * FROM ' + tabla
    
    try:
        cursor.execute(sql)
        lista_tabla = cursor.fetchall()
    except:
        titulo = 'Conexion a ' + tabla
        mensaje = 'Cree la base de datos ' + tabla
        messagebox.showerror(titulo, mensaje)
    return lista_tabla

listar_stock = lambda: listar('stock')
listar_pedido = lambda: listar('pedido')
listar_detapedido = lambda: listar('detallepedido')

    