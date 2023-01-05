from client.aniadirpedidosgui import VentanaPedido
import tkinter as tk
from tkinter import ttk
from BD.aplicacion_dao import *


def barra_menu(root):

    def cerrar_conexion():
        conexion.close()

    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width = 300, height = 300)
    menu_inicio = tk.Menu(barra_menu, tearoff = 0)
    menu_insertar = tk.Menu(barra_menu, tearoff= 0)
    menu_borrar = tk.Menu(barra_menu, tearoff= 0)
    barra_menu.add_cascade(label = 'Inicio', menu = menu_inicio)
    menu_inicio.add_command(label='Crear tabla stock en DB', command= crear_tabla_stock)
    menu_inicio.add_command(label = 'Crear tabla pedido en DB', command= crear_tabla_pedido)
    menu_inicio.add_command(label='Crear tabla detalle-pedido en DB', command= crear_tabla_detapedido)
    menu_inicio.add_command(label='Salir', command = root.destroy)
    menu_inicio.add_command(label="Cerrar conexión", command= cerrar_conexion)
    barra_menu.add_cascade(label = 'Insertar', menu = menu_insertar)
    menu_insertar.add_command(label= 'Insertar 10 tuplas predefinidas en tabla stock', command= insertar_tuplas_tabla_stock)
    barra_menu.add_cascade(label= 'Borrar', menu= menu_borrar)
    menu_borrar.add_command(label='Borrar tabla stock', command= borra_stock)
    menu_borrar.add_command(label='Borrar tabla pedido', command= borra_pedido)
    menu_borrar.add_command(label='Borrar tabla detalle-pedido', command= borra_detapedido)


