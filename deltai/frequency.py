from nltk.corpus import stopwords
import math
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer



def get_frequency(array_of_texts) :
    
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(array_of_texts)
    names = vectorizer.get_feature_names()
    data = vectors.todense().tolist()
    df = pd.DataFrame(data, columns=names)
    df = df[filter(lambda x: x not in stopwords.words('spanish') , df.columns)]

    N = 10
    return_array = []
    for i in df.iterrows():
        return_array.append(i[1].sort_values(ascending=False)[:N])
    return return_array
    


def verify_title(title, words) :
    words = [word.lower() for word in words]
    return title and any(element in words for element in title.lower().split(' '))