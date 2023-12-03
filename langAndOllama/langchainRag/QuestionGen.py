from langchain.document_loaders import PyPDFLoader
from langchain.llms import Ollama 
from langchain.chains import QAGenerationChain
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter

text_splitter =  RecursiveCharacterTextSplitter(chunk_overlap=500, chunk_size=2000)

llm = Ollama(model="mistral")

loader = PyPDFLoader("/home/caden/ragExperiment/langAndOllama/langchainRag/exampleData/polaris_3.pdf")
chain = QAGenerationChain.from_llm(llm=llm, text_splitter=text_splitter)

data = loader.load()[0]
qa = chain.run(data.page_content)

print(qa)