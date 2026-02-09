import matplotlib.pyplot as plt
import numpy as np

import k_mean as km

# x1 | x2 | Alarm state

array = (
    ( 7.5,  8.5, "Pending" ), ( 2.2,  7.3, "Pending" ), ( 3.2,  4.3, "Small"   ), #  1,  2,  3
    ( 4.2,  6.7, "Pending" ), ( 4.3,  5.8, "Small"   ), ( 4.5,  3.5, "Small"   ), #  4,  5,  6
    ( 2.2,  2.5, "Small"   ), ( 2.7,  3.7, "Small"   ), ( 4.5,  8.9, "Imminent"), #  7,  8,  9
    ( 8.5,  5.6, "Pending" ), ( 9.6,  4.6, "Pending" ), ( 7.5,  4.9, "Pending" ), # 10, 11, 12
    ( 4.5, 12.2, "Imminent"), ( 4.0, 13.5, "Imminent"), ( 8.6, 13.2, "Imminent"), # 13, 14, 15
    (10.2, 12.8, "Imminent"), (12.2, 17.8, "Imminent"), (13.5, 16.4, "Imminent"), # 16, 17, 18
    (15.6, 12.2, "Imminent"), (10.3, 10.4, "Pending" ), ( 9.8, 10.4, "Imminent"), # 19, 20, 21
    ( 8.3, 11.3, "Imminent"), ( 5.6,  7.8, "Imminent"), ( 7.8,  5.6, "Imminent"), # 22, 23, 24
    ( 4.7,  7.8, "Small"   ), ( 7.8,  4.6, "Pending" ), (13.3,  8.9, "Imminent"), # 25, 26, 27
    ( 3.4,  4.6, "Small"   ), ( 5.6,  6.6, "Small"   ), ( 7.9,  9.5, "Pending" ), # 28, 29, 30
    ( 5.8,  6.6, "Pending" ), ( 4.8,  4.6, "Pending" ), (12.4,  9.1, "Imminent")  # 31, 32, 33
)

array_np = np.array(array)

# Pick prototype form each state
x = array_np[:, 0]
y = array_np[:, 1]
centroids = [(x[0], y[0]), (x[2], y[2]), (x[23], y[23])] # Pending | Small | Imminent



# Draw plot
col = array_np[:, 2]
col = np.char.replace(col, "Small", "green")
col = np.char.replace(col, "Pending", "blue")
col = np.char.replace(col, "Imminent", "red")

xPoints = array_np[:, 0]
yPoints = array_np[:, 1]

for i in range(len(array_np)):
    plt.plot(xPoints[i], yPoints[i], 'x', c=col[i])

plt.xlabel("X1")
plt.ylabel("X2")
plt.title("Array")
plt.show()