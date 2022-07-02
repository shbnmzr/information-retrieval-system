from DocumentPreprocessor import DocumentPreprocessor
import os

class CollectionPreprocessor:
    def __init__(self, path):
        self.path = path
        self.documents = dict()
        self.retrieve_documents()
        self._inverted_index, self._inverted_index_without_freq = self.construct_inverted_index()
        self._biwords_inverted_index = self.construct_biwords_inverted_index()

    @property
    def get_inverted_index(self):
        return self._inverted_index

    @property
    def get_inverted_index_without_freq(self):
        return self._inverted_index_without_freq

    @property
    def get_biword_inverted_index(self):
        return self._biwords_inverted_index

    def retrieve_documents(self):
        doc_counter = 0
        for doc in os.listdir(self.path):
            if doc.endswith('.txt'):
                with open(os.path.join(self.path, doc), 'r') as data:
                    text = data.read()
                    self.documents[doc_counter] = DocumentPreprocessor(text)
                    doc_counter += 1

    def construct_inverted_index(self):
        term_doc_ids = dict()
        for doc_id, doc in self.documents.items():
            for term in doc.get_terms:
                if term not in term_doc_ids:
                    term_doc_ids[term] = [doc_id]
                else:
                    term_doc_ids[term].append(doc_id)

        return {
            (term, len(term_doc_ids[term])): term_doc_ids[term] for term in term_doc_ids
        }, {
            term: term_doc_ids[term] for term in term_doc_ids
        }

    def construct_biwords_inverted_index(self):
        term_doc_ids = dict()
        for doc_id, doc in self.documents.items():
            for term in doc.get_biwords:
                if term not in term_doc_ids:
                    term_doc_ids[term] = [doc_id]
                else:
                    term_doc_ids[term].append(doc_id)

        return {
                   term: term_doc_ids[term] for term in term_doc_ids
               }


def main():
    path = '../collection/'
    pre = CollectionPreprocessor(path)
    print(pre.get_inverted_index)
    print(pre.get_inverted_index_without_freq)
    print(pre.get_biword_inverted_index)


if __name__ == '__main__':
    main()
    