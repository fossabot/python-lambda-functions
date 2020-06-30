import json
import logging
import os
import jsonpickle
import json
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.sqlalchemy.query import XRaySessionMaker
from aws_xray_sdk.core import patch_all
from crud.model import Item, Submission
from crud import operations


def obj_dict(obj):
    return obj.__dict__


def create_item(event, context):
    """Creates a new item.

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: application/json

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    
    print(event)
    
    # Parse event dict (= http post payload) to Item object
    item = Item()
    json_event = event['body']
    for key in json_event:
        setattr(item, key, json_event[key])

    try:
        item = operations.create_item_db(item)
        item_serialized = {"id": item.id, "content": item.content, "status": item.status}
        return {
            "statusCode": 201,
            "body": item_serialized
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Could not create item. Check HTTP POST payload. Exception: {}".format(e)
        }


def update_item(event, context):
    """updates an existing item.

    Parameters
    ----------
    event: dict, required
        contains item

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: application/json

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    print(event)

    # Parse event dict (= http post payload) to Item object
    item = Item()
    json_event = event['body']
    for key in json_event:
        setattr(item, key, json_event[key])

    try:
        item = operations.update_item_db(item)
        item_serialized = {"id": item.id, "content": item.content, "status": item.status, "language": item.language}
        return {
            "statusCode": 201,
            "body": item_serialized
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Could not update item. Exception: {}".format(e)
        }


def get_all_items(event, context):
    """Gets all items.

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: application/json

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # X-Ray Tracing
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    patch_all()

    logger.info('Database access for item retrieval.')

    # New x-ray segment
    segment1 = xray_recorder.begin_subsegment('database-access')

    try:

        xray_recorder.put_annotation('point1', 'Getting items...')

        # Get all items as a list of Item objects
        items = operations.get_all_items_db()

        xray_recorder.put_annotation('point2', 'Retrieved items.')

        xray_recorder.end_subsegment()

        # Prepare response payload (list of serialized items)
        # TODO automatically serialize / dump objects (json.dumps cannot serialize custom classes like Item)
        items_serialized = []
        for item in items:
            items_serialized.append({"content": item.content, "language": item.language})

        return {
            "statusCode": 200,
            'headers': {"content-type": "application/json; charset=utf-8"},
            "body": items_serialized
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Could not get items. Check HTTP GET payload. Exception: {}".format(e)
        }


def create_submission(event, context):

    submission = Submission()

    json_event = event['body']
    for key in json_event:
        setattr(submission, key, json_event[key])

    try:
        operations.create_submission_db(submission)
        return {
            "statusCode": 201,
            "body": "Submission created successfully"
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Could not create submission. Check HTTP POST payload. Exception: {}".format(e)
        }


def get_all_submissions(event, context):

    try:
        submissions = operations.get_all_submissions_db()
        submissions_serialized = []

        for submission in submissions:
            submissions_serialized.append({"item_id": submission.item_id, "submission_date":submission.submission_date,
                                           "received_date":submission.received_date, "phone":submission.phone, "mail":submission.mail,
                                           "source":submission.source, "frequency":submission.frequency})
        return {
            "statusCode": 200,
            'headers': {"content-type": "application/json; charset=utf-8"},
            "body": submissions_serialized
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Could not get submissions. Check HTTP GET payload. Exception: {}".format(e)
        }


def get_item_by_content(event, context):

    try:
        json_event = event['body']
        content = json_event.get('content')
        try:
            item = operations.get_item_by_content_db(content)
            item_serialized = {"id": item.id, "content": item.content, "language": item.language}
            return {
                "statusCode": 200,
                'headers': {"content-type": "application/json; charset=utf-8"},
                "body": item_serialized
            }
        except Exception:
            return {
                "statusCode": 404,
                "body": "No item found with the specified content."
            }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": "Could not get item. Check HTTP GET payload. Exception: {}".format(e)
        }
