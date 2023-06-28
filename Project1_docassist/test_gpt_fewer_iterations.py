import os
import openai
import json
from embeddings.chatbot import get_chat_response

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def compare(actual_output, expected_output):

    generated_test_prompt_en_which_option = f'''
    Compare the following sentence with the options given below and indicate whether it conveys the same information or not. 
    If it conveys the same information, answer '1'; otherwise, answer '0'. 
    Additionally, provide the number of the option that conveys the same information.

    Example of how to answer for a sentence that conveys the same information as the first option: "1,1".
    Example of how to answer for a sentence that conveys the same information as the third option: "1,3".
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

            case_answer = get_chat_response(question, patient_id)
            case_answer = case_answer.split('\n')[0]

            g.write('Testing case: ' + test_index + '\n')
            #print('\nTesting case: ',test_index)

            result = compare(case_answer, reference_answers)

            passed = result.split(',')[0]
            option = result.split(',')[1]

            if (passed == '1'):
                g.write('Test case ' + test_index + ' - Passed!\n')
                g.write('Answer generated: ' + case_answer + '\n')
                g.write('Passing answer: ' + reference_answers[int(option) - 1] + '\n\n')
                #print('Test passed')
                #print('Answer generated:',case_answer)
                #print('Passing answer:',reference_answers[int(option) - 1])
                continue
            #print('Test failed')
            g.write('Test case ' + test_index + ' - Failed!\n\n')
            
