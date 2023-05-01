class ItemData:

    def __init__(self, date="unknown", name="unknown", price=float(0)):
        self.date = date
        self.name = name
        self.price = price


class MonthData:

    def __init__(self, raw_data, month='', year=0):
        self.items = []
        line_values = []
        self.month = month
        self.year = year

        for raw_data_line in raw_data:
            raw_data_line = raw_data_line.strip("\n")
            line_values.append(raw_data_line)
            if len(line_values) == 3:
                self.items.append(ItemData(line_values[0], line_values[1], float(line_values[2])))
                line_values.clear()

    def is_valid(self):
        return len(self.items) > 0 and self.month != 0 and self.year != 0


class MonthDataCollections:

    def __init__(self, current_month, current_year):
        self.current_month = current_month
        self.current_year = current_year
        self.months_dic = {}

    def insert(self, month_data):
        key = str(month_data.year) + str(month_data.month)
        self.months_dic[key] = month_data
