from dotenv import load_dotenv
import os
from asyncio.threads import to_thread
from langchain_community.llms.cohere import Cohere
from langchain_core.prompts import PromptTemplate

from src.shared.llm.llm import LLM
from src.shared.errors.technical import TechnicalError
from src.shared.logging.log import Logger

load_dotenv()

logger = Logger(__name__)


class LangChainMessageAnalyzer(LLM):

    def __init__(self):
        cohere_api_key = os.environ.get("COHERE_API_KEY")
        self.__model = Cohere(
            cohere_api_key=cohere_api_key, max_tokens=256, temperature=0.75
        )

    async def generate(self, prompt: str, input: dict) -> str:
        try:
            chain = __build_prompt_template(prompt, input) | self.__model
            msg = await to_thread(chain.invoke, input)

            return msg
        except Exception as e:
            error = TechnicalError(
                code="LlmError",
                message="Error generating text",
                attributes=input,
                cause=e,
            )

            logger.error(error)

            raise error from e


def __build_prompt_template(prompt: str, input: dict) -> PromptTemplate:
    return PromptTemplate(
        template=prompt,
        input_variables=list(input.keys()),
    )
