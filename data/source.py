import requests
import numpy as np
from datetime import datetime
import copy


class Source:

    directory = {'confirmed':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv',
                 'deaths':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv',
                 'recovered':'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
                 }

    def __init__(self):
        self.d = {}
        self.data_confirmed = requests.get(self.directory['confirmed'])
        self.data_deaths = requests.get(self.directory['deaths'])
        self.data_recovered = requests.get(self.directory['recovered'])
        self.data = None
        self.first_day = None

    def get_confirmed_data(self):
        self.data = self.data_confirmed
        self.data_processing()
        return copy.deepcopy(self.d)

    def get_deaths_data(self):
        self.data = self.data_deaths
        self.data_processing()
        return copy.deepcopy(self.d)

    def get_recovered_data(self):
        self.data = self.data_recovered
        self.data_processing()
        return copy.deepcopy(self.d)

    def data_processing(self):
        self.d = {}

        if '404: Not Found' in self.data.text:
            print('please update the URL for data if necessary')
        else:
            r1 = self.data.text.strip().split('\n')

            mainland_china = None
            out_of_mainland_china = None

            for i in r1:
                r2 = i.split(',')
                l = len(r2)

                if r2[0].startswith('\"'):
                    province = (r2[0]+","+r2[1], r2[2])
                    r2.pop(0)
                else:
                    province = (r2[0], r2[1])

                # print('\n', province, '\n')

                row_data= []

                if province[0] == 'Province/State':
                    row_data = [datetime.strptime(j.strip(), '%m/%d/%y').timestamp() for j in r2[4:l]]
                    row_data = np.asarray(row_data, dtype='float')
                    self.first_day = row_data[0]
                    row_data -= row_data[0]
                    row_data /= (24*3600)
                else:
                    row_data = [(float(j) if j else 0.0) for j in r2[4:l]]
                    row_data = np.asarray(row_data, dtype='float')

                # print(row_data)
                self.d.update({province : row_data})

                if province[1] == 'Mainland China':
                    if mainland_china is None:
                        mainland_china = row_data.copy()
                    else:
                        mainland_china += row_data.copy()
                elif province[1] != 'Country/Region':
                    if out_of_mainland_china is None:
                        out_of_mainland_china = row_data.copy()
                    else:
                        out_of_mainland_china += row_data.copy()

            self.d.update({('Total', 'Mainland China'): mainland_china})
            self.d.update({('Total', 'Out of Mainland China'): out_of_mainland_china})
