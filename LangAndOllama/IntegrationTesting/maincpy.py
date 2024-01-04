

import autogen

#from rag import rag_llm

import litellm


from langchain.document_loaders import OnlinePDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings
from langchain import PromptTemplate
from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

from langchain.document_loaders import PyPDFLoader

import sys
import os

#rag_llm = rag_llm()
class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

# load the pdf and split it into chunks
# loader = OnlinePDFLoader("https://d18rn0p25nwr6d.cloudfront.net/CIK-0001813756/975b3e9b-268e-4798-a9e4-2a9a7c92dc10.pdf")
# data = loader.load()

loader = PyPDFLoader("exampleData/RAGTEST.pdf")
data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

with SuppressStdout():
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

def retrive_content(query):
        loader = PyPDFLoader("exampleData/RAGTEST.pdf")
        data = loader.load()

        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        all_splits = text_splitter.split_documents(data)

        with SuppressStdout():
            vectorstore = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

        # while True:
        #     #
        #     query = input("\nQuery: ")
        #     if query == "exit":
        #         break
        #     if query.strip() == "":
        #         continue

    # Prompt
        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum and keep the answer as concise as possible. 
        {context}
        Question: {question}
        Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        llm = Ollama(model= "llama2", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectorstore.as_retriever(), 
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )




        result = qa_chain({"query": query})
        return (result)



litellm.add_function_to_prompt = True
config_list_Agent = [
    {
    'base_url' : "http://0.0.0.0:30943",
    'api_key' : "NULL"
    }
]
config_list_llama2 = [
    {
    'base_url' : "http://127.0.0.1:11434",
    'api_key' : "NULL"
    }
]

llm_config = {
    "functions": [
        {
            "name": "rag",
            "description": "Returns rag answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query that needs context to be answered using the retrive_content function.",
                    }
                },
                "required": ["query"],
            },
        },
    ],
    "config_list": config_list_llama2,
    "timeout": 60,
}

Agent_config = {
    "functions": [
        {
            "name": "rag",
            "description": "Returns the context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query that needs context to be answered using the retrive_content function.",
                    }
                },
                "required": ["query"],
            },
        },
    ],
    "config_list": config_list_Agent,
    "timeout": 60,
}

rag_assistant_agent_prompt = ""
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message=rag_assistant_agent_prompt,
    llm_config=Agent_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config={"work_dir": "/home/caden/ragExperiment/langAndOllama/evansWork/"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
    function_map={"retrive_content": retrive_content}
)

user_proxy.register_function(
    function_map= {
        "retrive_content": retrive_content,
    }
)

user_proxy.initiate_chat(
    assistant,
    # message="""
    # How should users set up their environment on Polaris for CUDA programming in C/C++, and what are the likely modules and compilers to be used?

    # """
    message="""how many apples does caden have?"""

)