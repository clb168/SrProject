Here we have the RAG working on the polaris documentation.

The folder LangAndOllama contains two folders:
 - Integration testing
 - langchainRag


langchainRag contains the functioning RAG for the polaris documentation. To run the RAG, navigate to the langchainRag folder and run python main.py. 
QuestionGen.py is a simple question generation script that scrapes the documentation and comes up with QA pairs. The quality of these QA pairs varies,
so only certain QA pairs generated can actually be used in testing. All required packages for main and QuestionGen can be found in requirements.txt.

IntegrationTesting is currently a WIP for integrating the rag into the autogen pipeline.

DataConversion folder simply contains a script to convery markdown files to text. This was used to convert the polaris documentation on github to one large text file. 

The polaris documentation github is also linked within the repo

The training material folder contains the documentation used in RAG
