from math import log

class NaiveBayesClassifier:

    def __init__(self, alpha):

        self.alpha = alpha
        self.dict = dict()
        self.prob = []


    def fit(self, X, y, y_d):
        
        self.prob = [0] * len(y_d)
        for i in range(len(y)):
            w = X[i].split()
            self.prob[y_d[y[i]]] += 1
            for j in w:
                if j not in self.dict:
                    self.dict[j] = [0] * (2 * len(y_d) + 1)
                self.dict[j][y_d[y[i]]] += 1
                self.dict[j][2 * len(y_d)] += 1
        t = [0] * len(y_d)
        for i in self.dict.keys():
            for j in range(len(y_d)):
                t[j] += self.dict[i][j]
        for i in self.dict.keys():
            for j in range(len(y_d)):
                self.dict[i][len(y_d) + j] = (self.dict[i][j] + self.alpha) / (self.dict[i][2 * len(y_d)] + self.alpha * len(self.dict))

        
    def predict(self, X):

        arr = []
        k = len(self.prob)
        for i in range(len(X)):
            words = X[i].split()
            probs = [log(x) for x in self.prob]
            for i in words:
                for j in range(k):
                    if i not in self.dict:
                        continue
                    probs[j] += log(self.dict[i][k + j])
            ind = 0
            maxim = probs[0]
            for j in range(1, k):
                if probs[j] > maxim:
                    maxim = probs[j]
                    ind = j
            #print(X[i], probs)
            arr.append(ind)
        return arr

       
    def score(self, X_test, y_test, y_d):

        k = 0
        arr = [y_d[i] for i in y_test]
        pd = self.predict(X_test)
        for i in range(len(y_test)):
            if pd[i] == arr[i]:
                k += 1
        return k / len(y_test)

x = [
    "i love this sandwich",
    "this is an amazing place",
    "i feel very good about these beers",
    "this is my best work",
    "what an awesome view",
    "i do not like this restaurant",
    "i am tired of this stuff",
    "i cant deal with this",
    "he is my sworn enemy",
    "my boss is horrible",
]
y = [
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
]
x_test = [
    "the beer was good",
    "i do not enjoy my job",
    "i aint feeling dandy today",
    "i feel amazing",
    "gary is a friend of mine",
    "i cant believe im doing this",
]
y_test = ["Positive", "Negative", "Negative", "Positive", "Positive", "Negative"]
y_dict = {"Positive": 0, "Negative": 1}
test = NaiveBayesClassifier(0.1)
test.fit(x, y, y_dict)

print(test.score(x_test, y_test, y_dict))
