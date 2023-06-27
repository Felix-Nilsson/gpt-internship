from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
from embeddings.chatbot import get_chat_response

query = "Har patient 654321 fått hjärtinfarkt?"
ref = ["Ja, han har fått akut transmural hjärtinfarkt"]#["Han fick transmural hjärtinfarkt, så det stämmer"]]
can = [get_chat_response(query,["654321"])]
can = can[0].split("*")[0].replace("\n","").strip()



#references = [['This is reference sentence 1.'], ['This is reference sentence 2.']]
#candidates = ['This is candidate sentence 1.', 'This is candidate sentence 2.']
print(can)
# Calculate BLEU score
score = sentence_bleu([ref], can)
print("BLEU score:", score)
