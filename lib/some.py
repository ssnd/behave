import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm

xx,yy = np.meshgrid(np.linspace(-5,5,500), np.linspace(-5, 5, 500))

X = 0.3*np.random.randn(100,2)
X_train = np.r_[X+2, X-2]

X = 0.3 * np.random.randn(20,2)
X_test = np.r_[X+2, X-2]
# X_outliers = np.random.uniform(low=-4, high=4, size=(20,2))


clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=.1)

clf.fit(X_train)

y_pred_train = clf.predict(X_train)

# y_pred_test = clf.predict(X_outliers)

# y_pred_outliers = clf.predict(X_outliers)

n_error_train= y_pred_train[y_pred_train == -1].size

# n_error_test = y_pred_test[y_pred_test == -1].size

# n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size



Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contour(xx,yy,Z,levels=np.linspace(Z.min(),0,7),cmap=plt.cm.PuBu)
a=plt.contour(xx,yy,Z,levels=[0],linewidths=2,colors='darkred')
plt.contour(xx,yy,Z,levels=[0,Z.max()],colors='palevioletred')

plt.show()


