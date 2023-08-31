import os
import openai
import urllib.request
import cv2


openai.api_key = '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'


def get_gpt(prompt):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response['choices'][0]['message']['content']

