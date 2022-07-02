import re
from sklearn.feature_extraction.text import TfidfVectorizer
from CollectionPreprocessor import CollectionPreprocessor
from sklearn.metrics.pairwise import cosine_similarity

path = '../collection/'


class RankedRetrieval:
    def __init__(self, query):
        self.query = query
        self.collection = CollectionPreprocessor(path)
        self.collection.retrieve_documents()
        self.documents = self.clean_documents()
        self.tfidfvectoriser = TfidfVectorizer()
        self.documents = self.clean_documents()

    def construct_inverted_index(self):
        doc_sents = dict()
        for doc_id, doc in self.collection.documents.items():
            doc_sents[doc_id] = doc.get_sentences

        return doc_sents

    def clean_documents(self):
        documents = self.construct_inverted_index()
        for doc in documents:
            sentences = [sentence.lower().strip() for sentence in documents[doc]]
            sentences = [re.sub(r'[^a-z0-9s]', ' ', sentence) for sentence in sentences]
            documents[doc] = sentences

        return documents

    def calculater_cosine(self):
        sims = []
        for document in self.documents:
            tfidf_matrix_train = self.tfidfvectoriser.fit_transform(self.documents[document])
            tfidf_matrix_test = self.tfidfvectoriser.transform([self.query])
            sims.append(cosine_similarity(tfidf_matrix_train, tfidf_matrix_test).sum())
        return sims

    def respond_to_query(self):
        sims = self.calculater_cosine()
        zipped = zip(self.documents.keys(), sims)

        ranked = sorted(zipped, key=lambda x: x[1], reverse=True)
        return ranked


def main():
    path = '../collection/'
    query = '1984 Julia world war civil'
    model = RankedRetrieval(query)
    response = model.respond_to_query()
    print(response)


if __name__ == '__main__':
    main()
