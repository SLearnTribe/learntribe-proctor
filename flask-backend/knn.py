import numpy as np
def euclidean_dist(X1,X2):
    return np.sqrt(np.sum((X1-X2)**2))
def KNN(X,Y,Query, k = 5):
    m = X.shape[0]
    vals = []
    for i in range(m):
        d = euclidean_dist(Query , X[i])
        vals.append((d,Y[i]))
    
    vals = sorted(vals,key= lambda x:x[0])[:k]
    vals = np.array(vals)
    
    new_vals = np.unique(vals[:,1],return_counts = True)
    index = new_vals[1].argmax()
    pred = new_vals[0][index]
    return pred  

