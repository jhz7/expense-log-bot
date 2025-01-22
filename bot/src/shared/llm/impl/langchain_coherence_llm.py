import os
from dotenv import load_dotenv
from asyncio.threads import to_thread
from langchain_community.llms.cohere import Cohere
from langchain_core.prompts import PromptTemplate

from src.shared.llm.llm import LLM
from src.shared.errors.technical import TechnicalError
from src.shared.logging.log import Logger

load_dotenv()
__cohere_api_key = os.environ.get("COHERE_API_KEY")
model = Cohere(cohere_api_key=__cohere_api_key, max_tokens=256, temperature=0.75)

logger = Logger(__name__)


class LangChainCohereTextGenerator(LLM):
    async def generate(self, prompt: str, input: dict) -> str:
        try:
            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=list(input.keys()),
            )
            chain = prompt_template | model

            msg = await to_thread(chain.invoke, input)

            logger.debug(f"Generated text: text={msg} input={input}")

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
