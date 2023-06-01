from dotenv import load_dotenv, find_dotenv
import os

if os.getenv("OPENAI_API_KEY") is None:
    if not load_dotenv(find_dotenv()):
        raise Exception(".env not found and OPENAI_API_KEY not set") 


from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI

class ChatBot:
    def __init__(self):
        with open("../content/content.txt") as f:
            content = f.read()
        text_splitter = CharacterTextSplitter(separator = " ", chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(content)

        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])

        template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
        Assume the question is about Arch Reactor asked by a member or prospective member.
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.

        QUESTION: {question}
        =========
        {summaries}
        ========= 
        FINAL ANSWER:"""
        PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
        llm = OpenAI(temperature=0.5, model_name='gpt-3.5-turbo')
        self.chain = load_qa_with_sources_chain(llm, chain_type="stuff", prompt=PROMPT)



    def __call__(self, query):
        docs = self.docsearch.similarity_search(query)
        return self.chain({"input_documents": docs, "question": query}, return_only_outputs=True)


