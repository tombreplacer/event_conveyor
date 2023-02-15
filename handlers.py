from enum import Enum
from event_conveyor import AbstractEvent, EventConveyor, EventType, Scope
from payload_types import Message


class EventType1(EventType, Enum):
    ZALUPA = "ZALUPA"
    USER_STARTED_TYPING = "USER_STARTED_TYPING"
    USER_FINISHED_TYPING = "USER_FINISHED_TYPING"
    NEW_MESSAGE_RECEIVED = "NEW_MESSAGE_RECEIVED"
    WORLD_COLLAPSED = "WORLD_COLLAPSED"


@EventConveyor.event
class ZalupaEvent(AbstractEvent):
    event_type = EventType1.ZALUPA
    scope: Scope
    message: Message


@EventConveyor.handler
def zalupa_handler(event: ZalupaEvent):
    print("zalupa_handler zalupa_handler")
    return 'ok'

@EventConveyor.event
class NewMessageEvent(AbstractEvent):
    event_type = EventType1.NEW_MESSAGE_RECEIVED
    scope: Scope
    message: Message


@EventConveyor.event
class UserStartedTypingEvent(AbstractEvent):
    event_type = EventType1.USER_STARTED_TYPING
    scope: Scope

@EventConveyor.event
class UserStartedTypingEvent(AbstractEvent):
    event_type = EventType1.USER_FINISHED_TYPING
    scope: Scope


@EventConveyor.handler(order=1)
def new_message_handler1(event: NewMessageEvent):
    print("new_message_handler success 1")
    print(event)
    return 'ok'

@EventConveyor.handler(order=-5)
def new_message_handler2(event: NewMessageEvent):
    print("new_message_handler success -5")
    return 'ok'

@EventConveyor.handler(order=50)
def new_message_handler2(event: NewMessageEvent):
    print("new_message_handler success 50")
    return 'ok'

# @EventConveyor.handler
# def user_started_typing(event: UserStartedTypingEvent):
#     print("user_started_typing")
#     return 'ok'

# @EventConveyor.handler
# def user_started_typing(event: WorldCollapsedEvent):
#     print("WORLD COLLAPSED")
#     return 'ok'