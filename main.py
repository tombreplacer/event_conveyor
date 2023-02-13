from event_conveyor import EventConveyor, EventBus
# from eventbus import EventBus
# from events import NewMessageEvent, deserialize_event
import handlers
import misc

bus = EventBus()


# event1 = misc.get_event_as_dict1()
# event2 = misc.get_event_as_dict2()
# event3 = misc.get_event_as_dict2()
# event4 = misc.get_event_as_dict2()
event5 = misc.get_event_as_dict1()
# event3 = misc.get_event_as_dict3()
# event4 = misc.get_event_as_dict_bad()

# event1_obj = deserialize_event(event1, "user_id")


# event2_obj = deserialize_event(event2)
# event3_obj = deserialize_event(event3)
# event4_obj = deserialize_event(event4)

event5_obj = EventConveyor.deserealize_event(event5)
# event3_obj = deserialize_event(event3)
# event4_obj = deserialize_event(event4)

# bus.put(event1_obj)
# bus.put(event2_obj)
# bus.put(event3_obj)
bus.put(event5_obj)
# bus.process(event3_obj)
# bus.process(event4_obj)