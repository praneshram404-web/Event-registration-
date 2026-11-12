
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_URL = "https://api.openai.com/v1/chat/completions"


def extract_registration(entry):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_actual_key_here":
        raise RuntimeError("OPENAI_API_KEY is missing from .env")

    prompt_path = Path(__file__).with_name("system_prompt.txt")
    system_prompt = prompt_path.read_text(encoding="utf-8")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": entry}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

        content = result["choices"][0]["message"]["content"]
        return json.loads(content)

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenAI API error ({error.code}): {details}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Network connection error: {error.reason}"
        ) from error

    except (KeyError, IndexError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Invalid response from OpenAI API: {error}"
        ) from error
