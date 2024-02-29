# generate a barchart
# which shows the expected word and the misclassification rate
# for each word in the test set
import matplotlib.pyplot as plt
import csv
import os 
import re
# read the csv file
expected = {} 
# find any files that start with results
# and read them
for file in os.listdir():
    if file.startswith('results'):
        print("Reading file: ", file)
        # the files may contain ^M characters
        # let's remove them
        with open(file, 'r', newline='\n') as file:
            reader = csv.reader(file)
            data = list(reader)
            # [['green', 'green', '1.0'] (Expected, Predicted, Confidence Rate by VOSK)]
            for row in data:
                if row[0] in expected:
                    expected[row[0]].append(row)
                else:
                    expected[row[0]] = [row]

fig,ax = plt.subplots(figsize=(8, 8))
ax.barh(
    list(expected.keys()),
    [len([x for x in expected[word] if x[0] != x[1]])/len(expected[word]) for word in expected.keys()],
    height=.6
)
ax.set_xlabel('Misclassification Rate')
ax.set_ylabel('Word')
ax.set_title('Misclassification Rate by Word')
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax.grid()
ax.set_axisbelow(True)
# save 
plt.savefig('misclassification_rate.png')

# new plot 
fig,ax = plt.subplots(figsize=(8, 8))
average = {}
for word in expected.keys():
    average[word] = sum([float(x[2]) for x in expected[word]])/len(expected[word])
ax.barh(list(average.keys()), list(average.values()), height=.6)
ax.set_xlabel('Average Confidence Rate')
ax.set_ylabel('Word')
ax.set_title('Average Confidence Rate by Word')
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax.grid()
ax.set_axisbelow(True)  # used to put grid behind data
# save
plt.savefig('average_confidence_rate.png')
