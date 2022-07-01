from DocumentPreprocessor import DocumentPreprocessor


class QueryProcessor(DocumentPreprocessor):
    def __init__(self, query):
        super().__init__(query)


def main():
    query = 'is 1984 a good film?'
    processor = QueryProcessor(query)
    print(processor.get_terms)


if __name__ == '__main__':
    main()