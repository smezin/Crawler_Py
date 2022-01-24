import json
import uuid
from typing import Dict, List
from markupsafe import string
from helpers.message_wrapper import delete_messages, receive_messages, delete_message
from consts import SQS_NAME
from helpers.queue_wrapper import get_queue
from models.url_scrape import UrlScrapeModel

def scrape() :
    """
    poping a pack of messages from queue and processing it
    """
    queue = get_queue(SQS_NAME)
    dict_ = {}
    messages = receive_messages(queue, 2, 0)
    messages_body = [json.loads(message.body) for message in messages]
  
    #Do my logic here
    #print('{}"\n"'.format(messages_body))
    delete_messages(queue, messages)
   
    return messages_body

def printit(scrapeModel: UrlScrapeModel):
    print(type(scrapeModel))
    print(scrapeModel.my_url)
    

print(scrape())