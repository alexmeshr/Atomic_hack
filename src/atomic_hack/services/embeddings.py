from abc import ABC, abstractmethod

from langchain_community.embeddings.gigachat import GigaChatEmbeddings
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_postgres.vectorstores import PGVector

from atomic_hack.settings import settings
from atomic_hack.utils import singleton


class ABSVectorStorage(ABC):
    _embeddings: Embeddings | None
    _vectorstore: VectorStore | None

    @abstractmethod
    def setup(self): ...

    @abstractmethod
    def add_texts(self, new_queries: list[str]): ...

    @abstractmethod
    def get_k_closest(self, query: str, k: int) -> list[Document]: ...


@singleton
class PGVectorStorage(ABSVectorStorage):
    __slots__ = ['_embeddings', '_vectorstore']

    _embeddings: GigaChatEmbeddings | None
    _vectorstore: PGVector | None

    def __init__(self):
        self._embeddings = None
        self._vectorstore = None

    @staticmethod
    def _get_pgvec_connection_uri() -> str:
        # example: postgresql+psycopg://langchain:langchain@localhost:6024/langchain
        pgvec_uri_fstring: str = 'postgresql+psycopg://{login}:{password}@{host}:{port}/{database}'
        return pgvec_uri_fstring.format(
            login=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_url,
            port=settings.postgres_port,
            database=settings.postgres_db,
        )

    def _ensure_initialized(self):
        if self._embeddings is None or self._vectorstore is None:
            raise RuntimeError('setup() must be called at first')

    def setup(self):
        # и нет, это нельзя выносить в __init__
        if self._embeddings is not None or self._vectorstore is not None:
            raise RuntimeError('setup() must be called only once')

        self._embeddings = GigaChatEmbeddings(
            credentials=settings.gigachat_credentials,
            model=settings.gigachat_model,
            verify_ssl_certs=False,
        )

        self._vectorstore = PGVector.from_texts(
            texts=[
                'У попа была собака, он её любил. Она съела кусок мяся - он её убил',
                'У бабы Дуни жила одна рыжая кошечка и 4 котёночка',
            ],
            embedding=self._embeddings,
            collection_name='instructions',
            connection=self._get_pgvec_connection_uri(),
            use_jsonb=True,
        )

    def add_texts(self, new_queries: list[str]):
        self._ensure_initialized()
        self._vectorstore.add_texts(texts=new_queries)

    def get_k_closest(self, query: str, k: int) -> list[Document]:
        self._ensure_initialized()
        return self._vectorstore.similarity_search(query, distance_metric='cos', k=k)
