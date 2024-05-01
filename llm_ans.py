from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain import PromptTemplate
from langchain.chains import RetrievalQA


class LlmResponse:
    def __init__(self, query):
        self.query = query

        self.template="""Use the following pieces of information to answer the user's question.
            Context:{context}
            Question:{question}

            """

        #Step-1: Load the document
        self.loader=DirectoryLoader('data/',
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)
        self.documents=self.loader.load()


        #Step-2: Chunkin operation
        self.text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.text_chunks=self.text_splitter.split_documents(self.documents)


        #Step-3: Load the Embedding Model
        self.embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', 
                                        model_kwargs={'device':'cpu'})


        #step-4: Use Vector DataBase to store the emeddings
        self.vector_store=FAISS.from_documents(self.text_chunks, self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={'k': 2})


        #Step-5: Initialize llm
        self.llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                        model_type="llama",
                        config={'max_new_tokens':128,
                                'temperature':0.01})

        #step-6: Use prompt template foruser query: Perform Q&A, using template from helper.py
        self.qa_prompt=PromptTemplate(template=self.template, input_variables=['context', 'question'])


        #Step-7: creating RetrievalQA chain 
        self.chain = RetrievalQA.from_chain_type(llm=self.llm,
                                        chain_type='stuff',
                                        retriever=self.retriever,
                                        return_source_documents=False,
                                        chain_type_kwargs={'prompt': self.qa_prompt})

    def get_response(self):
        query = self.query
        result=self.chain({'query':query })
        # print(f"Answer:{result['result']}")
        return result

if __name__ == "__main__":
    query = "What is infini-attension"
    obj = LlmResponse(query)
    result = obj.get_response()
    print(f"\n {result['result']}")