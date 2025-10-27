import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv(r"C:\Users\fesan\recommendation_system\datasets\the_movies_dataset\movies_metadata.csv", low_memory=False)



df.shape
df.head()
df.overview.isnull().sum()
df = df.dropna(subset=["overview"])
df.overview.isnull().sum()

df_sample = df.sample(n=10000)
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf_vectorizer.fit_transform(df_sample['overview'])

tfidf_matrix.shape

tfidf_vectorizer.get_feature_names_out()


cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

indices  = pd.Series(data = df_sample.index, index = df_sample["title"])

indices.index.value_counts()

df_sample_notduplicated = df_sample[~df_sample.duplicated(keep="last")]
cosine_sim[0]