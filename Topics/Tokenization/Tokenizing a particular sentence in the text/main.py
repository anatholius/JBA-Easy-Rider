from nltk.tokenize import regexp_tokenize, sent_tokenize

sentences = sent_tokenize(input())
tokenized = regexp_tokenize(sentences[int(input())], "[A-z']+")
print(tokenized)
