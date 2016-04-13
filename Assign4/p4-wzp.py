import os
import csv
import sys
from svmutil import *

def split(str):
    a = str.split(",")
    result = []
    result.append(float(a[0]))
    result.append(float(a[1]))
    result.append(float(a[2]))
    result.append(float(a[3]))
    result.append(float(a[4]))
    if (a[5] == "present\n"):
        result.append(1)
    else:
        result.append(0)
    return result

            
if __name__ == "__main__":
    print "This is the main function"
    sys.path.append('C:\\Users\\wzp\\Desktop\\NCSU\\SpringCourses\\791\\Homework\\Assignment4\\libsvm-master\\python')
    os.chdir('C:\\Users\\wzp\\Desktop\\NCSU\\SpringCourses\\791\\Homework\\Assignment4\\libsvm-master\\python')
    temperature = []
    humidity = []
    light = []
    co2 = []
    humidityratio = []
    occupacy = []

    with open('datatest1.csv') as csvfile:
        next(csvfile)
        for row in csvfile:
            values = split(row)
            temperature.append(values[0])
            humidity.append(values[1])
            light.append(values[2])
            co2.append(values[3])
            humidityratio.append(values[4])
            occupacy.append(values[5])

    #print temperature
    #print humidity
    #print light
    #print co2
    #print humidityratio
    #print occupacy

    size = len(temperature)
    x = []
    for i in range(size):
        x.append([temperature[i], humidity[i], light[i], co2[i], humidityratio[i]])
    #x = [temperature, humidity, light, co2, humidityratio]
    #print x
    y = occupacy
    print "The training data is ready"
    #print y
    prob = svm_problem(y, x)
    param = svm_parameter('-t 0 -c 4 -b 1')
    m = svm_train(prob, param)
    p_label, p_acc, p_val = svm_predict(y, x, m)
