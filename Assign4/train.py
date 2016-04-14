from svm import *
from svmutil import *
import os

import csv


def csv_to_libsvm(file_path, header, class_ind, num_cols):
    data_v = []
    class_v = []

    class_index = class_ind
    num_columns = num_cols

    for index in range(0, len(file_path)):
        try:
            input_path = file_path[index]
            fin = open(input_path, "r")

        except (IndexError, IOError) as err:
            print(err)
            exit(1)

        # create a file reader
        csv_reader = csv.reader(fin)

        # Ignore the first line
        if header:
            line = csv_reader.next()

        # Reading the training data and  populating the data and class vectors
        for line in csv_reader:
            if len(line) != num_columns:
                print "malformed record"
            else:
                if class_index != -1:
                    svm_line = str(class_map[line[class_index]]) + " "

                new_obj = {}
                for i in range(0, num_columns):
                    if i != class_index:
                        if class_index != -1:
                            svm_line = svm_line + str(i + 1) + ":" + str(line[i]) + " "
                        new_obj[i + 1] = float(line[i])

                data_v.append(new_obj)

                # If the class is present (i.e it is training data)
                if class_index != -1:
                    class_v.append(float(class_map[line[class_index]]))

        fin.close()
    return class_v, data_v


# Class map to represent string as integer/float which is required by libsvm format
class_map = {"absent": 0.0, "present": 1.0}
rev_class_map = {0.0: "absent", 1.0: "present"}
data_vector = []
class_vector = []

# Convert from csv to libsvm format
class_vector, data_vector = csv_to_libsvm(
    ["Occupancy Dataset/datatest1.csv", "Occupancy Dataset/datatest2.csv", "Occupancy Dataset/datatest3.csv"], True, 5,
    6)

# Debug statement
# print data_vector

# Creating a new parameter
param = svm_parameter('-t 0 -c 4 -b 1')
# Creating a problem set from data and class vectors
problem = svm_problem(class_vector, data_vector)
# Generating a model only if no model file is present
if os.path.exists("./svm.model"):
    model = svm_load_model("./svm.model")
else:
    model = svm_train(problem, param)
    svm_save_model("./svm.model", model)

# Debug statement
# print model

# For storing the test data values and their predicted class
test_data_vector = []
test_class_vector = []

# Here test_class_vector will be empty (-1 specifies no class dimension)
test_class_vector, test_data_vector = csv_to_libsvm(
    ["Occupancy Dataset/datatest1.csv"], True, 5, 6)

# test_class_vector = [0] * len(test_data_vector);
p_label, p_acc, p_val = svm_predict(test_class_vector, test_data_vector, model, '-b 1')

# Debug statement
# print p_label, p_acc, p_val

test_class_vector = p_label
target = open("result.csv", 'w')
# Writing to the output file
for i in range(0, len(test_class_vector)):
    target.write(rev_class_map[test_class_vector[i]] + ",")

target.close()



# os.system("./svm-train -t 1 -q ./Occupancy\ Dataset/datatest1.svm")
# os.system("./svm-predict ./Occupancy\ Dataset/test.svm datatest1.svm.model result.svm")


# os.system("./svm-predict ./Occupancy\ Dataset/datatest1.svm > model")
# #print svm_read_problem("Occupancy Dataset/datatest1.svm")
# print svm_train(svm_read_problem("Occupancy Dataset/datatest1.svm"))
