#Fix the imports of files in the embeddings folder
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import src.chatbot as chatbot
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import json
import numpy as np
import matplotlib.pyplot as plt


def run_bleu(reference_answers, can, method):
    
    smoothing = SmoothingFunction()
    function = getattr(smoothing,method)
    return sentence_bleu(reference_answers, can, smoothing_function=function)
    

def bleu_smoothing_eval():
    cb = chatbot.Chatbot()
    with open('Project3_intranet/tests/cases.json', encoding="utf-8") as file:
        data = json.load(file)
        matrix = np.empty((0,8))
        for case in data:
            question = case['question']
            print(question)
            reference_answers = case['reference_answers']
            ref_ans = [answer.split() for answer in reference_answers]

            can = [cb.get_chat_response(question)]
            can = can[0].split("*")[0].replace("\n","").strip()
            print(can)
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

    plt.savefig('Project3_intranet/tests/results/plots/boxplot_avg.png')

def run_bleu_test(is_negative=False):
    cb = chatbot.Chatbot()
    with open('Project3_intranet/tests/cases.json', encoding="utf-8") as file:
        path = "Project3_intranet/tests/results/data/bleu_positive.csv"
        if is_negative:
            path = "Project3_intranet/tests/results/data/bleu_negative.csv"

        with open(path,"w", encoding="utf-8") as f:

            print(f"\nRunning BLEU, negative={is_negative}")
            data = json.load(file)
        
            f.write('avg')

            for case in data:
                question = case['question']
                reference_answers = case['reference_answers']
                ref_ans = [answer.split() for answer in reference_answers]

                index = case["test_index"]
                print("\ttest case:",index)

                if is_negative:
                    can = [cb.get_chat_response(question, positive=False)]
                else:
                    can = [cb.get_chat_response(question, positive=True)]

                can = can[0].split("*")[0].replace("\n","").strip()
                can = can.split()

                result = run_bleu(ref_ans, can, "method5")

                f.write(f"\n{result}")

#bleu_smoothing_eval()
#run_bleu_test(is_negative=False)
run_bleu_test(is_negative=True) 