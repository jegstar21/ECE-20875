import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt


def main():
    # Importing dataset
    diamonds = pd.read_csv("diamonds.csv")

    # Feature and target matrices
    X = diamonds[["carat", "depth", "table", "x", "y", "z", "clarity", "cut", "color"]]
    y = diamonds[["price"]]

    # Training and testing split, with 25% of the data reserved as the test set
    X = X.to_numpy()
    y = y.to_numpy()
    [X_train, X_test, y_train, y_test] = train_test_split(
        X, y, test_size=0.25, random_state=101
    )

    # Normalizing training and testing data
    [X_train, trn_mean, trn_std] = normalize_train(X_train)
    X_test = normalize_test(X_test, trn_mean, trn_std)

    # Define the range of lambda to test
    lmbda = np.logspace(-1, 2, 51)

    MODEL = []
    MSE = []
    for l in lmbda:
        # Train the regression model using a regularization parameter of l
        model = train_model(X_train, y_train, l)

        # Evaluate the MSE on the test set
        mse = error(X_test, y_test, model)

        # Store the model and mse in lists for further processing
        MODEL.append(model)
        MSE.append(mse)

    # Plot the MSE as a function of lmbda
    plt.plot(lmbda, MSE)
    plt.show()

    # Find best value of lmbda in terms of MSE
    ind = MSE.index(min(MSE))
    [lmda_best, MSE_best, model_best] = [lmbda[ind], MSE[ind], MODEL[ind]]

    print(
        "Best lambda tested is "
        + str(lmda_best)
        + ", which yields an MSE of "
        + str(MSE_best)
    )

    return model_best


# Function that normalizes features in training set to zero mean and unit variance.
# Input: training data X_train
# Output: the normalized version of the feature matrix: X, the mean of each column in
# training set: trn_mean, the std dev of each column in training set: trn_std.


def normalize_train(X_train):

    std = []
    mean = []
    loop = len(X_train[0])

    for x in range(loop):
        column = X_train[:, x]
        trn_mean = np.mean(column)
        trn_std = np.std(column)
        std.append(trn_std)
        mean.append(trn_mean)

    X = (X_train - np.array(mean)) / (np.array(std))

    return X, mean, std


# Function that normalizes testing set according to mean and std of training set
# Input: testing data: X_test, mean of each column in training set: trn_mean, standard deviation of each
# column in training set: trn_std
# Output: X, the normalized version of the feature matrix, X_test.


def normalize_test(X_test, trn_mean, trn_std):

    X = (X_test - trn_mean) / trn_std

    return X


# Function that trains a ridge regression model on the input dataset with lambda=l.
# Input: Feature matrix X, target variable vector y, regularization parameter l.
# Output: model, a numpy object containing the trained model.


def train_model(X, y, l):

    train = linear_model.Ridge(alpha=l, fit_intercept=True)
    model = train.fit(X, y)

    return model


# Function that calculates the mean squared error of the model on the input dataset.
# Input: Feature matrix X, target variable vector y, numpy model object
# Output: mse, the mean squared error
def error(X, y, model):

    y_naught = model.predict(X)
    mse = np.mean(sum(pow((y - y_naught), 2)))

    return mse


if __name__ == "__main__":
    model_best = main()

    # We use the following functions to obtain the model parameters instead of model_best.get_params()
    print(model_best.coef_)
    print(model_best.intercept_)
