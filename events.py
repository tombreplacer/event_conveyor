# from abc import ABC, abstractmethod
# from enum import Enum

# from pydantic import BaseModel

# from payload_Types import Message

# class EventType(str, Enum):
#     USER_STARTED_TYPING = "USER_STARTED_TYPING"
#     USER_FINISHED_TYPING = "USER_FINISHED_TYPING"
#     NEW_MESSAGE_RECEIVED = "NEW_MESSAGE_RECEIVED"
#     WORLD_COLLAPSED = "WORLD_COLLAPSED"

# class ScopeType(str, Enum):
#     SYSTEMWIDE = "SYSTEMWIDE"
#     ROOM = "ROOM"


# class Scope(BaseModel):
#     scope_type: ScopeType
#     target_id: str | None
#     current_user_id: str | None


# class AbstractEvent(ABC, BaseModel):
#     event_type: EventType
#     scope: Scope
    
# # @event
# class NewMessageEvent(AbstractEvent):
#     event_type = EventType.NEW_MESSAGE_RECEIVED
#     scope: Scope
#     message: Message
# # @event
# class UserStartedTypingEvent(AbstractEvent):
#     event_type = EventType.USER_STARTED_TYPING
#     scope: Scope

# # @event
# class UserStartedTypingEvent(AbstractEvent):
#     event_type = EventType.USER_FINISHED_TYPING
#     scope: Scope

# # @event
# class WorldCollapsedEvent(AbstractEvent):
#     event_type = EventType.USER_FINISHED_TYPING
#     scope: Scope


# event_types = {
#     EventType.NEW_MESSAGE_RECEIVED: NewMessageEvent,
#     EventType.USER_STARTED_TYPING: UserStartedTypingEvent,
#     EventType.WORLD_COLLAPSED: WorldCollapsedEvent,
# }

# def deserialize_event(event: dict, user_id: str = None) -> AbstractEvent:
#     if not 'event_type' in event:
#        raise Exception(f"Provided object is not an event") 
#     deserializer = event_types[event["event_type"]]
#     if not deserializer:
#        raise Exception(f"No handler for event of type {event['event_type']}")
#     result: AbstractEvent = deserializer.parse_obj(event)
#     result.scope.current_user_id = user_id
#     return result