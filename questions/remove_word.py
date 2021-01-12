import random
from questions import replace_dash


# For a sentence create a blank space.
# It first tries to randomly selection proper-noun
# and if the proper noun is not found, it selects a noun randomly.
def remove_word(sentence, poss):
    words = None
    if 'NNP' in poss:
        words = poss['NNP']
    elif 'NN' in poss:
        words = poss['NN']
    elif 'NNS' in poss:
        words = poss['NNS']
    else:
        return None, sentence, None
    if len(words) > 0:
        word = random.choice(words)
        replaced = replace_dash.replace_ic(word, sentence)
        return word, sentence, replaced
    else:
        return None, sentence, None
