import PySimpleGUI as sg
import os.path
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
from collections import Counter
from SearchAPI import *


def draw_figure_on_canvas(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')


MLINE_KEY = 'Textbox'

layout = [[sg.Text('Web Search')],
          [sg.Text('Enter Query: '), sg.InputText(key='Query'), sg.Button('Search', bind_return_key=True),
           sg.Button('Reset')],
          [sg.Multiline(key=MLINE_KEY, size=(70, 30), disabled=True), sg.Canvas(size=(70, 30), key='Canvas')]]

# Create the Window
window = sg.Window('Project', layout)
# Event Loop to process "events" and get the "values" of the inputs
fig_agg = None
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    if event == 'Reset':
        window['Query'].update('')
    if event == 'Search' and values['Query'] != "" and not values['Query'].isspace():
        window[MLINE_KEY].update(search(values['Query']))
        if fig_agg is not None:
            delete_fig_agg(fig_agg)
        fig_agg = draw_figure_on_canvas(window['Canvas'].TKCanvas, plot())
window.close()
