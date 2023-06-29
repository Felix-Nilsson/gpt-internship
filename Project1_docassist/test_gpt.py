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
    Compare the following sentence with the options given below and indicate whether each option conveys the same information or not. 
    Provide a list, with no spaces, that is as long as the options list, with a '1' in the corresponding position if an option is deemed to convey the same information as the sentence, or a '0' if it does not.

    EXAMPLE (bounded by #####)
    ####
    Example Sentence to compare: 'I enjoy playing the guitar.'

    Example Options: ['Playing the guitar brings me joy.', 'I dislike playing musical instruments.', 'My favorite hobby is playing the guitar.',
    'The guitar is a difficult instrument to learn.', 'I prefer playing the piano over the guitar.']
    
    Example response: [1,0,1,0,0]
    ####

    Sentence to compare: '{actual_output}'

    Options: {expected_output}
    '''

    #Provide a string of 0s and 1s, separated by commas, corresponding to each option sentence, indicating whether they answer the same question and convey the same main points of information as the sentence provided.

    #Update the context with relevant information for every question
    messages = [{'role':'user', 'content': generated_test_prompt_en_which_option}]

    test_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )

    return(test_response.choices[0].message["content"])

with open("Project1_docassist/tests/gpt_test_results.txt","w", encoding="utf-8") as g:

    with open("Project1_docassist/tests/cases.json","r", encoding="utf-8") as f:
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
            if re.match(r'^\[([01](?:,[01])*)\]$', result) is None:
                g.write('Test case ' + test_index + ':  ERROR: wrong format from GPT\n')
                continue #Throw error instead?

            #Clean result string
            result = str(result).replace('[','').replace(']','').split(',')
            
            #Write results to file
            if '1' in result:
                g.write('Test case ' + test_index + ':  PASSED\n')
            else:
                g.write('Test case ' + test_index + ':  FAILED\n')

            g.write('Generated answer: "' + case_answer + '"\n\n')

            g.write('Refence answers:\n')

            for i in range(0, len(result)):
                if result[i] == '1':
                    g.write('✓  "' + reference_answers[i] + '"\n')
                else:
                    g.write('X  "' + reference_answers[i] + '"\n')

            if int(test_index) < len(data) - 1:
                g.write('\n\n')