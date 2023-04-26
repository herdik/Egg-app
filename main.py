from tkinter import *
from customtkinter import *
import time
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


input_test = ""
current_dato = time.localtime()
monthly_profit = 0
monthly_losses = 0
id_item = 0

months_options = [
    "Január",
    "Február",
    "Marec",
    "Apríl",
    "Máj",
    "Jún",
    "Júl",
    "August",
    "September",
    "Október",
    "November",
    "December"
]

items_options = []
customers_options = []


# funckia pre aktuálny rok
def current_year_fun():
    current_year = current_dato[0]
    return current_year


# funckia pre int aktuálneho mesiaca
def current_month_fun():
    current_month_number = current_dato[1]
    my_calendar = {
        1: "Január",
        2: "Február",
        3: "Marec",
        4: "Apríl",
        5: "Máj",
        6: "Jún",
        7: "Júl",
        8: "August",
        9: "September",
        10: "Október",
        11: "November",
        12: "December"
    }
    current_month = my_calendar[current_month_number]
    return current_month


# funckia pre dátum pre entry a vloženie do tabuľky
def current_date_numbers_for_input_date():
    current_day = f"{current_dato[2]}.{current_dato[1]}.{current_dato[0]}"
    return current_day


def clicked_input_price_fun(e):
    input_price.delete(0, END)
    input_price.configure(text_color=text_color_input)


def add_items_press_button_add_item():
    global id_item
    table_date = input_date.get()
    # table_item = input_item.get().capitalize()
    table_item = drop_down_table_items.get() + "-" + drop_down_customer_losses.get()
    table_price = input_price.get()
    # ******* nastavenie dvojfarebných riadkov v tabuľke podla:
    # table.tag_configure("oddrow", background="#333")
    # table.tag_configure("evenrow", background="#4d4d4d")
    # *******

    if float(table_price) < 0:
        table.insert(parent="", index=END, iid=f"{id_item}", text="", values=(f"{table_date}", f"{table_item}",
                                                                              f"{table_price}"), tags=("minus", ))
    elif float(table_price) > 0:
        table.insert(parent="", index=END, iid=f"{id_item}", text="", values=(f"{table_date}", f"{table_item}",
                                                                              f"{table_price}"), tags=("plus",))
    else:
        pass

    input_price.delete(0, END)
    # input_item.insert(0, "Zadaj názov položky")
    # input_item.configure(text_color=temporary_input_font_color)
    input_price.insert(0, "Zadaj cenu")
    input_price.configure(text_color=temporary_input_font_color)
    current_month_label.focus()
    input_date.delete(0, END)
    input_date.insert(0, current_date_numbers_for_input_date())
    sort_out_table_by_date()


def delete_item_line_from_table():
    # [0] znamená pokiaľ p´má označený jeden alebo viacej prvkov tak vymaže prvok na pozácii 0, ak tam dám 1 tak vymaže
    # prvok na pozícii 1
    selected_item = table.selection()[0]
    table.delete(selected_item)


def clear_selected():
    # prechádzam všetky označené prvky
    # ak je prvok medzi označenými vymaž ho
    selected_items = table.selection()
    for one_selected in selected_items:
        table.delete(one_selected)


def clear_table():
    all_items = table.get_children()
    for one_item in all_items:
        table.delete(one_item)


def save_file_fun():
    empty_table = table.get_children()
    if len(empty_table) == 0:
        pass
    else:
        with open(f"{drop_down_month.get().lower() + str(drop_down_year.get())}.txt", mode="w") as file:
            my_items = table.get_children()
            for one_item in my_items:
                first_item = str(table.item(one_item)["values"][0])
                second_item = str(table.item(one_item)["values"][1])
                third_item = str(table.item(one_item)["values"][2])
                if first_item.endswith("\n") or second_item.endswith("\n") or third_item.endswith("\n"):
                    file.write(first_item)
                    file.write(second_item)
                    file.write(third_item)
                else:
                    file.write(first_item + "\n")
                    file.write(second_item + "\n")
                    file.write(third_item + "\n")


