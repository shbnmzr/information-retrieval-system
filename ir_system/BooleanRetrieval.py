from CollectionPreprocessor import CollectionPreprocessor
from QueryProcessor import QueryProcessor

path = '../collection/'


class BooleanRetrieval:
    operator = {
        'and', 'or', 'not'
    }

    def __init__(self, query):
        self.query = QueryProcessor(query)
        self.collection = CollectionPreprocessor(path)
        self.inverted_index = self.collection.get_inverted_index_without_freq

    @staticmethod
    def intersect(term1_list, term2_list):
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

    @staticmethod
    def union(term1_list, term2_list):
        i = 0
        j = 0
        merged = []

        while i < len(term1_list) and j < len(term2_list):
            if term1_list[i] == term2_list[j]:
                merged.append(term1_list[i])
                i += 1
                j += 1
            elif term1_list[i] < term2_list[j]:
                merged.append(term1_list[i])
                i += 1
            else:
                merged.append(term2_list[j])
                j += 1

        if i < len(term1_list):
            merged.extend(term1_list[i:])
        if j < len(term2_list):
            merged.extend(term2_list[j:])

        return merged

    @staticmethod
    def complement(term_list, collection):
        i = 0
        j = 0
        complemented = []

        while i < len(term_list):
            if term_list[i] == collection[j]:
                i += 1
                j += 1
            else:
                complemented.append(collection)
                j += 1
        if j < len(collection):
            complemented.extend(collection[j:])

        return complemented

    def perform_operation(self, operator, term1, term2):
        operators = {
            'and': BooleanRetrieval.intersect,
            'or': BooleanRetrieval.union,
            'not': BooleanRetrieval.complement
        }

        term1_docs = self.inverted_index[term1]
        term2_docs = self.inverted_index[term2]

        return operators[operator](term1_docs, term2_docs)

    def split_query_terms(self):
        terms = self.query.get_lemmas
        return terms

    def response_to_query(self, terms):
        pass


def main():
    query = '1984 or baby and not some'
    boolean = BooleanRetrieval(query)
    boolean.split_query_terms()
    print(boolean.perform_operation('or', '1984', 'the'))
    print(boolean.perform_operation('and', '1984', 'the'))


if __name__ == '__main__':
    main()
