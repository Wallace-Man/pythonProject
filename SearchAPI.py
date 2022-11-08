import nltk
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

global text


def search(query):
    # query = input("What would you like to search?\n")
    search = query.replace(' ', '+')
    results = 40
    url = (f"https://www.google.com/search?q={search}&num={results}")
    global text
    text = ""
    returned_text = ""
    requests_results = requests.get(url)
    soup_link = BeautifulSoup(requests_results.content, "html.parser")
    links = soup_link.find_all("a")
    n = 1

    for link in links:
        link_href = link.get('href')
        if "url?q=" in link_href and not "webcache" in link_href:
            title = link.find_all('h3')
            if len(title) > 0:
                returned_text = returned_text + (str(n) + ". " + title[0].getText()) + "\n"
                returned_text = returned_text + (link.get('href').split("?q=")[1].split("&sa=U")[0]) + "\n"
                returned_text = returned_text + "------\n"
                n = n + 1
                text = text + title[0].getText() + " "
    return returned_text


def plot():
    global text
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    # Top 20 words
    n = 20
    counts = dict(Counter(tokens_without_sw).most_common(n))
    labels, values = zip(*counts.items())

    # sort your values in descending order
    indSort = np.argsort(values)[::1]

    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]
    y_pos = np.arange(len(labels))
    #plot.clf()
    # Create horizontal bars
    plt.barh(y_pos, values)
    # Create names on the x-axis
    plt.yticks(y_pos, labels)
    # Show graphic

    return plt.gcf()
    #plt.show()
    #plt.clf()
