"""
Culture Officer: Scheduled Google Cloud Function to query GPT for
cultural events coming up in London, and email results.
"""

from format_culture_html import parse_and_format_culture_html
import os
import requests
import functions_framework
import logging
from config import Config
from mailjet_rest import Client
from typing import Optional
from cultural_officer_system_prompt import system_prompt
from flask import Request

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger("culture_officer")


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
        "max_tokens": config.openai_max_tokens,
        "temperature": config.openai_temperature,
        "top_p": config.openai_top_p,
    }
    logger.info("Sending request to OpenAI API...")
    response = requests.post(api_url, headers=headers, json=data, timeout=180)
    response.raise_for_status()
    result = response.json()
    logger.info("Received response from OpenAI API.")
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
    user_prompt = os.getenv(
        "CULTURE_OFFICER_USER_PROMPT", "What's new in the world of culture this week?"
    )
    logger.info("Calling GPT with system prompt and user prompt.")
    gpt_result = call_gpt(system_prompt, user_prompt, config)
    subject = "Culture Officer Report"
    html_body = parse_and_format_culture_html(gpt_result)
    if config.debug:
        debug_path = os.path.join(
            os.path.dirname(__file__), "culture_officer_debug.txt"
        )
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(gpt_result)
        logger.info("Debug mode: GPT output saved to %s", debug_path)
    status_code, response_json = send_email(subject, html_body, config)
    logger.info("Handler completed. Status: %s", status_code)
    return {"statusCode": status_code, "body": response_json, "log": gpt_result}