def reopen_saved_file():
    global id_item
    count = 0
    data = []
    data_values = []
    try:
        with open(f"{current_month_fun().lower() + str(current_year_fun())}.txt", mode="r") as file:
            for one_line in file:
                one_line = one_line.strip("\n")
                data_values.append(one_line)
                if len(data_values) == 3:
                    data.append(data_values)
                    data_values = []
                    if float(data[count][2]) < 0:
                        table.insert(parent="", index=END, iid=f"{id_item}", text="",
                                     values=(data[count][0], data[count][1], data[count][2]), tags=("minus", ))
                    elif float(data[count][2]) > 0:
                        table.insert(parent="", index=END, iid=f"{id_item}", text="",
                                     values=(data[count][0], data[count][1], data[count][2]), tags=("plus",))
                    else:
                        pass
                    count += 1
                    id_item += 1
    except:
        print("Súbor sa nenašiel")


def check_all_existing_files():
    all_years = []
    existing_file_in_year = []
    line_values = []
    prices = []
    yearly_profit = 0
    yearly_losses = 0
    my_calendar = {
        1: "Január",
        2: "Február",
        3: "Marec",
        4: "Apríl",
        5: "Máj",
        6: "Jún",
        7: "Júl",
        8: "August",
        9: "September",
        10: "Október",
        11: "November",
        12: "December"
    }
    checked_year = current_year_fun()

    while checked_year > 2021:
        for one_month in reversed(my_calendar):
            checked_month = my_calendar[one_month]
            try:
                with open(f"{checked_month + str(checked_year)}.txt", mode="r") as file:
                    # print(f"{checked_month + str(checked_year)}")
                    existing_file_in_year.append(int(checked_year))
                    for file_line in file:
                        file_line = file_line.strip("\n")
                        line_values.append(file_line)
                        if checked_year == current_year_fun():
                            if len(line_values) == 3:
                                prices.append(float(line_values[2]))
                                line_values = []
            except:
                # print(f"{checked_month + str(checked_year)} súbor sa nenašiel")
                pass
        checked_year -= 1

    existing_file_in_year = set(existing_file_in_year)
    existing_file_in_year = list(existing_file_in_year)
    for i in range(len(existing_file_in_year)):
        all_years.append(str(existing_file_in_year[i]))

    for one_price in prices:
        if one_price >= 0:
            yearly_profit += one_price
            if str(yearly_profit).endswith(".0"):
                yearly_profit = int(yearly_profit)
        else:
            yearly_losses += one_price
            if str(yearly_losses).endswith("0"):
                yearly_losses = int(yearly_losses)
    profit_label.configure(text=f"Príjmy         {yearly_profit}")
    losses_label.configure(text=f"Výdavky    {yearly_losses}")

    return all_years


