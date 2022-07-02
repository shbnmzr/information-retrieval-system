from CollectionPreprocessor import CollectionPreprocessor
from QueryProcessor import QueryProcessor

path = '../collection/'

class BooleanRetrieval:
    operator = {
        'and': 1,
        'or': 1,
        'not': 2
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

    @staticmethod
    def perform_operation(operator, term1, term2):
        operators = {
            'and': BooleanRetrieval.intersect,
            'or': BooleanRetrieval.union,
            'not': BooleanRetrieval.complement
        }

        return operators[operator](term1, term2)

    def split_query_terms(self):
        terms = self.query.get_lemmas
        return terms

    def respond_to_query(self):
        postings_stack = []
        operators_stack = []

        i = 0
        while i < len(self.query.get_lemmas):
            if (current := self.query.get_lemmas[i]) == '(':
                operators_stack.append(current)
            elif current not in BooleanRetrieval.operator.keys():
                if current in self.inverted_index:
                    postings_stack.append(self.inverted_index[current])
                else:
                    return []
            elif current == ')':
                while operators_stack[-1] != '(' and len(operators_stack) != 0:
                    term1 = postings_stack.pop()
                    term2 = postings_stack.pop()
                    operator = operators_stack.pop()

                    postings_stack.append(BooleanRetrieval.perform_operation(operator, term1, term2))
                operators_stack.pop()

            else:
                if current == 'not':
                    next_term = self.query.get_lemmas[i + 1]
                    complemented = BooleanRetrieval.perform_operation(current, self.inverted_index[next_term], self.collection.get_inverted_index_without_freq[next_term])
                    postings_stack.append(complemented)
                    i += 2
                    continue

                while len(operators_stack) != 0:
                    term1 = postings_stack.pop()
                    term2 = postings_stack.pop()
                    operator = operators_stack.pop()

                    postings_stack.append(BooleanRetrieval.perform_operation(operator, term1, term2))
                operators_stack.append(current)
            i += 1

        while len(operators_stack) != 0:
            term1 = postings_stack.pop()
            term2 = postings_stack.pop()
            operator = operators_stack.pop()

            postings_stack.append(BooleanRetrieval.perform_operation(operator, term1, term2))

        return postings_stack[-1]


def main():
    query = '(1984 or world) or not the'
    boolean = BooleanRetrieval(query)
    boolean.split_query_terms()
    print(boolean.respond_to_query())


if __name__ == '__main__':
    main()
