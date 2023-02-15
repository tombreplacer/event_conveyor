def deserialize_event(event: object):
    pass

def get_event_as_dict1():
    result = {
        "event_type": "NEW_MESSAGE_RECEIVED",
        "scope": {
            "scope_type": "ROOM",
            "target_id": "123"
        },
        "message": {
            "id": "333",
            "text": "text-text-text"
        }
    }
    return result

def get_event_as_dict2():
    result = {
        "event_type": "USER_STARTED_TYPING",
        "scope": {
            "scope_type": "ROOM",
            "target_id": "123"
        }
    }
    return result

def get_event_as_dict3():
    result = {
        "event_type": "USER_FINISHED_TYPING",
        "scope": {
            "scope_type": "ROOM",
            "target_id": "123"
        }
    }
    return result


def get_event_as_dict4():
    result = {
        "event_type": "WORLD_COLLAPSED",
        "scope": {
            "scope_type": "SYSTEM",
            "target_id": None
        }
    }
    return result

def get_event_as_dict_bad():
    result = {
        "hello": "WORLD",
    }
    return result



def get_event_as_dict6():
    result = {
        "event_type": "ZALUPA",
        "scope": {
            "scope_type": "ROOM",
            "target_id": "123"
        },
        "message": {
            "id": "333",
            "text": "text-text-text"
        }
    }
    return result





# @staticmethod
# def handler(group:str=None,order = 0,entity_type:type=None,payload_type:type=None):
#     def decorator_func(handler):
#         Conveyor.register_handler(handler=handler,group=group,order=order,entity_type=entity_type,payload_type=payload_type)
#         return handler
#     return decorator_func
