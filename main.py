from tkinter import *
from customtkinter import *
import time
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkcalendar import DateEntry
from datetime import date
from datetime import datetime


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


def return_number_of_month():
    global my_calendar
    # my_calendar_number = {
    #         "Január": 1,
    #         "Február": 2,
    #         "Marec": 3,
    #         "Apríl": 4,
    #         "Máj": 5,
    #         "Jún": 6,
    #         "Júl": 7,
    #         "August": 8,
    #         "September": 9,
    #         "Október": 10,
    #         "November": 11,
    #         "December": 12
    #     }
    for key in my_calendar:
        if drop_down_month.get() == my_calendar[key]:
            return key


# funckia pre aktuálny rok
def current_year_fun():
    current_year = current_dato[0]
    return current_year


# funckia pre int aktuálneho mesiaca
def current_month_fun():
    global my_calendar
    current_month_number = current_dato[1]
    current_month = my_calendar[current_month_number]
    return current_month


# funckia pre dátum pre entry a vloženie do tabuľky
def current_date_numbers_for_input_date():
    return current_dato[0], current_dato[1], current_dato[2]


# def clicked_input_price_fun(e):
#     input_price.delete(0, END)
#     input_price.configure(text_color=text_color_input)


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

    if drop_down_customer_losses.get() == "Výdavok":
        table.insert(parent="", index=END, iid=f"{id_item}", text="", values=(f"{table_date}", f"{table_item}",
                                                                              f"-{table_price}"), tags=("minus",))
    else:
        table.insert(parent="", index=END, iid=f"{id_item}", text="", values=(f"{table_date}", f"{table_item}",
                                                                              f"{table_price}"), tags=("plus",))
    input_price.delete(0, END)
    hidden_label_input_price.configure(text="Zadaj cenu")
    hidden_label_input_price.grid_configure(row=0, column=2)
    input_price.bind('<KeyRelease>', lambda e: delete_placeholder())
    hidden_label_input_price.bind('<Button-1>', lambda e: input_price.focus())
    # input_item.insert(0, "Zadaj názov položky")
    # input_item.configure(text_color=temporary_input_font_color)
    # input_price.insert(0, "Zadaj cenu")
    # input_price.configure(text_color=temporary_input_font_color)
    current_month_label.focus()
    # input_date.delete(0, END)
    # input_date.set_date(date(int(drop_down_year.get()), current_date_numbers_for_input_date()[1],
    #                          current_date_numbers_for_input_date()[2]))
    sort_out_table_by_date()
    id_item += 1


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
    # empty_table = table.get_children()
    # if len(empty_table) == 0:
    #     pass
    # else:
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


# def reopen_saved_file():
#     global id_item
#     count = 0
#     data = []
#     data_values = []
#     try:
#         with open(f"{current_month_fun().lower() + str(current_year_fun())}.txt", mode="r") as file:
#             for one_line in file:
#                 one_line = one_line.strip("\n")
#                 data_values.append(one_line)
#                 if len(data_values) == 3:
#                     data.append(data_values)
#                     data_values = []
#                     if float(data[count][2]) < 0:
#                         table.insert(parent="", index=END, iid=f"{id_item}", text="",
#                                      values=(data[count][0], data[count][1], data[count][2]), tags=("minus", ))
#                     elif float(data[count][2]) > 0:
#                         table.insert(parent="", index=END, iid=f"{id_item}", text="",
#                                      values=(data[count][0], data[count][1], data[count][2]), tags=("plus",))
#                     else:
#                         pass
#                     count += 1
#                     id_item += 1
#     except:
#         print("Súbor sa nenašiel")


