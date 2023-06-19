import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

text_to_summarize = """
Medical Record

Patient Name: John Smith
Date of Birth: January 10, 1985
Gender: Male
Medical Record Number: 123456789

Chief Complaint:
The patient complains of persistent foul odor emanating from his feet.

History of Present Illness:
John Smith presents with a history of excessively smelly feet for the past six months. He reports that the odor is particularly strong, causing social discomfort and embarrassment. The patient mentions that the odor is more noticeable after physical activities and during warm weather. He has tried over-the-counter foot powders and antiperspirants but has not experienced significant improvement.

Past Medical History:

    Allergic Rhinitis: Diagnosed at the age of 12. The patient reports seasonal nasal congestion and sneezing, managed with antihistamines.
    No known history of diabetes or peripheral vascular disease.
    No previous foot infections or fungal conditions.

Medications:

    Loratadine 10mg once daily for allergic rhinitis.

Family History:
There is no significant family history of foot odor or related conditions.

Social History:
John Smith works as an office administrator and leads a sedentary lifestyle. He does not smoke and consumes alcohol occasionally. No illicit drug use. He is in a stable relationship and lives with his partner.

Review of Systems:
General: No weight loss, fever, or fatigue.
Dermatological: No skin rashes, lesions, or itching elsewhere on the body.
Respiratory: Seasonal allergies as mentioned above.
Musculoskeletal: No joint pain or swelling.

Physical Examination:
On examination, the patient appears well and in no acute distress. Vital signs are within normal limits. Dermatological examination of the feet reveals no obvious abnormalities such as skin discoloration, rash, or lesions. The patient's feet exhibit increased moisture, particularly between the toes, and a strong, unpleasant odor is noted. No signs of inflammation or tenderness.

Assessment and Plan:
Based on the patient's history and physical examination, the diagnosis of bromhidrosis (excessive foot odor) is suspected. To further evaluate the condition and rule out any underlying causes, the following steps are planned:

    Laboratory Tests:
        Complete blood count (CBC) to rule out systemic infection.
        Fasting blood glucose to evaluate for diabetes mellitus.

    Referral:
        Podiatry consultation for a thorough evaluation of the feet and expert advice on foot hygiene.

    Education and Hygiene Measures:
        Educate the patient on proper foot hygiene, including daily washing with antibacterial soap and thorough drying, especially between the toes.
        Advise the use of moisture-wicking socks and breathable footwear.
        Recommend the application of over-the-counter antifungal creams or powders.

Follow-Up:
The patient is scheduled for a follow-up visit in two weeks to review the laboratory results and assess the response to hygiene measures. Depending on the findings, further interventions or referrals may be considered.

Signed:
Dr. Jane Miller, MD
Date: June 16, 2023
"""

prompt = f"""
Your task is to generate a summary of ...
Summarize the journal delimited with ``` 
Journal: ```{text_to_summarize}```
"""

response = get_completion(prompt)

print(response)