dimport pandas as pd
from sklearn.model_selection import train_test_split
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score
nltk.download('punkt')
nltk.download('stopwords')

class DialogAnalisis:
    def __init__(self, df=pd.read_csv("/content/labeled.csv", sep=",")):
        self.df = df
        self.train_df = None
        self.test_df = None
        self.model_pipeline_c_10 = None
        self.thresholds_c_10 = 0.3205092817191188

    def prepare(self):
        self.df["toxic"] = self.df["toxic"].apply(int)
        self.train_df, self.test_df = train_test_split(self.df, test_size=500)

    def tokenize_sentence(sentence: str, remove_stop_words: bool = True):
        snowball = SnowballStemmer(language="russian")
        russian_stop_words = stopwords.words("russian")
        tokens_ = word_tokenize(sentence, language="russian")
        tokens = []
        for i in tokens_:
            if i not in string.punctuation:
                tokens.append(i)
        tokens_ = tokens[:]
        tokens = []
        if remove_stop_words:
            for i in tokens_:
                if i not in russian_stop_words:
                    tokens.append(i)
        tokens = [snowball.stem(i) for i in tokens]
        return tokens

    def learning_model(self):
        self.model_pipeline_c_10 = Pipeline([
            ("vectorizer", TfidfVectorizer(tokenizer=lambda x: self.tokenize_sentence(x, remove_stop_words=True))),
            ("model", LogisticRegression(random_state=0, C=10.))
        ])

        self.model_pipeline_c_10.fit(self.train_df["comment"], self.train_df["toxic"])

    def get_metrics(self):
        precision = precision_score(y_true=self.test_df["toxic"],
                        y_pred=self.model_pipeline_c_10.predict_proba(self.test_df["comment"])[:, 1] > self.thresholds_c_10)
        recall = recall_score(y_true=self.test_df["toxic"],
                        y_pred=self.model_pipeline_c_10.predict_proba(self.test_df["comment"])[:, 1] > self.thresholds_c_10)

        return {'precision': precision, 'recall': recall}

    def analis_chat(self, chat):
        pass