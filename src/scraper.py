from asyncio.log import logger
import json
from msilib.schema import Error
from urllib.request import urlopen
from typing import Dict, List
from helpers.message_wrapper import delete_messages, receive_messages
from consts import SNS_NAME, SQS_NAME
from helpers.notifications_wrapper import SnsWrapper
from helpers.queue_wrapper import get_queue
from lxml.html import parse

def scrape(queue_name: str) -> List[Dict]:
    """
    poping a pack of messages from queue and processing it
    """
    try:
        queue = get_queue(queue_name)
        if queue is None:
            logger.info(f'queue named <{queue_name}> was not found')
            return

        sns_object = SnsWrapper()
        list_topics = sns_object.list_topics()
        for topic_name in list_topics:
            if SNS_NAME in str(topic_name):
                topic = topic_name
        
        messages_body = []
        messages = receive_messages(queue, 2, 0)
        while messages:
            messages_body = [json.loads(message.body) for message in messages]
            #Logic thingies here
            for message in messages_body:
                message['title'] = extract_title(message['my_url'])
                sns_object.publish_message(topic, json.dumps(message), {})
                print(message)

            #Logic ended
            delete_messages(queue, messages)
            messages = receive_messages(queue, 2, 0)
    except Exception as ex:
        logger.exception(f'scrape method failed: {ex}')
        raise Error
    else:
        return messages_body

def extract_title (page_url: str) -> str:
    page = urlopen(page_url)
    parsed_page = parse(page)
    return parsed_page.find('.//title').text
    

scrape(SQS_NAME)