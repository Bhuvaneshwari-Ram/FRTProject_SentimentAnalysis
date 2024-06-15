import os
import requests
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            text = req_body.get('text')

    if text:
        sentiment = analyze_sentiment(text)
        return func.HttpResponse(json.dumps({"sentiment": sentiment}), mimetype="application/json")
    else:
        return func.HttpResponse(
            "Please pass text on the query string or in the request body",
            status_code=400
        )


def analyze_sentiment(text):
    subscription_key = os.getenv("TEXT_ANALYTICS_KEY")
    endpoint = os.getenv("TEXT_ANALYTICS_ENDPOINT")

    sentiment_url = f"{endpoint}/text/analytics/v3.0/sentiment"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    documents = {"documents": [{"id": "1", "text": text}]}
    response = requests.post(sentiment_url, headers=headers, json=documents)

    if response.status_code == 200:
        sentiments = response.json()
        return sentiments["documents"][0]["sentiment"]
    else:
        return "Error"
