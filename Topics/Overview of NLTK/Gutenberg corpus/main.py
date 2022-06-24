# 1° Don't download gutenberg corpus. Just import it
from nltk.corpus import gutenberg

number = int(input())  # a row number of a sentence in Gutenberg corpus

# 2° get needed sentences
sentences = gutenberg.sents('whitman-leaves.txt')  # you yourself are `misspelt` :P

# 3° print required sentence
print(sentences[number])
