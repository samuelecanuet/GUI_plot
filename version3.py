# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 15:18:31 2022

@author: samue
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 18:12:36 2022

@author: samue
"""
import sys
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path
import numpy as np
import PIL
from lmfit.models import ExpressionModel
from matplotlib.lines import Line2D

def update_data(data_, skip_, deli_, err_):
    data_ = np.genfromtxt(data_, skip_header = int(skip_), delimiter = deli_)
    
    x = data_[:,0]
    y = data_[:,1]
    
    if err_[0] == 0 and err_[1] == 0 and err_[2] == 0 and err_[3] == 0:
        return x, y, 0, 0
    
    if err_[2] == 0 and err_[3] == 0:
        if err_[0] == 0:
            return x, y, 0, [i*err_[1] for i in range(len(x))]
        if err_[1] == 0:
            return x, y, [i*err_[0] for i in range(len(x))], 0  
        else:
            return x, y, [i*err_[0] for i in range(len(x))], [i*err_[1] for i in range(len(x))]
    
    else:
        if err_[2] == 0:
            return x, y, 0, data_[:, err_[3]]
        if err_[3] == 0:
            return x, y, data_[:, err_[2]], 0
        else:
            return x, y, data_[:, err_[2]], data_[:, err_[3]]
            
        

def update_fit(expression_, x_, y_):
    gmod = ExpressionModel(expression_)
    for i in gmod.param_names:
        gmod.set_param_hint(i, value=1)
    params = gmod.make_params()
    result = gmod.fit(y_, params, x=x_).best_fit
    
    return x_, result

def update_figure(xdata_, xdataerr_, ydata_, ydataerr_, sdata_, cdata_, mdata_, legdata_, xfit_, yfit_, sfit_, cfit_, mfit_, legfit_, grid_, xlab_, ylab_, xlim_, ylim_):
    mdata_ = [k for k, v in Line2D.markers.items() if v == mdata_][0]
    mfit_ = [k for k, v in Line2D.markers.items() if v == mfit_][0]
    axes[0].scatter(xdata_, ydata_ ,color = cdata_, s=sdata_, marker = str(mdata_), label = legdata_)
    #axes[0].errorbar(xdata, ydata, xerr=xdataerr_, yerr=ydataerr_, capsize=serr_, ecolor=cerr_)
    
    try:
        len(xfit_)
        res=True
    except TypeError:
        res=False
    
    if res==True:
        axes[0].plot(xfit_, yfit_, color = cfit_, linewidth=sfit_, marker = str(mfit_), label = legfit_)
        
    

    if xlim_[0]!=xlim_[1] and xlim_[0] < xlim_[1]:
        ax.set_xlim(xlim_)
    if ylim_[0]!=ylim_[1] and ylim_[0] < ylim_[1]:
        ax.set_ylim(ylim_)
        
    if legdata_== ' ' and legfit_== ' ': 
        pass
    if legdata_ != ' ' and legfit_ == ' ':
        ax.legend()
    else:
        ax.legend()
        
        
    ax.grid(grid_)
    ax.set_ylabel(ylab_)
    ax.set_xlabel(xlab_)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

def update_lim(lims_):
    for i in lims_:
        try:
            int(values[i])
            res=True
        except ValueError:
            res=False
            
        if res==True and len(values[i]) > len(values[i])-1:
            window[i].set_size((len(values[i])+1,None))
         
sg.ChangeLookAndFeel('Reddit')
graphic_layout = [
    [sg.Checkbox('Grid', key='-GRID-', enable_events=False)],
    [sg.Text('x label : '), sg.Input('x', key='-X_LAB-', size=(1, 1)), sg.Push(), sg.Text('x limit : '), sg.Input(key='-X_LIMd-', size=(2, 1)), sg.Text('to'), sg.Input(key='-X_LIMu-', size=(2, 1))],
    [sg.Text('y label : '), sg.Input('y', key='-Y_LAB-', size=(1, 1)), sg.Push(), sg.Text('y limit : '), sg.Input(key='-Y_LIMd-', size=(2, 1)), sg.Text('to'), sg.Input(key='-Y_LIMu-', size=(2, 1))]     
    ]

layouterror=[[sg.Text('Cap size = '), sg.Slider(key='-bar_size-', orientation='h', range=(1, 10), default_value=5, resolution=0.1)], 
           [sg.In("", visible=False, enable_events=True, key='bar_color'), sg.Text('Point size : '), sg.Slider(range = (0.1,30), orientation = 'h', key = '-POINT_DATA-', default_value = 5, resolution = 0.5)],
           [sg.Text('Color : '), sg.ColorChooserButton("", size=(5, 1), target='bar_color', button_color=('#FF0000', '#FF0000'), border_width=1, key='data_color_chooser')],
           [sg.Text('Legend : '), sg.InputText( ' ', key='bar_legend')]
           ]

data_layout = [
    [sg.In("", visible=False, enable_events=True, key='data_color'), sg.Text('Point size : '), sg.Slider(range = (0.1,30), orientation = 'h', key = '-POINT_DATA-', default_value = 5, resolution = 0.5)],
    [sg.Text('Color : '), sg.ColorChooserButton("", size=(5, 1), target='data_color', button_color=('#FF0000', '#FF0000'), border_width=1, key='data_color_chooser')],
    [sg.Text('Marker : '), sg.InputCombo([i for i in Line2D.markers.values()], size=(20, 1), key='data_marker', default_value = 'circle')],
    [sg.Text('Legend : '), sg.InputText( ' ', key='data_legend')],
    [sg.Frame('Error bar', layouterror, visible=False)]
    ]

fit_layout = [
    [sg.In("", visible=False, enable_events=True, key='fit_color'), sg.Text('Point size : '), sg.Slider(range = (0.1,30), orientation = 'h', key = '-POINT_FIT-', default_value = 5, resolution = 0.5)],
    [sg.Text('Color : '), sg.ColorChooserButton("", size=(5, 1), target='fit_color', button_color=('#0000FF', '#0000FF'), border_width=1, key='fit_color_chooser')],
    [sg.Text('Marker : '), sg.InputCombo([i for i in Line2D.markers.values()], size=(20, 1), key='fit_marker', default_value = 'circle')],
    [sg.Text('Legend : '), sg.Input(key='fit_legend')]
    ]

control_col = sg.Column([
    [sg.Frame('Graphic Setup', layout = graphic_layout)],
    [sg.Frame('Data Setup', layout = data_layout)],
    [sg.Frame('Fit Setup' , layout = fit_layout)]
    ])

graphic_col = sg.Column([
    [sg.Text(r'f(x) = '), sg.Input(key='-Function-'), sg.Button('Run')],
	[sg.Canvas(key = '-CANVAS-')]
])

layout=[[graphic_col, control_col], [sg.Push(), sg.Button('Save As')]]


changefit=False
changedata=False
colordata = 'r'
colorfit = 'b'
colorerror = 'grey'
legenddata = None
legendfit = None
legenderror = None

layoutdatax = [[sg.Checkbox('Column in data file', visible=True, key='-data_filex-', default=False), sg.Checkbox('Systematic', visible=True, key='-systematicx-', default=False)],
               [sg.Text('Column data : n°', key='-txt_datax-', visible=False), sg.Input(key='-input_colx-', visible=False, size=(3, 1)), sg.Text('x error = ', key='-txt_sysx-', visible=False), sg.Input(key='-input_sysx-', visible=False, size=(5, 1))]
               ]
layoutdatay = [[sg.Checkbox('Column in data file', visible=True, key='-data_filey-', default=False), sg.Checkbox('Systematic', visible=True, key='-systematicy-', default=False)], 
               [sg.Text('Column data : n°', key='-txt_datay-', visible=False), sg.Input(key='-input_coly-', visible=False, size=(3, 1)), sg.Text('y error = ', key='-txt_sysy-', visible=False), sg.Input(key='-input_sysy-', visible=False, size=(5, 1))]
               ]
              

layoutpop = [[sg.Text('Filename')],[sg.Input(' ', key='-File_Path-'), sg.FileBrowse(key='browse')], 
  [sg.Text('Delimiter : '), sg.Input(key='-Delimiter-', size=(2,1)), sg.Text('Skip Header : '), sg.Input(key='-SkipHeader-', size=(2,1))],
  [sg.Checkbox('Input error', key='-Input_Error-')],
  [sg.Frame('x Error', layoutdatax, visible=False, key='-xerror-'), sg.Frame('y Error', layoutdatay, visible=False, key='-yerror-')],
  [sg.Button('OK'), sg.Button('Visualize')],
  ]


location=(600, 600)
windowpop = sg.Window('Get CSV file', layoutpop)

openn=0
while True:
    eventpop, valuespop = windowpop.Read(timeout=100)
    if eventpop == sg.WIN_CLOSED:
        break

    if valuespop['-Input_Error-']:
        windowpop['-xerror-'].Update(visible=True)
        windowpop['-yerror-'].Update(visible=True)
    else:
        windowpop['-xerror-'].Update(visible=False)
        windowpop['-yerror-'].Update(visible=False)
           
        
    if valuespop['-data_filex-']==True:
        if valuespop['-systematicx-']==False:
            windowpop['-txt_datax-'].Update(visible=True)
            windowpop['-input_colx-'].Update(visible=True)
            
        if valuespop['-systematicx-']==True:
            windowpop['-data_filex-'].Update(value=False)
    
    else:
        windowpop['-txt_datax-'].Update(visible=False)
        windowpop['-input_colx-'].Update(visible=False)
        
        if valuespop['-systematicx-']==False:
            windowpop['-txt_sysx-'].Update(visible=False)
            windowpop['-input_sysx-'].Update(visible=False)
            
            
        if valuespop['-systematicx-']==True:
            windowpop['-txt_sysx-'].Update(visible=True)
            windowpop['-input_sysx-'].Update(visible=True)
                
  
        
    if valuespop['-data_filey-']==True:
        if valuespop['-systematicy-']==False:
            windowpop['-txt_datay-'].Update(visible=True)
            windowpop['-input_coly-'].Update(visible=True)
            
        if valuespop['-systematicy-']==True:
            windowpop['-data_filey-'].Update(value=False)
    
    else:
        windowpop['-txt_datay-'].Update(visible=False)
        windowpop['-input_coly-'].Update(visible=False)
        
        if valuespop['-systematicy-']==False:
            windowpop['-txt_sysy-'].Update(visible=False)
            windowpop['-input_sysy-'].Update(visible=False)
            
            
        if valuespop['-systematicy-']==True:
            windowpop['-txt_sysy-'].Update(visible=True)
            windowpop['-input_sysy-'].Update(visible=True)
        

        
    if eventpop == 'OK':
        data = valuespop['-File_Path-']
        skip = valuespop['-SkipHeader-']
        deli = valuespop['-Delimiter-']
        listefit = [None, None]
        listedata=[0, 0]
        listeerr=[0, 0]
        error=[0, 0, 0, 0]
        
        
        
        
        if valuespop['-systematicx-']==True:
            error[0] = (valuespop['-input_sysx-'])
        if valuespop['-systematicy-']==True:
            error[1] = (valuespop['-input_sysy-'])
            
            
        if valuespop['-data_filex-']==True:
            error[2] = (valuespop['-input_colx-'])
        if valuespop['-data_filey-']==True:
            error[3] = (valuespop['-input_coly-'])

        
        
    
        listedata[0], listedata[1], listeerr[0], listeerr[1] = update_data(data, skip, deli, error)
        
    
        
    if eventpop == 'OK':
        openn=1
        break
         
windowpop.close()


if openn==1:
    window = sg.Window('Graph App', layout, finalize=True)
    # matplotlib
    fig = matplotlib.figure.Figure(dpi=110)
    ax=fig.add_subplot(111)
    ax.plot([],[])
    figure_canvas_agg = FigureCanvasTkAgg(fig,window['-CANVAS-'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()
    axes = fig.axes
    

    while True:
        event, values = window.read(timeout=1000)
        if event == sg.WIN_CLOSED:
            break
        
        axes[0].clear()
        update_figure(listedata[0], 
                      listeerr[0],
                          listedata[1],
                          listeerr[1],
                          values['-POINT_DATA-'],
                          colordata,
                          values['data_marker'],
                          values['data_legend'],
                          listefit[0],
                          listefit[1],
                          values['-POINT_FIT-'],
                          colorfit,
                          values['fit_marker'],
                          values['fit_legend'],
                          values['-GRID-'],
                          values['-X_LAB-'], 
                          values['-Y_LAB-'],
                          (values['-X_LIMd-'], values['-X_LIMu-']),
                          (values['-Y_LIMd-'], values['-Y_LIMu-']))
        
        if event == 'Run':
            try:
                listefit[0], listefit[1] = update_fit(values['-Function-'], listedata[0], listedata[1])
            except:
                sg.PopupError('{}'.format(sys.stdout))
                
                
        if event == 'Save as':
            save_path = sg.popup_get_file('Save', save_as = True, no_window = True) + '.png'
            image = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
            image.save(save_path, 'PNG')
        
        update_lim(('-X_LIMd-', '-X_LIMu-', '-Y_LIMd-', '-Y_LIMu-', '-X_LAB-', '-Y_LAB-'))
            
        if event == 'data_color':
            window['data_color_chooser'].Update(button_color=(values[event], values[event]))
            colordata=values[event]
        
        if event == 'fit_color':
            window['fit_color_chooser'].Update(button_color=(values[event], values[event]))
            colorfit=values[event]
            
            
            
        
        
        
    window.close()