def open_choosed_file():
    clear_table()
    count = 0
    data = []
    data_values = []
    try:
        with open(f"{drop_down_month.get().lower() + str(drop_down_year.get())}.txt", mode="r") as file:
            for one_line in file:
                one_line = one_line.strip("\n")
                data_values.append(one_line)
                if len(data_values) == 3:
                    data.append(data_values)
                    data_values = []
                    if float(data[count][2]) < 0:
                        table.insert(parent="", index=END, iid=f"{count}", text="",
                                     values=(data[count][0], data[count][1], data[count][2]), tags=("minus",))
                    elif float(data[count][2]) > 0:
                        table.insert(parent="", index=END, iid=f"{count}", text="",
                                     values=(data[count][0], data[count][1], data[count][2]), tags=("plus",))
                    else:
                        pass
                    count += 1
    except:
        print("Súbor sa nenašiel")

    line_values = []
    prices = []
    yearly_profit = 0
    yearly_losses = 0
    my_calendar = {
        1: "Január",
        2: "Február",
        3: "Marec",
        4: "Apríl",
        5: "Máj",
        6: "Jún",
        7: "Júl",
        8: "August",
        9: "September",
        10: "Október",
        11: "November",
        12: "December"
    }

    for one_month in reversed(my_calendar):
        checked_month = my_calendar[one_month]
        try:
            with open(f"{checked_month + str(drop_down_year.get())}.txt", mode="r") as file:
                # print(f"{checked_month + str(checked_year)}")
                for file_line in file:
                    file_line = file_line.strip("\n")
                    line_values.append(file_line)
                    if drop_down_year.get():
                        if len(line_values) == 3:
                            prices.append(float(line_values[2]))
                            line_values = []
        except:
            # print(f"{checked_month + str(checked_year)} súbor sa nenašiel")
            pass
    # existing_file_in_year = set(existing_file_in_year)
    # existing_file_in_year = list(existing_file_in_year)
    for one_price in prices:
        if one_price >= 0:
            yearly_profit += one_price
            if str(yearly_profit).endswith(".0"):
                yearly_profit = int(yearly_profit)
        else:
            yearly_losses += one_price
            if str(yearly_losses).endswith("0"):
                yearly_losses = int(yearly_losses)
    profit_label.configure(text=f"Príjmy         {yearly_profit}")
    losses_label.configure(text=f"Výdavky    {yearly_losses}")
    current_year_label.configure(text=f"Rok  {drop_down_year.get()}")
    monthly_profit_label.configure(text=f"Príjem za mesiac {drop_down_month.get()}")
    monthly_losses_label.configure(text=f"Výdavky za mesiac {drop_down_month.get()}")
    monthly_profit_label_value.configure(text=f"{update_monthly_profit_losses()[0]}")
    monthly_losses_label_value.configure(text=f"{update_monthly_profit_losses()[1]}")


def save_file_and_update_profit_and_losses():
    save_file_fun()
    check_all_existing_files()
    open_choosed_file()
    # monthly_profit_label_value.configure(text=f"{update_monthly_profit_losses()[0]}")
    # monthly_losses_label_value.configure(text=f"{update_monthly_profit_losses()[1]}")


def all_options_to_drop_down_table_items():
    with open("moje_položky.txt", mode="r") as file:
        for one_line in file:
            items_options.append(one_line.strip("\n"))
    return items_options


def all_options_to_drop_down_customer_or_new_item():
    with open("zákazníci.txt", mode="r") as file:
        for one_line in file:
            customers_options.append(one_line.strip("\n"))
    return customers_options


def sort_out_table_by_date():
    checking_table = []
    my_items = table.get_children()
    for one_item in my_items:
        first_item = str(table.item(one_item)["values"][0])
        second_item = str(table.item(one_item)["values"][1])
        third_item = str(table.item(one_item)["values"][2])
        checking_table.append((first_item, second_item, third_item))
    # usportiadanie podľa dátumu u listu podľa 0-tého parametru z tuple
    checking_table.sort(key=lambda x: x[0])
    clear_table()
    for index in range(len(checking_table)):
        if float(checking_table[index][2]) >= 0:
            table.insert(parent="", index=END, iid=f"{index}", text="", values=(checking_table[index][0],
                                                                                checking_table[index][1],
                                                                                checking_table[index][2]),
                         tags=("plus",))
        else:
            table.insert(parent="", index=END, iid=f"{index}", text="", values=(checking_table[index][0],
                                                                                checking_table[index][1],
                                                                                checking_table[index][2]),
                         tags=("minus",))


def update_monthly_profit_losses():
    my_line_values = []
    value_prices = []
    plus_values = 0
    minus_values = 0
    try:
        with open(f"{drop_down_month.get().lower()}{drop_down_year.get()}.txt", mode="r") as file:
            for file_line in file:
                file_line = file_line.strip("\n")
                my_line_values.append(file_line)
                if len(my_line_values) == 3:
                    value_prices.append(float(my_line_values[2]))
                    my_line_values = []
    except:
        pass
    for value in value_prices:
        if float(value) >= 0:
            plus_values += float(value)
        else:
            minus_values += float(value)

    if str(plus_values).endswith(".0"):
        plus_values = int(plus_values)
    if str(minus_values).endswith(".0"):
        minus_values = int(minus_values)

    return plus_values, minus_values


