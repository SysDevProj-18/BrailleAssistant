from speech import SpeechRecognition
import csv


recognizer = SpeechRecognition(log_time=True)
with open ('results.csv', 'a') as file:
    while True:
        expected_word = input("Enter the expected word for this speech: ")
        num_samples = int(input("Enter the number of samples you would like to process: "))
        i = 0
        print("Please speak the word: ", expected_word)
        for (text, time) in recognizer.listen_loop():
            if text != '':
                i += 1
                csv.writer(file).writerow([expected_word, text.lower(), time])
                if i == num_samples:
                    break
                print("Please speak the word: ", expected_word)
        choice = input("Do you want to continue with another test? (yes/no): ").lower()
        if choice != 'yes':
            break
