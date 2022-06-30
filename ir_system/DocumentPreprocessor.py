import nltk.tokenize
import nltk.stem
from nltk import PorterStemmer


class DocumentPreprocessor:
    def __init__(self, doc_unit):
        self.text = doc_unit
        self.sentences = self.tokenize_sentences()
        self._tokens = self.tokenize_words()
        self._stemmed = self.stem_tokens()
        self._lemmas = self.lemmatize_tokens()
        self._terms = self.determine_terms()
        self._tfs = self.calculater_tf()

    @property
    def get_tokens(self):
        return self._tokens

    @property
    def get_lemmas(self):
        return self._lemmas

    @property
    def get_terms(self):
        return self._terms

    @property
    def get_tfs(self):
        return self._tfs

    def tokenize_words(self) -> list[str]:
        # keeps contractions as a single token instead of breaking them up
        return nltk.tokenize.regexp_tokenize(self.text, "[\w']+")

    def tokenize_sentences(self) -> list[str]:
        return nltk.tokenize.sent_tokenize(self.text)

    def stem_tokens(self) -> list[str]:
        stemmer = nltk.stem.PorterStemmer(mode=PorterStemmer.NLTK_EXTENSIONS)
        stemmed_tokens = [stemmer.stem(token) for token in self._tokens]
        return stemmed_tokens

    def lemmatize_tokens(self) -> list[str]:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemmas = [lemmatizer.lemmatize(token, pos='v').lower() for token in self._tokens]
        return lemmas

    def determine_terms(self) -> set:
        return set(self._lemmas)

    def calculater_tf(self) -> dict:
        return {
            term: self._lemmas.count(term) for term in self._terms
        }


def main():
    with open('../collection/1984.txt', 'r') as data:
        text = data.read()
        preprocessor = DocumentPreprocessor(text)
        tokens = preprocessor.get_tokens
        print(tokens)

        lemmas = preprocessor.get_lemmas
        print(lemmas)
        print(len(lemmas))

        terms = preprocessor.get_terms
        print(terms)
        print(len(terms))

        tf = preprocessor.get_tfs
        print(tf)


if __name__ == '__main__':
    main()
