# Information Retrieval System

## Introduction
This is lightweight Python-based information retrieval system that attempts to address an *ad hoc retrieval* task, in which a system provides documents from within a collection that are relevant to an arbitrary *information need*, communicated by means of a one-off user-initiated *query*.

The project supports document indexing, query processing, and result ranking on a simple corpus. 
It is designed for educational purposes and is extensible for experimentation.

## Project Structure

```text
.
├── App.py
├── ClientSide
│   ├── app.js
│   ├── icons
│   │   ├── calculator.svg
│   │   ├── circle-2.svg
│   │   ├── mouse.svg
│   │   └── trophy-star.svg
│   ├── index.html
│   └── styles.css
├── collection
│   ├── 1984.txt
│   ├── handmaids-tale.txt
│   ├── to-kill-a-mocking-bird.txt
│   └── wh.txt
└── core
    ├── BiwordRetrieval.py
    ├── BooleanRetrieval.py
    ├── CollectionPreprocessor.py
    ├── DocumentPreprocessor.py
    ├── PositionalIndexing.py
    ├── PositionalRetrieval.py
    ├── QueryProcessor.py
    ├── RankedRetrieval.py
    └── api.py
```

## Retrieval Algorithms
The heart of the system lies in the `core/` directory, where each retrieval model is implemented modularly for clarity and flexibility.

### `core/DocumentPreprocessor.py`

Handles text normalization and feature extraction at the document level. Tokenizes, lemmatizes, and constructs term-level data structures.

#### Functionality

Processes a single document through NLTK-based NLP operations and stores all intermediate representations for retrieval and indexing.

#### Core Capabilities

- Sentence and word tokenization
- Lowercasing and punctuation handling
- Lemmatization with WordNet (verb POS)
- Term set extraction
- Term frequency calculation
- Biword construction (adjacent lemma pairs)

#### API Overview

- `get_text`, `get_sentences`, `get_tokens`, `get_lemmas`, `get_terms`, `get_tfs`, `get_biwords`

#### Dependencies

- NLTK (requires Punkt and WordNet)
- Assumes raw `.txt` input files

#### Integration

Used by `CollectionPreprocessor` to provide structured data to indexing and retrieval modules.

### `core/QueryProcessor.py`

Subclass of `DocumentPreprocessor` for query inputs. Initialized with a string query and inherits all preprocessing behavior.

#### Features

- Fully reuses sentence and word tokenization, lemmatization, and biword generation
- Ensures consistency between user queries and the preprocessed document collection

#### Integration

Used by all retrieval modules to normalize user queries for accurate term matching.

### `core/CollectionPreprocessor.py`

Handles document loading, preprocessing, and index construction.

#### Input

- Takes path to `.txt` files in the `collection/` folder

#### Features

- Loads documents and preprocesses them via `DocumentPreprocessor`
- Builds:
  - Inverted index (with and without term frequencies)
  - Biword inverted index (for adjacent term pairs)

#### API Overview

- `get_inverted_index`
- `get_inverted_index_without_freq`
- `get_biword_inverted_index`

#### Integration

Automatically invoked during class initialization. Provides indexing backbone for Boolean, Biword, and Ranked retrieval modules.

### `core/BooleanRetrieval.py`

Implements Boolean logic (AND, OR, NOT) with support for parentheses and operator precedence.

#### Features

- Indexes with `CollectionPreprocessor`
- Parses normalized queries with `QueryProcessor`
- Resolves:
  - `AND`: intersection of document lists
  - `OR`: union of lists
  - `NOT`: complement using full set of document IDs

### `core/PositionalIndexing.py`
The `PositionalIndexing` module is designed to build a **positional inverted index** from a collection of text documents. Unlike standard inverted indexes that only store document IDs for each term, a positional index captures the exact positions (word indices) of terms within documents, enabling support for **phrase queries** and **proximity searches**.

---

#### Features

- **Document Loading**: Scans a specified directory for `.txt` files, reads their content, and preprocesses each document using `DocumentPreprocessor`.
- **Lemmatized Token Stream**: Applies the same preprocessing pipeline as used elsewhere in the system to ensure consistent vocabulary normalization.
- **Positional Index Construction**:
  - For each unique term, stores a mapping of document IDs to lists of positions where the term appears.
  - Enables efficient lookup of where terms occur within documents, rather than just whether they occur.

---

#### Inverted Index Structure

The generated positional index is a nested dictionary:
- Keys: lemmatized terms
- Values: dictionaries mapping each document ID to a list of positions (indices)

This allows for more advanced querying, such as:
- Identifying whether a phrase appears with exact word order
- Determining how close two words occur in the text

---

#### API Overview

- `get_inverted_index`: Property that returns the full positional index.
- `retrieve_documents()`: Loads and preprocesses all documents in the given directory.
- `construct_inverted_index()`: Builds the positional index from the lemmatized tokens of each document.
- `indices()`: Static method that returns all word positions of a given term within a document.

---

#### Use Cases

- **Phrase Matching**: Quickly determine if terms appear consecutively in a document.
- **Proximity Search**: Identify documents where terms appear within a certain number of words from one another.
- **Passage Retrieval**: Extract specific contexts in which terms co-occur.

---

#### Dependencies

- Python Standard Library: `os`, `collections`
- Custom Module: `DocumentPreprocessor` for text normalization and tokenization

---

This module provides a deeper level of document indexing essential for supporting advanced retrieval tasks beyond simple keyword search.

### `core/PositionalRetrieval.py`

