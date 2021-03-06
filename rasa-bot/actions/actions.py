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


from typing import Text, List, Any, Dict

import requests
import json
import typing
from typing import Text, Dict, List, Any

from rasa_sdk.knowledge_base.utils import (
    SLOT_OBJECT_TYPE,
    SLOT_LAST_OBJECT_TYPE,
    SLOT_ATTRIBUTE,
    reset_attribute_slots,
    SLOT_MENTION,
    SLOT_LAST_OBJECT,
    SLOT_LISTED_OBJECTS,
    get_object_name,
    get_attribute_slots,
)
from rasa_sdk import utils
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.knowledge_base.storage import KnowledgeBase

if typing.TYPE_CHECKING:  # pragma: no cover
    from rasa_sdk.types import DomainDict
from rasa_sdk import utils
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase


class ValidateGeneralForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_general_form"

    # def validate_thinking(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     """Validate thinking value."""
    #     intent = tracker.latest_message['intent'].get('name')
    #     SlotSet("context","critical")
    #     currentResult = tracker.get_slot('result')
    #     dispatcher.utter_message(template="utter_critical")

    #     if intent == "critical_bad":
    #         dispatcher.utter_message(template="utter_critical_bad")
    #         return {"result": currentResult-1}
    #     else:
    #         # validation failed, set this slot to None so that the
    #         # user will be asked for the slot again
    #         dispatcher.utter_message(template="utter_critical_good")
    #         return {"result": currentResult+1}

    def create_validation_function(name_of_slot):
        """Function generate our validation functions, since
        they're pretty much the same for each slot"""

        def validate_slot(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
            """Validate thinking value."""
            intent = tracker.latest_message['intent'].get('name')
            currentResult = tracker.get_slot('result')

            if intent == "affirm" and (not name_of_slot == "ratgeber" or not name_of_slot == "einstieg"):
                dispatcher.utter_message(
                    response="utter_"+name_of_slot+"_bad")
                return {"result": currentResult}
            else:
                dispatcher.utter_message(
                    response="utter_"+name_of_slot+"_good")
                return {"result": currentResult+1}

        return validate_slot

    validate_grades = create_validation_function(name_of_slot="grades")
    validate_ratgeber = create_validation_function(name_of_slot="ratgeber")
    validate_einstieg = create_validation_function(name_of_slot="einstieg")
    validate_exams = create_validation_function(name_of_slot="exams")
    validate_wissenschaftlich = create_validation_function(
        name_of_slot="wissenschaftlich")
    validate_theory = create_validation_function(name_of_slot="theory")


class ActionResult(Action):

    def name(self) -> Text:
        return "action_result"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        result = tracker.get_slot('result')
        message = ""
        quality = ""

        dispatcher.utter_message(
            "Du hast " + str(result)+" von 6 Punkten erreicht")

        if result >= 5:
            message = "Du scheinst viele F??higkeiten zu besitzen die f??r ein duales Studium wichtig sind, ein Duales Studium scheint f??r dich geeignet zu sein."
            quality = "good"
        elif result < 5 and result >= 3:
            message = "Du besitzt schon einige F??higkeiten zu besitzen, die es f??r ein duales Studium braucht. Allerdings gibt es auch einige Themenbereiche, bei denen du dich verbessern k??nntest."
            quality = "medium"
        else:
            message = "Dein Ergebnis scheint etwas kontrovers zu sein, vielleicht ist eine andere Form des Studiums f??r dich eher geeignet. Wenn du m??chtest, kannst du gerne ein pers??nliches Gespr??ch vereinbaren um mehr zu erfahren"
            quality = "bad"

        dispatcher.utter_message(message)

        return {quality: quality}


class ActionAsk(Action):

    def name(self) -> Text:
        return "action_ask"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        context = tracker.get_slot('requested_slot')
        dispatcher.utter_message(response="utter_"+context)
        return[]

class ActionAskResult(Action):

    def name(self) -> Text:
        return "action_ask_result"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        slot = tracker.get_slot('quality')

        dispatcher.utter_message(response="utter_result_"+slot)
        return[]


class ActionResetAllSlots(Action):

    def name(self) -> Text:
        return "action_reset_all_slots"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:


        return[SlotSet("grades",None),SlotSet("ratgeber", None), SlotSet("exams", None), SlotSet("einstieg", None), SlotSet("theory", None), SlotSet("wissenschaftlich",None), SlotSet("result", 0)] 

class ActionWannaStudy(Action):

    def name(self) -> Text:
        return "action_wanna_study"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        studiengang = tracker.get_slot('object_type')

        if studiengang is None:
            dispatcher.utter_message(response="utter_ask_studiengang")
        else:
            dispatcher.utter_message(response="utter_"+studiengang.lower())

        return[]

class ActionSearchDatabase(Action):

    def name(self) -> Text:
        return "action_search_database"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        response = requests.get("https://db.benita-dietrich.de/api")
        data = response.json()

        object_type = tracker.get_slot('object_type')
        attribute = tracker.get_slot('attribute')
        specific_info = tracker.get_slot('specific_info')

        try:
            data[object_type]['template']
        except KeyError:
            if not object_type == "studiengang" and not attribute is None:
                if specific_info is None:
                    li = [str(item) for item in data[object_type][attribute]]
                    dispatcher.utter_message(
                        response="utter_"+object_type+"_"+attribute, values=' '.join(li))
                else:
                    li = [str(item) for item in data[object_type][attribute]]
                    print("checking li", li)
                    if specific_info in li:
                        dispatcher.utter_message(response="utter_affirm")
                    else:
                        dispatcher.utter_message(response="utter_decline")
        except TypeError:
            if attribute is None:
                li = [item.get('id') for item in data[object_type]]
                print(li)
                dispatcher.utter_message(
                    response="utter_studiengang", values=' '.join(li))
            elif not specific_info is None:
                r = data[object_type][attribute][specific_info]
                dispatcher.utter_message(
                    response="utter_studiengang_"+specific_info, info=attribute, values=r)
        else:
            dispatcher.utter_message(response=(data[object_type]['template']))

        return[SlotSet("attribute", None)]
