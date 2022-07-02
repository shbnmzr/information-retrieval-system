from CollectionPreprocessor import CollectionPreprocessor
from QueryProcessor import QueryProcessor

path = '../collection/'


class BiwordRetrieval:
    def __init__(self, query):
        self.query = QueryProcessor(query)
        self.collection = CollectionPreprocessor(path)
        self.inverted_index = self.collection.get_biword_inverted_index

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
        query_terms = self.query.get_biwords

        responses = []
        for biword in query_terms:
            if biword in self.inverted_index:
                responses.append(self.inverted_index[biword])

        intersection = responses
        while len(intersection) > 1:
            intersection.append(BiwordRetrieval.merge(intersection[0], intersection[1]))
            intersection.pop(0)
            intersection.pop(0)

        response = {index: self.collection.texts[index] for index in intersection[0]}
        return intersection[0], response


def main():
    query = 'United States'
    pos = BiwordRetrieval(query)
    print(pos.respond_to_query())


if __name__ == '__main__':
    main()