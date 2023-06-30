#Fix the imports of files in the embeddings folder
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import embeddings.chatbot as chatbot
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import json
import numpy as np
import matplotlib.pyplot as plt


def run_bleu(reference_answers,can, method):
    
    smoothing = SmoothingFunction()
    function = getattr(smoothing,method)
    return sentence_bleu(reference_answers, can, smoothing_function=function)
    

def bleu_smoothing_eval():
    cb = chatbot.Chatbot('Doctor')
    with open('Project_assistant/testing/tests/cases.json', encoding="utf-8") as file:
        data = json.load(file)
        matrix = np.empty((0,8))
        for case in data:
            question = case['question']
            reference_answers = case['reference_answers']
            ref_ans = [answer.split() for answer in reference_answers]
            identifier = case['patient_id']

            can = [cb.get_chat_response(question,[identifier])]
            can = can[0].split("*")[0].replace("\n","").strip()
            can = can.split()

            results = []
            
            for i in range(0,8):
                method = f"method{i}"
                results.append(run_bleu(ref_ans, can, method))

            matrix = np.vstack((matrix,results))       

    fig, ax = plt.subplots()

    boxplot = ax.boxplot(matrix, vert=True, patch_artist=True) 

    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink', 'lightgray', 'lightsalmon', 'darkorchid', 'goldenrod']
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

    ax.set_xlabel('Smoothing method')
    ax.set_ylabel('Score')
    ax.set_title('bleu score vs smoothing method')

    plt.show()

def run_bleu_test(is_negative=False):
    cb = chatbot.Chatbot('Doctor')
    with open('Project_assistant/testing/tests/cases.json', encoding="utf-8") as file:
        path = "Project_assistant/testing/tests/data/bleu_positive.csv"
        if is_negative:
            path = "Project_assistant/testing/tests/data/bleu_negative.csv"

        with open(path,"w", encoding="utf-8") as f:

            print(f"Running BLEU, negative={is_negative}")
            data = json.load(file)
        
            for case in data:
                question = case['question']
                reference_answers = case['reference_answers']
                ref_ans = [answer.split() for answer in reference_answers]
                identifier = case['patient_id']

                if is_negative:
                    identifier = ""

                index = case["test_index"]
                print("\ttest case:",index)

                can = [cb.get_chat_response(question,[identifier])]
                can = can[0].split("*")[0].replace("\n","").strip()
                can = can.split()

                print(can)

                result = run_bleu(ref_ans, can, "method5")

                
                f.write(f"{result}\n")


#run_bleu_test(is_negative=False)
run_bleu_test(is_negative=True) 