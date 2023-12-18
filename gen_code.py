import random
import string

def generic_code():
    code = ""
    len_code = random.randint(5, 15)
    for i in range(len_code):
        choises = random.randint(0, 3)
        if choises == 0:
            symbol = str(random.randint(1, 10))
            code += symbol
        else:
            word = random.choice(string.ascii_lowercase)
            code += word

    final_code = ""
    for sym in code:
        choises = random.randint(0, 2)
        if choises == 0:
            sym = sym.upper()
            final_code += sym
        else:
            final_code += sym

    return final_code