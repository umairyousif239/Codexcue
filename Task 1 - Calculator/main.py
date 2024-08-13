import tkinter as tk

#Defining the functions
calculation = ""

def add_to_calculation(symbol):
    global calculation
    calculation += str(symbol)
    text_result.delete(1.0, "end")
    text_result.insert(1.0, calculation)

def evaluate_calculation():
    global calculation
    try:
        calculation = str(eval(calculation))
        text_result.delete(1.0, "end")
        text_result.insert(1.0, calculation)
    except:
        clear_field()
        text_result.insert(1.0, "Error")

def clear_field():
    global calculation
    calculation = ""
    text_result.delete(1.0, "end")

def delete_btn():
    global calculation
    if calculation:
        calculation = calculation[:-1]
        text_result.delete(1.0, "end")
        text_result.insert(1.0, calculation)

def create_button(root, text, command, row, column):
    button = tk.Button(root, text=text, command=command, width=5, font=("Arial", 14), bg=btn_color, fg=btn_fg_color, borderwidth=0)
    button.grid(row=row, column=column, padx=2, pady=2)
    return button

#GUI Properties
root = tk.Tk()
root.title("Calculator")

width = 296
height = 275
root.geometry(f"{width}x{height}")
root.resizable(False, False)

#Button customization and color
bg_color = "#333333"
fg_color = "#FFFFFF"
btn_color = "#444444"
btn_fg_color = "#FFFFFF"

root.configure(bg=bg_color)

text_result = tk.Text(root, height=2, width=16, font=("Arial", 24), bg=bg_color, fg=fg_color, borderwidth=0) 
text_result.grid(columnspan=5)

#Buttons
buttons = [
    ('C', clear_field, 2, 1), ('.', lambda: add_to_calculation("."), 2, 2), ('<', delete_btn, 2, 3), ('÷', lambda: add_to_calculation("/"), 2, 4),
    ('7', lambda: add_to_calculation(7), 3, 1), ('8', lambda: add_to_calculation(8), 3, 2), ('9', lambda: add_to_calculation(9), 3, 3), ('*', lambda: add_to_calculation("*"), 3, 4),
    ('4', lambda: add_to_calculation(4), 4, 1), ('5', lambda: add_to_calculation(5), 4, 2), ('6', lambda: add_to_calculation(6), 4, 3), ('-', lambda: add_to_calculation("-"), 4, 4),
    ('1', lambda: add_to_calculation(1), 5, 1), ('2', lambda: add_to_calculation(2), 5, 2), ('3', lambda: add_to_calculation(3), 5, 3), ('+', lambda: add_to_calculation("+"), 5, 4),
    ('(', lambda: add_to_calculation("("), 6, 1), ('0', lambda: add_to_calculation(0), 6, 2), (')', lambda: add_to_calculation(")"), 6, 3), ('=', evaluate_calculation, 6, 4)
]

for text, command, row, column in buttons:
    create_button(root, text, command, row, column)

root.mainloop()
