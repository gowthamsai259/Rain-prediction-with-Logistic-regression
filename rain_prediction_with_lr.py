# -*- coding: utf-8 -*-
"""Rain_prediction with LR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11Kr3cOAK2G5YY2M3WBO1vrwiHPRXrI69
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

rain = pd.read_csv("weather.csv")
rain.head()

rain.columns
rain.drop(['WindGustDir','WindDir9am','WindDir3pm','RISK_MM'],axis = 1,inplace = True)
rain.head()

rain.describe()

rain.fillna(rain.mean(),inplace = True)
rain.head()

rain.RainToday = [1 if x == 'Yes' else 0 for x in rain.RainToday]
rain.RainTomorrow = [1 if x == 'Yes' else 0 for x in rain.RainTomorrow]
rain.sample(3)

x_rain = rain.drop('RainTomorrow',axis = 1)
y = rain.RainTomorrow.values
x_rain.head()

#normalizing the data
x = (x_rain - np.min(x_rain)) / (np.max(x_rain) - np.min(x_rain))
x.head()

x_train,x_test,y_train,y_test = train_test_split(x,y, test_size = 0.2, random_state = 42)

x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T
x_test.shape
x_train.shape
y_test.shape
y_train.shape

#creating weight and bias
def weight_bias(dim):
  w = np.full((dim,1),0.01)
  b = 0.0
  return w,b

#defining sigmoid function
def sigmoid(z):
  y_sig = 1 / (1 + np.exp(-z))
  return y_sig

#defining forward and backward proportion

def forward_backward_propagation(w, b, x_train, y_train):
  #forward proportion
  z = np.dot(w.T,x_train) + b
  y_sig = sigmoid(z)
  loss = -(1 - y_train) * np.log(1 - y_sig) - y_train * np.log(y_sig)
  cost = (np.sum(loss)) / x_train.shape[1]
  #backward proportion
  derivative_weight = (np.dot(x_train,((y_sig-y_train).T))) / x_train.shape[1]
  derivative_bias = np.sum(y_sig - y_train) / x_train.shape[1]

  gradients = {'derivative_weight': derivative_weight, 'derivative_bias': derivative_bias}
  return cost,gradients

def update(w, b, x_train, y_train, learning_rate, nu_of_iteration):
    cost_list = []
    cost_list2 = []
    index = []
    
    # Initialize for-back propagation for the number of iteration times. Then updating w and b values and writing the cost values to a list:  
    for i in range(nu_of_iteration):
        cost, gradients = forward_backward_propagation(w, b, x_train, y_train)
        cost_list.append(cost)
    
        # Update weight and bias values:
        w = w - learning_rate * gradients['derivative_weight']
        b = b - learning_rate * gradients['derivative_bias']
        # Show every 20th value of cost:
        if i % 20 == 0:
            cost_list2.append(cost)
            index.append(i)
            print('Cost after iteration %i: %f' %(i,cost))
    
    parameters = {'weight': w, 'bias':b}
    
    # Visulization of cost values:
    plt.plot(index, cost_list2)
    plt.xlabel('Nu of Iteration')
    plt.ylabel('Cost Function Value')
    plt.show()
    
    return parameters, gradients, cost_list

def prediction(w, b, x_test):
    z = sigmoid(np.dot(w.T, x_test) + b)
    y_prediction = np.zeros((1,x_test.shape[1]))
    
    for i in range(z.shape[1]):
        if z[0,i]<= 0.5:
            y_prediction[0,i] = 0
        else:
            y_prediction[0,i] = 1
            
    return y_prediction

def logistic_regression(x_train, y_train, x_test, y_test, learning_rate, nu_of_iteration):
    dimension = x_train.shape[0]
    w, b = weight_bias(dimension)    # Creating an initial weight matrix of (x_train data[0] x 1)
    
    # Updating our w and b by using update method. 
    # Update method contains our forward and backward propagation.
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learning_rate, nu_of_iteration)
    
    # Lets use x_test for predicting y:
    y_test_predictions = prediction(parameters['weight'], parameters['bias'], x_test) 
    
    # Investigate the accuracy:
    print('Test accuracy: {}%'.format(100 - np.mean(np.abs(y_test_predictions - y_test))*100))

logistic_regression(x_train, y_train, x_test, y_test, learning_rate=1, nu_of_iteration=400)

from sklearn.linear_model import LogisticRegression

# Creating our model named 'lr'
lr = LogisticRegression()

# Training it by using our train data:
lr.fit(x_train.T, y_train.T)

# Printing our accuracy by using our trained model and test data:
print('Test accuracy of sklearn logistic regression library: {}'.format(lr.score(x_test.T, y_test.T)))