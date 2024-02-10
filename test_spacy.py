import spacy

# nlp = spacy.load("en_core_web_sm")
# text = "I have a meeting tomorrow at 3 PM."
#
# doc = nlp(text)
#
# for ent in doc.ents:
#     if ent.label_ == "DATE":
#         print(ent.text)
from dateparser import parse

text = "Let's meet tomorrow at 2 PM"
date_info = parse(text)

if date_info:
    print(date_info.date())
