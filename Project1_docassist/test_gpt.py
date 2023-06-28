import os
import openai
import json
import re
import time
from embeddings.chatbot import get_chat_response

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def compare(actual_output: str, expected_output: list[str]):
    """Tests if a sentence conveys the same info as one of the sentences in a list, returns 'a,b', a = 1/0 if test passes/fails, b = index of expected answer that passed"""

    generated_test_prompt_en_which_option = f'''
    Compare the following sentence with the options given below and indicate whether it conveys the same information or not. 
    If it conveys the same information, answer '1'; otherwise, answer '0'. 
    Additionally, provide the index of the option that conveys the same information.

    Example of how to answer for a sentence that conveys the same information as the first option: "1,0".
    Example of how to answer for a sentence that conveys the same information as the third option: "1,2".
    Example of how to answer for a sentence that conveys the same information as the tenth option: "1,10"
    Example of how to answer for a sentence that does not convey the same information as any option: "0,0"

    Sentence to compare: '{actual_output}'

    Options: {expected_output}
    '''

    #Update the context with relevant information for every question
    messages = [{'role':'user', 'content': generated_test_prompt_en_which_option}]

    test_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )

    return(test_response.choices[0].message["content"])

with open("Project1_docassist/tests/gpt_test_results.txt","w") as g:

    with open("Project1_docassist/tests/cases.json","r") as f:
        data = json.load(f)

        for case in data:
            test_index = case['test_index']
            patient_id = case['patient_id']
            question = case['question']
            reference_answers = case['reference_answers']

            case_answer = get_chat_response(question, patient_id, False)
            case_answer = case_answer.split('\n')[0]

            result = compare(case_answer, reference_answers)

            #Check so that result has the right format
            if re.match(r"^[01],\d+$", result) is None:
                g.write('Test case ' + test_index + ':  ERROR: wrong format from GPT\n')
                continue #Throw error instead?

            passed = result.split(',')[0]
            option = result.split(',')[1]

            #Give the API time to rest?
            time.sleep(6) #seconds

            if (passed == '1'):
                g.write('Test case ' + test_index + ':  PASSED\n')
                g.write('Generated answer: "' + case_answer + '"\n')
                g.write('Reference answer: "' + reference_answers[int(option)] + '"\n\n')
                continue
            g.write('Test case ' + test_index + ':  FAILED\n\n')
            
