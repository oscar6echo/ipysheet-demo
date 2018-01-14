
import datetime as dt
import numpy as np
import pandas as pd
import itertools as it

import ipywidgets as widgets
import ipysheet

from .pricer import Price_Call, Price_Put


li_input_data = [
    ['spot', 'Spot', 'S', 100, 0.0001, 200],
    ['strike', 'Strike', 'K', 100, 0.0001, 200],
    ['mat', 'Mat (y)', 'T', 3, 0.0001, 10],
    ['vol', 'Vol (%)', 'v', 15, 0.0001, 40],
    ['rate', 'Rate (%)', 'r', 2, -2, 10],
    ['div', 'Div (%)', 'q', 0.5, -2, 5],
]

li_output_data = [
    ['d1', 'd1'],
    ['N_d1', 'N(d1)'],
    ['N_minus_d1', 'N(-d1)'],
    ['N_prime_d1', "N'(d1)"],
    ['d2', 'd2'],
    ['N_d2', 'N(d2)'],
    ['N_minus_d2', 'N(-d2)'],
    ['N_prime_d2', "N'(d2)"],
    ['price', 'Price'],
    ['delta', 'Delta'],
    ['gamma', 'Gamma'],
    ['vega', 'Vega'],
    ['theta', 'Theta'],
    ['rho', 'Rho'],
    ['voma', 'Voma'],
    ['PV', 'PV'],
    ['PV_K', 'PV*K'],
    ['payoff', 'Payoff'],
    ['PV_payoff', 'PV*Payoff']
]


