import numpy as np
from matplotlib import pyplot as plt
from predictor import predictor as p
from data import source
from datetime import datetime


def label_outer(ax):
    """Modified label_outer()

    x-labels are only kept for subplots on the last row; y-labels only for
    subplots on the first column.
    """
    lastrow = ax.is_last_row()
    firstcol = ax.is_first_col()
    if not lastrow:
        ax.set_xlabel("")
    if not firstcol:
        ax.set_ylabel("")


class MultiplePlots:

    def __init__(self):
        self.s = source.Source()

    def plot(self, model, days, plot_type):
        if '404: Not Found' in self.s.data_confirmed.text:
            print('please update the URL for data if necessary')
        else:
            d = None

            if plot_type == 'confirmed':
                d = self.s.get_confirmed_data()
            elif plot_type == 'deaths':
                d = self.s.get_deaths_data()
            else:  # recovered
                d = self.s.get_recovered_data()

            n = len(d)-1
            px = 3
            py = int(np.ceil(n/px))
            plt.rcParams['figure.figsize'] = [15, 5*py]
            fig, axs = plt.subplots(py, px)
            x = d[('Province/State', 'Country/Region')]

            # list of keys for dictionary
            k = list(d.keys())

            # skip the first entry
            k_index = 1

            for i in range(py):
                for j in range(px):
                    if k_index >= len(k):
                        axs[i, j].axis('off')
                    else:
                        y = d[k[k_index]]

                        if y is None:
                            continue

                        axs[i, j].plot(x, y, '.')
                        axs[i, j].set_title(k[k_index])

                        pred = p.Predictor(days, np.array([x, y]))
                        u = None

                        if model == 'polynomial_2':
                            u = pred.polynomial_regression(2)
                        elif model == 'polynomial_3':
                            u = pred.polynomial_regression(3)
                        elif model == 'polynomial_4':
                            u = pred.polynomial_regression(4)
                        elif model == 'polynomial_5':
                            u = pred.polynomial_regression(5)
                        elif model == 'exponential':
                            u = pred.exponential_regression()
                        else:
                            # default polynomial_1
                            u = pred.polynomial_regression(1)

                        axs[i, j].plot(u[0], u[1], 'r')

                        print('\n', k[k_index])
                        day_num = self.s.first_day + 24*3600*(u[0][-days:])

                        print('time range:', datetime.fromtimestamp(day_num[0]).date(), '-',
                              datetime.fromtimestamp(day_num[-1]).date())

                        print('predictions:',
                              u[1][-days:])

                        k_index += 1

            for ax in axs.flat:
                if plot_type == 'confirmed':
                    ax.set(xlabel='Days', ylabel='Confirmed Cases')
                elif plot_type == 'deaths':
                    ax.set(xlabel='Days', ylabel='Deaths')
                else:  # recovered
                    ax.set(xlabel='Days', ylabel='Recovered Cases')

            # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                label_outer(ax)


if __name__ == "__main__":
    days = 3
    z = MultiplePlots()
    z.plot('exponential', days, 'confirmed')