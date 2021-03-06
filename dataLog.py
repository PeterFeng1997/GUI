'''

    ************************************************************************
    *   FILE NAME:      dataLog.py
    *   AUTHORS:         Dylan Vogel, Peter Feng
    *   PURPOSE:        This file contains functions used for logging the results
    *                   of heater tests
    *
    *   EXTERNAL REFERENCES:    os, time
    *
    *
    *   NOTES:          None.
    *
    *
    *   REVISION HISTORY:
    *
    *                   2017-05-22: Created file.
    *                   2017-05-23: Wrote a function for creating plots.

'''

import os
import time

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import datetime

import controller
#



from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

#
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout

global datafile


def setup(label):
    global datafile

    t = time.localtime()
    dir_name = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        os.chmod(dir_name, 0o777)

    file_name = label + '-' + str(t.tm_hour) + '-' + str(t.tm_min) + '-' + str(t.tm_sec)
    datafile = open(dir_name + '/' + file_name, 'a')
    '''
    datafile.write('Working temperature:' + str(work_temp)+ '\n' )
    datafile.write('Safe temperature:' + str(safe_temp)+ '\n' )
    datafile.write('Bonding time:' + str(heat_time) + '\n')
    datafile.write('PWM frequency:' + str(pwm_freq) + '\n')
    datafile.write('PID parameter SSR1: Kp/Ki/Kd:' + str(pid1.Kp) + '\t\t' + str(pid1.Ki) +'\t\t'+ str(pid1.Kd) +'\n')
    datafile.write('PID parameter SSR2: Kp/Ki/Kd:' + str(pid2.Kp) + '\t\t' + str(pid2.Ki) +'\t\t'+ str(pid2.Kd)+'\n')
    datafile.write('Time (s) \tTemp1 (C) \tTemp2 (C) \tDutyCycle1 \tDutyCycle2 \n')   # Column header
    '''


def write(type, data, message):
    ''' Valid types (thus far):
        COL
        LINE
    '''
    if (type == 'COL'):
        for i in range(0, len(data)):
            datafile.write(message[i] + str(data[i]) + '\t')
        datafile.write('\n')
    elif (type == 'LINE'):
        datafile.write(message + str(data) + '\n')


def createPlot(x, y1, y2, heat_time, coefficients_center, coefficients_edge, original_center_values,
               original_edge_values, window):
    # getting the current time and date
    now = datetime.datetime.now()

    # creating strings to describe the PID setup for the center and edge thermocouples
    # pid_center_string = "center- [" + str(coefficients_center['P']) + "," + str(coefficients_center['I']) + "," + str(coefficients_center['D']) + "] "
    # pid_edge_string = "edge- [" + str(coefficients_edge['P']) + "," + str(coefficients_edge['I']) + "," + str(coefficients_edge['D']) + "] "

    original_center_string = "(" + str(original_center_values['P']) + "," + str(
        original_center_values['I']) + "," + str(original_center_values['D']) + ")"
    new_center_string = "(" + str(coefficients_center['P']) + "," + str(coefficients_center['I']) + "," + str(
        coefficients_center['D']) + ")"
    original_edge_string = "(" + str(original_edge_values['P']) + "," + str(original_edge_values['I']) + "," + str(
        original_edge_values['D']) + ")"
    new_edge_string = "(" + str(coefficients_edge['P']) + "," + str(coefficients_edge['I']) + "," + str(
        coefficients_edge['D']) + ")"

    pid_center_string = "center - [" + original_center_string + "," + new_center_string + "]"
    pid_edge_string = "edge - [" + original_edge_string + "," + new_edge_string + "]"


    #GUI graphing
    window.graphWidget.figure = plt.figure()
    window.graphWidget.canvas = FigureCanvas(window.graphWidget.figure)
    window.graphWidget.toolbar = NavigationToolbar(window.graphWidget.canvas, window)

    window.graphWidget.layout = QVBoxLayout()
    window.graphWidget.layout.addWidget(window.graphWidget.toolbar)
    window.graphWidget.layout.addWidget(window.graphWidget.canvas)

    window.graphWidget.setLayout(window.graphWidget.layout)


    # instead of ax.hold(False)
    window.graphWidget.figure.clear()

    # create an axis
    window.graphWidget.ax = window.graphWidget.figure.add_subplot(111)

    # discards the old graph
    # ax.hold(False) # deprecated, see above

    # plot data
    window.graphWidget.ax.plot(x, y1, 'r', x, y2, 'b')
    window.graphWidget.ax.set_xlabel('Time From Start (s)')
    window.graphWidget.ax.set_ylabel('Temperature (C)')
    window.graphWidget.ax.set_title('Heating Characteristics for ' + pid_center_string + ' ' + pid_edge_string)


    # refresh canvas
    window.graphWidget.canvas.draw()
    window.update()



    #GUI graphing

    # the original pdf that will be saved as a pdf
    fig_original = plt.figure()
    fig_original.set_size_inches(12, 10)

    plt.plot(x, y1, 'r', x, y2, 'b')
    plt.ylabel('Temperature (C)')
    plt.xlabel('Time From Start (s)')
    plt.title('Heating Characteristics for ' + pid_center_string + ' ' + pid_edge_string)

    # saving the figure with a formatted name that includes information about the PID setup and the time and date
    fig_original.savefig(pid_center_string + pid_edge_string + now.strftime("%I:%M%p - %B %d - %Y") + '-graph.pdf')


def write_line_to_log(t_center, t_edge, pwm_center, pwm_edge, curr_t, start_t, cent_temps, edge_temps, times, window): #change
    d_time = round((curr_t - start_t), 2)

    times.append(d_time)
    cent_temps.append(t_center)
    edge_temps.append(t_edge)

    write('COL', [d_time, t_center, t_edge, round(pwm_center, 3), round(pwm_edge, 3)],
          ['Time: ', 'Temp_1: ', 'Temp_2: ', 'Duty_center: ', 'Duty_edge: '])
    '''
    print('Time: ' + str(d_time) + '\t' + 'Temp_1: ' + str(t_center) + '\t' + 'Temp_2: ' + str(
        t_edge) + '\t' + 'Duty_center: ' + str(round(pwm_center, 3)) + '\t' + 'Duty_edge: ' + str(round(pwm_edge, 3)))
    '''

    window.outputMessage.append('[Time: ' + str(d_time) + ']\t' + '[Temp_1: ' + str(t_center) + ']\t' + '[Temp_2: ' + str(
        t_edge) + ']\t' + '[Duty_center: ' + str(round(pwm_center, 3)) + ']\t' + '[Duty_edge: ' + str(round(pwm_edge, 3)) + "]")

    window.outputMessage.update()

def close():
    datafile.close()
