from tkinter import *
def key_pressed(event):
    key_sym = event.keysym
    print("Код клавіші:", key_sym)

# Приклад використання
root = Tk()
root.bind('<KeyPress>', key_pressed)
root.mainloop()