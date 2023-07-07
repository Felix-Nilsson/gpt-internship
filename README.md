<h1 align= center>Sahlgrenska AI Hjälp</h1>



<p align="center">
  <img src="img/SAH.png" />
</p>

<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
<img src="https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
</p>


Sahlgrenska AI Hjälp is a chatbot designed to assist medical staff and patients in finding medical information which for example are stored in journals or calendars.

It was made in python using GPT-3.5 Turbo & Streamlit.

This is one of three projects produced as part of AI Swedens "GPT Summer Internship" for the summer of 2023, and was a collaboration between AI Sweden and Sahlgrenska University Hospital in Gothenburg.

Sahlgrenska AI Hjälp is designed primarily with swedish in mind.

🔗 [Link to blog]( https://my.ai.se/projects/287)

<p align="center">
  <img src="img/dialoguenew.png" />
</p>


## Table of Contents 
- [Table of Contents](#table-of-contents)
- [📋 Description](#-description)
- [🚀 Getting Started](#-getting-started)
  - [Dependencies](#dependencies)
  - [Executing program](#executing-program)
- [🧪 Testing](#-testing)
- [✍️ Authors](#️-authors)
- [🤝 Acknowledgments](#-acknowledgments)




## 📋 Description

Sahlgrenska AI Hjälp is designed with two users in mind:

* Medical Staff: doctors, nurses
* Non Medical Staff: patients, caretakers of patients
  
Currently these come in the form of just doctors and patients, with the difference being that a patient has access to a single directory of documents, their own, whereas doctors can access a list of patients documents.

Documents are of imaginary patients since in practice these are very sensitive and for legal reasons cannot "leave" the hospital.
They were however made to be similar in structure to real documents, with guidance from data scientists working in the field.

Upon prompting, Sahlgrenska AI Hjälp will check if the user is a doctor or patient, and depending on the query will pick suitable documents as background (using embeddings and similarity scoring) to produce a high quality answer. This is done via a web interface in the form of a simple chat.

## 🚀 Getting Started

### Dependencies

* You need to store your API key to OpenAI under the environment variable ```OPENAI_API_KEY```.
* You need to have streamlit installed to run the web interface
* Possibly need to install some miscellaneous libraries python libaries like ```pandas```, ```PyPDF2``` or ```SciPy```

### Executing program

To run the web interface, first make sure that your terminal is positioned in the gpt-internship directory, for example by running:
```
cd some/path/gpt-internship
```
Next, run the following streamlit command:
```
streamlit run Project_assistant/streamlit_app.py
```
Please note that if you restart the interface, you need to close down your previous tab/tabs that were running it or this will produce some errors.


## 🧪 Testing
Testing applications that use LLMs can be difficult, and we are in the process of trying out different metrics and test cases to see what gives the best results.
Currently, there is only a small handcrafted dataset consisting of queries made by our different fictional doctors, and reference responses that Sahlgrenska AI Hjälp should match.
We check the likeness between these reference responses and the candidate response generated during the test. The candidate responses are generated in two ways:

* Negative: Without access to background information, this is to check that Sahlgrenska AI Hjälp does not hallucinate a fictious answer. It should basically answer "I don't know".
* Positive: With access, to see that the information is used and the likeness it high.

This is done with the following metrics, and the latest scores are presented bellow:
* [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity), using [embedded](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings) versions of reference and candidate answers
* [BLEU score](https://en.wikipedia.org/wiki/BLEU)
* GPT Testing: We prompt GPT to itself judge whether the generated candidate answer provides the same information as the reference answers.

<p align="center">
  <img src="Project_assistant/tests/results/plots/barplot_tot.png" />
</p>



In particular, the BLEU scoring and Embedded Similarity are most similar since for any test $x$ we have $x \in [0,1]$, whereas GPT tests have $x \in \{0,1\}$. With this in mind we present the variance in the tests:

<p align="center">
  <img src="Project_assistant/tests/results/plots/boxplot_avg.png" />
</p>

To run the tests for yourself run the following python script with the same positioning of the terminal as before:
```
python3 Project_assistant/tests/test.py
```
To run individiual tests or disable generation of plots, please edit the file ```test.py``` accordingly.

Resulting data and plots are stored in the directories ```tests/results/data``` & ```tests/results/plots```.


## ✍️ Authors
[Henrik Johansson](https://github.com/henkejson)

[Oskar Pauli](https://github.com/OGPauli)

[Felix Nilsson](https://github.com/Felix-Nilsson)


## 🤝 Acknowledgments

We would like to thank Isak Barbopoulos at Sahlgrenska for supervising this project and providing guidance.