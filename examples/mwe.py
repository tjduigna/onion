#!/usr/bin/env python

import nltk
nltk.download('webtext')
nltk.download('gutenberg')
import pandas as pd
import onion


books = pd.DataFrame((' '.join(sent) for sent in
        nltk.corpus.gutenberg.sents('chesterton-brown.txt')
    ), columns=('sentence',))

tweets = pd.DataFrame((' '.join(sent) for sent in
        nltk.corpus.webtext.sents('overheard.txt')
    ), columns=('tweet',))


o = onion.Onion(
    'text', {
        'text': ['tweets', 'books'],
    }, {
        'text': ['tweets', 'books'],
        'books': books,
        'tweets': tweets
    }
)

print(o.predict('books', 'twasnt a thought'))
print(o.predict('tweets', 'taxi cab'))
