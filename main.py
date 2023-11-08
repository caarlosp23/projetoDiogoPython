if __name__ == "__main__":
    import tkinter as tk
    from controller import *
    from config import DB_CONFIG

    root = tk.Tk()
    useradmin = 'teste'
    controller = LoginController(root,DB_CONFIG) 

    #controller = CadastroCategoriaController(root) 
    root.mainloop()

#root,useradmin