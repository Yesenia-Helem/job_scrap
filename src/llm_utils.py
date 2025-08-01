from langchain_community.llms import Ollama
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def get_llm(model="llama3"):
    return Ollama(model=model)

def get_llm_chain(prompt_template: str) -> LLMChain:
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["html"],
        template=prompt_template
    )
    return LLMChain(llm=llm, prompt=prompt)
