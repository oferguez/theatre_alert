"""
Culture Officer: Scheduled Google Cloud Function to query GPT for
cultural events coming up in London, and email results.
"""

from pprint import PrettyPrinter
from format_culture_html import parse_and_format_culture_html
import os
import requests
import functions_framework
import logging
from config import Config
from mailjet_rest import Client
from typing import Optional
import json

from cultural_officer_system_prompt import system_prompt, user_prompt

# from ppx_cultural_officer_system_prompt import system_prompt

from flask import Request

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("culture_officer")


def call_perplexity(system_prompt: str, user_prompt: str, config: Config) -> str:
    """
    Calls Perplexity with the given prompts and config parameters.
    """
    logger.info("Calling Perplexity API with model: %s", config.perplexity_model)
    api_url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.perplexity_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": config.perplexity_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful research assistant. Provide comprehensive, well-sourced answers with citations.",
            },
            {
                "role": "user",
                "content": system_prompt,
            },  # todo: sort out user/system prompts
        ],
        "temperature": 0.2,  # Lower for more factual responses
        "max_tokens": 2000,
    }

    logger.info("Sending request to OpenAI API...")
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(f"API call failed: {e}")
        return None
    logger.info("Received response from Perplexity API.")
    return result


def call_gpt(system_prompt: str, user_prompt: str, config: Config) -> str:
    """
    Calls OpenAI GPT API with the given prompts and config parameters.
    """
    logger.info("Calling OpenAI GPT API with model: %s", config.openai_model)
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.openai_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_completion_tokens": max(256, int(config.openai_max_tokens)),  # ensure >0
        # temperature and top_p not supported by search-preview model
        # "temperature": config.openai_temperature,
        # "top_p": config.openai_top_p,
        "response_format": {"type": "text"},  # force plain text
    }
    logger.info("Sending request to OpenAI API...")
    if config.debug:
        logger.info(
            "System Prompt: \n%s\n", json.dumps(data, indent=2, ensure_ascii=False)
        )
    response = requests.post(api_url, headers=headers, json=data, timeout=600)
    logger.info("OpenAI API response: %s", PrettyPrinter().pprint(response))
    if response.status_code != 200:
        logger.error(
            "OpenAI API call failed with status code %s: %s",
            response.status_code,
            response.text,
        )
    response.raise_for_status()
    result = response.json()
    logger.info("Received response from OpenAI API.")
    if config.debug:
        logger.info("System Prompt: \n%s\n", system_prompt)
        logger.info("json result: \n%s\n", json.dumps(result, indent=2))

    msg = result["choices"][0]["message"]
    content = msg.get("content", "")
    if isinstance(content, list):
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))

    if not content:
        logger.warning("finish_reason: %s", result["choices"][0].get("finish_reason"))
        logger.warning("full choice: %s", json.dumps(result["choices"][0], indent=2))

    return result["choices"][0]["message"]["content"]


def send_email(subject: str, html_body: str, config: Config):
    """
    Sends an email using Mailjet API to one or both recipients as configured.
    """
    logger.info(
        "Sending email via Mailjet to: %s",
        [config.email_recipient, getattr(config, "email_recipient_2", None)],
    )
    mailjet = Client(
        auth=(config.mailjet_api_key, config.mailjet_secret), version="v3.1"
    )
    to_list = [{"Email": config.email_recipient, "Name": "Recipient"}]
    if getattr(config, "email_recipient_2", ""):
        to_list.append({"Email": config.email_recipient_2, "Name": "Recipient"})
    email_data = {
        "Messages": [
            {
                "From": {"Email": config.email_sender, "Name": "The Culture Officer"},
                "To": to_list,
                "Subject": subject,
                "HTMLPart": html_body,
            }
        ]
    }
    response = mailjet.send.create(data=email_data)
    logger.info("Mailjet response status: %s", response.status_code)
    return response.status_code, response.json()


@functions_framework.http
def handler(request: Request) -> dict:
    """
    Google Cloud Function entry point for scheduled trigger.
    """
    logger.info("Handler triggered.")
    config = Config().load_and_validate()
    # Customize these prompts as needed
    logger.info("Calling GPT with system prompt and user prompt.")
    html_search_result = call_gpt(system_prompt, user_prompt, config)
    # search_result = call_perplexity(system_prompt, user_prompt, config)
    subject = "Culture Officer Report"
    # html_body = parse_and_format_culture_html(html_search_result)
    if config.debug:
        debug_path = os.path.join(os.path.dirname(__file__), "html_result.html")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(html_search_result)
        logger.info("Debug mode: LLM output saved to %s", debug_path)
    status_code, response_json = send_email(subject, html_search_result, config)
    logger.info("Handler completed. Status: %s", status_code)
    return {"statusCode": status_code, "body": response_json, "log": html_search_result}
