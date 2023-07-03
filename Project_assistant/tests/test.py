from test_gpt import run_gpt_test
from test_bleu import run_bleu_test
from test_embeddings import run_positive_tests, run_negative_tests
from plot_scripts.barplot import barplot_vector, create_vector
from plot_scripts.plot import plot
from plot_scripts.boxplot import boxplot

def run_tests(gpt=False, bleu=False, embeddings=False, is_negative=None):
    """Run all tests
    
    gpt: run gpt test?
    bleu: run bleu test?
    embeddings: run embeddings test?
    is_negative: Whether to run negative or positive tests, if None, both positive and negative tests will be run.
    """
    
    if gpt:
        if is_negative == None:
            run_gpt_test(True)
            run_gpt_test(False)
        else: 
            run_gpt_test(is_negative)

    if bleu:
        if is_negative == None:
            run_bleu_test(True)
            run_bleu_test(False)
        else:
            run_bleu_test(is_negative)

    if embeddings:
        if is_negative == None:
            run_negative_tests()
            run_positive_tests()
        elif is_negative:
            run_negative_tests()
        else:
            run_positive_tests()


    #PLOTS

    #SIMILARITY
    plot()

    #BARPLOT
    barplot_vector(create_vector())

    #BOXPLOT
    boxplot()


run_tests(gpt=False, bleu=False, embeddings=False, is_negative=None)