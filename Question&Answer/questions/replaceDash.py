import re


# Create the blank in string
def replaceIC(word, sentence):
    insensitive_hippo = re.compile(word, re.IGNORECASE)
    return insensitive_hippo.sub('__________________', sentence)
