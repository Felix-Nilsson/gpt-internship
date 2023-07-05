#Fix the imports of files in the embeddings folder
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import src.chatbot as chatbot
from src.embeddings import make_embedding
from src.similarity import strings_ranked_by_relatedness
import numpy as np
from numpy.linalg import norm

import json

def run_similarity_test(question,reference_answers):
    cb = chatbot.Chatbot()

    candidate = [cb.get_chat_response(question)]
    candidate = candidate[0].split("*")[0].replace("\n","").strip()

    embedded_references = [make_embedding(reference_answer) for reference_answer in reference_answers]
    embedded_candidate = make_embedding(candidate)

    score = []
    for i in range(len(embedded_references)):
        score.append(np.dot(embedded_candidate,embedded_references[i])/(norm(embedded_candidate)*norm(embedded_references[i])))

    print(question)
    print(candidate)

    return score



def run_positive_tests():

    print(f"\nRunning Embeddings Test, negative={False}")


    with open("Project3_intranet/tests/results/data/positive_results.csv","w", encoding="utf-8") as g:
        g.write("index,max,min,avg")

        with open("Project3_intranet/tests/cases.json","r", encoding="utf-8") as f:
            data = json.load(f)
            for case in data:
                index = case["test_index"]
                print("\nrunning test: " + index)
                question = case['question']
                reference_answers = case['reference_answers']

                results = run_similarity_test(question,reference_answers)
                low = min(results)
                high = max(results)
                mean = np.mean(results)

                g.write(f"\n{index},{high},{low},{mean}")

def run_negative_tests():

    print(f"\nRunning Embeddings Test, negative={True}")

    with open("Project3_intranet/tests/results/data/negative_results.csv","w", encoding="utf-8") as g:
        g.write("index,max,min,avg")

        with open("Project3_intranet/tests/cases.json","r", encoding="utf-8") as f:
            data = json.load(f)
            for case in data:
                index = case["test_index"]
                print("\nrunning test: " + case["test_index"])
                question = case['question']
                reference_answers = case['reference_answers']
                

                results = run_similarity_test(question,reference_answers)
                low = min(results)
                high = max(results)
                mean = np.mean(results)

                g.write(f"\n{index},{high},{low},{mean}")

def run_specific_test(index):
    pass

            
run_positive_tests()
#run_negative_tests()