class Frame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width = 480, height = 320)
        self.root = root
        self.pack()
        self.config(background='#E4CFFF')
        self.campos_detapedido()
        self.deshabilitar_campos()

    def campos_detapedido(self):
        
        #Nombres de cada campo
        self.label_nombre = tk.Label(self, text = 'Nombre de cliente: ')
        self.label_nombre.config(font = ('Arial', 12, 'bold'))
        self.label_nombre.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.label_producto = tk.Label(self, text = 'Código del producto: ')
        self.label_producto.config(font = ('Arial', 12, 'bold'))
        self.label_producto.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.label_cantidad = tk.Label(self, text = 'Cantidad: ')
        self.label_cantidad.config(font = ('Arial', 12, 'bold'))
        self.label_cantidad.grid(row = 2, column = 0, padx = 10, pady = 10)
        
        #datos de entrada
        self.mi_nombre = tk.StringVar();
        self.entrada_nombre = tk.Entry(self, textvariable= self.mi_nombre)
        self.entrada_nombre.config(width = 50, font=('Arial', 12))
        self.entrada_nombre.grid(row = 0, column = 1, padx = 10, pady = 10, columnspan= 2)

        self.mi_producto = tk.StringVar()
        self.entrada_producto = tk.Entry(self, textvariable= self.mi_producto)
        self.entrada_producto.config(width = 50, font=('Arial', 12))
        self.entrada_producto.grid(row = 1, column = 1, padx = 10, pady = 10, columnspan= 2)

        self.mi_cantidad = tk.StringVar()
        self.entrada_cantidad = tk.Entry(self, textvariable= self.mi_cantidad)
        self.entrada_cantidad.config(width = 50, font=('Arial', 12))
        self.entrada_cantidad.grid(row = 2, column = 1, padx = 10, pady = 10, columnspan= 2)

        #botones para las entradas
        self.boton_nuevo = tk.Button(self, text = "Nuevo pedido", command = self.habilitar_campos)
        self.boton_nuevo.config(width = 20, font = ('Arial', 12, 'bold'), fg = 'white', 
                                bg = '#1296D8', cursor='hand2', activebackground = '#12C0D8', 
                                activeforeground= 'white')
        self.boton_nuevo.grid(row = 3 , column = 0, padx = 10, pady = 10)

        
        self.boton_guardar = tk.Button(self, text = "Guardar", command = self.guardar_pedido)
        self.boton_guardar.config(width = 20, font = ('Arial', 12, 'bold'), fg = 'white', 
                                bg = '#406340', cursor='hand2', activebackground = '#97E797', 
                                activeforeground= 'white')
        self.boton_guardar.grid(row = 3 , column = 1, padx = 10, pady = 10)

        self.boton_cancelar = tk.Button(self, text = "Cancelar", command = self.deshabilitar_campos)
        self.boton_cancelar.config(width = 20, font = ('Arial', 12, 'bold'), fg = 'white', 
                                bg = '#630303', cursor='hand2', activebackground = '#FF0000', 
                                activeforeground= 'white')
        self.boton_cancelar.grid(row = 3 , column = 2, padx = 10, pady = 10)

        #botones para ver las tablas
        self.tstock = tk.Button(self, text = "Tabla Stock", command = self.tabla_stock)
        self.tstock.config(width = 20, font = ('Arial', 12, 'bold'), fg = 'white', 
                                bg = '#D38805', cursor='hand2', activebackground = '#FFA303', 
                                activeforeground= 'white')
        self.tstock.grid(row = 4 , column = 0, padx = 10, pady = 10)

        self.tpedido = tk.Button(self, text = "Tabla Pedido", command = self.tabla_pedido)
        self.tpedido.config(width = 20, font = ('Arial', 12, 'bold'), fg = 'white', 
                                bg = '#D38805', cursor='hand2', activebackground = '#FFA303', 
                                activeforeground= 'white')
        self.tpedido.grid(row = 4 , column = 1, padx = 10, pady = 10)

        self.tdetapedido = tk.Button(self, text = "Tabla Detalle_Pedido", command = self.tabla_detalle_pedido)
        self.tdetapedido.config(width = 20, font = ('Arial', 12, 'bold'), fg = 'white', 
                                bg = '#D38805', cursor='hand2', activebackground = '#FFA303', 
                                activeforeground= 'white')
        self.tdetapedido.grid(row = 4 , column = 2, padx = 10, pady = 10)



    def habilitar_campos(self):
        #campos vacios
        self.mi_nombre.set('')
        self.mi_cantidad.set('')
        self.mi_producto.set('')

        #habilitar funciones
        self.entrada_nombre.config(state='normal')
        self.entrada_cantidad.config(state='normal')
        self.entrada_producto.config(state='normal')

        self.boton_guardar.config(state='normal')
        self.boton_cancelar.config(state='normal')

    def deshabilitar_campos(self):
        #campos vacios
        self.mi_nombre.set('')
        self.mi_cantidad.set('')
        self.mi_producto.set('')

        #deshabilitar funciones
        self.entrada_nombre.config(state='disabled')
        self.entrada_cantidad.config(state='disabled')
        self.entrada_producto.config(state='disabled')

        self.boton_guardar.config(state='disabled')
        self.boton_cancelar.config(state='disabled')

    def guardar_pedido(self):

        pedido = Pedido(
            self.mi_nombre.get(),
            self.mi_producto.get(),
            self.mi_cantidad.get(),
        )

        comprobacion = guardar_pedido(pedido)
            
        if comprobacion:
            ventana = tk.Tk()
            ventana.title("Seguir añadiendo pedidos")
            funciones = VentanaPedido(ventana)

        self.deshabilitar_campos()

    def tabla_stock(self):
        self.lista_stock = listar("stock")

        self.deshabilitar_campos()
        self.tabla_stock = ttk.Treeview(self, column=('Cproducto','Cantidad'))
        self.tabla_stock.grid(row= 5, column = 0, columnspan = 4, padx=10, pady=10)
        self.tabla_stock.heading('#1', text='Cproducto')
        self.tabla_stock.heading('#2', text='Cantidad')

        #iteramos la lista
        for i in self.lista_stock:
            self.tabla_stock.insert('', 0, text = '', values = (i[0], i[1]))

    def tabla_pedido(self):
        self.lista_pedido = listar("pedido")

        self.deshabilitar_campos()
        self.tabla_pedido = ttk.Treeview(self, column = ('Ccliente, Fecha-pedido'))
        self.tabla_pedido.grid(row=5, column=0, columnspan= 4, padx= 10, pady= 10)
        self.tabla_pedido.heading('#0', text='Cpedido')
        self.tabla_pedido.heading('#1', text='Ccliente')
        self.tabla_pedido.heading('#2', text='Fecha-pedido')
        #iteramos la lista
        for i in self.lista_pedido:
            self.tabla_pedido.insert('', 0, text = i[0], values = (i[1], i[2]))
        
    def tabla_detalle_pedido(self):
        self.lista_detallepedido = listar("detallepedido")

        self.deshabilitar_campos()
        self.tabla_detpedido = ttk.Treeview(self, column = ('Cpedido, Cantidad'))
        self.tabla_detpedido.grid(row=5, column=0, columnspan= 4, padx= 10, pady= 10)
        self.tabla_detpedido.heading('#0', text='Cproducto')
        self.tabla_detpedido.heading('#1', text='Cpedido')
        self.tabla_detpedido.heading('#2', text='Cantidad')
        #iteramos la lista
        for i in self.lista_detallepedido:
            self.tabla_detpedido.insert('', 0, text = i[0], values = (i[1], i[2]))
