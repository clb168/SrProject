from langchain.document_loaders import PyPDFLoader
from langchain.llms import Ollama 
from langchain.chains import QAGenerationChain
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter

text_splitter =  RecursiveCharacterTextSplitter(chunk_overlap=500, chunk_size=2000)

llm = Ollama(model="mistral")

loader = PyPDFLoader("/home/caden/ragExperiment/langAndOllama/langchainRag/exampleData/polaris_3.pdf")
chain = QAGenerationChain.from_llm(llm=llm, text_splitter=text_splitter)

data = loader.load()[100] #this chunck size and overlap seems to give 113 pages. -1 is referring to the last page
#the pdf is 113 pages
qa = chain.run(data.page_content)
#print(data)
print(qa)
