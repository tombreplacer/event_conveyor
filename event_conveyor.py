from abc import ABC
from enum import Enum
from functools import wraps

from pydantic import BaseModel

__handlers__ = []
__events__ = []

class EventType(str, Enum):
    USER_STARTED_TYPING = "USER_STARTED_TYPING"
    USER_FINISHED_TYPING = "USER_FINISHED_TYPING"
    NEW_MESSAGE_RECEIVED = "NEW_MESSAGE_RECEIVED"
    WORLD_COLLAPSED = "WORLD_COLLAPSED"

class ScopeType(str, Enum):
    SYSTEMWIDE = "SYSTEMWIDE"
    ROOM = "ROOM"

class Scope(BaseModel):
    scope_type: ScopeType
    target_id: str | None

class AbstractEvent(ABC, BaseModel):
    event_type: EventType
    scope: Scope

class EventConveyor:
    def process(self, entity:object) -> dict:
        is_self = isinstance(self,EventConveyor)
        self1 = self if is_self else EventConveyor
        entity1 = entity if is_self else self

        resp_dict = {}
        for handler in EventConveyor.find_handlers(entity1):
            resp = (self1.class_handler_manager(handler["handler"]).process if handler["isclass"] else handler["handler"])(entity1) if \
                 handler["payload_type"] else \
                      (self1.class_handler_manager(handler["handler"]).process if handler["isclass"] else handler["handler"])(entity1)

            resp_dict[handler["handler"].__name__] = resp
        return resp_dict

    @staticmethod
    def handler(order = 0,entity_type:type=None):
        def decorator_func(handler):
            # EventConveyor.register_handler(handler=handler,order=order,entity_type=entity_type)
            return handler
        return decorator_func

    @staticmethod
    def event(msg='default'):
        def decorator(klass):
            old_foo = klass.foo
            @wraps(klass.foo)
            def decorated_foo(self, *args ,**kwargs):
                print('@decorator pre %s' % msg)
                old_foo(self, *args, **kwargs)
                print('@decorator post %s' % msg)
            klass.foo = decorated_foo
            return klass
        return decorator
    
    @staticmethod
    def deserealize_event(msg='default') -> AbstractEvent:
        def decorator(klass):
            old_foo = klass.foo
            @wraps(klass.foo)
            def decorated_foo(self, *args ,**kwargs):
                print('@decorator pre %s' % msg)
                old_foo(self, *args, **kwargs)
                print('@decorator post %s' % msg)
            klass.foo = decorated_foo
            return klass
        return decorator
    

    @staticmethod
    def register_handler(handler,group:str=None,order = 0,entity_type:type=None,payload_type:type=None):
        """
        Append handler method
        Args:
            handler (`function` or `class`): Handler type.
            group (`str`, optional): Grouping name to split handlers of same entity and payload to manage starting cases.
            entity_type (`type`, optional): base or concrete class of entity.
            payload_type (`type`, optional): base or concrete class of payload.
        """

        handler_func = None
        is_class = False
        if not inspect.isfunction(handler):
            if(hasattr( handler, 'process' ) and callable( handler.process )):
                handler_func = handler.process
                is_class=True
            else:
                raise ValueError("Handler must be a function or a class that contains 'process' method. {function}".format(function = handler))
        else:
            handler_func=handler
        sign = inspect.signature(handler_func)
        items = list(sign.parameters)
        
        if is_class:
            items.remove(items[0])
        params_len = items.__len__()

        if params_len<1:
            raise ValueError("Handler process method must contains minimum 1 argument: entity object, payload object (optional). Handler: {function}".format(function = handler))

        entity_type = entity_type or sign.parameters.get(items[0]).annotation if sign.parameters.get(items[0]).annotation != sign.parameters.get(items[0]).empty else None

        if not entity_type:
            raise ValueError("Type of entity in handler method must be specified. handler: {function}".format(function = handler))

        payload_type = payload_type or sign.parameters.get(items[1]).annotation if params_len > 1 and sign.parameters.get(items[1]).annotation != sign.parameters.get(items[1]).empty else None

        if params_len>1 and not payload_type:
            raise ValueError("If your handler has payload, his type must be specified. Handler: {function}, payload: {payload}".format(function = handler,payload=payload_type))

        if not any(x["handler"]==handler and x["entity_type"]==entity_type and x["payload_type"]==payload_type and x["group"]==group for x in __handlers__):
            __handlers__.append({"handler":handler,"iscoroutine":inspect.iscoroutinefunction(handler),"isclass":inspect.isclass(handler),"entity_type":entity_type,"payload_type":payload_type,"group":group,"order":order})




class EventBus:
    conveyor = EventConveyor()

    def put(self, event: AbstractEvent):
        self.conveyor.process(event)
