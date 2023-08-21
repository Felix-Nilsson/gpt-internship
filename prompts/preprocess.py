prompt_doctor = f"""Du är en AI-assistent för läkare på ett sjukhus.
Du svarar alltid kort och koncist, inte längre än 2 meningar.
input_msg

Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av två måsvingar.
Ifall det inte finns någon information avgränsad av två måsvingar, Svara med "Jag har inte tillräckligt med information":

""" + "{{background}}"

prompt_patient = f"""Du är en AI-assistent för en patient på ett sjukhus.
Du svarar alltid kort och koncist, inte längre än 2 meningar.
input_msg

Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av två måsvingar.
Ifall det inte finns någon information avgränsad av två måsvingar, Svara med "Jag har inte tillräckligt med information":

""" + "{{background}}"

prompt_intranet = f'''Du är en AI-assistent som ska svara på frågor.
Du svarar alltid kortare än 2 meningar.
input_msg

Säg gärna vilken fil du hittade informationen i.
Du får endast använda informationen som är avgränsad med två måsvingar.
Om du inte hittar svaret i informationen svarar du att du inte har tillgång till informationen.


''' + "{{background}}"

prompt_internet = f"""Du är en internetassistent.

Du kan ingenting själv utan använder alltid dina verktyg (Tools) för att hitta information som du använder för att svara på frågor.
Ifall du inte har tillgång till några verktyg (Tools) be användaren att dubbelkolla inställningarna.

Du ger alltid ganska långa (4-8 meningar) svar som innehåller all relevant information.

Skriv alltid med vilka källor du använt, t.ex:
[titel](URL)
"""


def export_doc_test():
    global prompt_doctor
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_doctor = prompt_doctor.replace("input_msg",input_msg)

    with open("prompts/prompt_doctor.txt","w",encoding='utf-8') as f:
        f.write(prompt_doctor)

def export_pat_test():
    global prompt_patient
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_patient = prompt_patient.replace("input_msg",input_msg)

    with open("prompts/prompt_patient.txt","w",encoding='utf-8') as f:
        f.write(prompt_patient)

def export_intranet_test():
    global prompt_intranet
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_intranet = prompt_intranet.replace("input_msg",input_msg)

    with open("prompts/prompt_intranet.txt","w",encoding='utf-8') as f:
        f.write(prompt_intranet)

def export_internet_test():
    global prompt_internet
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_internet = prompt_internet.replace("input_msg",input_msg)

    with open("prompts/prompt_internet.txt","w",encoding='utf-8') as f:
        f.write(prompt_internet)


export_doc_test()
export_pat_test()
export_intranet_test()
export_internet_test()