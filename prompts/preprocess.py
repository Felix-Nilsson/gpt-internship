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


def export_doc_test():
    global prompt_doctor
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_doctor.replace("input_msg",input_msg)

    with open("prompts/prompt_doctor_test.txt","w") as f:
        f.write(prompt_doctor)

def export_pat_test():
    global prompt_patient
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_patient.replace("input_msg",input_msg)

    with open("prompts/prompt_patient_test.txt","w") as f:
        f.write(prompt_patient)


# export_doc_test()

export_pat_test()