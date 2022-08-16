# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
# from actions.vital_sign_rest_api import fetch_vital_signs
# from actions.vital_sign_rest_api import weather_things_speak


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "authentication_form"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["auth_code"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_authentication_submit"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 code=tracker.get_slot("auth_code"))


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "diagnosis_forms"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["vital_signs"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_diagnosis_submit"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # vital_signs = fetch_vital_signs()
        #temp = weather_things_speak()['field1']
        vital_signs = [[12, 222, 444, 666, 666, 777]]
        if len(vital_signs) > 0:

            # tempr = str(temp)
            # resp = str(temp)
            # hr = str(temp)
            # spo2 = str(temp)
            tempr = str(vital_signs[0][5])
            resp = str(vital_signs[0][4])
            hr = str(vital_signs[0][2])
            spo2 = str(vital_signs[0][3])
        else:
            tempr = "No data"
            resp = "No data"
            hr = "No Data"
            spo2 = "No data"
        # dispatcher.utter_message(template="utter_vital_sign",
        #                          vital_sign=tracker.get_slot("vital_signs"))
        if tracker.get_slot('vital_signs') == "temperature":
            dispatcher.utter_message(template="utter_temperature",
                                     temperature=tempr)
        elif tracker.get_slot('vital_signs') == "heart":
            dispatcher.utter_message(template="utter_heart",
                                     heart=hr)

        elif tracker.get_slot('vital_signs') == "pressure":
            dispatcher.utter_message(template="utter_pressure",
                                     pressure=spo2)

        elif tracker.get_slot('vital_signs') == "respiration":
            dispatcher.utter_message(template="utter_respiration",
                                     respiration=resp)

        elif tracker.get_slot('vital_signs') == "all":
            dispatcher.utter_message(template="utter_all",
                                     all="temp: pressure: heart rate:respiration: ")

        else:
            dispatcher.utter_message(template="utter_none",
                                     none="No vital sign selected")

        return [SlotSet("requested_slot", None)]