def window_settings():
    # funckie pre vymazanie textu po kliknutí
    def click_input_item_fun(e):
        input_item.delete(0, END)
        input_item.configure(text_color=text_color_input)

    # pridanie položky aleno zákazníka do Options menu
    def add_new_option_to_drop_down_table_items_or_new_customer():
        new = input_item.get().capitalize()
        if drop_down_customer_or_new_item.get() == "Nová položka":
            items_options.append(new)
            drop_down_table_items_2.configure(values=items_options)

        else:
            customers_options.append(new)
            drop_down_customer_losses_2.configure(values=customers_options)

        input_item.delete(0, END)
        input_item.insert(0, "Zadaj položku/zákazníka")
        input_item.configure(text_color=temporary_input_font_color)
        settings_window.focus()

    # Odobratie zákazníka z Options menu
    def remove_customer_from_drop_down_customer_losses():
        customers_options.remove(drop_down_customer_losses_2.get())
        drop_down_customer_losses_2.configure(values=customers_options)
        drop_down_customer_losses_2.set(customers_options[0])

    # Odobratie položky z Options menu
    def remove_item_from_drop_down_table_items():
        items_options.remove(drop_down_table_items_2.get())
        drop_down_table_items_2.configure(values=items_options)
        drop_down_table_items_2.set(items_options[0])

    # Uloženie možností z Options menu do súboru a transfer dát do main okna
    def update_customers_options():
        with open("moje_položky.txt", mode="w") as file:
            for one_item in items_options:
                file.write(one_item + str("\n"))
        with open("zákazníci.txt", mode="w") as file:
            for one_item in customers_options:
                file.write(one_item + str("\n"))
        drop_down_customer_losses.configure(values=customers_options)
        drop_down_table_items.configure(values=items_options)

    settings_window = CTkToplevel()
    settings_window.geometry("640x366+400+280")
    settings_window.title("Velušovské vajíčko 1.0")
    settings_window.iconbitmap("icon.ico")
    settings_window.resizable(False, False)
    settings_window.grab_set()
    first_toplevel_frame = CTkFrame(settings_window, fg_color="transparent")
    first_toplevel_frame.pack(pady=30)
    second_toplevel_frame = CTkFrame(settings_window, fg_color="transparent")
    second_toplevel_frame.pack()
    # Customer/New Item
    drop_down_customer_or_new_item = CTkOptionMenu(first_toplevel_frame, values=["Nová položka", "Nový zákazník"],
                                                   fg_color=button_color, button_color="#3d345f")
    drop_down_customer_or_new_item.grid(row=0, column=0)

    # Item input
    input_item = CTkEntry(first_toplevel_frame, width=185, font=input_font, border_width=3,
                          text_color=temporary_input_font_color)
    input_item.insert(0, "Zadaj položku/zákazníka")
    input_item.grid(row=0, column=1, padx=10)

    # Button Add item
    button_add_option = CTkButton(first_toplevel_frame, text="Pridaj", width=100, font=input_font,
                                  fg_color=button_color,
                                  border_width=3, command=add_new_option_to_drop_down_table_items_or_new_customer)
    button_add_option.grid(row=0, column=2)

    # Bind the Entry widget with Mouse Button to clear the content
    input_item.bind("<FocusIn>", click_input_item_fun)

    # Customer/Losses Options Menu
    drop_down_customer_losses_2 = CTkOptionMenu(first_toplevel_frame,
                                                values=customers_options,
                                                fg_color=button_color, button_color="#3d345f")
    drop_down_customer_losses_2.grid(row=1, column=0, pady=20)

    # Delete button for OptionMenu customer_losses options
    delete_button_selected_option = CTkButton(first_toplevel_frame, width=150, text="Odstrániť zákazníka",
                                              font=input_font,
                                              fg_color=button_color, border_width=3,
                                              command=remove_customer_from_drop_down_customer_losses)
    delete_button_selected_option.grid(row=1, column=1)

    # Items Options Menu
    drop_down_table_items_2 = CTkOptionMenu(first_toplevel_frame, values=items_options,
                                            fg_color=button_color,
                                            button_color="#3d345f")
    drop_down_table_items_2.grid(row=2, column=0)

    # Delete button for OptionMenu items options
    delete_button_selected_option = CTkButton(first_toplevel_frame, width=150, text="Odstrániť položku",
                                              font=input_font,
                                              fg_color=button_color, border_width=3,
                                              command=remove_item_from_drop_down_table_items)
    delete_button_selected_option.grid(row=2, column=1)

    # Save settings button
    save_settings = CTkButton(second_toplevel_frame, text="Uložiť nastavenia", width=100, height=50, font=input_font,
                              fg_color=button_color,
                              border_width=3, command=update_customers_options)
    save_settings.grid(row=0, column=0, pady=(80, 10))


