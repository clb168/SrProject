from langchain.llms import Ollama
llama2 = "llama2"
llm = Ollama(base_url="http://127.0.0.1:11434", model=llama2)
#llm = Ollama(model="llama2")
res = llm.predict("hello")
print (res)