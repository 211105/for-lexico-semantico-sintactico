import re
import tkinter as tk
from tkinter import messagebox

def lexer(code):
    tokens = []
    current_token = ""
    special_symbols = ["=", "<", ";", "+", ".", "(", ")", "{", "}"]
    keywords = ["for", "int", "system", "out", "println"]

    in_string = False  # Variable para rastrear si estamos dentro de una cadena

    line_number = 1
    variables = {}  # Almacén para rastrear las variables definidas

    for char in code:
        if char == "\"":
            if in_string:
                current_token += char
                tokens.append((line_number, "<CADENA " + current_token + ">"))
                current_token = ""
                in_string = False
            else:
                in_string = True
                current_token += char
        elif in_string:
            current_token += char
        elif char.isspace():
            if current_token:
                tokens.append((line_number, current_token))
                current_token = ""
        elif char in special_symbols:
            if current_token:
                tokens.append((line_number, current_token))
                current_token = ""
            tokens.append((line_number, "<simbolo: " + char + ">"))
        else:
            current_token += char

        if char == "\n":
            line_number += 1

    if current_token:
        tokens.append((line_number, current_token))

    arr = [token[1] for token in tokens]

    for i, token in enumerate(tokens):
        line_number, token_value = token
        if token_value in keywords:
            tokens[i] = (line_number, "<" + token_value.upper() + ">")
        elif re.match(r"^[0-9]+$", token_value):
            tokens[i] = (line_number, "<NUM>" + token_value)

    for i, token in enumerate(tokens):
        line_number, token_value = token
        if token_value == "<INT>" and tokens[i+2][1] == "<simbolo: =>":
            var_name = tokens[i+1][1]
            variables[var_name] = True
        elif re.match(r"^[a-zA-Z]+$", token_value) and token_value not in keywords and token_value not in special_symbols:
            if token_value not in variables:
                error_message(f"Variable '{token_value}' no declarada", line_number)

    for i, token in enumerate(tokens):
        line_number, token_value = token
        if token_value in variables and token_value != "<INT>":
            variables[token_value] = False

    for i, token in enumerate(tokens):
        line_number, token_value = token
        if token_value == "<INT>":
            var_name = tokens[i+1][1]
            if variables.get(var_name) is None:
                error_message(f"Variable '{var_name}' no declarada", line_number)
            else:
                variables[var_name] = True

    for var_name, used in variables.items():
        if not used:
            error_message(f"Variable '{var_name}' declarada pero no usada", line_number)

    return tokens

def error_message(message, line_number):
    messagebox.showerror("Error de sintaxis", f"{message}\nEn la línea {line_number}")

def process_code():
    code = code_text.get("1.0", "end-1c")
    tokens = lexer(code)
    result_text.delete("1.0", "end")
    for token in tokens:
        line_number, token_value = token
        result_text.insert("end", f"Linea {line_number}: {token_value}\n")

window = tk.Tk()
window.title("Lexer")
window.geometry("600x400")

code_label = tk.Label(window, text="Ingrese el código:")
code_label.pack()

code_text = tk.Text(window, height=10, width=50)
code_text.pack()

process_button = tk.Button(window, text="Procesar", command=process_code)
process_button.pack()

result_label = tk.Label(window, text="Tokens:")
result_label.pack()

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

window.mainloop()
