import os
from asyncio.threads import to_thread
from langchain_community.llms.cohere import Cohere
from langchain_core.prompts import PromptTemplate

from src.shared.llm.llm import LLM
from src.shared.errors.technical import TechnicalError
from src.shared.logging.log import Logger

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

logger = Logger(__name__)


class LangChainCohereTextGenerator(LLM):
    def __init__(self):
        super().__init__()
        self.model = Cohere(
            cohere_api_key=COHERE_API_KEY, max_tokens=256, temperature=0.75
        )

    async def generate(self, prompt: str, input: dict) -> str:
        try:
            prompt_template = PromptTemplate(
                template=prompt,
                input_variables=list(input.keys()),
            )
            chain = prompt_template | self.model

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
