import requests, random
from bs4 import BeautifulSoup, element

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



def details(word, num_examples=5):
    url = "http://www.dictionary.com/browse/"
    req = requests.get(url + word, headers=headers)
    bs = BeautifulSoup(req.text, "html.parser")
    examples = [e.text.strip() for e in bs.select("#source-example-sentences .partner-example-text")]
    synonyms = [x.text.strip() for x in bs.select("div.tail-content.ce-spot div.tail-elements")]
    random.shuffle(examples)
    return {
        "examples": examples[:num_examples],
        "synonyms": synonyms
    }



def get_words():
    words = []
    meanings = []
    nums = ["0" + str(x) for x in range(1,10)] + map(str, range(10,16))
    for n in nums:
        print "getting list", n
        words_req = requests.get("http://www.majortests.com/gre/wordlist_" + n, headers=headers)
        words_bs = BeautifulSoup(words_req.text, "html.parser")

        words += [x.text.strip() for x in words_bs.select(".wordlist th")]
        meanings += [x.text.strip() for x in words_bs.select(".wordlist td")]
    return zip(words, meanings)


words = get_words()
text = "<style>.pagebreak { page-break-inside: avoid; } html{font-size:12px;} </style>\n"

count = 1
for w in words:
    text += '<div class="pagebreak">'
    text += "<b>" + w[0] + "</b>" + ": " + w[1]


    d = details(w[0])
    text += "<em>"
    text += " ".join(d["synonyms"])
    text += "</em>"

    text += "<ul><li>"
    text += "</li><li>".join(d["examples"])
    text += "</li></ul>"

    text += "</div>\n"

    count += 1
    file = open("gre3.html", "w+")
    file.write(unicode(text).encode("utf-8"))

print text
