import os
import openai
import json
import re
import time
import sys

#This is to enable importing from the embeddings folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import src.chatbot as chatbot

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

    return(test_response.choices[0].message['content'])

def run_gpt_test(is_negative=False, positive=True):
    """Test the AI GPT assistant using another GPT, returns the number of passed test cases"""

    print(f"\nRunning GPT Test, negative={is_negative}")

    if is_negative:
        result_file_path = 'Project3_intranet/tests/results/data/gpt_test_results_negative.txt'
    else:
        result_file_path = 'Project3_intranet/tests/results/data/gpt_test_results_positive.txt'


    with open(result_file_path, 'w', encoding='utf-8') as g:

        with open('Project3_intranet/tests/cases.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            ans = 0

            for case in data:
                cb = chatbot.Chatbot()

                test_index = case['test_index']
                question = case['question']
                reference_answers = case['reference_answers']


                #To keep track of it running
                print('[GPT] Running case:',test_index)

                case_answer = cb.get_chat_response(question, remember=False, positive=positive)
                print(case_answer)
                case_answer = case_answer.split('\n')[0]

                result = compare(case_answer, reference_answers)

                #Check so that result has the right format
                if re.match(r'^\[([01](?:,[01])*)\]$', result) is None:
                    g.write('Test case ' + test_index + ':  ERROR: wrong format from GPT\n\n')
                    continue #Throw error instead?

                #Clean result string
                result = str(result).replace('[','').replace(']','').split(',')
                
                #Write results to file
                if '1' in result:
                    ans += 1
                    g.write('Test case ' + test_index + ':  PASSED\n')
                else:
                    g.write('Test case ' + test_index + ':  FAILED\n')

                #Write the generated answer for comparison with the reference answers
                g.write('Generated answer: "' + case_answer + '"\n\n')

                #Show which, if any, reference answers that the generated answer passses for
                g.write('Refence answers:\n')
                for i in range(0, len(result)):
                    if result[i] == '1':
                        g.write('✓  "' + reference_answers[i] + '"\n')
                    else:
                        g.write('X  "' + reference_answers[i] + '"\n')

                g.write('\n\n')

        #Write the total pass ratio for the test cases
        g.write('Tests passed: ' + str(ans) + '/' + str(len(data)))

    return ans

#Run positive test
#run_gpt_test(is_negative=0)

#Run negative test
run_gpt_test(is_negative=1, positive=False)

    