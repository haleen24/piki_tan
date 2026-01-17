from abc import ABC, abstractmethod
from itertools import chain
from typing import List, Iterable

from .knowledge_extraction import KnowledgeExtraction
from .model import GraphSearchResponse


class GraphDataBaseProvider(ABC):

    @abstractmethod
    def search(self, query: str, n_results: int = None, **kwargs) -> GraphSearchResponse:
        pass

    @abstractmethod
    def add_knowledge(self, extractions: List[KnowledgeExtraction], **kwargs):
        pass


def union_graph_search_response(responses: Iterable[GraphSearchResponse]) -> GraphSearchResponse:
    all_relations = chain.from_iterable(response.relations for response in responses)
    return GraphSearchResponse(relations=all_relations,
                               full_response=(i.full_response for i in responses if i.full_response))


class GraphDataBaseMultiStrategyProvider(GraphDataBaseProvider):

    def __init__(self, search_db: list[GraphDataBaseProvider] | GraphDataBaseProvider,
                 insert_db: list[GraphDataBaseProvider] | GraphDataBaseProvider):
        self.search_dbs = search_db if isinstance(search_db, list) else [search_db]
        self.insert_dbs = insert_db if isinstance(insert_db, list) else [insert_db]

    def add_knowledge(self, extractions: List[KnowledgeExtraction], **kwargs):
        for db in self.insert_dbs:
            db.add_knowledge(extractions, **kwargs)

    def search(self, query: str, n_results: int = None, **kwargs) -> GraphSearchResponse:
        return union_graph_search_response(
            (db.search(query, n_results, **kwargs) for db in self.search_dbs))