class BlackScholesCalculator:

    def __init__(self):
        self.li_input_data = li_input_data
        self.li_output_data = li_output_data
        self.li_ip_key = [e[0] for e in li_input_data]
        self.li_op_key = [e[0] for e in li_output_data]

        self.sheet_in = None
        self.sheet_out = None
        self.cells_in = None
        self.cells_out = None
        self.button_price = None
        self.box = None
        self.df_pricing_one = None
        self.df_pricing_batch = None

        self.build_sheet_in()
        self.build_sheet_out()
        self.build_button_price()
        self.build_status()
        self.build_plot_zone()
        self.build_box()

        self.add_listeners()

        self.show()

        # self.li_op_label = [e[1] for e in li_output_data]
        # self.dic_op_name_label = dict(li_output_data)
        # self.dic_op_label_name = {v: k for k,
        #                           v in self.dic_op_name_label.items()}

        # self.dic_price = None
        # self.df_data_2d = None
        # self.df_data_3d = None
        # self.axis_z = None

        # self.start()

    def build_sheet_in(self):
        """
        """
        sheet = ipysheet.sheet(rows=10,
                               columns=5,
                               row_headers=False,
                               column_headers=False)
        sheet.stretch_headers = 'none'
        sheet.column_width = [110, 80, 100, 100, 100]

        cells = {}
        style_header = {'backgroundColor': '#d0d3d4',
                        'fontWeight': 'bold',
                        'textAlign': 'right',
                        'color': 'black'}
        style_header_2 = {'backgroundColor': '#d0d3d4',
                          'fontWeight': 'bold',
                          'textAlign': 'center',
                          'color': 'black'}

        for k, h in enumerate(['name', 'symbol', 'value', 'min', 'max']):
            c = ipysheet.cell(0, 0 + k, h, read_only=True, color='black')
            c.style = style_header

        for k, e in enumerate(self.li_input_data):
            r = k + 1
            key, name, symbol, val, val_min, val_max = e
            cells[key] = {}

            ipysheet.cell(r, 0, name, read_only=True, color='black')
            ipysheet.cell(r, 1, symbol, read_only=True, color='black')

            cells[key]['value'] = ipysheet.cell(r, 2, val, type='numeric')
            cells[key]['value_min'] = ipysheet.cell(
                r, 3, val_min, type='numeric')
            cells[key]['value_max'] = ipysheet.cell(
                r, 4, val_max, type='numeric')

        for k, h in enumerate(['Graph', 'Option', 'Nb step', 'x', 'y']):
            c = ipysheet.cell(7, 0 + k, h, read_only=True, color='black')
            c.style = style_header_2

        cells['graph'] = ipysheet.cell(
            8, 0, 'true', type='checkbox', style={'textAlign': 'center'})
        cells['graph_state'] = ipysheet.cell(
            9, 0, '2D', style={'textAlign': 'center'})
        cells['option'] = ipysheet.cell(
            8, 1, 'true', type='checkbox', style={'textAlign': 'center'})
        cells['option_state'] = ipysheet.cell(
            9, 1, 'Call', style={'textAlign': 'center'})
        cells['nb_step'] = ipysheet.cell(8, 2, '10', type='dropdown', choice=[
                                         '10', '50', '100', '200', '500'])
        cells['x'] = ipysheet.cell(
            8, 3, 'spot', type='dropdown', choice=self.li_ip_key)
        cells['y'] = ipysheet.cell(
            8, 4, 'mat', type='dropdown', choice=self.li_ip_key)

        self.sheet_in = sheet
        self.cells_in = cells

    def build_sheet_out(self):
        """
        """
        sheet = ipysheet.sheet(rows=1+len(self.li_op_key),
                               columns=2,
                               column_headers=False,
                               row_headers=False)
        sheet.stretch_headers = 'none'
        sheet.column_width = [110, 110]

        style_header = {'backgroundColor': '#d0d3d4',
                        'fontWeight': 'bold',
                        'textAlign': 'right',
                        'color': 'black'}

        style_title_output = {'textAlign': 'right',
                              'color': 'black'}

        c = ipysheet.cell(0, 0, 'qty', read_only=True)
        c.style = style_header
        c = ipysheet.cell(0, 1, 'value', read_only=True)
        c.style = style_header

        cells_out = {}

        for k, [key, name] in enumerate(self.li_output_data):
            c = ipysheet.cell(1+k, 0, name, read_only=True)
            c.style = style_title_output
            cells_out[key] = ipysheet.cell(1+k, 1, 0, type='numeric')

        self.sheet_out = sheet
        self.cells_out = cells_out

    def build_button_price(self):
        """
        """
        self.button_price = widgets.Button(description='Price',
                                           button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                           tooltip='Update results',
                                           icon='check')

    def build_status(self):
        """
        """

        self.status = widgets.Text(value='No pricing available',
                                   #    description='Last Price',
                                   disabled=False,
                                   border='3px solid red',
                                   layout=widgets.Layout(width='180px'))

    def build_plot_zone(self):
        """
        """
        self.plot_zone = widgets.HTML(value='PlotZone',
                                      width='500px',
                                      height='500px',
                                      border='3px solid red')

    def build_box(self):
        """
        """
        b1 = widgets.VBox([self.sheet_in, self.button_price, self.status],
                          layout=widgets.Layout(display='flex',
                                                flex_direction='column',
                                                justify_content='space-around',
                                                align_items='center',
                                                height='320px'
                                                ))
        b2 = widgets.HBox([b1, self.sheet_out],
                          layout=widgets.Layout(display='flex',
                                                flex_direction='row',
                                                justify_content='space-around',
                                                width='800px'
                                                ))
        b3 = widgets.VBox([b2, self.plot_zone],
                          layout=widgets.Layout(display='flex',
                                                flex_direction='column',
                                                justify_content='space-around',
                                                # height='700px'
                                                ))
        self.box = b3

    def show(self):
        """
        """
        return self.box

    def add_listeners(self):
        """
        """

        # display graph status

        def react_graph(change):
            # print('graph', 'changed from', change.old, 'to', change.new)
            cs = self.cells_in['graph_state']
            cs.value = '2D' if change.new in ['true', 1] else '3D'

        self.cells_in['graph'].observe(react_graph, 'value')

        # display option status

        def react_option(change):
            # print('option', 'changed from', change.old, 'to', change.new)
            cs = self.cells_in['option_state']
            cs.value = 'Call' if change.new in ['true', 1] else 'Put'

        self.cells_in['option'].observe(react_option, 'value')

        def react_button(b):
            # print('button pressed')
            option_state = self.cells_in['option_state'].value

            df_in = self.build_price_input(batch=False)
            df_res = self.price(df_in, option_state)
            # print(df_res.shape)
            self.df_pricing_one = df_res.copy()

            self.display_price_result_vector(df_res)

            df_in = self.build_price_input(batch=True)
            df_res = self.price(df_in, option_state)
            # print(df_res.shape)
            self.df_pricing_batch = df_res.copy()

            # self.display_price_result_plot(df_res)

        self.button_price.on_click(react_button)

    def build_price_input(self, batch=True):
        """
        """
        cells = self.cells_in
        li_ip_key = self.li_ip_key

        graph = cells['graph'].value
        x = cells['x'].value
        y = cells['y'].value

        li_input = []

        for key in li_ip_key:
            cell = cells[key]['value']
            value = [cell.value]
            if batch:
                if (key == x) or (key == x and graph == '3D'):
                    x_min = cells[key]['value_min'].value
                    x_max = cells[key]['value_max'].value
                    nb_step = int(cells['nb_step'].value)
                    value = list(np.linspace(x_min, x_max, num=nb_step))
            li_input.append(value)

        keys = li_ip_key
        values = li_input
        li_cartesian_prod = [dict(zip(keys, e)) for e in it.product(*values)]

        df_in = pd.DataFrame(li_cartesian_prod)
        df_in = df_in[li_ip_key]

        df_in['vol'] = df_in['vol'] / 100
        df_in['rate'] = df_in['rate'] / 100
        df_in['div'] = df_in['div'] / 100

        return df_in

    def price(self, df_in, option_state):
        """
        """
        pricer = {'Call': Price_Call, 'Put': Price_Put}[option_state]

        li_input = df_in.values.tolist()
        li_price = []

        for p in li_input:
            li_price.append(pricer(*p))

        df_out = pd.DataFrame([e for e in li_price])
        li_col = [c for c in self.li_op_key if c in df_out.columns]
        df_out = df_out[li_col]

        df_res = pd.concat([df_in, df_out], axis=1)

        self.status.value = 'Last Price: ' + dt.datetime.now().strftime('%d %b %H:%M:%S')

        return df_res

    def display_price_result_vector(self, df_res):
        """
        """
        for k in self.li_op_key:
            c = self.cells_out[k]
            c.value = 0

        dic_res = df_res.T.to_dict()[0]
        for k, v in dic_res.items():
            if k in self.li_op_key:
                c = self.cells_out[k]
                c.value = v
