from client.gui import *

def main():
     
     root = tk.Tk()
     root.title('Conexion base de datos')
     root.config(background='#E4CFFF')
     barra_menu(root)

     app = Frame(root = root)
     app.mainloop()

if __name__ == '__main__':
    main()