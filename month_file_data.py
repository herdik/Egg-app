class ItemData:

    def __init__(self, date="unknown", name="unknown", price=float(0)):
        self.date = date
        self.name = name
        self.price = price


class MonthData:

    def __init__(self, raw_data):
        self.items = []
        line_values = []

        for raw_data_line in raw_data:
            raw_data_line = raw_data_line.strip("\n")
            line_values.append(raw_data_line)
            if len(line_values) == 3:
                self.items.append(ItemData(line_values[0], line_values[1], float(line_values[2])))
                line_values.clear()
