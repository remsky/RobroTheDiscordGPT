import os
import re
import requests
import openai

summary_api = os.environ['SUMMARY_API']


def extract_url(text):
    pattern = r"readlink<([^>]+)>"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def remove_read_link(text):
    pattern = r"readlink<[^>]+>"
    return re.sub(pattern, "", text)

def summarize_link(url, sentence_count=4, keyword_count=None):
    base_url = f"https://api.smmry.com/&SM_API_KEY={summary_api}&SM_URL={url}"


    payload = {
        "SM_API_KEY": summary_api,
        "SM_URL": url,
        "SM_LENGTH": sentence_count,
    }

    if keyword_count is not None:
        payload["SM_KEYWORD_COUNT"] = keyword_count

    response = requests.get(base_url, params=payload)
    result = response.json()

    if "sm_api_error" in result:
        print(f"Error {result['sm_api_error']}: {result['sm_api_message']}")
        return

    title = result.get("sm_api_title", "No title available")
    content = result.get("sm_api_content", "No content available")

    return title, content
