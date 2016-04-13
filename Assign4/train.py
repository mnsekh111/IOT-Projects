from svm import *
from svmutil import *
import os
import csv


def csv_to_libsvm(file_path, header, class_ind, num_cols):
    class_index = class_ind
    num_columns = num_cols

    try:
        input_path = file_path
        fin = open(input_path, "r")

    except (IndexError, IOError) as err:
        print(err)
        exit(1)

    # create a file reader
    csv_reader = csv.reader(fin)

    # Ignore the first line
    if header:
        line = csv_reader.next()

    data_v = []
    class_v = []

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
class_map = {"absent": 0, "present": 1}
data_vector = []
class_vector = []

# Convert from csv to libsvm format
class_vector, data_vector = csv_to_libsvm("Occupancy Dataset/datatest.csv", True, 5, 6)

print data_vector

problem = svm_problem(class_vector, data_vector)
model = svm_train(problem)


print model


# For storing the test data values and their predicted class
test_data_vector = []
test_class_vector = []

# Here test_class_vector will be empty (-1 specifies no class dimension)
test_class_vector, test_data_vector = csv_to_libsvm("test.csv", True, -1, 5)
test_class_vector = model.predict(test_data_vector)

print test_class_vector


target = open("result.csv", 'w')
# Writing to the output file
for i in range(0,len(test_class_vector)):
    target.write(test_class_vector[i]+",")

target.close()



# os.system("./svm-train -t 1 -q ./Occupancy\ Dataset/datatest1.svm")
# os.system("./svm-predict ./Occupancy\ Dataset/test.svm datatest1.svm.model result.svm")


# os.system("./svm-predict ./Occupancy\ Dataset/datatest1.svm > model")
# #print svm_read_problem("Occupancy Dataset/datatest1.svm")
# print svm_train(svm_read_problem("Occupancy Dataset/datatest1.svm"))
