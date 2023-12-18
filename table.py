import gspread
from gen_code import generic_code

gs = gspread.service_account(filename="cred.json")
sheets = gs.open_by_url('https://docs.google.com/spreadsheets/d/1hoTP5VCkJWlD0H_0-2BOWtnZcXeqOLOO5u-3_Oq0OzM/edit?hl=ru#gid=0').worksheets()

def check_unn(unn, total_price):


    get_val = sheets[0].get_all_values()
    for mas in get_val[1:]:
        if int(mas[0]) == unn and int(mas[1]) < total_price:
           return generic_code()

def check_number(number_phone):
    get_number = sheets[1].col_values(1)
    for number in get_number[1:]:
        if int(number) == int(number_phone):
            return True