window = CTk()
window.geometry("1280x732+100+100")
window.title("Velušovské vajíčko 1.0 - nastavenia")
window.iconbitmap("icon.ico")
window.resizable(False, False)

# Farby a fonty
main_color = "#35005f"
button_color = "#7161a9"
main_text_color = "#f6f6f6"
text_color_input = "#b3b3b3"
temporary_input_font_color = "#525959"

main_font = ("Century Gothic", 24)
bottom_label_font = ("Century Gothic", 16)
input_font = ("Century Gothic", 14)


window.config(set_appearance_mode("Dark"))


# Framy
head_frame = CTkFrame(window, fg_color="transparent")
head_frame.pack(padx=(100, 0), pady=(10, 20))

second_frame = CTkFrame(window, fg_color="transparent")
second_frame.pack()

customer_losses_frame = CTkFrame(window, fg_color="transparent")
customer_losses_frame.pack(pady=(20, 0))

table_items_frame = CTkFrame(window, fg_color="transparent")
table_items_frame.pack(pady=20)

graphics_frame = CTkFrame(window, fg_color="transparent")
graphics_frame.pack()
# graphics_frame.pack(pady=(0, 20))

buttons_frame_table = CTkFrame(window, fg_color="transparent")
buttons_frame_table.pack()

bottom_frame = CTkFrame(window, fg_color="transparent")
bottom_frame.pack()


# ===============
# MY CODE:
# ===============

# Label Current month label
current_month_label = CTkLabel(head_frame, text="Aktuálny mesiac", font=main_font)
current_month_label.grid(row=0, column=0)

# Label Profit a losses
profit_and_losses_label = CTkLabel(head_frame, text="Celkové ročný obrat", font=main_font)
profit_and_losses_label.grid(row=0, column=1, padx=(300, 80))

# Label Year overview of profit and losses
year_overview_profit_and_losses = CTkLabel(head_frame, text="Mesačný prehľad", font=main_font)
year_overview_profit_and_losses.grid(row=0, column=2, padx=(80, 50))
# HEAD FRAME END

# HEAD FRAME

# SECOND FRAME
# Visualisation of current month
drop_down_month = CTkOptionMenu(second_frame, values=months_options, fg_color=button_color, button_color="#3d345f")
drop_down_month.set(current_month_fun())
drop_down_month.grid(row=0, column=0, padx=(30, 10))

# Label of profit
profit_label = CTkLabel(second_frame, text=f"Príjmy         0", font=main_font)
# profit_label.grid(row=1, column=2, padx=(300, 80))
profit_label.grid(row=0, column=3, padx=(140, 0))

# Label of losses
losses_label = CTkLabel(second_frame, text=f"Výdavky    0", font=main_font)
losses_label.grid(row=1, column=3, padx=(140, 0))

drop_down_year = CTkOptionMenu(second_frame, values=check_all_existing_files(), fg_color=button_color,
                               button_color="#3d345f")
drop_down_year.set(current_year_fun())
drop_down_year.grid(row=0, column=1)

