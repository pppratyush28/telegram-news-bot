import os
from gnewsclient import gnewsclient
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud.dialogflow_v2.types import TextInput, QueryInput

# Set up Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"

# Dialogflow setup
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = 'newsbot-dyok'

# Detect intent
def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = TextInput(text=text, language_code=language_code)
    query_input = QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

# Get reply from Dialogflow
def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)
    if response.intent.display_name.lower() == "get_news":
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text

# Fetch news from GNewsClient
def fetch_news(parameters):
    print("[DEBUG] Parameters passed to fetch_news:", parameters)

    topic = parameters.get('topic', [])
    country = parameters.get('geo-country', [])
    language = parameters.get('language', [])

    client = gnewsclient.NewsClient()
    client.topic = topic[0] if topic else 'Top Stories'
    client.location = country[0] if country else 'India'
    client.language = language[0] if language else 'en'

    print("[DEBUG] Normalized inputs -> topic:", client.topic, "| location:", client.location, "| language:", client.language)

    news_items = client.get_news()
    print("[DEBUG] News fetched:", news_items)
    return news_items[:5]
