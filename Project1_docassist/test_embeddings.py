from embeddings.make_embeddings import make_embeddings
from embeddings.chatbot import get_chat_response
from embeddings.run_query import strings_ranked_by_relatedness
import numpy as np

import json

def run_test(question,reference_answers,identifier):

    candidate = [get_chat_response(question,[str(identifier)])]
    candidate = candidate[0].split("*")[0].replace("\n","").strip()

    embedded_references = make_embeddings(reference_answers)

    print(question)
    print(candidate)

    return strings_ranked_by_relatedness(candidate,embedded_references)[1]
"""
q = "Vad åt patient 112288 till lunch igår?"
refs = ["Han åt pizza igår till lunch", "Igår åt patient 112288 pizza till lunch"]
res = run_test(q,refs,112288)
print(res,np.mean(res))
"""

with open("Project1_docassist/tests/results.csv","w") as g:
    g.write("max,min,avg")

    with open("Project1_docassist/tests/cases.json","r") as f:
        data = json.load(f)
        for case in data:
            question = case['question']
            reference_answers = case['reference_answers']
            identifier = case['patient_id']

            results = run_test(question,reference_answers,identifier)
            low = min(results)
            high = max(results)
            mean = np.mean(results)

            g.write(f"\n{high},{low},{mean}")

            
