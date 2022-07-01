from PositionalIndexing import PositionalIndexing
from QueryProcessor import QueryProcessor

path = '../collection/'


class PositionalRetrieval():
    def __init__(self, query):
        self.query = QueryProcessor(query)
        self.collection = PositionalIndexing(path)
        self._inverted_index = self.collection.get_inverted_index

    @staticmethod
    def merge(term1_list, term2_list):
        i = 0
        j = 0
        intersection = []

        while i < len(term1_list) and j < len(term2_list):
            if term1_list[i] == term2_list[j]:
                intersection.append(term1_list[i])
                i += 1
                j += 1
            elif term1_list[i] < term2_list[j]:
                i += 1
            else:
                j += 1

        return intersection

    def respond_to_query(self):
        query_terms = self.query.get_lemmas
        indices = self.collection.get_inverted_index
        for i in range(len(query_terms) - 1):
            if query_terms[i] in indices:
                if query_terms[i + 1] in indices:
                    doc1 = [index.keys() for index in indices[query_terms[i]]]
                    doc2 = [index.keys() for index in indices[query_terms[i + 1]]]
                    print(indices[query_terms[i]])
                    print(doc2)


def main():
    query = '1984 baby the world'
    pos = PositionalRetrieval(query)
    print(pos.respond_to_query())


if __name__ == '__main__':
    main()
