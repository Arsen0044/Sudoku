from tkinter import *
from tkinter import ttk

SUDOKU = [[2,3,0,5,0,0,4,0,0],
          [0,0,0,0,0,0,0,0,3],
          [0,0,7,0,6,0,0,1,0],
          [0,8,0,0,0,6,0,3,1],
          [3,1,0,4,0,5,0,0,0],
          [0,0,2,0,0,0,0,0,0],
          [8,0,0,0,0,4,0,6,0],
          [9,2,4,6,0,0,0,0,0],
          [1,0,5,0,8,9,0,0,0]]
fail = 0
frame_list = []
end_list = []

# Створення самого судоку
class create_sudoku_square():

    def __init__(self,sudoku,row,col,grid_row_frame,grid_col_frame,counter):
        frame = ttk.Frame(window, style='My.TFrame')
        frame.configure(style='My.TFrame', borderwidth=2, relief='solid')
        frame.grid(row=grid_row_frame, column=grid_col_frame)
        end_list.append(frame)
        grid_row = 0
        grid_col = 0
        entry_list = []
        for _ in range(9):
            var = IntVar()
            str_var = StringVar()
            entry = Entry(frame, width=3, validate='all', validatecommand=(vcmd, "%P"),font=("Consolas",15))
            if sudoku[row][col] != 0:
                var.set(sudoku[row][col])
                entry.config(state='readonly', textvariable=var)
            else:
                entry.config(textvariable=str_var)
                entry.bind("<Return>", lambda event, e=entry, r=row, c=col, v=str_var: on_enter(event, e, r, c, v))
            col += 1
            if col == counter:
                row += 1
                col = counter-3
            entry.grid(row=grid_row, column=grid_col)
            entry_list.append(entry)
            grid_col += 1
            if grid_col == 3:
                grid_row += 1
                grid_col = 0
        frame_list.append(entry_list)

# Функція яка не дає ввести нічого крім 1-9
def check_symbol(P):
    if str.isdigit(P) and P != "":
        if int(P) == 0:
            return False
    if len(P) > 1:
        return False
    elif str.isdigit(P) or P == "":
        return True
    else:
        return False

# Перевірка на правильність вписаної цифри
def on_enter(event, entry, row, col, var):
    global solved_sudoku, fail
    if var.get() != "":
        text = int(var.get())
        if solved_sudoku[row][col] == text:
            var.set(solved_sudoku[row][col])
            entry.config(state='readonly')
        else:
            label = Label(window,image=foto,width=15,height=15)
            label.grid(row=3,column=fail)
            fail += 1
            if fail == 3:
                for frame in end_list:
                    frame.destroy()
                    end_label = Label(window,height=4, width=12,text="GAME OVER",font=("Consolas",40),fg='red')
                    end_label.grid(row=0,column=0,rowspan=3,columnspan=3)

# Вивід розвязаного судоку
def print_solved_sudoku(event,s):
    global frame_list
    row = 0
    col = 0
    for frame in frame_list:
        local_row = row
        local_col = col
        for entry in frame:
            x = IntVar()
            entry.config(textvariable=x,state='readonly')
            x.set(s[local_row][local_col])
            local_col += 1
            if local_col == col+3:
                local_row += 1
                local_col = col
        col += 3
        if col == 9:
            row += 3
            col = 0

# Перевірка чи можна поставити передану цифру в певну клітинку
def is_safe(sudoku,row,col,num):
    for i in sudoku[row]:
        if i == num:
            return False
    for i in range(9):
        if sudoku[i][col] == num:
            return False

    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if sudoku[i][j] == num:
                return False

    return True

# Розвязання судоку
def solve(sudoku,row,col):
    if col == 9:
        row += 1
        if row == 9:
            return sudoku
        col = 0
    if sudoku[row][col] != 0:
        return solve(sudoku,row,col+1)
    for num in range(1,10):
        if is_safe(sudoku,row,col,num):
            sudoku[row][col] = num
            result = solve(sudoku,row, col+1)
            if result:
                return result
            sudoku[row][col] = 0


window = Tk()
window.config(background='#FFFFFF')
window.resizable(False,False)
style = ttk.Style()
style.configure('My.TFrame', background='black')
vcmd = window.register(check_symbol)
foto = PhotoImage(file='img_10.png')

sudoku_1 = create_sudoku_square(SUDOKU,0,0,0,0,3)
sudoku_2 = create_sudoku_square(SUDOKU,0,3,0,1,6)
sudoku_3 = create_sudoku_square(SUDOKU,0,6,0,2,9)
sudoku_4 = create_sudoku_square(SUDOKU,3,0,1,0,3)
sudoku_5 = create_sudoku_square(SUDOKU,3,3,1,1,6)
sudoku_6 = create_sudoku_square(SUDOKU,3,6,1,2,9)
sudoku_7 = create_sudoku_square(SUDOKU,6,0,2,0,3)
sudoku_8 = create_sudoku_square(SUDOKU,6,3,2,1,6)
sudoku_9 = create_sudoku_square(SUDOKU,6,6,2,2,9)

solved_sudoku = solve(SUDOKU,0,0)
window.bind("<space>", lambda event,s=solved_sudoku: print_solved_sudoku(event,s))

window.mainloop()