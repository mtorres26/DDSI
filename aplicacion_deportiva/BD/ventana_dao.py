import BD.aplicacion_dao as ad
from tkinter import messagebox
from datetime import date

def aniadir_detapedido(pedido):
    
    fecha = date.today()

    try:
        
        #CONSULTAMOS LA CANTIDAD QUE HAY DISPONIBLE DEL PRODUCTO SOLICITADO
        sql = """SELECT * FROM stock WHERE Cproducto = %s"""
        ad.cursor.execute(sql, (pedido.cproducto,))
        consulta = ad.cursor.fetchall()
        cantidad_producto = int(consulta[0][1])
        cantidad_total = cantidad_producto - int(pedido.cantidad)

        if cantidad_total< 0:
            titulo = "Guardar pedido"
            mensaje = "No se ha podido relizar el pedido debido a que solo hay " 
            + cantidad_producto + " del producto " + consulta["Cproducto"]
            messagebox.showwarning(titulo, mensaje)

        else:
            #ACTUALIZAMOS LA NUEVA CANTIDAD DE LA TUPLA CORRESPONDIENTE EN LA TABLA stock
            new_cantidad_producto = cantidad_producto - int(pedido.cantidad)
            sql = """ UPDATE stock SET Cantidad=%s WHERE Cproducto=%s """
            ad.cursor.execute(sql,(new_cantidad_producto, pedido.cproducto))

            #ALMACENAMOS DETALLES DEL PEDIDO
            sql = """SELECT * FROM pedido WHERE (Ccliente=%s) AND (Fecha=%s)"""
            ad.cursor.execute(sql, (pedido.nombre, fecha))
            consulta = ad.cursor.fetchall()

            sql = """INSERT INTO detallepedido(Cproducto, Cpedido, Cantidad) VALUES (%s,%s,%s)"""
            ad.cursor.execute(sql, (pedido.cproducto, consulta[0][0], pedido.cantidad))


            titulo = "Guardar pedido"
            mensaje = "La operacion se ha realizado correctamente"
            messagebox.showinfo(titulo, mensaje)
            comprobacion = True


    except:
        titulo = "Guardar pedido"
        mensaje = "Ha habido algún fallo y no se ha realizado la operacion"
        messagebox.showerror(titulo, mensaje)

    




def eliminar_detalles():
    sql = " ROLLBACK TO SAVEPOINT primerpedido"
    ad.cursor.execute(sql)


def guardar_perm():
    print("hola")
    ad.conexion.commit()

def borrar_todo():
    sql = "ROLLBACK TO SAVEPOINT borrartodo"
    ad.cursor.execute(sql)
    

