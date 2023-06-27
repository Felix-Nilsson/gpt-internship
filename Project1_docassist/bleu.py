from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from embeddings.chatbot import get_chat_response
import json


def run_bleu(question, reference_answers, identifier):
    can = [get_chat_response(question,[identifier])]
    can = can[0].split("*")[0].replace("\n","").strip()
    can = can.split()
    return sentence_bleu(reference_answers, can)
    

with open('Project1_docassist/tests/cases.json') as file:
    data = json.load(file)
    
    for case in data:
        question = case['question']
        reference_answers = case['reference_answers']
        reference_answers = [answer.split() for answer in reference_answers]
        identifier = case['patient_id']

        results = run_bleu(question,reference_answers,identifier)
        print(results)




