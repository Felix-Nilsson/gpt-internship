import pandas as pd
import matplotlib.pyplot as plt

positive = pd.read_csv("testing/tests/data/positive_results.csv")
negative = pd.read_csv("testing/tests/data/negative_results.csv")

plt.plot(positive['avg'],'-o', color='lightsalmon', label="Positive")
plt.plot(negative['avg'],'-o', color='orchid', label="Negative")

plt.fill_between(positive.index, positive['min'], positive['max'], color='lightblue', alpha=0.4, label='Min vs Max')
plt.fill_between(negative.index, negative['min'], negative['max'], color='lightblue', alpha=0.4)

plt.xticks(positive.index)
plt.legend()

plt.xlabel("Test Cases")
plt.ylabel("Cosine Similarity")
plt.title("Average similarity between generated answers and reference answers")

plt.savefig("testing/tests/plots_n_results/similarity.png")