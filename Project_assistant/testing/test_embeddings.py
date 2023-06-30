#Fix the imports of files in the embeddings folder
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import embeddings.chatbot as chatbot
from embeddings.make_embeddings import make_embeddings
from embeddings.run_query import strings_ranked_by_relatedness
import numpy as np

import json

def run_similarity_test(question,reference_answers,identifier):
    cb = chatbot.Chatbot('Doctor')

    candidate = [cb.get_chat_response(question,[str(identifier)])]
    candidate = candidate[0].split("*")[0].replace("\n","").strip()

    embedded_references = make_embeddings(reference_answers)

    print(question)
    print(candidate)

    return strings_ranked_by_relatedness(candidate,embedded_references)[1]



def run_positive_tests():
    with open("Project_assistant/testing/tests/data/positive_results.csv","w", encoding="utf-8") as g:
        g.write("index,max,min,avg")

        with open("Project_assistant/testing/tests/cases.json","r", encoding="utf-8") as f:
            data = json.load(f)
            for case in data:
                index = case["test_index"]
                print("\nrunning test: " + index)
                question = case['question']
                reference_answers = case['reference_answers']
                identifier = case['patient_id']

                results = run_similarity_test(question,reference_answers,identifier)
                low = min(results)
                high = max(results)
                mean = np.mean(results)

                g.write(f"\n{index},{high},{low},{mean}")

def run_negative_tests():
    with open("Project_assistant/testing/tests/data/negative_results.csv","w", encoding="utf-8") as g:
        g.write("index,max,min,avg")

        with open("Project_assistant/testing/tests/cases.json","r", encoding="utf-8") as f:
            data = json.load(f)
            for case in data:
                index = case["test_index"]
                print("\nrunning test: " + case["test_index"])
                question = case['question']
                reference_answers = case['reference_answers']
                

                results = run_similarity_test(question,reference_answers,"")
                low = min(results)
                high = max(results)
                mean = np.mean(results)

                g.write(f"\n{index},{high},{low},{mean}")

def run_specific_test(index):
    pass

            
run_positive_tests()
#run_negative_tests()