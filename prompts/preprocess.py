prompt_doctor = f"""
    Du är en AI-assistent för läkare på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    input_msg

    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
    Ifall det inte finns någon information avgränsad av två måsvingar, Svara med "Jag har inte tillräckligt med information":

    """ + "{{background}}"

prompt_patient = f"""
    Du är en AI-assistent för en patient på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    input_msg

    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
    Ifall det inte finns någon information avgränsad av två måsvingar, Svara med "Jag har inte tillräckligt med information":

    """ + "{{background}}"

prompt_intranet = f'''
    Du är en AI-assistent som ska svara på frågor.
    Du svarar alltid kortare än 2 meningar.
    input_msg

    Säg gärna vilken fil du hittade informationen i.
    Du får endast använda informationen som är avgränsad med tre understreck.
    Använd bara informationen som är avgränsad med två måsvingar.
    Om du inte hittar svaret i informationen svarar du att du inte har tillgång till informationen.

    
    ''' + "{{background}}"


def export_doc_test():
    global prompt_doctor
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_doctor.replace("input_msg",input_msg)

    with open("prompts/prompt_doctor_test.txt","w",encoding='utf-8') as f:
        f.write(prompt_doctor)

def export_pat_test():
    global prompt_patient
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_patient.replace("input_msg",input_msg)

    with open("prompts/prompt_patient_test.txt","w",encoding='utf-8') as f:
        f.write(prompt_patient)

def export_intranet_test():
    global prompt_intranet
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_intranet.replace("input_msg",input_msg)

    with open("prompts/prompt_intranet_test.txt","w",encoding='utf-8') as f:
        f.write(prompt_intranet)

# export_doc_test()
# export_pat_test()
export_intranet_test()