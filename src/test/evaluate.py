import py_midicsv
import csv


def convert_to_csv(file, output_name):
    """
    This functions converts a midi file to a csv file to help make comparisons easier
    :param file: string
    path to file to be converted
    :param output_name: string
    the chosen name of output file
    """
    csv_string = py_midicsv.midi_to_csv(file)
    with open(output_name, 'w') as file:
        for line in csv_string:
            file.write(line)


oracle = {}
result = {}

with open('tidied.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
            line_count += 1
        else:
            oracle[row[0]] = row[1]
            # print(f'\t{row[0]} works in the {row[1]})
            line_count += 1


with open('tidiedR.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            pass
            line_count += 1
        else:
            result[row[0]] = int(row[1])+12
            line_count += 1

match = 0
error = 70
for key, item in oracle.items():
    for i in range(int(key)-error, int(key)+error):
        check = result.get(str(i), None)
        if check:
            if int(check) == int(item):
                print("MATCH")
                match += 1

recall = match/len(oracle)
precision = match/len(result)
fscore = 2*((precision*recall)/(precision+recall))

print("Recall:", recall)
print("Precision:", precision)
print("F1 Score:", fscore)


