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

def scale(original_value, max_value, min_value):
    #print type(original_value), type(max_value), type(min_value)
    #print original_value, max_value
    return (float(original_value) - float(min_value)) * 1.0 / (float(max_value) - float(min_value))

def convert_with_scale(filename):
    values = []
    temperature = []
    humidity = []
    light = []
    co2 = []
    humidityratio = []
    occupacy = []
    with open(filename) as csvfile:
        #print "success"
        next(csvfile)
        for row in csvfile:
            values = row.split(",")
           
            temperature.append(float(values[0]))
            humidity.append(float(values[1]))
            light.append(float(values[2]))
            co2.append(float(values[3]))
            humidityratio.append(float(values[4]))
            occupacy.append(values[5])
    csvfile.close()
    
    max_temperature = max(temperature)
    max_humidity    = max(humidity)
    max_light       = max(light)
    max_co2         = max(co2)
    max_humidityratio = max(humidityratio)

    min_temperature = min(temperature)
    min_humidity    = min(humidity)
    min_light       = min(light)
    min_co2         = min(co2)
    min_humidityratio = min(humidityratio)

    
    #max_occupacy    =[]
    
    print max_temperature, max_humidity, max_light, max_co2, max_humidityratio
    new_file_name = "".join(filename + ".converted")

    num = len(temperature)
    print num
    with open(new_file_name, 'w') as convertedfile:
        for i in range(num):
            tmp_temperature = scale(temperature[i], max_temperature, min_temperature)
            tmp_humidity = scale(humidity[i], max_humidity, min_temperature)
            tmp_light = scale(light[i], max_light, min_light)
            tmp_co2 = scale(co2[i], max_co2, min_co2)
            tmp_humidityratio = scale(humidityratio[i], max_humidityratio, min_humidityratio)
            if (occupacy[i] == "present\n"):
                presence = "+1"
            else:
                presence = "-1"
            convertedfile.write(presence + " 1:" + str(tmp_temperature) + " 2:" + str(tmp_humidity) + " 3:" + str(tmp_light) + " 4:" + str(tmp_co2) + " 5:" + str(tmp_humidityratio) + "\n")
    convertedfile.close()    


def convert(filename):
    new_file_name = "".join(filename + ".converted")
    f = open(new_file_name, 'w')
    with open(filename) as csvfile:
        next(csvfile)
        for row in csvfile:
            values = row.split(",")
#            print values
            #temperature.append(values[0])
            #humidity.append(values[1])
            #light.append(values[2])
            #co2.append(values[3])
            #humidityratio.append(values[4])
            #occupacy.append(values[5])
            if (values[5] == "present\n"):
                presence = "+1"
            else:
                presence = "-1"
            f.write(presence + " 1:" + values[0] + " 2:" + values[1] + " 3:" + values[2] + " 4:" + values[3] + " 5:" + values[4] + "\n")
            #f.write(values[5] + "\n")
    f.close()
            
            
if __name__ == "__main__":
    print "This is the main function"
    sys.path.append('C:\\Users\\wzp\\Desktop\\NCSU\\SpringCourses\\791\\Homework\\Assignment4\\libsvm-master\\python')
    os.chdir('C:\\Users\\wzp\\Desktop\\NCSU\\SpringCourses\\791\\Homework\\Assignment4\\libsvm-master\\python')

    scaling = "yes"

    for C_index in range(-1, 4):
        for gamma_index in range(-1, 4):
            print C_index, gamma_index
            C_value = 2**C_index
            gamma_value = 2**gamma_index
            dtrain_name = ["123.csv"]
            for i in dtrain_name:
                if (scaling == "yes"):
                    print "converted"
                    convert_with_scale(i)
                else:
                    convert(i)
                train_y, train_x = svm_read_problem(i + ".converted")
                #m = svm_train(train_y, train_x, '-c 2 -t 2')
                param = '-t 2 -v 10 -c %f -g %f' % (C_value, gamma_value)
                print param
                m = svm_train(train_y, train_x, param)
            #print "Training is finished"
    
    #dtrain_name = ["datatest1.csv", "datatest2.csv", "datatest3.csv"]
    #for i in dtrain_name:
    #    if (scaling == "yes"):
    #        print "converted"
    #        convert_with_scale(i)
    #    else:
    #        convert(i)
    #    train_y, train_x = svm_read_problem(i + ".converted")
    #    #m = svm_train(train_y, train_x, '-c 2 -t 2')
    #    m = svm_train(train_y, train_x, '-t 2 -v 10')
    #    print "Training is finished"
    #
    #    dtest_name = ["datatest1.csv", "datatest2.csv", "datatest3.csv"]
    #    for j in dtest_name:
    #        if (scaling == "yes"):
    #            convert_with_scale(j)
    #        else:
    #            convert(j)
    #        test_y, test_x = svm_read_problem(j + ".converted")
    #        p_label, p_acc, p_val = svm_predict(test_y, test_x, m)


    #print temperature
    #print humidity
    #print light
    #print co2
    #print humidityratio
    #print occupacy

    #size = len(temperature)
    #x = []
    #for i in range(size):
    #    x.append([temperature[i], humidity[i], light[i], co2[i], humidityratio[i]])
    #x = [temperature, humidity, light, co2, humidityratio]
    #print x
    #y = occupacy
    #print "The training data is ready"
    #print y
    #prob = svm_problem(y, x)
    #param = svm_parameter('-t 0 -c 4 -b 1')
    #m = svm_train(prob, param)
    #p_label, p_acc, p_val = svm_predict(y, x, m)
