import json

def response_builder(event:dict, /, **kwargs:dict) -> dict:
    """
    This function has the sole responsibility to build the response to be sent back to Lex.
    Follows Single Responsibility Principle.
    """
    
    # Run if a problem was encountered while validating slots
    if kwargs.get('validate_slots_result', False):
        validate_slots_result = kwargs['validate_slots_result']
        if not validate_slots_result['slots_valid']:
            return {
                "sessionId": event['sessionId'],
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": validate_slots_result['invalid_slot'],
                        "message": {
                            "contentType": "PlainText",
                            "content": validate_slots_result['message']
                        }
                    },
                    "intent": event['sessionState']['intent'],
                    "sessionAttributes": event['sessionState']['sessionAttributes'],
                    "originatingRequestId": event['sessionState']['originatingRequestId']
                },
                "messages": [{
                            "contentType": "PlainText",
                            "content": validate_slots_result['message']
                        }]
            }

    # Runs if a confirmation is required
    elif kwargs.get('confirm_intent', False):
        info_package = kwargs['confirm_intent']
        return {
            "sessionId": event['sessionId'],
            "sessionState": {
                "dialogAction": info_package['dialogAction'],
                "intent": event['sessionState']['intent'],
                "sessionAttributes": event['sessionState']['sessionAttributes'],
                "originatingRequestId": event['sessionState']['originatingRequestId']
            },
            "messages": [info_package['dialogAction']['message']]
        }
    
    # Runs if we have reached fullfilment state
    elif kwargs.get('fulfillment_state', False):
        fulfillment_state = kwargs['fulfillment_state']
        event['sessionState']['intent']['state'] = "Fulfilled"
        return {
            "sessionId": event['sessionId'],
            "sessionState": {
                "dialogAction": fulfillment_state['dialogAction'],
                "intent": event['sessionState']['intent'],
                "sessionAttributes": event['sessionState']['sessionAttributes'],
                "originatingRequestId": event['sessionState']['originatingRequestId']
            },
            "messages": [
                fulfillment_state['dialogAction']['message'],
            ]
        }
    
    # Runs if there is no special requirement and we let Lex decide the next step.
    return {
        "sessionId": event['sessionId'],
        "sessionState": {
            "dialogAction": {
                "type": "Delegate"
            },
            "intent": event['sessionState']['intent'],
            "sessionAttributes": event['sessionState']['sessionAttributes'],
            "originatingRequestId": event['sessionState']['originatingRequestId']
        },
        "messages": None
    }

def get_subjects(event) -> list[str]:
    interpretations = event["interpretations"]
    search_intent_block = interpretations[0]
    slots:dict[str, dict] = search_intent_block["intent"]["slots"]
    
    for value in slots.values():
        if value is not None:
            yield value['value']['interpretedValue']
    

def SearchIntentHandler(event):
    currSubjects = ' '.join(get_subjects(event))
    print (currSubjects)
    response_info = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": currSubjects
            }
        }
    }
    return response_builder(event, fulfillment_state=response_info)

def FulfillmentCodeHookHandler(event):
    return response_builder(event)

def lambda_handler(event, context):
    print(event)
    response = response_builder(event)

    invocation_source = event['invocationSource']
    
    if invocation_source == 'DialogCodeHook':
        intent = event['sessionState']['intent']['name']
        if intent is not None:
            try:
                # This is a way to dynamically call a function
                # instead of using a bunch of if-else statements
                response = eval(f"{intent}Handler(event)")
            except NameError as error:
                print(error)
                print(traceback.format_exc())
                
    elif invocation_source == 'FulfillmentCodeHook':
        response = FulfillmentCodeHookHandler(event)
    
    print(response)
    return response