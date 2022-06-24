from nltk.tokenize import regexp_tokenize

tokenized = regexp_tokenize(input(), '[A-Za-z]+')
print(tokenized[int(input())])
