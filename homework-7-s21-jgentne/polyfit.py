import matplotlib.pyplot as plt
import numpy as np

# Return fitted model parameters to the dataset at datapath for each choice in degrees.
# Input: datapath as a string specifying a .txt file, degrees as a list of positive integers.
# Output: paramFits, a list with the same length as degrees, where paramFits[i] is the list of
# coefficients when fitting a polynomial of d = degrees[i].


def main(datapath, degrees):

    paramFits = []

    # iterate through each n in degrees, calling the feature_matrix and least_squares functions to solve

    data = np.loadtxt(datapath)
    x_file = data[:, 0]
    y_file = data[:, 1]

    # for the model parameters in each case. Append the result to paramFits each time.
    # read the input file, assuming it has two columns, where each row is of the form [x y] as
    # in poly.txt.

    for n in degrees:
        z = feature_matrix(x_file, n)
        paramFits.append(least_squares(z, y_file))

    plt.scatter(x_file, y_file)
    x_file = np.sort(x_file)

    for deg in degrees:
        beta = paramFits[deg - 1]
        matrx = feature_matrix(x_file, deg)
        prediction = matrx @ beta
        plt.plot(x_file, prediction, label=deg)

    plt.legend()
    plt.savefig("Graph 1")

    return paramFits


# Return the feature matrix for fitting a polynomial of degree d based on the explanatory variable
# samples in x.
# Input: x as a list of the independent variable samples, and d as an integer.
# Output: X, a list of features for each sample, where X[i][j] corresponds to the jth coefficient
# for the ith sample. Viewed as a matrix, X should have dimension #samples by d+1.


def feature_matrix(x, d):

    # There are several ways to write this function. The most efficient would be a nested list comprehension
    # which for each sample in x calculates x^d, x^(d-1), ..., x^0.

    X = []

    for u, v in enumerate(x):
        X.append([])
        for app in range(d, -1, -1):
            X[u].append(v ** app)

    return X


# Return the least squares solution based on the feature matrix X and corresponding target variable samples in y.
# Input: X as a list of features for each sample, and y as a list of target variable samples.
# Output: B, a list of the fitted model parameters based on the least squares solution.


def least_squares(X, y):
    X = np.array(X)
    y = np.array(y)

    # fill in
    # Use the matrix algebra functions in numpy to solve the least squares equations. This can be done in just one line.

    B = (np.linalg.inv(X.T @ X)) @ X.T @ y

    return B


if __name__ == "__main__":
    datapath = "poly.txt"
    degrees = [1, 2, 3, 4, 5]

    paramFits = main(datapath, degrees)
    print(paramFits)
