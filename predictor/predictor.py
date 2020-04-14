import numpy as np
import numpy.polynomial.polynomial as poly
from matplotlib import pyplot as plt


class Predictor:

    def __init__(self, days, data):
        data = data.transpose()
        self.x = data[:, 0:1].copy()
        self.y = data[:, 1:2].copy()
        self.days = days

    def polynomial_regression(self, n):
        # get regression
        first_col = np.ones((self.x.shape[0], 1))
        a = np.append(first_col, self.x, axis=1)

        if n >= 2:
            for i in range(2, n+1):
                a = np.append(a, self.x**i, axis=1)

        b = self.y
        a2 = np.matmul(a.transpose(), a)
        b2 = np.matmul(a.transpose(), b)
        c = np.matmul(np.linalg.inv(a2), b2)
        c = c.transpose()[0]
        val = np.arange(1, self.days+1, dtype=float)
        val += self.x[-1]
        val = val.reshape((1, val.shape[0]))
        val = np.append(self.x.transpose(), val, axis=1)

        return np.array([val[0], poly.polyval(val[0], c)])

    def exponential_regression(self):
        # get regression
        first_col = np.ones((self.x.shape[0], 1))
        a = np.append(first_col, self.x, axis=1)

        temp = self.y.copy()

        for i in range(self.y.shape[0]):
            if self.y[i, 0] <= 0:
                self.y[i, 0] = 0.001

        b = np.log(self.y)
        a2 = np.matmul(a.transpose(), a)
        b2 = np.matmul(a.transpose(), b)
        c = np.matmul(np.linalg.inv(a2), b2)
        c = np.exp(c.transpose()[0])

        val = np.arange(1, self.days+1, dtype=float)
        val += self.x[-1]
        val = val.reshape((1, val.shape[0]))
        val = np.append(self.x.transpose(), val, axis=1)

        self.y = temp

        return np.array([val[0], c[0]*np.power(c[1], val[0])])

    def derivative(self):
        der = np.array([])

        n = self.y.shape[0]

        for i in range(n):
            if i == 0:
                der = np.append(der, self.y[i, 0])
            else:
                der = np.append(der, self.y[i, 0] - self.y[i-1, 0])

        return der

    def gaussian(self):
        """Adjusting a Gaussian function to the daily increment
        f(x) = A * exp((-(x-B)^2)/(2*C^2))

        :return:
        """

        d = np.expand_dims(self.derivative(), axis=1)
        der_x = self.x.copy()

        # data preprocessing
        while d[0] == 0:
            # remove zeros at start
            d = np.delete(d, 0, axis=0)
            der_x = np.delete(der_x, 0, axis=0)

            if d.size == 0:
                break

        for i in reversed(range(d.shape[0])):
            if d[i] <= 0:
                d = np.delete(d, i, axis=0)
                der_x = np.delete(der_x, i, axis=0)

        if der_x.shape[0] == 0:
            return np.array([[0], [0]])

        der_y = np.log(d)

        # get regression
        first_col = np.ones((der_x.shape[0], 1))
        a = np.append(first_col, der_x, axis=1)

        for i in range(2, 3):
            a = np.append(a, der_x**i, axis=1)

        b = der_y
        a2 = np.matmul(a.transpose(), a)
        b2 = np.matmul(a.transpose(), b)

        c = np.matmul(np.linalg.pinv(a2), b2)

        if c[2] == 0:
            c[2] = 0.001

        # square of c2
        c2_2 = -1/(2*c[2])

        c1 = c[1]*(-1/(2*c[2]))
        c0 = np.exp(c[0]+0.5*(c1**2/c2_2))

        val = np.arange(1, self.days+1, dtype=float)
        val += self.x[-1, :]
        val = val.reshape((val.shape[0], 1))
        val = np.append(self.x, val, axis=0)

        y2 = c0*np.exp((-(val - c1)**2)/(2*c2_2))
        plt.plot(val, y2, 'r')

        return np.array([val.transpose()[0], y2.transpose()[0]])


if __name__ == "__main__":
    p = Predictor(30, np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]]))
    # print(p.polynomial_regression(2))
    # print(p.exponential_regression())
    print(p.gaussian())
