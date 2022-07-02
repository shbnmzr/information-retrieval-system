from PositionalIndexing import PositionalIndexing
from QueryProcessor import QueryProcessor

path = '../collection/'


class PositionalRetrieval:
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
        responses = []
        for i in range(len(query_terms) - 1):
            if query_terms[i] in indices:
                if query_terms[i + 1] in indices:
                    term1 = indices[query_terms[i]]
                    term2 = indices[query_terms[i + 1]]
                    res = []
                    for key, value in term1.items():
                        if key in term2:
                            if PositionalRetrieval.check_positions(term1[key], term2[key]):
                                res.append(key)
                    responses.append(res)

        intersection = responses
        while len(intersection) > 1:
            intersection.append(PositionalRetrieval.intersect(intersection[0], intersection[1]))
            intersection.pop(0)
            intersection.pop(0)

        return intersection[0]

    @staticmethod
    def check_positions(term1_list, term2_list):
        i = 0
        j = 0

        while i < len(term1_list) and j < len(term2_list):
            if term2_list[j] - term1_list[i] == 1:
                return True
            elif term2_list[j] - term1_list[i] < 0:
                j += 1
            else:
                i += 1

        return False

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


def main():
    query = 'in the world'
    pos = PositionalRetrieval(query)
    print(pos.respond_to_query())

if __name__ == '__main__':
    main()
