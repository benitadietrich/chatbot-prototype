# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# from typing import Text, List, Any, Dict

# from rasa_sdk import Tracker, FormAction
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.types import DomainDict


# class PersonalityForm(FormAction):
#     def name(self) -> Text:
#         return "personality_form"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""

#         return ["criticalThinking"]

#     def submit(self, tracker: Tracker, dispatcher: CollectingDispatcher,):
#         """Define what the form has to do
#             	after all required slots are filled"""

#        	dispatcher.utter_template('utter_submit', tracker)
#         return []

#     def slot_mappings(self):
#         """A dictionary to map required slots to
#         - an extracted entity
#         - intent: value pairs
#         - a whole message or a list of them, where a first
#                                  match will be picked"""

#         return { "criticalThinking": [
#                       self.from_intent(intent='critical_good',
#                                                  value="good"),
#                       self.from_intent(intent='critical_bad',
#                                                  value="bad")]}

    # def validate_criticalThinking(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     """Validate critical thinking value."""

    #     required_slots = ["criticalThinking"]
    #     intent = tracker.latest_message.get("intent", {}).get("name")

    #     if intent == "intent_good"  :
    #         return {"criticalThinking": "good"}
    #     else:
    #         # validation failed, set this slot to None so that the
    #         # user will be asked for the slot again
    #         return {"criticalThinking": None}
