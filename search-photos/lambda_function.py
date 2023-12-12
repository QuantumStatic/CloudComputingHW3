import json
import boto3
import urllib.parse
import requests

lex_runtime = boto3.client('lexv2-runtime', region_name='us-east-1', aws_access_key_id='AKIAZ6CDUAO4OVQ7RBHF', aws_secret_access_key="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")

botId = "VLZEHAU8SM"
botAliasId = "TSTALIASID"
localeId = "en_US"
sessionId = "69"

def extract_query(event):
    try:
        query = event['queryStringParameters']['q']
    except TypeError:
        return ""
    else:
        return query
    
    # return "cat and dog

def search_index(query:str):
    es_host='search-photos-swywglfely7rbgh5hv5567ouo4.us-east-1.es.amazonaws.com'
    region = 'us-east-1'
    service = 'es'
    
    access_id = 'quantumstatic'
    access_secret = 'cavhom-3josgi-qucBuw'

    headers = {
        "Content-Type": "application/json"
    }
    url = f"https://{es_host}/photos/_search?q={query}&pretty=true"
    
    response = requests.get(url, auth=(access_id, access_secret), headers=headers)
    # response = requests.get(url, auth=auth, headers=headers)
    hits = json.loads(response.content)['hits']['hits']

    return tuple(map(lambda hit: hit['_source']["objectKey"], hits))

def lambda_handler(event, context):
    print(event)
    print(context)
    
    query = extract_query(event)
    
    image_links = []
    
    if query:
    
        bot_response = get_bot_resonse(query)
        
        bot_response = clean_response(bot_response)
        
        print(f"bot:{bot_response}")
        
        es_search_query = " OR ".join(bot_response)
        
        es_search_query = urllib.parse.quote(es_search_query)
        
        print(es_search_query)
        
        search_results = search_index(es_search_query)
        
        image_links = [f"https://assbucket2.s3.amazonaws.com/{img}" for img in search_results]
        
        print(image_links)
    
    return {
        'statusCode': 200,
        'body': json.dumps(image_links)
    }
    
def get_bot_resonse(user_input:str) -> str:
    response = lex_runtime.recognize_text (
        botId=botId,
        botAliasId=botAliasId,
        localeId=localeId, 
        sessionId=sessionId, 
        text=user_input
    )
    return response['messages'][0]["content"]
    
def clean_response(bot_response:str):
    bot_response = tuple(map(lambda x: x.lstrip("and") if x.startswith('and') else x, bot_response.strip().split()))
    return bot_response