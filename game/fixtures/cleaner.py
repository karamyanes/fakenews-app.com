# Python program to read & clean json file

import json
import nltk
import time


timestr = time.strftime("%Y%m%d-%H%M%S")

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def tokenize(doc_text):
    """
    Function to tokenize the doc.
    """
    # doc_text = "In the race to the White House, who is the most patriotic candidate? Not the Democrats, a recent Facebook post suggests. Not a single American flag at the Democrat Debate, reads the text next to a photo of the presidential candidates who participated in the first of two nights of debates hosted by NBC. The image was posted on Facebook on June 27, before the second debate, and riled up some commenters who took the opportunity to denounce the Democratic Party's values. This post, which was shared more than 4,300 in less than 24 hours, was flagged as part of Facebook's efforts to combat false news and misinformation on its News Feed. (Read more about our partnership with Facebook.) A spokeswoman for NBC News did not immediately respond to PolitiFact's email asking about the claim. But looking at photos of the debate, we found more than the digital image of a White House that appears behind the candidates in the Facebook post. This Getty photo, for example, shows the NBC News logo with the red and white stripes of the flag, and a graphic behind the candidates that resembles a flag rippling in the wind. Red, white and blue and stars and stripes dominate the stage. You can see more such photos here and here. Additionally, we found photos of a number of candidates sporting American flag lapel pins, including Rep. Tim Ryan, Rep. Tulsi Gabbard, former Maryland congressman John Delaney, New York City Mayor Bill DeBlasio There are no physical flags in the pictures. But searching for photos of the 2016 Republican presidential debates, it appears similar sets were used — lots of stars, stripes and an American color palette. Searching through pages of Getty Images photos from the first debate, we saw none with a physical American flag made of cloth. But the stage had a digital set that prominently featured images of the flag — including one hanging on the White House image that appears in the Facebook post — and several candidates wore flag pins on their lapels. We rate this claim False"
    sentences = nltk.sent_tokenize(doc_text)  
    return sentences


with open("politifact_claims.json", "r") as jsonFile:
    data = json.load(jsonFile)
    for d in data:
        new_doc = tokenize(d['fields']['doc'])
        if new_doc:
            d['fields']['doc'] = new_doc
        else:
            d['fields']['doc'] = 'empty hint'

# Save our changes to JSON file & close it
jsonFile = open("politifact_%s.json" % timestr, "w+")  # generating file with timestamp
jsonFile.write(json.dumps(data))
jsonFile.close()
