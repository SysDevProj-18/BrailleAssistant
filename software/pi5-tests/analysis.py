import seaborn as sns
import matplotlib.pyplot as plt
import csv
import os


class DataPoint:
    def __init__(self, name, expected, actual, confidence):
        self.name = name
        self.expected = expected
        self.actual = actual
        self.confidence = confidence


# read the csv file
expected: dict[str, list[DataPoint]] = {}
# find any files that start with results
# and read them
for file in os.listdir():
    if file.startswith("results"):
        print("Reading file: ", file)
        # the files may contain ^M characters
        # let's remove them
        with open(file, "r", newline="\n") as file:
            reader = csv.reader(file)
            data = list(reader)
            # [[flo,the colour is red,the colors red,1.0]]
            for row in data:
                name = row[0]
                expected_word = row[1].lower()
                actual_word = row[2].lower()
                confidence = row[3]

                if expected_word in expected:
                    expected[expected_word].append(
                        DataPoint(name, expected_word, actual_word, confidence)
                    )
                else:
                    expected[expected_word] = [
                        DataPoint(name, expected_word, actual_word, confidence)
                    ]

samples = sum([len(expected[sentence]) for sentence in expected.keys()])
total_misclassification = sum(
    [
        len(
            [
                datapoint
                for datapoint in expected[sentence]
                if datapoint.expected != datapoint.actual
            ]
        )
        for sentence in expected.keys()
    ]
)

print(f"Total samples: {samples}")
print(f"Total misclassification: {total_misclassification}")
print(f"Misclassification rate: {total_misclassification/samples}")


def wer(ref: str, hyp: str) -> float:
    """
    Calculate the Word Error Rate (WER).
    """
    # build the matrix
    d = [[0] * (len(hyp) + 1) for _ in range(len(ref) + 1)]
    for i in range(len(ref) + 1):
        for j in range(len(hyp) + 1):
            if i == 0:
                d[i][j] = j
            elif j == 0:
                d[i][j] = i
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            if ref[i - 1] == hyp[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    return d[len(ref)][len(hyp)] / len(ref)


sentence_wer = {}
for sentence in expected.keys():
    sentence_wer[sentence] = sum(
        [wer(datapoint.expected, datapoint.actual) for datapoint in expected[sentence]]
    ) / len(expected[sentence])

print("WER by sentence")
print(sentence_wer)


sentence_wer_by_speaker = {}
for sentence in expected.keys():
    for datapoint in expected[sentence]:
        if datapoint.name in sentence_wer_by_speaker:
            sentence_wer_by_speaker[datapoint.name].append(
                wer(datapoint.expected, datapoint.actual)
            )
        else:
            sentence_wer_by_speaker[datapoint.name] = [
                wer(datapoint.expected, datapoint.actual)
            ]

# normalize the wer by speaker
for speaker in sentence_wer_by_speaker.keys():
    sentence_wer_by_speaker[speaker] = sum(sentence_wer_by_speaker[speaker]) / len(
        sentence_wer_by_speaker[speaker]
    )
print("WER by speaker")
print(sentence_wer_by_speaker)

# bar chart where the sentences are on the y-axis
# and the x-axis is the WER
# sort the sentences by WER
sentence_wer = dict(sorted(sentence_wer.items(), key=lambda item: item[1]))
f, ax = plt.subplots(figsize=(6, 15))
sns.barplot(
    x=list(sentence_wer.values()),
    y=list(sentence_wer.keys()),
    palette="viridis",
)
ax.set(xlim=(0, 1))

plt.title("Word Error Rate by sentence")
# color the bars based on the WER
for i in range(len(list(sentence_wer.keys()))):
    ax.patches[i].set_facecolor(
        plt.cm.viridis(sentence_wer[list(sentence_wer.keys())[i]])
    )
# save but make sure that it's not cut off
plt.tight_layout()
plt.savefig("wer_sentence.png", bbox_inches="tight")
