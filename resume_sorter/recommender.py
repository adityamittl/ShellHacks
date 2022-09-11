def removeStopWords(sentence):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)

    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    return " ".join(filtered_sentence)

def removePunc(sentence):
    import string
    text = [char for char in sentence if char not in string.punctuation]
    return ''.join(text)

def recommendPosition(resume):
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    df = pd.read_csv('UpdatedResumeDataSet.csv')

    df['Resume_filtered'] = df['Resume'].apply(removeStopWords)
    df['Resume_filtered'] = df['Resume_filtered'].apply(removePunc)

    resume = removeStopWords(resume)
    resume = removePunc(resume)

    resume = [resume]

    data = list(df['Resume_filtered']) + resume

    cv = CountVectorizer(max_features=1000,stop_words='english')
    vector = cv.fit_transform(data).toarray()

    similarity = cosine_similarity(vector)

    distances = sorted(list(enumerate(similarity[962])),reverse=True,key = lambda x: x[1])
    
    return df.iloc[distances[1][0]].Category
