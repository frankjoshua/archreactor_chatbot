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
from langchain.chat_models import ChatOpenAI

class ChatBot:
    def __init__(self):
        print("Loading content...")
        with open("./content/content.txt") as f:
            content = f.read()
        text_splitter = CharacterTextSplitter(separator = " ", chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(content)
        print("Loaded content")

        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])

        template = """
        I want you to act as a mental health adviser. 
        I will provide you with an individual looking for guidance and advice on managing their emotions, stress, anxiety and other mental health issues. 
        You should use your knowledge of cognitive behavioral therapy, meditation techniques, mindfulness practices, and other 
        therapeutic methods in order to create strategies that the individual can implement in order to improve their overall wellbeing
        
        =========
        Here are some summaries of articles that might be relevant to the individual's situation:
        {summaries}
        ========= 
        QUESTION: {question}
        FINAL ANSWER:"""
        PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])
        llm = ChatOpenAI(temperature=0.5, model_name='gpt-3.5-turbo')
        self.chain = load_qa_with_sources_chain(llm, chain_type="stuff", prompt=PROMPT)

    def getChain(self):
        return self.chain

    def __call__(self, query):
        docs = self.docsearch.similarity_search(query)
        return self.chain({"input_documents": docs, "question": query}, return_only_outputs=False)


