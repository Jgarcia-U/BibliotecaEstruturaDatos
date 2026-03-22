import tkinter as tk
from frontend.gui import BibliotecaGUI

def main():
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
