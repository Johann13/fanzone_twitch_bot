import gspread


class QuoteSheet:

    def __init__(self, ws: gspread.spreadsheet.Worksheet):
        self.ws = ws

    def get_quotes_by_index(self, index):
        quote_index = self.ws.cell(index, 1).value
        if quote_index == '':
            return None
        quote_text = self.ws.cell(index, 2).value
        quote_game = self.ws.cell(index, 3).value
        quote_date = self.ws.cell(index, 4).value
        return f'Quote #{quote_index}\n{quote_text}\n[{quote_game}] [{quote_date}]'

    def add_quote(self, text, game, date):
        n = self.last_quote_index() + 1
        print(f'_add_quote n: {n}')
        self.ws.update_cell(n, 1, n)
        self.ws.update_cell(n, 2, text)
        self.ws.update_cell(n, 3, game)
        self.ws.update_cell(n, 4, date)
        return str(n), text, game, date

    def last_quote_index(self):
        str_list = list(filter(None, self.ws.col_values(1)))
        return len(str_list)

    def get_all_quotes(self) -> []:
        return [v for v in
                zip(self.ws.col_values(1), self.ws.col_values(2), self.ws.col_values(3), self.ws.col_values(4))]

    pass
