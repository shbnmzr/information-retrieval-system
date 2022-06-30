from CollectionPreprocessor import CollectionPreprocessor
from DocumentPreprocessor import DocumentPreprocessor


class BooleanRetrieval:
    operators = {'AND': intersect,
                 'OR': union,
                 'NOT': complement}

    def __init__(self, query, inverted_index):
        self.query = query
        self.query_terms = self.extract_query_terms()
        self.inverted_index = inverted_index

    def extract_query_terms(self):
        preprocessor = DocumentPreprocessor(self.query)
        return preprocessor.get_terms

    @staticmethod
    def intersect(term1_list, term2_list):
        i = 0
        j = 0
        intersection = []

        while i < len(term1_list) and j < len(term2_list):
            if term1_list[i] == term2_list[j]:
                intersection.append(term1_list[i])
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
    def complement(term_list, collection_list):
        i = 0
        j = 0
        complemented = []

        while i < len(term_list):
            if term_list[i] == collection_list[j]:
                i += 1
                j += 1
            else:
                complemented.append(collection_list)
                j += 1
        if j < len(collection_list):
            complemented.extend(collection_list[j:])

        return complemented
