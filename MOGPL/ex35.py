from numpy import arange, array, ones, linalg
from pylab import plot, show


def showplots():
    xi = array([4, 17, 31, 55, 88, 96])
    A = array([xi, ones(6)])
    # linearly generated sequence
    y = [11, 25, 46, 48, 65, 71]
    # obtaining the parameters
    w = linalg.lstsq(A.T, y)[0]
    print(w)
    # plotting the line
    line = w[0] * xi + w[1]
    plot(xi, line, 'r-', xi, y, 'o')
    show()


    xi = array([4, 17, 31, 55, 88, 14])
    A = array([xi, ones(6)])
    # linearly generated sequence
    y = [11, 25, 46, 48, 65, 97]
    # obtaining the parameters
    w = linalg.lstsq(A.T, y)[0]
    print(w)
    # plotting the line
    line = w[0] * xi + w[1]
    plot(xi, line, 'r-', xi, y, 'o')
    show()



def q35(xi, yi):
    A = array([xi, ones(6)])
    # obtaining the parameters
    w = linalg.lstsq(A.T, yi)[0]
    sommel = [(yii - (w[0] * xii) - w[1], -yii + (w[0] * xii) + w[1]) for xii, yii in zip(xi, yi)]
    zl = [max(e1, e2) for e1, e2 in sommel]
    print(f"sommel: {sommel}")
    print(f"zl: {zl}")
    print(f"zmax: {max(zl)}")
    return max(zl)


x1 = array([4, 17, 31, 55, 88, 96])
y1 = [11, 25, 46, 48, 65, 71]
x2 = array([4, 17, 31, 55, 88, 14])
y2 = [11, 25, 46, 48, 65, 97]

q35(x1, y1)
q35(x2, y2)