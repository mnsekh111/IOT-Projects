from svm import *
from svmutil import *
import csv

class_map = {"absent": 0, "present": 1}

# Convert from csv to libsvm format
try:
    input_path = "Occupancy Dataset/datatest1.csv"
    output_path = input_path.split('.')
    output_path = output_path.pop(0) + ".svm"
    print output_path
    fin = open(input_path, "r")
except (IndexError, IOError) as err:
    print(err)
    exit(1)

try:
    fout = open(output_path, "w")
except IOError as err:
    print(err)
    exit(1)

csv_reader = csv.reader(fin)

# ignore the first line which is a header
line = csv_reader.next()

class_index = 5
num_columns = 6

for line in csv_reader:
    if len(line) != num_columns:
        print "malformed record"
    else:

        svm_line = str(class_map[line[class_index]]) + " "
        for i in range(0, num_columns):
            if i != class_index:
                svm_line = svm_line + str(i + 1) + ":" + str(line[i]) + " "

        # print svm_line
        fout.write(svm_line + "\n")


fout.close()
fin.close()


#print svm_read_problem("Occupancy Dataset/datatest1.svm")
print svm_train(svm_read_problem("Occupancy Dataset/datatest1.svm"))