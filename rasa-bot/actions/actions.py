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

            if intent == "accept" and not name_of_slot == "ratgeber" and not name_of_slot == "einstieg":
                dispatcher.utter_message(response="utter_"+name_of_slot+"_good")
                return {"result": currentResult-1}
            else:
                dispatcher.utter_message(
                    response="utter_"+name_of_slot+"_bad")
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
            "Du hast " + str(result)+" von 10 Punkten erreicht")

        if result >= 7:
            message = "Du scheinst viele Fähigkeiten zu besitzen die für ein duales Studium wichtig sind, ein Duales Studium scheint für dich geeignet zu sein."
            quality = "good"
        elif result < 7 and result >= 5:
            message = "Du besitzt schon einige Fähigkeiten zu besitzen, die es für ein duales Studium braucht. Allerdings gibt es auch einige Themenbereiche, bei denen du dich verbessern könntest."
            quality = "medium"
        else:
            message = "Dein Ergebnis scheint etwas kontrovers zu sein, vielleicht ist eine andere Form des Studiums für dich eher geeignet. Wenn du möchtest, kannst du gerne ein persönliches Gespräch vereinbaren um mehr zu erfahren"
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

        try:
            attribute
        except NameError:
            print("not defined")
        else:
            dispatcher.utter_message(response=(data[object_type]['template']))
            return[]


class MyKnowledgeBaseAction(ActionQueryKnowledgeBase):

    def __init__(self):
        knowledge_base = InMemoryKnowledgeBase(".\data.json")
        super().__init__(knowledge_base)

    async def utter_objects(
        self,
        dispatcher: CollectingDispatcher,
        object_type: Text,
        objects: List[Dict[Text, Any]],
    ) -> None:
        """
        Utters a response to the user that lists all found objects.

        Args:
            dispatcher: the dispatcherter
            object_type: the object type
            objects: the list of objects
        """
        if objects:

            repr_function = await self.knowledge_base.get_representation_function_of_object(
                object_type
            )

            if object_type == "studiengang":
                message = ""

                for i, obj in enumerate(objects, 1):
                    if i < len(objects)-1:
                        message = message + repr_function(obj)
                    else:
                        message = message + repr_function(obj) + ", "

                dispatcher.utter_message(
                    response="utter_inform", inform=message)
        else:
            dispatcher.utter_message(
                text=f"ich konnte keine Informationen zu '{object_type}' finden."
            )
