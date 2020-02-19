import numpy as np
import numpy.polynomial.polynomial as poly


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

        for i in range(self.y.shape[0]):
            if self.y[i, 0] == 0:
                self.y[i, 0] += 0.001

        b = np.log(self.y)
        a2 = np.matmul(a.transpose(), a)
        b2 = np.matmul(a.transpose(), b)
        c = np.matmul(np.linalg.inv(a2), b2)
        c = np.exp(c.transpose()[0])

        val = np.arange(1, self.days+1, dtype=float)
        val += self.x[-1]
        val = val.reshape((1, val.shape[0]))
        val = np.append(self.x.transpose(), val, axis=1)

        return np.array([val[0], c[0]*np.power(c[1], val[0])])


if __name__ == "__main__":
    p = Predictor(7, np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]]))
    print(p.polynomial_regression(2))
    print(p.exponential_regression())