# Label current year
current_year_label = CTkLabel(second_frame, text=f"Rok  {current_year_fun()}", font=main_font)
# current_year_label.grid(row=1, column=3, padx=(80, 50))
current_year_label.grid(row=0, column=4, padx=(260, 90))

# Confirm button
button_confirm_choose_file = CTkButton(second_frame, text="Vybrať", width=140, font=input_font,
                                       fg_color=button_color, border_width=3, command=open_choosed_file)
button_confirm_choose_file.grid(row=0, column=2, padx=(10, 0))


# CUSTOMER/LOSSES FRAME
# Customer/Losses
drop_down_customer_losses = CTkOptionMenu(customer_losses_frame, values=all_options_to_drop_down_customer_or_new_item(),
                                          fg_color=button_color, button_color="#3d345f")
drop_down_customer_losses.grid(row=0, column=0)

# Label for # Customer/Losses
customer_or_losses_label = CTkLabel(customer_losses_frame, width=100, text="Zákazník / Výdavok", font=bottom_label_font)
customer_or_losses_label.grid(row=0, column=1, padx=(10, 776))

# CUSTOMER/LOSSES FRAME - END

# TABLE ITEMS FRAME
# Date input
input_date = CTkEntry(table_items_frame, width=87, font=input_font, border_width=3)
input_date.insert(0, current_date_numbers_for_input_date())
input_date.grid(row=0, column=0)

drop_down_table_items = CTkOptionMenu(table_items_frame, values=all_options_to_drop_down_table_items(),
                                      fg_color=button_color,
                                      button_color="#3d345f")
drop_down_table_items.grid(row=0, column=1, padx=10)

# Price input
input_price = CTkEntry(table_items_frame, width=100, font=input_font, border_width=3,
                       text_color=temporary_input_font_color)
input_price.insert(0, "Zadaj cenu")
input_price.grid(row=0, column=2)

# Button Add item
button_add_item = CTkButton(table_items_frame, text="Pridaj položku", width=50, font=input_font, fg_color=button_color,
                            border_width=3, command=add_items_press_button_add_item)
button_add_item.grid(row=0, column=3, padx=(10, 750))

# TABLE ITEMS FRAME - END

# Bind the Entry widget with Mouse Button to clear the content

clicked_input_price = input_price.bind("<FocusIn>", clicked_input_price_fun)

# ====== Graphics Frame =======
# TABLE treeview

# Table style
style = ttk.Style()
# Výber theme
style.theme_use("clam")
# Konfigurácia Treeviews colors
style.configure("Treeview",
                # pozadie pridaných položiek
                background="#4d4d4d",
                # "#4d4d4d"
                # "#333"
                # farba textu pridaných položiek
                foreground="white",
                # výška riadku
                rowheight=25,
                # farba pozadia tabuľky+nepracuje s každou themou stylu preto musíme pridať map a nastaviť style.theme
                fieldbackground="#4d4d4d")
# Zmena vybranej farby
style.map("Treeview",
          background=[("selected", button_color)])
# Table konštruckia
table = ttk.Treeview(graphics_frame)

table["columns"] = ("Dátum", "Názov položky", "Cena")
table.column("#0", width=0, stretch=NO)
table.column("Dátum", anchor=W, width=100, minwidth=50)
table.column("Názov položky", anchor=CENTER, width=240, minwidth=80)
table.column("Cena", anchor=CENTER, width=120, minwidth=50)

table.heading("#0", text="")
table.heading("Dátum", text="Dátum", anchor=W)
table.heading("Názov položky", text="Názov položky", anchor=CENTER)
table.heading("Cena", text="Cena", anchor=CENTER)

# *******vytvorenie dvojfarebných riadkov v tabuľke*******
table.tag_configure("minus", background="#d00")
table.tag_configure("plus", background="#218727")

table.grid(row=0, column=0)


# Scrollbar
scrollbar_table = CTkScrollbar(graphics_frame, command=table.yview)
scrollbar_table.grid(row=0, column=1, padx=(0, 10), sticky=N+S)
table.configure(yscrollcommand=scrollbar_table.set)

