from embeddings.make_embeddings import make_embeddings
from embeddings.chatbot import get_chat_response
from embeddings.run_query import strings_ranked_by_relatedness

import json

def run_test(question,reference_answers,identifier):

    candidate = [get_chat_response(question,[str(identifier)])]
    candidate = candidate[0].split("*")[0].replace("\n","").strip()

    embedded_references = make_embeddings(reference_answers)

    return strings_ranked_by_relatedness(candidate,embedded_references)[1]

with open("Project1_docassist/tests/cases.json") as f:
    data = json.load(f)
    for case in data:
        question = case['question']
        reference_answers = case['reference_answers']
        identifier = case['patient_id']

        results = run_test(question,reference_answers,identifier)
        print(results)
