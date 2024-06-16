import os

from tqdm import tqdm
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from atomic_hack.services import embeddings


def process_folder_with_pdfs(path_to_folder: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        separators=['\n\n', '.'],
    )

    print('creating loaders')
    loaders = [PyPDFLoader(os.path.join(path_to_folder, pdf)) for pdf in os.listdir(path_to_folder)]

    bad_chars = ('!', '*', '\n', '..')
    def _remove_all_bad(doc: Document) -> Document:
        """INPLACE"""
        for char in bad_chars:
            doc.page_content = doc.page_content.replace(char, '')
        return doc

    print('processing')
    all_pages: list[Document] = [
        _remove_all_bad(p) for loader in tqdm(loaders) for p in loader.load_and_split(text_splitter)
        if p.metadata['page'] > 4
    ]

    print('saving')
    pgvs = embeddings.PGVectorStorage()
    pgvs.setup()

    pgvs.add_documents(all_pages)

    del pgvs
