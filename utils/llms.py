import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")

class LLMModel:
    def __init__(self,model_name="meta-llama/llama-4-maverick-17b-128e-instruct"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name=model_name
        self.groq_model=ChatGroq(model_name=self.model_name)

    def get_model(self):
        return self.groq_model


if __name__=="__main__":
    llm_object=LLMModel()
    llm=llm_object.get_model()
    response=llm.invoke("hi")
    print(response)        