The `PositionalRetrieval` class implements a phrase-based search system that utilizes a **positional inverted index** to identify documents containing exact adjacent term pairs from the input query. It supports efficient phrase matching by checking if consecutive query terms appear in sequential positions within documents.
This module builds on top of the `PositionalIndexing` and `QueryProcessor` components to:
- Parse and normalize queries using lemmatization
- Access positional term data within the document corpus
- Detect co-occurrence of query terms in immediate succession (i.e., phrases)

---

#### Features

- **Phrase-Level Matching**: Checks for adjacent terms (distance = 1) within the same document to determine phrase presence.
- **Lemmatized Query Support**: Ensures consistency with the preprocessing pipeline used in indexing.
- **Efficient Document Filtering**: Uses sorted list merging and two-pointer techniques to intersect document lists and confirm position alignment.
- **Stacked Intersection**: For multi-term queries, intersections are progressively merged to identify common phrase spans across the query.

---

#### API Overview

- `merge()`: Intersects two document ID lists for two terms.
- `check_positions()`: Determines whether the second term occurs immediately after the first in any document.
- `respond_to_query()`: Main method that:
  - Extracts lemmatized terms from the query
  - Identifies adjacent term matches using the positional index
  - Merges matches iteratively to find complete multi-word phrase spans
  - Returns matched document IDs and their full text content

---

#### Dependencies

- Requires:
  - `QueryProcessor` for query tokenization and lemmatization
  - `PositionalIndexing` for accessing indexed positional data
- Assumes a valid document collection in `../collection/` format

---

#### Use Cases

- Precise phrase retrieval: e.g., identifying documents that contain the exact sequence "machine learning"
- Use in combination with TF-IDF or BM25 for hybrid ranked phrase retrieval
- Suitable for document retrieval in legal, scientific, or news corpora where phrase fidelity is essential

---

This module adds fine-grained phrase querying capability to the overall IR system, complementing Boolean and ranked retrieval by introducing structure-sensitive search.

### `core/BiwordRetrieval.py`

The `BiwordRetrieval` class provides a simplified phrase-based search capability using **biword indexing**. It matches queries by identifying exact sequences of two adjacent words (biwords) within documents, enabling lightweight phrase matching with lower complexity compared to full positional indexing.
This module supports phrase queries by:
- Preprocessing user input using lemmatization
- Extracting biwords from the normalized query
- Comparing them directly against a precomputed **biword inverted index**

It is ideal for short queries where adjacent word pairs matter more than complex phrase structure or proximity logic.

---

#### Features

- **Biword-Level Matching**: Checks if query-derived biwords appear in documents.
- **Efficient Set Intersection**: Uses a two-pointer merge strategy to find common documents containing all query biwords.
- **Lemmatized Input**: Ensures that biwords in the query are linguistically consistent with those in the indexed corpus.
- **Simple Output Structure**: Returns matching document IDs and corresponding full text content.

---

#### API Overview

- `respond_to_query()`: 
  - Processes the user query and generates biwords
  - Matches each biword against the inverted index
  - Performs progressive intersection to retain only documents containing all biwords
- `merge()`: 
  - Merges two document lists to identify documents common to both

---

#### Dependencies

- Requires:
  - `QueryProcessor` to normalize and generate biwords from the query
  - `CollectionPreprocessor` to build the biword inverted index from the document corpus
- Assumes that documents are stored in a `.txt` format under `../collection/`

---

#### Use Cases

- Detecting short fixed phrases (e.g., “climate change”, “data science”)
- Educational demos of n-gram retrieval techniques
- Performance-conscious applications needing simple phrase support without the complexity of full positional indexing

---

The `BiwordRetrieval` module is a lightweight, effective way to retrieve documents containing exact word pairs and serves as a bridge between single-term and full-phrase search strategies.

### `core/RankedRetrieval.py`
The `RankedRetrieval` module implements a **TF-IDF-based vector space model** to rank documents according to their similarity to a user query. It computes cosine similarity between query vectors and document sentence vectors using `scikit-learn`'s `TfidfVectorizer`, enabling ranked retrieval of documents based on relevance.

This module provides a basic **ranked information retrieval** system using term frequency–inverse document frequency (TF-IDF) weighting. It focuses on measuring **semantic similarity** between a query and preprocessed sentences from documents, making it useful for retrieving the most relevant results rather than simply exact matches.

---

#### Features

- **TF-IDF Representation**: Converts both documents and query into TF-IDF vectors.
- **Sentence-Level Granularity**: Processes each document at the sentence level for improved granularity and matching precision.
- **Cosine Similarity Scoring**: Measures how closely the query aligns with document content using cosine similarity.
- **Ranked Results**: Returns documents in descending order of similarity scores, filtering out those with no match.

---

#### Internal Workflow

- **Document Preprocessing**:
  - Extracts all sentences from each document using `CollectionPreprocessor`.
  - Lowercases and strips punctuation using regular expressions.
- **TF-IDF Vectorization**:
  - Each document's sentences are vectorized using a shared `TfidfVectorizer` instance.
  - The query is transformed using the same vectorizer.
- **Similarity Calculation**:
  - Cosine similarity is computed between each document's sentence matrix and the query vector.
  - Sentence-level scores are summed to yield a document-level similarity score.
- **Ranking**:
  - Results are sorted based on similarity and returned with document content.

---

#### Dependencies

- `scikit-learn`: For TF-IDF vectorization and cosine similarity computation
- `re`: For regex-based cleaning
- `CollectionPreprocessor`: For document loading and sentence extraction

---

#### Use Cases

- Ranked search for short to medium queries
- Educational demonstration of vector space IR models
- Retrieval systems requiring relevance-based scoring rather than Boolean logic

---

The `RankedRetrieval` module introduces a relevance-scored approach to document retrieval and complements the binary decision models in the IR system with a soft ranking mechanism.
