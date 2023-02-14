from event_conveyor import AbstractEvent, EventConveyor, EventType, Scope
from payload_types import Message

@EventConveyor.event
class NewMessageEvent(AbstractEvent):
    event_type = EventType.NEW_MESSAGE_RECEIVED
    scope: Scope
    message: Message

@EventConveyor.event
class UserStartedTypingEvent(AbstractEvent):
    event_type = EventType.USER_STARTED_TYPING
    scope: Scope

@EventConveyor.event
class UserStartedTypingEvent(AbstractEvent):
    event_type = EventType.USER_FINISHED_TYPING
    scope: Scope


@EventConveyor.handler
def new_message_handler(event: NewMessageEvent):
    print("new_message_handler")
    return 'ok'


# @EventConveyor.handler
# def user_started_typing(event: UserStartedTypingEvent):
#     print("user_started_typing")
#     return 'ok'

# @EventConveyor.handler
# def user_started_typing(event: WorldCollapsedEvent):
#     print("WORLD COLLAPSED")
#     return 'ok'