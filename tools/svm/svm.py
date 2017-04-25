print(__doc__)

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm

sys.path.append("../")
from server.models import Collect

sys.path.append("../../")
from lib.old.keyboard import Keyboard


chunk_names = ['dataChunk1', 'dataChunk2', 'dataChunk3']

id = 1

selected_user = Collect.query.all()[id]

json = selected_user.get_json_data(selected_user.dataChunk4)

instance = Keyboard(data=json)

press_to_press_average =instance.average(instance.press_to_press()["_letter"])

release_to_release_average = instance.average(instance.release_to_release()["_letter"])

correct_data = [[press_to_press_average, release_to_release_average]]

train_data = []

for chunk_name in chunk_names:

	chunk = getattr(selected_user, chunk_name)

	json = selected_user.get_json_data(chunk)

	class_instance = Keyboard(data=json)

	release_to_release = class_instance.release_to_release()['_letter']

	release_to_release_average = class_instance.average(release_to_release)

	press_to_press = class_instance.press_to_press()['_letter']

	press_to_press_average = class_instance.average(press_to_press)

	train_data.append([press_to_press_average, release_to_release_average])

id = 2

selected_user = Collect.query.all()[id]

outliers_data = []

for chunk_name in chunk_names:

	chunk = getattr(selected_user, chunk_name)

	json = selected_user.get_json_data(chunk)

	class_instance = Keyboard(data=json)

	release_to_release = class_instance.release_to_release()['_letter']

	release_to_release_average = class_instance.average(release_to_release)

	press_to_press = class_instance.press_to_press()['_letter']

	press_to_press_average = class_instance.average(press_to_press)

	outliers_data.append([press_to_press_average, release_to_release_average])


id = 3

selected_user = Collect.query.all()[id]

# outliers_data = []

for chunk_name in chunk_names:

	chunk = getattr(selected_user, chunk_name)

	json = selected_user.get_json_data(chunk)

	class_instance = Keyboard(data=json)

	release_to_release = class_instance.release_to_release()['_letter']

	release_to_release_average = class_instance.average(release_to_release)

	press_to_press = class_instance.press_to_press()['_letter']

	press_to_press_average = class_instance.average(press_to_press)

	outliers_data.append([press_to_press_average, release_to_release_average])


# X_train = np.array(train_data)

# X_outliers = np.array(outliers_data)

# X_test = np.array(correct_data)


X_train = np.array([[1,1,1],[1,2,1],[1,1,1]])

X_outliers = np.array([[6.9313, -0.85151, 3], [9.56926, -3.66626, 2]])

# X_test = np.array([[1,1,1], [2,2,2]])



# xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
# Generate train data
# X = 0.3 * np.random.randn(100, 2)
# X = X_train = np.array([[1,1], [2,2]])
# X_train = np.r_[X + 2, X - 2]
# Generate some regular novel observations
# X = 0.3 * np.random.randn(20, 2)
# X_test = np.r_[X + 2, X - 2]
# Generate some abnormal novel observations
# X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))
# X_outliers = np.array([[3,3], [4,4]])

# fit the model
clf = svm.OneClassSVM(nu=.4, kernel="rbf", gamma=0.9)
clf.fit(X_train)
y_pred_train = clf.predict(X_train)
print y_pred_train

y_pred_outliers = clf.predict(X_outliers)
print y_pred_outliers

# y_pred_test = clf.predict(X_test)
# print y_pred_test

# n_error_train = y_pred_train[y_pred_train == -1].size

n_error_outliers = y_pred_outliers[y_pred_outliers == 1].size

# plot the line, the points, and the nearest vectors to the plane
# Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
# Z = Z.reshape(xx.shape)

# plt.title("Novelty Detection")
# plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.PuBu)
# a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred')
# plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='palevioletred')

# s = 40
# b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=s)

# b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='blueviolet', s=s)

# c = plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='gold', s=s)
# plt.axis('tight')
# plt.xlim((-5, 5))
# plt.ylim((-5, 5))

# plt.show()