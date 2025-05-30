import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nodes import pass_message, scheduler, call_action_action_router
message_status = "queued"

def test_pass_message():
    convo = [
        {"AI": "Hello"},
        {"caller": "Hi can you schedule a callback"},
        {"AI": "Sure when and what is your name"},
        {"caller": "My name is Timothy Wesley and tomorow at 9"},
        {"AI": "O it is schedules have a good day"},
    ]
    assert pass_message({"convo": convo}) == message_status
    
def test_scheduler():
    convo = [
        {"AI": "Hello"},
        {"caller": "Hi can you pass a message"},
        {"AI": "Sure"},
        {"caller": "My name is Timothy Wesley and i just want to tell Joh he has court tommorow"},
        {"AI": "Ok I will pass it along"},
    ]
    assert scheduler({"convo": convo, "caller_id": "7726210972"}) == message_status
    
def test_call_action_action_router():
    convo = [
        {"AI": "Hello"},
        {"caller": "I have court tomorow"},
        {"AI": "Would you like to schedule a callback? or pass a message?"},
        {"caller": "No"},
        {"AI": "OK goodbye"}
    ]
    result = call_action_action_router({"convo": convo})
    actions = ["schedule_callback", "pass_message", "nothing"]
    assert result in actions