import nltk.tokenize
import nltk.stem
from nltk import PorterStemmer


class Preprocessor:
    def __init__(self, doc_unit):
        self.text = doc_unit
        self.sentences = self.tokenize_sentences()
        self.tokens = self.tokenize_words()
        self.stemmed = self.stem_tokens()
        self.lemmas = self.lemmatize_tokens()

    def tokenize_words(self) -> list[str]:
        # keeps contractions as a single token instead of breaking them up
        return nltk.tokenize.regexp_tokenize(self.text, "[\w']+")

    def tokenize_sentences(self) -> list[str]:
        return nltk.tokenize.sent_tokenize(self.text)

    def stem_tokens(self):
        stemmer = nltk.stem.PorterStemmer(mode=PorterStemmer.NLTK_EXTENSIONS)
        stemmed_tokens = [stemmer.stem(token) for token in self.tokens]
        return stemmed_tokens

    def lemmatize_tokens(self):
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token, pos='v') for token in self.tokens]
        return lemmas


def main():
    with open('./collection/1984.txt', 'r') as data:
        text = data.read()
        preprocessor = Preprocessor(text)
        tokens = preprocessor.tokens
        print(tokens)

        stemmed = preprocessor.stemmed
        print(stemmed)

        lemmas = preprocessor.lemmas
        print(lemmas)


if __name__ == '__main__':
    main()