def check_all_existing_files():
    global my_calendar
    all_years = []
    existing_file_in_year = []
    line_values = []
    prices = []
    yearly_profit = 0
    yearly_losses = 0
    checked_year = current_year_fun()

    while checked_year > 2021:
        for one_month in reversed(my_calendar):
            checked_month = my_calendar[one_month].lower()
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
    global id_item
    global my_calendar
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
                        table.insert(parent="", index=END, iid=f"{id_item}", text="",
                                     values=(data[count][0], data[count][1], data[count][2]), tags=("minus",))
                    elif float(data[count][2]) > 0:
                        table.insert(parent="", index=END, iid=f"{id_item}", text="",
                                     values=(data[count][0], data[count][1], data[count][2]), tags=("plus",))
                    else:
                        pass
                    count += 1
                    id_item += 1
    except:
        print("Súbor sa nenašiel")

    line_values = []
    prices = []
    yearly_profit = 0
    yearly_losses = 0

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

    final_profit_sum = yearly_profit + yearly_losses

    if str(final_profit_sum).endswith("0"):
        final_profit_sum = int(final_profit_sum)

    profit_label.configure(text=f"Príjmy         {yearly_profit}")
    losses_label.configure(text=f"Výdavky    {yearly_losses}")
    current_year_label.configure(text=f"Rok  {drop_down_year.get()}")
    monthly_profit_label.configure(text=f"Príjem - {drop_down_month.get()}")
    monthly_losses_label.configure(text=f"Výdavky - {drop_down_month.get()}")
    final_monthly_profit_label.configure(text=f"Zisk/strata - {drop_down_month.get()}")
    monthly_profit_label_value.configure(text=f"{update_monthly_profit_losses()[0]}")
    monthly_losses_label_value.configure(text=f"{update_monthly_profit_losses()[1]}")
    final_monthly_profit_label_value.configure(text=f"{update_monthly_profit_losses()[2]}")
    value_final_profit.configure(text=f"{final_profit_sum}")

    if int(drop_down_year.get()) == current_date_numbers_for_input_date()[0] \
            and return_number_of_month() == current_date_numbers_for_input_date()[1]:
        input_date.set_date(date(current_date_numbers_for_input_date()[0], current_date_numbers_for_input_date()[1],
                                 current_date_numbers_for_input_date()[2]))
    else:
        input_date.set_date(date(int(drop_down_year.get()), return_number_of_month(),
                                 1))

    # int(drop_down_year.get()) != current_date_numbers_for_input_date()[0]:

    profit_graph = yearly_profit
    losses_graph = yearly_losses * -1
    pie_graph_call(profit_graph, losses_graph)
    bar_graph_values_update()


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
        # first_item = change_date_or_add_zero_to_date(first_item)
        second_item = str(table.item(one_item)["values"][1])
        third_item = str(table.item(one_item)["values"][2])
        checking_table.append((first_item, second_item, third_item))
    # usportiadanie podľa dátumu u listu podľa 0-tého parametru z tuple
    checking_table.sort(key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"))
    clear_table()
    for index in range(len(checking_table)):
        # modified_date = change_date_or_remove_zero_to_date(checking_table[index][0])
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

    monthly_profit_sum = plus_values + minus_values

    if str(plus_values).endswith(".0"):
        plus_values = int(plus_values)
    if str(minus_values).endswith(".0"):
        minus_values = int(minus_values)
    if str(monthly_profit_sum).endswith(".0"):
        monthly_profit_sum = int(monthly_profit_sum)

    return plus_values, minus_values, monthly_profit_sum


def window_settings():
    # Reminder to save settings
    def reminde_window_func():
        # Close setting window and reminde window
        def close_settings_and_reminde_window():
            reminde_window.destroy()
            settings_window.destroy()

        def reminde_save_changes_settings():
            update_customers_options()
            reminde_window.destroy()
            settings_window.destroy()

        reminde_window = CTkToplevel(window)
        reminde_window.geometry("400x250+530+280")
        reminde_window.title("Velušovské vajíčko 1.0 - Upozornenie")
        reminde_window.iconbitmap("icon.ico")
        reminde_window.resizable(False, False)
        reminde_window.grab_set()

        reminde_frame = CTkFrame(reminde_window, fg_color="transparent")
        reminde_frame.pack()

        buttons_frame_questions_window = CTkFrame(reminde_window, fg_color="transparent")
        buttons_frame_questions_window.pack()

        question_label_settings = CTkLabel(reminde_frame, width=300, text="Naozaj chcete zatvoriť okno s nastaveniami?",
                                           text_color=text_color_input, font=input_font)
        question_label_settings.grid(row=0, column=0, pady=(5, 10))

        button_yes_close = CTkButton(reminde_frame, width=80, text="Áno", text_color=text_color_input,
                                     fg_color=button_color, font=bottom_label_font,
                                     command=close_settings_and_reminde_window)
        button_yes_close.grid(row=1, column=0)

        question_label_2_settings = CTkLabel(reminde_frame, width=300,
                                             text="Ak ste nastavenia neuložili, stále ich môžete uložiť?",
                                             text_color=text_color_input, font=input_font)
        question_label_2_settings.grid(row=2, column=0, pady=(15, 10))

        button_save = CTkButton(reminde_frame, width=80, text="Uložiť", text_color=text_color_input,
                                fg_color=button_color, font=bottom_label_font, command=reminde_save_changes_settings)
        button_save.grid(row=3, column=0)
    # funckie pre vymazanie textu po kliknutí
    # def click_input_item_fun(e):
    #     input_item.delete(0, END)
    #     input_item.configure(text_color=text_color_input)

    def delete_placeholder_input_item():
        if len(input_item.get()) > 0:
            hidden_label_input_item.grid_forget()
        else:
            hidden_label_input_item.configure(text="Zadaj položku/zákazníka")
            hidden_label_input_item.grid_configure(row=0, column=1)

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
        hidden_label_input_item.configure(text="Zadaj položku/zákazníka")
        hidden_label_input_item.grid_configure(row=0, column=1)
        input_item.bind('<KeyRelease>', lambda e: delete_placeholder_input_item())
        hidden_label_input_item.bind('<Button-1>', lambda e: input_item.focus())
        # input_item.insert(0, "Zadaj položku/zákazníka")
        # input_item.configure(text_color=temporary_input_font_color)
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
    settings_window.geometry("640x366+400+190")
    settings_window.title("Velušovské vajíčko 1.0 - nastavenia")
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
    input_item = CTkEntry(first_toplevel_frame, width=160, font=input_font, border_width=3,
                          text_color=text_color_input, fg_color="#343638")
    # input_item.insert(0, "Zadaj položku/zákazníka")
    input_item.grid(row=0, column=1, padx=10, ipadx=2)

    input_item.bind('<KeyRelease>', lambda e: delete_placeholder_input_item())

    # placeholder fo input_item
    hidden_label_input_item = CTkLabel(first_toplevel_frame, width=141, height=8, text="Zadaj položku/zákazníka",
                                       text_color=temporary_input_font_color, fg_color="#343638")
    hidden_label_input_item.grid(row=0, column=1)
    hidden_label_input_item.bind('<Button-1>', lambda e: input_item.focus())

    # Button Add item
    button_add_option = CTkButton(first_toplevel_frame, text="Pridaj", width=100, font=input_font,
                                  fg_color=button_color,
                                  border_width=3, command=add_new_option_to_drop_down_table_items_or_new_customer)
    button_add_option.grid(row=0, column=2)

    # Bind the Entry widget with Mouse Button to clear the content
    # input_item.bind("<FocusIn>", click_input_item_fun)

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

    # Event close settings window call reminde window function
    settings_window.protocol("WM_DELETE_WINDOW", reminde_window_func)


def pie_graph_call(profit_graph, losses_graph):
    year_annual_turnover = np.array([profit_graph, losses_graph])
    my_labels = [f"Príjmy", f"Výdavky"]
    fig = Figure((5, 3.5), dpi=80)
    fig.subplots_adjust(right=0.68)
    canvas = FigureCanvasTkAgg(fig, graphics_frame)
    canvas.get_tk_widget().grid(row=0, column=2)
    no_data_label = CTkLabel(graphics_frame, text="", font=info_font, width=200, text_color="#fff", fg_color="#d00")
    no_data_label.grid(row=0, column=2)

    if profit_graph == 0 and losses_graph == 0:
        no_data_label.configure(text="Žiadne dáta pre zobrazenie grafu")
    else:
        no_data_label.grid_remove()
        legend_labels = [f"Príjmy {profit_graph}", f"Výdavky -{losses_graph}"]
        if losses_graph == 0:
            legend_labels = [f"Príjmy {profit_graph}", f"Výdavky {losses_graph}"]

        my_colors = ["#218727", "#d00"]
        my_explode = [0.1, 0]

        ax = fig.add_subplot(111)
        _, _, autopcts = ax.pie(year_annual_turnover, labels=my_labels, colors=my_colors, explode=my_explode,
                                shadow=True, textprops={'fontsize': 10.5, 'weight': 'bold'}, autopct='%1.0f%%',
                                labeldistance=1.12, startangle=90)
        for autopct in autopcts:
            autopct.set_color('white')

        ax.legend(title="Celkový ročný obrat", labels=legend_labels, loc="center left", bbox_to_anchor=(1.02, 1.02),
                  prop={"size": 8, 'weight': 'bold'}, title_fontproperties={'weight': 'bold', "size": 9})


# def change_date_or_add_zero_to_date(check_text):
#     new_text = "0"
#     date_index = check_text.find(".")
#     if date_index == 1:
#         for symbol in check_text:
#             new_text += symbol
#     else:
#         new_text = check_text
#     return new_text


# def change_date_or_remove_zero_to_date(check_text):
#     new_text = ""
#     if check_text[0] == "0":
#         for index in range(1, len(check_text)):
#             new_text += check_text[index]
#     else:
#         new_text = check_text
#     return new_text


def bar_graph_values_update():
    global my_calendar
    line_items = []
    price_items = []
    graph_values = []
    check_number = 1
    plus_values = 0
    minus_values = 0
    y_profit = []
    z_losses = []

    for one_month in my_calendar:
        checked_month = my_calendar[one_month]
        if one_month == check_number:
            try:
                with open(f"{checked_month + str(drop_down_year.get())}.txt", mode="r") as file:
                    # print(f"{checked_month + str(checked_year)}")
                    for file_line in file:
                        file_line = file_line.strip("\n")
                        line_items.append(file_line)
                        if drop_down_year.get():
                            if len(line_items) == 3:
                                if float(line_items[2]) > 0:
                                    plus_values += float(line_items[2])
                                else:
                                    minus_values += float(line_items[2])
                                line_items = []
                    price_items.append(plus_values)
                    price_items.append(minus_values)
                    plus_values = 0
                    minus_values = 0
            except:
                # print(f"{checked_month + str(checked_year)} súbor sa nenašiel")
                pass
        graph_values.append(price_items)
        price_items = []
        check_number += 1

    def autolabel(rectangle_group):
        for rect in rectangle_group:
            height = rect.get_height()
            my_annotate = str(height)
            if str(height).endswith(".0"):
                my_annotate = str(int(height))
            if height == 0:
                my_annotate = ''
            ax_2.annotate(my_annotate, xy=(rect.get_x() + rect.get_width() / 2, height), ha='center', xytext=(1, 5),
                          textcoords='offset points', color='black', fontsize=7, rotation=90)

    # ===Graph===
    x_months = ['Jan', 'Feb', 'Mar', 'Apr', 'Máj', 'Jún', 'Júl', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec']

    for i in range(len(graph_values)):
        try:
            one_graph_value = graph_values[i][0]
        except:
            one_graph_value = 0
        y_profit.append(one_graph_value)

    for i in range(len(graph_values)):
        try:
            second_graph_value = graph_values[i][1] * -1
        except:
            second_graph_value = 0
        z_losses.append(second_graph_value)

    # y_profit = [graph_values[0][0], graph_values[1][0], 70, 51, 4, 60, 30, 190, 70, 51, 4, 60]
    # z_losses = [graph_values[0][1] * -1, 110, 15, 14, 56, 48, 6, 110, 15, 14, 56, 48]

    fig_2 = Figure(figsize=(5, 3.5), dpi=80)
    # fig_2.set_size_inches(4, 2.75)

    ax_2 = fig_2.add_subplot(111)

    x_axis = np.arange(len(x_months))

    rect1 = ax_2.bar(x_axis - 0.2, y_profit, 0.4, label="Príjmy", color="g")
    rect2 = ax_2.bar(x_axis + 0.2, z_losses, 0.4, label="Výdavky", color="r")

    ax_2.set_xticks(x_axis, x_months)
    ax_2.set_ylabel('Príjmy a výdavky v mene €')

    ax_2.legend(loc='upper right', ncols=2, bbox_to_anchor=(0.8, 1.15))

    # annotate function called
    autolabel(rect1)
    autolabel(rect2)

    # get higest number to set_ylim
    highest_y = max(y_profit)
    highest_z = max(z_losses)
    if highest_y > highest_z:
        highest_number = highest_y + 20
    else:
        highest_number = highest_z + 20

    ax_2.set_ylim(0, highest_number)

    canvas_2 = FigureCanvasTkAgg(fig_2, graphics_frame)
    canvas_2.draw()
    canvas_2.get_tk_widget().grid(row=0, column=3, padx=(15, 400))


def customers_overview():

    def current_and_passed_customers():
        global my_calendar
        checking_year = current_year_fun()
        one_line_values = []
        current_passed_customers_options = []

        while checking_year > 2021:
            for month in reversed(my_calendar):
                checking_month = my_calendar[month].lower()
                try:
                    with open(checking_month + str(checking_year) + str(".txt"), mode="r") as file:
                        for one_line in file:
                            striped_line = one_line.strip("\n")
                            one_line_values.append(striped_line)
                            if len(one_line_values) == 3:
                                txt = one_line_values[1].split("-")
                                if len(txt) > 1:
                                    if txt[len(txt)-1] != "Výdavok":
                                        current_passed_customers_options.append(txt[len(txt)-1])
                                one_line_values.clear()
                except:
                    pass
            checking_year -= 1
        current_passed_customers_options = list(set(current_passed_customers_options))

        return current_passed_customers_options

    # Delete all customers and items from table treeview
    def clear_table_customers_overview():
        all_items = table_customers_overview.get_children()
        for item in all_items:
            table_customers_overview.delete(item)

    # Delete all labels from labels frame - labels items, choosed_customer_overview_frame - finally result
    # Reset all label grid position to none
    def clear_labels_frame():
        list_labels = labels_frame.grid_slaves()
        for first in list_labels:
            first.destroy()

    def clear_result_summary_label():
        list_results = choosed_customer_overview_frame.grid_slaves()
        for second in list_results:
            second.destroy()

    # def clear():
    #     list_labels = labels_frame.grid_slaves()
    #     list_results = choosed_customer_overview_frame.grid_slaves()
    #     for first, second in zip(list_labels, list_results):
    #         first.destroy()
    #         second.destroy()

    def table_customers_overview_fill_up():
        clear_table_customers_overview()
        clear_labels_frame()
        clear_result_summary_label()

        global my_calendar
        item_index = 0
        year_to_check = drop_down_customers_year.get()
        customer_to_check = drop_down_customer_options.get()
        line_values = []
        all_items_dict = {}

        # creating dictionary to fill up according customer and his ordered items
        for one_item in items_options:
            all_items_dict[one_item] = 0

        for one_month in my_calendar:
            month_to_check = my_calendar[one_month].lower()
            try:
                with open(str(month_to_check) + str(year_to_check) + ".txt", mode="r") as file:
                    for one_line in file:
                        line_to_check = one_line.strip("\n")
                        line_values.append(line_to_check)
                        if len(line_values) == 3:
                            customer = line_values[1].split("-")
                            if customer[len(customer)-1] == customer_to_check:
                                table_date = line_values[0]
                                table_item_customer = line_values[1]
                                table_price = line_values[2]
                                checking_item = line_values[1].replace(str("-") + customer[len(customer)-1], "")

                                for key in all_items_dict:
                                    if key == checking_item:
                                        all_items_dict[key] += float(table_price)

                                if item_index % 2 != 0:
                                    table_customers_overview.insert(parent="", index=END, iid=f"{item_index}", text="",
                                                                    values=(f"{table_date}", f"{table_item_customer}",
                                                                            f"{table_price}"), tags=("even",))
                                else:
                                    table_customers_overview.insert(parent="", index=END, iid=f"{item_index}", text="",
                                                                    values=(f"{table_date}", f"{table_item_customer}",
                                                                            f"{table_price}"), tags=("odd", ))
                                item_index += 1
                            line_values.clear()
                            customer.clear()
            except:
                pass

        valid_item = []
        for key in all_items_dict:
            if all_items_dict[key] > 0:
                if str(all_items_dict[key]).endswith(".0"):
                    all_items_dict[key] = int(all_items_dict[key])
                valid_item.append([key, all_items_dict[key]])

        i_2 = 0
        for i in range(0, len(valid_item)):
            if i < 10:
                CTkLabel(labels_frame, text=valid_item[i][0], width=150,
                         font=bottom_label_font).grid(row=0, column=i, padx=8, pady=15)
                CTkLabel(labels_frame, text=str(valid_item[i][1]), width=80, fg_color="green",
                         font=bottom_label_font).grid(row=1, column=i)
            if 5 <= i < 10:
                CTkLabel(labels_frame, text=valid_item[i][0], width=150,
                         font=bottom_label_font).grid(row=2, column=i_2, padx=8, pady=15)
                CTkLabel(labels_frame, text=str(valid_item[i][1]), width=80, fg_color="green",
                         font=bottom_label_font).grid(row=3, column=i_2)
                i_2 += 1

        # Empty table and fix bug after if table are filled up and after chosed customer without any order - empty table
        my_labels = 0
        for key in all_items_dict:
            if all_items_dict[key] == 0:
                my_labels += 1
        if my_labels == len(all_items_dict):
            clear_labels_frame()

        # Show finnaly result labels summary order and customer
        summary = 0
        for i in range(len(valid_item)):
            summary += valid_item[i][1]
            if str(summary).endswith(".0"):
                summary = int(summary)
        CTkLabel(choosed_customer_overview_frame, text=f"{customer_to_check} za rok {year_to_check}", width=350,
                 font=main_font).grid(row=0, column=0, padx=8, pady=(35, 5))
        CTkLabel(choosed_customer_overview_frame, text=str(summary), width=100, fg_color="green",
                 font=main_font).grid(row=1, column=0, padx=8, pady=(5, 5))

    customers_window = CTkToplevel()
    customers_window.geometry("840x732+400+10")
    customers_window.title("Velušovské vajíčko 1.0 - Prehľad zákazníkov")
    customers_window.iconbitmap("icon.ico")
    customers_window.resizable(False, False)
    customers_window.grab_set()

    # Frames
    first_frame_customers_window = CTkFrame(customers_window, fg_color="transparent")
    first_frame_customers_window.pack(pady=12)

    table_frame_customers_window = CTkFrame(customers_window, fg_color="transparent")
    table_frame_customers_window.pack()

    labels_frame = CTkFrame(customers_window, fg_color="transparent")
    labels_frame.pack()

    choosed_customer_overview_frame = CTkFrame(customers_window, fg_color="transparent")
    choosed_customer_overview_frame.pack()

    # Label for choose year
    choose_year_label = CTkLabel(first_frame_customers_window, width=150, text="Potvrď výber roku",
                                 font=bottom_label_font)
    choose_year_label.grid(row=0, column=0)

    # Year options to choose customers overview
    drop_down_customers_year = CTkOptionMenu(first_frame_customers_window, values=check_all_existing_files(),
                                             fg_color=button_color,
                                             button_color="#3d345f")
    drop_down_customers_year.set(current_year_fun())
    drop_down_customers_year.grid(row=0, column=1, padx=10)

    # Label for choose customer in selected year
    choose_customer_label = CTkLabel(first_frame_customers_window, width=150, text="Vyber zákazníka",
                                     font=bottom_label_font)
    choose_customer_label.grid(row=1, column=0, pady=10)

    # Year options to choose customers overview
    drop_down_customer_options = CTkOptionMenu(first_frame_customers_window,
                                               values=current_and_passed_customers(),
                                               fg_color=button_color, button_color="#3d345f")

    drop_down_customer_options.set("Žiaden zákazník")
    drop_down_customer_options.grid(row=1, column=1, padx=10, pady=10)

    # Confirm button to show customer overview table
    confirm_button_2 = CTkButton(first_frame_customers_window, text="Potvrdiť", width=140, font=input_font,
                                 fg_color=button_color, border_width=3, command=table_customers_overview_fill_up)
    confirm_button_2.grid(row=1, column=2, pady=10)

    # TABLE - Begining
    # table for customers overview
    table_customers_overview = ttk.Treeview(table_frame_customers_window)

    # creating colums
    table_customers_overview["columns"] = ("Dátum", "Položka - Zákazník", "Cena")
    # config colums
    table_customers_overview.column("#0", width=0, stretch=NO)
    table_customers_overview.column("Dátum", anchor=W, width=100, minwidth=50)
    table_customers_overview.column("Položka - Zákazník", anchor=CENTER, width=340, minwidth=160)
    table_customers_overview.column("Cena", anchor=CENTER, width=120, minwidth=50)

    # config heading
    table_customers_overview.heading("#0", text="")
    table_customers_overview.heading("Dátum", text="Dátum", anchor=W)
    table_customers_overview.heading("Položka - Zákazník", text="Položka - Zákazník", anchor=CENTER)
    table_customers_overview.heading("Cena", text="Cena", anchor=CENTER)

    # config background added items to table_customers_overview
    table_customers_overview.tag_configure("even", background="#218727")
    table_customers_overview.tag_configure("odd", background="#0a270b")

    table_customers_overview.grid(row=0, column=0)

    # Scrollbar for table_customers_overview
    scrollbar_table_customers_overview = CTkScrollbar(table_frame_customers_window,
                                                      command=table_customers_overview.yview)
    scrollbar_table_customers_overview.grid(row=0, column=1, sticky=N+S)
    table_customers_overview.configure(yscrollcommand=scrollbar_table_customers_overview.set)
    # TABLE - END


def delete_placeholder():
    if len(input_price.get()) > 0:
        hidden_label_input_price.grid_forget()
        input_price.configure(text_color=text_color_input)
    else:
        hidden_label_input_price.configure(text="Zadaj cenu")
        hidden_label_input_price.grid_configure(row=0, column=2)


# event to CLOSE APP
def event_close_main_window():
    # event SAVE table
    def event_save_table():
        # Closing app after Saved TABLE
        def close_app_save_table():
            save_file_and_update_profit_and_losses()
            save_questions_window.destroy()
            window.destroy()

        # Closing save_questions_window and continue
        def close_save_questions_window_and_continue():
            save_questions_window.destroy()

        # Main content of event SAVE table
        questions_window.destroy()
        save_questions_window = CTkToplevel(window)
        save_questions_window.geometry("400x250+530+280")
        save_questions_window.iconbitmap("icon.ico")
        save_questions_window.title("Uloženie aplikácie")
        save_questions_window.resizable(False, False)
        save_questions_window.grab_set()

        save_question_frame = CTkFrame(save_questions_window, fg_color="transparent")
        save_question_frame.pack()

        save_buttons_frame_questions_window = CTkFrame(save_questions_window, fg_color="transparent")
        save_buttons_frame_questions_window.pack()

        save_question_label = CTkLabel(save_question_frame, width=300,
                                       text="Chcete uložiť tabuľku a ukončiť aplikáciu?",
                                       text_color=text_color_input, font=bottom_label_font)
        save_question_label.grid(row=0, column=0, pady=(50, 40))

        save_button_yes = CTkButton(save_buttons_frame_questions_window, width=80, text="Áno",
                                    text_color=text_color_input, fg_color=button_color, font=bottom_label_font,
                                    command=close_app_save_table)
        save_button_yes.grid(row=1, column=0, padx=10)

        save_button_no = CTkButton(save_buttons_frame_questions_window, width=80, text="Nie",
                                   text_color=text_color_input, fg_color=button_color, font=bottom_label_font,
                                   command=close_save_questions_window_and_continue)
        save_button_no.grid(row=1, column=1, padx=10)

    # close app clicked button yes
    def close_app():
        questions_window.destroy()
        window.destroy()

    questions_window = CTkToplevel(window)
    questions_window.geometry("400x250+530+280")
    questions_window.iconbitmap("icon.ico")
    questions_window.title("Ukončenie aplikácie")
    questions_window.resizable(False, False)
    questions_window.grab_set()

    question_frame = CTkFrame(questions_window, fg_color="transparent")
    question_frame.pack()

    buttons_frame_questions_window = CTkFrame(questions_window, fg_color="transparent")
    buttons_frame_questions_window.pack()

    question_label = CTkLabel(question_frame, width=300, text="Naozaj chcete ukončiť aplikáciu?",
                              text_color=text_color_input, font=bottom_label_font)
    question_label.grid(row=0, column=0, pady=(50, 40))

    button_yes = CTkButton(buttons_frame_questions_window, width=80, text="Áno", text_color=text_color_input,
                           fg_color=button_color, font=bottom_label_font, command=close_app)
    button_yes.grid(row=1, column=0, padx=10)

    button_no = CTkButton(buttons_frame_questions_window, width=80, text="Nie", text_color=text_color_input,
                          fg_color=button_color, font=bottom_label_font, command=event_save_table)
    button_no.grid(row=1, column=1, padx=10)


def update_year_options():
    options_years = []
    # new_year_to_add = str(current_year_fun())
    for one_year in range(2022, current_year_fun() + 1):
        options_years.append(str(one_year))

    return options_years


window = CTk()
window.geometry("1360x732+10+10")
window.title("Velušovské vajíčko 1.0")
window.iconbitmap("icon.ico")
window.resizable(False, False)

# Farby a fonty
main_color = "#35005f"
button_color = "#7161a9"
main_text_color = "#f6f6f6"
text_color_input = "#b3b3b3"
temporary_input_font_color = "#525959"

main_font = ("Century Gothic", 24)
info_font = ("Century Gothic", 20)
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
graphics_frame.pack(pady=(0, 20))

buttons_frame_table = CTkFrame(window, fg_color="transparent")
buttons_frame_table.pack()

bottom_frame = CTkFrame(window, fg_color="transparent")
bottom_frame.pack()


# ===============
# MY CODE:
# ===============

# Label Current month label
current_month_label = CTkLabel(head_frame, text="Aktuálny mesiac", font=main_font, width=205)
current_month_label.grid(row=0, column=0, ipadx=3, padx=(50, 0))

# Label Profit a losses
profit_and_losses_label = CTkLabel(head_frame, text="Celkové ročný obrat", font=main_font, width=255)
profit_and_losses_label.grid(row=0, column=1, padx=(220, 80), ipadx=3)

# Label Year overview of profit and losses
year_overview_profit_and_losses = CTkLabel(head_frame, text="Mesačný prehľad", font=main_font, width=220)
year_overview_profit_and_losses.grid(row=0, column=2, padx=(80, 130), ipadx=3)
# HEAD FRAME END

# HEAD FRAME

# SECOND FRAME
# Visualisation of current month
drop_down_month = CTkOptionMenu(second_frame, values=months_options, fg_color=button_color, button_color="#3d345f")
drop_down_month.set(current_month_fun())
drop_down_month.grid(row=0, column=0, padx=(30, 10))

# Label of profit
profit_label = CTkLabel(second_frame, text=f"Príjmy         0", font=main_font, width=200)
# profit_label.grid(row=1, column=2, padx=(300, 80))
profit_label.grid(row=0, column=3, padx=(140, 0), ipadx=8)

# Label of losses
losses_label = CTkLabel(second_frame, text=f"Výdavky    0", font=main_font, width=200)
losses_label.grid(row=1, column=3, padx=(140, 0), ipadx=8)

drop_down_year = CTkOptionMenu(second_frame, values=update_year_options(), fg_color=button_color,
                               button_color="#3d345f")
drop_down_year.set(current_year_fun())
drop_down_year.grid(row=0, column=1)

# Label current year
current_year_label = CTkLabel(second_frame, text=f"Rok  {current_year_fun()}", font=main_font, width=120)
# current_year_label.grid(row=1, column=3, padx=(80, 50))
current_year_label.grid(row=0, column=4, padx=(240, 180))

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
customer_or_losses_label.grid(row=0, column=1, padx=(10, 0))

# Final yearly profit label
final_profit = CTkLabel(customer_losses_frame, text="Ročný zisk/strata", font=main_font, width=120)
final_profit.grid(row=0, column=2, padx=(240, 450), ipadx=20)


# CUSTOMER/LOSSES FRAME - END

# TABLE ITEMS FRAME
# Date input
# input_date = CTkEntry(table_items_frame, width=87, font=input_font, border_width=3)
# input_date.insert(0, current_date_numbers_for_input_date())
# input_date.grid(row=0, column=0)

style_date = ttk.Style()
style_date.theme_use('clam')  # -> uncomment this line if the styling does not work
style_date.configure('my.DateEntry',
                     fieldbackground=button_color,
                     background='transparent',
                     foreground="#fff",
                     arrowcolor="#fff",
                     bordercolor='purple',
                     insertcolor="#6f6f6f",)
style_date.map('my.DateEntry',
               background=[('!active', '#3d345f'), ('pressed', '#203A4F'), ('active', '#3d345f')])


input_date = DateEntry(table_items_frame, selectmode="day", date_pattern="d.m.y", style='my.DateEntry',
                       font=("Century Gothic", 11), locale="sk",
                       mindate=date(2021, 12, 31), background='#3d345f', foreground="white", selectbackground='#3d345f',
                       justify="center")
input_date.set_date(date(int(drop_down_year.get()), current_date_numbers_for_input_date()[1],
                    current_date_numbers_for_input_date()[2]))
input_date.grid(row=0, column=0, ipady=1)

drop_down_table_items = CTkOptionMenu(table_items_frame, values=all_options_to_drop_down_table_items(),
                                      fg_color=button_color,
                                      button_color="#3d345f")
drop_down_table_items.grid(row=0, column=1, padx=10)

# Price input
input_price = CTkEntry(table_items_frame, width=100, font=input_font, border_width=3,
                       text_color=text_color_input)
# input_price.insert(0, "Zadaj cenu")
input_price.grid(row=0, column=2, ipadx=2)
input_price.bind('<KeyRelease>', lambda e: delete_placeholder())

# placeholder for input price
hidden_label_input_price = CTkLabel(table_items_frame, font=input_font, text_color=temporary_input_font_color,
                                    fg_color="#343638", text="Zadaj cenu", height=8, width=80)
hidden_label_input_price.grid(row=0, column=2)
hidden_label_input_price.bind('<Button-1>', lambda e: input_price.focus())

# Button Add item
button_add_item = CTkButton(table_items_frame, text="Pridaj položku", width=50, font=input_font, fg_color=button_color,
                            border_width=3, command=add_items_press_button_add_item)
button_add_item.grid(row=0, column=3, padx=(10, 0))

# Final yearly profit label VALUE
value_final_profit = CTkLabel(table_items_frame, text="0", width=120, font=main_font)
value_final_profit.grid(row=0, column=4, padx=(170, 550))

# TABLE ITEMS FRAME - END

# Bind the Entry widget with Mouse Button to clear the content

# clicked_input_price = input_price.bind("<FocusIn>", clicked_input_price_fun)

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

"Položka - Zákazník"
table.tag_configure("minus", background="#d00")
table.tag_configure("plus", background="#218727")

table.grid(row=0, column=0, padx=(30, 0))


# Scrollbar
scrollbar_table = CTkScrollbar(graphics_frame, command=table.yview)
scrollbar_table.grid(row=0, column=1, padx=(0, 10), sticky=N+S)
table.configure(yscrollcommand=scrollbar_table.set)


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
button_clear_table.grid(row=0, column=2, padx=(5, 830))

# Settings Button
button_settings = CTkButton(buttons_frame_table, text="Nastavenia", width=140, font=input_font,
                            fg_color=button_color, border_width=3, command=window_settings)
button_settings.grid(row=1, column=0, padx=(0, 5), pady=20)

# Save file
button_save_file = CTkButton(buttons_frame_table, text="Uložiť tabuľku", width=140, font=input_font,
                             fg_color=button_color, border_width=3, command=save_file_and_update_profit_and_losses)
button_save_file.grid(row=1, column=1, padx=(5, 5), pady=20)

# Customer overview button
button_customer_overview = CTkButton(buttons_frame_table, text="Prehľad zákazníkov", width=140, font=input_font,
                                     fg_color=button_color, border_width=3, command=customers_overview)
button_customer_overview.grid(row=1, column=2, padx=(5, 830), pady=20)


# BOTTOM FRAME
# Monthly label profit
monthly_profit_label = CTkLabel(bottom_frame, text=f"Príjem - {drop_down_month.get()}", font=bottom_label_font,
                                width=200)
monthly_profit_label.grid(row=0, column=0, padx=(0, 10), ipadx=10)

# Monthly label profit value
monthly_profit_label_value = CTkLabel(bottom_frame, text=f"{update_monthly_profit_losses()[0]}", font=bottom_label_font,
                                      fg_color="#218727", width=50)
monthly_profit_label_value.grid(row=1, column=0, padx=(0, 10), ipadx=10)

# Monthly label losses
monthly_losses_label = CTkLabel(bottom_frame, text=f"Výdavky - {drop_down_month.get()}", font=bottom_label_font,
                                width=200)
monthly_losses_label.grid(row=0, column=1, padx=(10, 0), ipadx=10)

# Monthly label losses value
monthly_losses_label_value = CTkLabel(bottom_frame, text=f"{update_monthly_profit_losses()[1]}", font=bottom_label_font,
                                      fg_color="#d00", width=50)
monthly_losses_label_value.grid(row=1, column=1, padx=(10, 0), ipadx=10)

# Monthly label for final profit in choosed_month
final_monthly_profit_label = CTkLabel(bottom_frame, text=f"Zisk/strata - {drop_down_month.get()}",
                                      font=("Century Gothic", 16, "bold"),
                                      width=200, fg_color="white", text_color="black")
final_monthly_profit_label.grid(row=0, column=2, padx=(140, 500), ipadx=10)

# Monthly label for final profit in choosed_month VALUE
final_monthly_profit_label_value = CTkLabel(bottom_frame, text=f"{update_monthly_profit_losses()[2]}",
                                            font=("Century Gothic", 18, "bold"),
                                            width=200, fg_color="white", text_color="black")
final_monthly_profit_label_value.grid(row=1, column=2, padx=(140, 500), ipadx=10)


# Insert picture/logo
canvas_3 = Canvas(window, width=120, height=89, background='gray14', highlightthickness=0)
canvas_3.place(x=1230, y=630)

egg_picture = PhotoImage(file="logo.png")
canvas_3.create_image(0, 0, anchor="nw", image=egg_picture)


# # Mazanie vstupu pre funkciu
# clicked_input_price_key = input_price.bind("<Key>", clicked_input_price_key_fun)


# reopen saved file
# reopen_saved_file()
check_all_existing_files()
open_choosed_file()
# calculate profit form table
# calculate losses from table

# new_month_new_year_annual_turnover()
# check_all_existing_files()
# update_monthly_profit_losses()
# get_bar_values()
window.protocol("WM_DELETE_WINDOW", event_close_main_window)

window.mainloop()
