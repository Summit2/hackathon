import numpy as np


class MyLinearRegression():

    def __init__(self,learning_rate = 0.001 ):
        
        self.mu,self.sigma = 0, 0.1
        
        self.weights = None #W+bias
        self.bias= None  #will be added after model.fit complete

        self.lr = learning_rate
        self.epochs = 10000

    def exact_solution(self, X ,y ):
        return np.linalg.inv(X.T @ X) @ X.T @ y
    
    def grad(self, X,y):
        
        error = X@self.weights-y
        return 2 * X.T@(error) / (X.shape[0]), np.mean(error)
    


    def fit(self, X,y):
        y = y.reshape(-1, 1)

        x0 = np.ones(shape = (X.shape[0],1)) #this is bias
        X = np.concatenate([X, x0],axis =1) # add to arr
        

        error = 1 # random digit > than 0
        counter = 0 #if we can't make it under number of epochs

        self.weights = np.random.normal(self.mu,self.sigma,(X.shape[1],1))
        while (abs(error)>0.001):
            grad_i, error = self.grad(X,y)

            self.weights  -= self.lr * grad_i
            counter+=1
            if counter>=self.epochs:
                break
            # print('Error',error)
        print(f"Модель сошлась за {counter} эпох")
        
        self.weights = self.weights[:-1]
        self.bias = self.weights[-1]

    def predict(self,X):
        return X@self.weights 
