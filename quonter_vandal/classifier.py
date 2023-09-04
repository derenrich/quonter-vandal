from dataclasses import dataclass
import os
import yaml
from typing import Optional
import openai
from aiolimiter import AsyncLimiter

MODEL = "ft:gpt-3.5-turbo-0613:personal::7rFQlteL"

SYSTEM_PROMPT = """
You are a Wikidata administrator in the year 2023. You will be shown a Wikidata item and an edit to that item. You should decide whether the edit should be reverted then output a rationale for your decision and your decision in YAML format.
"""


@dataclass
class ClassificationResult:
    revert: Optional[bool]
    rationale: Optional[str]
    doc: str


class Classifier:
    def __init__(self):
        key_file = os.path.expanduser("~/openai.key")
        with open(key_file, 'r') as f:
            openai.api_key = f.read().strip()
        # maximum rate of 3/minute
        self._limiter = AsyncLimiter(3)

    async def classify(self, doc) -> Optional[ClassificationResult]:
        async with self._limiter:
            try:
                completion = await openai.ChatCompletion.acreate(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": doc},
                    ]
                )
                if completion:
                    doc = completion.get("choices")[0].get(
                        "message").get("content")
                    try:
                        response = yaml.safe_load(doc)
                        revert = response.get("revert")
                        rationale = response.get("rationale")
                        return ClassificationResult(revert, rationale, doc)
                    except:
                        return ClassificationResult(None, None, doc)
            except:
                return None
