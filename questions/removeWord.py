import random
from questions import replaceDash


# For a sentence create a blank space.
# It first tries to randomly selection proper-noun
# and if the proper noun is not found, it selects a noun randomly.
def removeWord(sentence, poss):
    words = None
    if 'NNP' in poss:
        words = poss['NNP']
    elif 'NN' in poss:
        words = poss['NN']
    else:
        return None, sentence, None
    if len(words) > 0:
        word = random.choice(words)
        replaced = replaceDash.replaceIC(word, sentence)
        return word, sentence, replaced
    else:
        return None, sentence, None
