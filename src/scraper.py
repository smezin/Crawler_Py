from asyncio.log import logger
import json
from tkinter.messagebox import NO
from urllib.request import urlopen
from typing import Dict, List
from helpers.message_wrapper import delete_messages, receive_messages
from consts import SQS_NAME
from helpers.notifications_wrapper import SnsWrapper
from helpers.queue_wrapper import get_queue
from lxml.html import parse

def scrape(queue_name: str) -> List[Dict]:
    """
    poping a pack of messages from queue and processing it
    """
    queue = get_queue(queue_name)
    if queue is None:
        logger.info(f'queue named <{queue_name}> was not found')
        return
    #notifier = SnsWrapper()
    messages_body = []
    messages = receive_messages(queue, 2, 0)
    while messages:
        messages_body = [json.loads(message.body) for message in messages]
        #Logic thingies here
        for message in messages_body:
            message['title'] = extract_title(message['my_url'])
        print(message)
        #Logic ended
        delete_messages(queue, messages)
        messages = receive_messages(queue, 2, 0)
    
    return messages_body

def extract_title (page_url: str) -> str:
    page = urlopen(page_url)
    parsed_page = parse(page)
    return parsed_page.find('.//title').text
    

scrape(SQS_NAME)