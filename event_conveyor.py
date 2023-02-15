from abc import ABC
from enum import Enum, IntEnum
from functools import wraps
import inspect
from pydantic import BaseModel

__handlers__ = []
__events__ = {}

class EventType(str, Enum):
    pass
    # USER_STARTED_TYPING = "USER_STARTED_TYPING"
    # USER_FINISHED_TYPING = "USER_FINISHED_TYPING"
    # NEW_MESSAGE_RECEIVED = "NEW_MESSAGE_RECEIVED"
    # WORLD_COLLAPSED = "WORLD_COLLAPSED"

class ScopeType(str, Enum):
    SYSTEMWIDE = "SYSTEMWIDE"
    ROOM = "ROOM"

class Scope(BaseModel):
    scope_type: ScopeType
    target_id: str | None

class AbstractEvent(BaseModel):
    event_type: str
    scope: Scope

class EventConveyor:
    @staticmethod
    def process(event: AbstractEvent) -> dict:
        results = {}
        for handler in EventConveyor.find_handlers(event):
            result = handler["handler_func"](event)
            results[handler["handler_func"].__name__] = result
        return results

    @staticmethod
    def event(cls:type):
        if not issubclass(cls, AbstractEvent):
            raise Exception("Provided object is not an event")
        EventConveyor.register_event(cls)
        print('@event registered "%s"' % cls.__name__)
        return cls
    
    @staticmethod
    def register_event(cls: type):
        key = cls.__fields__["event_type"].default
        if key in __events__:
            raise Exception("Only one event class per event type is allowed. %s already used in %s" % (key, __events__[key].__name__))
        else:
            __events__[key] = cls

    @staticmethod
    def deserealize_event(event: dict) -> AbstractEvent:
        if not "event_type" in event:
            raise Exception("Provided object is not an event because missing field 'event_type'")
        key = event["event_type"] 
        if not key in __events__:
            raise Exception("Event of type %s is not registered make sure you have declared subclass of AbstractEvent and decorated it with @EventConveyor.event", key)
        deserealizer = __events__[key]
        result = deserealizer.parse_obj(event)
        return result


    @staticmethod
    def handler(order = 0):
        def decorator(handler_func):
            EventConveyor.register_handler(handler_func, order)
            print('@handler registered "%s"' % handler_func.__name__)
            def decorator_func(handler):
                return handler
        return decorator


    @staticmethod
    def register_handler(handler_func,order = 0):
        if not inspect.isfunction:
            raise Exception("Handler should be a function")
        # if not issubclass(event_type, AbstractEvent):
        #     raise Exception("Handler event_type argument should")
        signature = inspect.signature(handler_func)
        params = list(signature.parameters)
        params_len = signature.parameters.__len__()

        if params_len<1:
            raise Exception("Handler function must contain minimum 1 argument: event object. Handler: %s" % handler_func)

        event_class = signature.parameters.get(params[0]).annotation if signature.parameters.get(params[0]).annotation != signature.parameters.get(params[0]).empty else None

        if not event_class:
            raise Exception("Type of entity in handler method must be specified. handler: %s" % handler_func)
      
        __handlers__.append({"handler_func":handler_func,"event_class":event_class,"order":order})


    @staticmethod
    def find_handlers(event: AbstractEvent):
        results = []
        event_class = event.__class__
        for handler in __handlers__:
            if(handler["event_class"] == event_class):
                results.append(handler)
        results.sort(key=lambda x:x["order"])
        return results

class EventBus:
    conveyor = EventConveyor()

    def put(self, event: AbstractEvent):
        self.conveyor.process(event)
