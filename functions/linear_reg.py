# Linear Regression
#code from xavier lizarraga

import numpy as np
import matplotlib.pyplot as plt

def linear_regression(x: np.ndarray, y: np.ndarray, degree: int, draw: bool):
    print(f"x: {x}")
    print(f"y: {y}")

    if len(x) != len(y):
        print("x and y have to have the same lenght!")
        return 0

    if degree > 0:
        X = np.ones(len(x))
        for i in range(1, degree):
            x_over = pow(x, i)
            X = np.vstack((X, x_over))
        # transpose X
        X = np.stack(X, axis=1)
        theta = ((np.linalg.pinv(X.T.dot(X))).dot(X.T)).dot(y)

    if draw:
        # Display y
        _, ax = plt.subplots()
        ax.plot(y, "ro", label="y")
        ax.plot(X.dot(theta), "bs", label="Ax")
        plt.axis([-1, x.size + 1, -0.5, 1.5])
        plt.title(f"y vs X*theta with degree= {str(degree)}")
        plt.ylabel("samples")
        plt.xlabel("y[n]")
        ax.legend(loc="upper right", shadow=True)
        plt.grid()
        plt.show()
        error = sum(pow(abs(X.dot(theta) - y), 2))
        return theta, error

draw = True
y = np.random.rand(10)

for i in range(2, 20):
    degree = i
    theta, error = linear_regression(np.arange(0.0, 1.0, 0.1), y, degree, draw)
    print(f"degree: {str(degree)}\nerror: {str(error)}")