prompt_doctor = f"""
    Du är en AI-assistent för läkare på ett sjukhus.
    Du svarar alltid kort och koncist, inte längre än 2 meningar.
    input_msg

    Ifall meddelandet ber om information om en specifik patient, använd informationen avgränsad av tre understreck.
    Ifall det inte finns någon information avgränsad av tre understreck, Svara med "Jag har inte tillräckligt med information":

    """


def export_test():
    global prompt_doctor
    input_msg = 'Du ska svara på följande meddelande "{{input}}".'
    prompt_doctor.replace("inpu_msg",input_msg)
    prompt_doctor += "{{background}}"

    with open("prompts/prompt_doctor_cb.txt","w") as f:
        f.write(prompt_doctor)

export_test()