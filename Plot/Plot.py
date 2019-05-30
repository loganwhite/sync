import copy
import math

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rc

# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.



def plot_config(plt):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    matplotlib.rc('xtick', labelsize=18)
    matplotlib.rc('ytick', labelsize=18)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.rc('axes', axisbelow=True)
    plt.grid(True, linestyle='--')


def set_box_color(bp, color, hatch):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)




"""
    plot a figure with given parameter and save it to a pdf file

    filename: the name of the generated PDF file
    title: the title of the figure displayed
    figsize: the width and the height of the figure in inches
    x_vector: the x scale value of each point
    y_vector: the y scale value of each point
    style: the style of strokes.
"""
def plot_pdf(filename="figure.pdf", title="", figsize=(3,3), num_round=0,
        x_vector=[], y_vector_list=[], x_label="", y_label="", legend=[], style=[], marker=[]):
    # plot the figure with set iterations
    if num_round != 0:
        iterations = num_round
        x_vector = x_vector[:num_round]
        for i in range(len(y_vector_list)):
            y_vector_list[i] = y_vector_list[i][:num_round]


    with PdfPages(filename) as pdf:
        plot_config(plt)

        min_value = min(min(y_vector_list))
        max_value = max(max(y_vector_list))
        margin = (max_value - min_value) * 0.01
        plt.ylim(ymin=min_value - margin * 5, ymax=max_value+margin*55)
        for i in range(len(y_vector_list)):
            plt.plot(x_vector, y_vector_list[i], linestyle=style[i], marker=marker[i], linewidth=3)
        plt.title(title)
        plt.xlabel(x_label, fontsize=18)
        plt.ylabel(y_label, fontsize=18)
        if len(legend) != 0:
            plt.legend(legend, loc='best', ncol=2)
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


def simple_plot(filename="figure.pdf", x_vector=[], y_vector_list=[], legend=[], marker=[], x_label="", y_lable=""):
    print y_vector_list
    with PdfPages(filename) as pdf:
        plot_config(plt)

        for i in range(len(y_vector_list)):
            plt.plot(x_vector, y_vector_list[i], linewidth=3, marker=marker[i])

        plt.xlabel(x_label, fontsize=18)
        plt.ylabel(y_lable, fontsize=18)
        if len(legend) != 0:
            plt.legend(legend, loc='best', ncol=3)
        plt.tight_layout(pad=1)

        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

def box_pdf(filename="box.pdf", data=[], xtick=[], x_label="", y_label=""):

    num_list = [i for i in range(1, len(xtick) + 1)]

    with PdfPages(filename) as pdf:
        plot_config(plt)

        plt.xlabel(x_label, fontsize=18)
        plt.ylabel(y_label, fontsize=18)
        plt.xticks(num_list, xtick, rotation=90)
        plt.tight_layout(pad=1)

        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

def box_group_pdf(filename="box.pdf", data=[], xtick=[], x_label="", y_label="",
                  legend=[], width=0.3, hline=0):
    index = np.arange(len(data[0]), dtype=np.float)
    index *= ((width + 0.1) * len(data))

    # num_list = [i for i in range(1, len(xtick) + 1)]

    with PdfPages(filename) as pdf:
        if 'two' in filename:
            plt.figure(figsize=(15, 5))
        else:
            plt.figure()

        plot_config(plt)


        for i in range(len(data)):
            pos = index + width * (i + 1) - len(data) / 2 * width
            boxplt = plt.boxplot(data[i],
                                 positions=pos,
                                 # positions=index + width * (i+1) + width,
                                 widths=width,
                                 # patch_artist=True,
                                 whis=[0, 100])
            set_box_color(boxplt, ['blue', 'darkorange', 'darkgreen',
                                   'black', 'darkorange', 'cyan', 'magenta'][i],
                          ['/', '\\', '|', '-', '+', 'x', '.', '*', 'o', 'O'][i])

            # draw temporary red and blue lines and use them to create a legend
            plt.axhline(y=hline, color='black', linestyle='--')
            plt.plot([], c=['blue', 'darkorange', 'darkgreen',
                            'black', 'darkorange', 'cyan', 'magenta'][i], label=legend[i])


        tick_pos = index + (width * len(data) / 2)
        if 'two' in filename:
            plt.legend(loc='best', ncol=3, fontsize=25)
            plt.xlabel(x_label, fontsize=25)
            plt.ylabel(y_label, fontsize=25)
            plt.xticks(tick_pos, xtick, fontsize=25)
        else:
            plt.legend(loc='best', fontsize=18)
            plt.xlabel(x_label, fontsize=18)
            plt.ylabel(y_label, fontsize=20)
            plt.xticks(tick_pos, xtick, fontsize=18)
        plt.tight_layout(pad=1)
        plt.xlim(left=-0.5)

        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


def bar_char_pdf(filename="barchar.pdf", data=[], xticks=[], width=0.35,
                 legend=[], x_label="", y_label=""):
    index = np.arange(len(data[0]), dtype=np.float)
    index *= ((width+0.1) * len(data))


    with PdfPages(filename) as pdf:

        if 'two' in filename:
            plt.figure(figsize=(15, 5))
        else:
            plt.figure()
        plot_config(plt)
        min_value = min(min(data))
        max_value = max(max(data))
        if min_value == 0:
            copy_data = copy.deepcopy(data)
            copy_data.remove(min(copy_data))
            min_value = min(min(copy_data))


        margin = (max_value - min_value) * 0.1
        # axes = plt.gca()
        # axes.set_xlim([xmin, xmax])
        # axes.set_ylim([max_value - margin * 5, max_value + margin * 5])
        y_min = (min_value - margin * 5)
        y_max = (max_value + margin * 5)
        if y_min < 0:
            y_min = 0

        if y_max != y_min:
            plt.ylim(ymin=y_min, ymax=y_max)
        else:
            if y_max != 0:
                plt.ylim(ymax=y_max * 1.25)
        # if 'Percent' in filename:
        #     plt.ylim(ymin=0, ymax=1.5)

        for i in range(len(data)):
            plt.bar(index + width * i, data[i], width,
                    hatch=['/', '-', '+', '\\', '|', 'x', '.', '*', 'o', 'O'][i])

        if len(legend) != 0:
            if 'two' in filename:
                plt.legend(legend, loc='best', ncol=3, fontsize=25)
                plt.xlabel(x_label, fontsize=25)
                plt.ylabel(y_label, fontsize=25)
                plt.xticks(index + width * len(data) / 2, xticks, fontsize=25)
            else:
                plt.legend(legend, loc='best', ncol=2, fontsize=18)
                plt.xlabel(x_label, fontsize=18)
                plt.ylabel(y_label, fontsize=20)
                plt.xticks(index + width * len(data) / 2, xticks, fontsize=18)

        plt.tight_layout(pad=1)

        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


