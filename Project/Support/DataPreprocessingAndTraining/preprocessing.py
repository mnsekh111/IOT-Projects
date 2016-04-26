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


# This function will be called by convert with scale, and only store the selected column
def write_to_file(file_pointer, presence, tmp_temperature, tmp_humidity, tmp_light, tmp_co2, tmp_humidityratio, tmp_one_more):
    file_pointer.write(presence + " 1:" + str(tmp_temperature) + " 2:" + str(tmp_humidity) + " 3:" + str(tmp_light) \
                       + " 4:" + str(tmp_co2) + " 5:" + str(tmp_humidityratio) + " 6:" + str(tmp_one_more) + "\n")
    

# This function will convert the data, but it will also scale the data;
def convert_with_scale(filename):
    values = []
    temperature = []
    humidity = []
    light = []
    co2 = []
    humidityratio = []
    one_more = []
    occupacy = []

    new_file_name = "".join(filename + "processed")
    convertedfile = open(new_file_name, 'w') 
    with open(filename) as csvfile:
        # read first line
        row = csvfile.readline()
        values = row.split(",")

        temperature.append(float(values[0]))
        humidity.append(float(values[1]))
        light.append(float(values[2]))
        co2.append(float(values[3]))
        humidityratio.append(float(values[4]))
        one_more.append(float(values[5]))
        occupacy.append(values[6]) # Occupacy is a string
	# record the current flag
        current_flag = values[6]
        
        for row in csvfile:
            values = row.split(",")
            if current_flag == values[6]:
            	temperature.append(float(values[0]))
            	humidity.append(float(values[1]))
            	light.append(float(values[2]))
            	co2.append(float(values[3]))
            	humidityratio.append(float(values[4]))
            	one_more.append(float(values[5]))
            	occupacy.append(values[6]) # Occupacy is a string
            else:
                tmp_temperature = sum(temperature) / len(temperature)
                tmp_humidity 	= sum(humidity) / len(humidity)
                tmp_light 	= sum(light) / len(light)
                tmp_co2 	= sum(co2) / len(co2)
                tmp_humidityratio = sum(humidityratio) / len(humidityratio)
                tmp_one_more    = sum(one_more) / len(one_more)
                if (current_flag == "open\n"):
                    presence = "+1"
                else:
                    presence = "-1"
                write_to_file(convertedfile, presence, tmp_temperature, tmp_humidity, tmp_light, tmp_co2, tmp_humidityratio, tmp_one_more)
		# Clear the list
                temperature = []
                humidity = []
                light = []
                co2 = []
                humidityratio = []
                one_more = []
                occupacy = []
                # Push the just read data into the list
                temperature.append(float(values[0]))
                humidity.append(float(values[1]))
                light.append(float(values[2]))
                co2.append(float(values[3]))
                humidityratio.append(float(values[4]))
                one_more.append(float(values[5]))
                occupacy.append(values[6]) 
                current_flag = values[6]
    csvfile.close()
    convertedfile.close()

# This fnction is used to convert csv file to the file format that is needed by libsvm
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
    sys.path.append('C:\\Users\\wzp\\Desktop\\NCSU\\SpringCourses\\791\\Homework\\Project\\libsvm-master\\python')
    os.chdir('C:\\Users\\wzp\\Desktop\\NCSU\\SpringCourses\\791\\Homework\\Project\\libsvm-master\\python')

    scaling = "yes"

    dtrain_name = ["test - Copy.csv"]
    for i in dtrain_name:
        if (scaling == "yes"):
            print "converted"
            convert_with_scale(i)
        else:
            convert(i)

            #print "Training is finished"

    # This paragraph is for parameter selection
'''
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
'''    
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