profit = 69
losses = 32

year_annual_turnover = np.array([profit, losses])
my_labels = [f"Príjmy {profit}", f"Výdavky {losses}"]
my_colors = ["#218727", "#d00"]
my_explode = [0.1, 0]

fig = Figure()
ax = fig.add_subplot(111)
ax.pie(year_annual_turnover, radius=1, labels=my_labels, colors=my_colors, explode=my_explode, shadow=True)
ax.legend(title="Celkový ročný obrat", loc='center left', bbox_to_anchor=(0.5, 1.02))

canvas = FigureCanvasTkAgg(fig, graphics_frame)
canvas.get_tk_widget().grid(row=0, column=2)

# ====== Graphics Frame END =======

# Buttons for table
# Remove item
button_remove_item_line = CTkButton(buttons_frame_table, text="Odstrániť položku", width=140, font=input_font,
                                    fg_color=button_color, border_width=3,
                                    command=delete_item_line_from_table)
button_remove_item_line.grid(row=0, column=0)

# Delete selected items
button_clear_selected = CTkButton(buttons_frame_table, text="Vymazať výber", width=140, font=input_font,
                                  fg_color=button_color, border_width=3,
                                  command=clear_selected)
button_clear_selected.grid(row=0, column=1, padx=(10, 5))

# Delete all items
button_clear_table = CTkButton(buttons_frame_table, text="Vymazať tabuľku", width=140, font=input_font,
                               fg_color=button_color, border_width=3, command=clear_table)
button_clear_table.grid(row=0, column=2, padx=(5, 750))

# Settings Button
button_settings = CTkButton(buttons_frame_table, text="Nastavenia", width=140, font=input_font,
                            fg_color=button_color, border_width=3, command=window_settings)
button_settings.grid(row=1, column=0, padx=(0, 5), pady=20)

# Save file
button_save_file = CTkButton(buttons_frame_table, text="Uložiť tabuľku", width=140, font=input_font,
                             fg_color=button_color, border_width=3, command=save_file_and_update_profit_and_losses)
button_save_file.grid(row=1, column=1, padx=(5, 5), pady=20)

# Quit file
button_quit_file = CTkButton(buttons_frame_table, text="Zavrieť súbor", width=140, font=input_font,
                             fg_color=button_color, border_width=3, command=window.destroy)
button_quit_file.grid(row=1, column=2, padx=(5, 750), pady=20)


# BOTTOM FRAME
# Monthly label profit
monthly_profit_label = CTkLabel(bottom_frame, text=f"Príjem za mesiac {drop_down_month.get()}", font=bottom_label_font)
monthly_profit_label.grid(row=0, column=0, padx=(0, 10), ipadx=10)

# Monthly label profit value
monthly_profit_label_value = CTkLabel(bottom_frame, text=f"{update_monthly_profit_losses()[0]}", font=bottom_label_font,
                                      fg_color="#218727")
monthly_profit_label_value.grid(row=1, column=0, padx=(0, 10), ipadx=10)

# Monthly label losses
monthly_losses_label = CTkLabel(bottom_frame, text=f"Výdavky za mesiac {drop_down_month.get()}", font=bottom_label_font)
monthly_losses_label.grid(row=0, column=1, padx=(10, 760), ipadx=10)

# Monthly label losses value
monthly_losses_label_value = CTkLabel(bottom_frame, text=f"{update_monthly_profit_losses()[1]}", font=bottom_label_font,
                                      fg_color="#d00")
monthly_losses_label_value.grid(row=1, column=1, padx=(10, 760), ipadx=10)

# # Mazanie vstupu pre funkciu
# clicked_input_price_key = input_price.bind("<Key>", clicked_input_price_key_fun)


# reopen saved file
reopen_saved_file()
# calculate profit form table
# calculate losses from table

# new_month_new_year_annual_turnover()
# check_all_existing_files()
# update_monthly_profit_losses()


window.mainloop()
