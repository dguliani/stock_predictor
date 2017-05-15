import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import csv
import datetime

def find_share(share):
    ret = []
    with open('s&p500_contituent_prices.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if share in row:
                ret.append(row)

    return np.array(ret)

appl = find_share("AXP")
months = []
last_month = datetime.datetime.strptime(appl[-1][1], "%Y-%m-%d").month
features = []
y = []
cumy = []

price = np.array([])
vol = np.array([])

for i in range(1, len(appl[:,0])+1):
    row = appl[-i]
    date = datetime.datetime.strptime(row[1], "%Y-%m-%d")
    if date.month is not last_month:
        months.append(row)
        t = []
        # print row

        low = np.min(price)
        high = np.max(price)
        avg = np.mean(price)
        avg_vol = np.mean(vol)

        # t.append(row[1])
        t.append(low)
        t.append(high)
        t.append(avg)
        t.append(avg_vol)

        inc = float(row[4])/price[0]
        # print row[4]
        y.append(inc)

        if len(y)>1:
            cumy.append(cumy[-1]* (inc))
        else:
            cumy.append(inc)

        features.append(t)
        last_month = date.month
        price = np.array([])
        vol = np.array([])
        # low = 0
        # high = 0
        # avg = 0
        # avg_vol = 0
    else:
        price = np.append(price, float(row[4]))
        vol = np.append(vol, float(row[2]))

features = np.array(features)

seperation_pt = len(features)/2

train = features[:seperation_pt]
test = features[seperation_pt:]
ytrain = cumy[:seperation_pt]
ytest = cumy[seperation_pt:]


svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
for i in range(1):
    svr_rbf = svr_rbf.fit(train, ytrain)

y_rbf = svr_rbf.predict(features)
# print y_rbf

rmse = np.sqrt(np.average((y_rbf - y)**2))
print rmse
lw = 2
plt.scatter(range(len(features)), cumy, color='darkorange', label='data')
plt.hold('on')
plt.plot(range(len(features)), y_rbf, color='navy', lw=lw, label='RBF model')
# plt.plot(X, y_lin, color='c', lw=lw, label='Linear model')
# plt.plot(X, y_poly, color='cornflowerblue', lw=lw, label='Polynomial model')
# plt.xlabel('data')
# plt.ylabel('target')
# plt.title('Support Vector Regression')
plt.legend()
plt.show()