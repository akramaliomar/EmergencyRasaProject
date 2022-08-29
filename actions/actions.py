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
from actions.vital_sign_rest_api import fetch_vital_signs, fetch_aggr_signs, fetch_heath_status


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "validate_authentication_form"

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


class ActionCheckStatus(Action):
    def name(self) -> Text:
        return "check_heath_status_action"
    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(template="utter_health_status", health_status="dssddsdsds")
        prediction = fetch_heath_status()
        if len(prediction) > 0:
            output = prediction["msg"]
            dispatcher.utter_message(template="utter_health_status",
                                 health_status=str(output))
            if output==str("Abnormal"):
                vital_signs = fetch_vital_signs()
                tempr = vital_signs[0]["tempr"]
                resp = vital_signs[0]["resp"]
                hr = vital_signs[0]["hr"]
                spo2 = vital_signs[0]["spo2"]
                if tempr>=30:
                    dispatcher.utter_message(template="utter_exceed_tempr",
                                             tempr=str(tempr))
                elif tempr<=20:
                    dispatcher.utter_message(template="utter_less_tempr",
                                             tempr=str(tempr))

                if resp>=30:
                    dispatcher.utter_message(template="utter_exceed_resp",
                                             resp=str(resp))
                elif resp<=20:
                    dispatcher.utter_message(template="utter_less_resp",
                                             resp=str(resp))

                if hr>=30:
                    dispatcher.utter_message(template="utter_exceed_hr",
                                             hr=str(hr))
                elif hr<=20:
                    dispatcher.utter_message(template="utter_less_hr",
                                             hr=str(hr))
                if spo2>=90:
                    dispatcher.utter_message(template="utter_high_pressure",
                                             spo2=str(spo2))
                elif spo2<=60:
                    dispatcher.utter_message(template="utter_low_pressure",
                                             spo2=str(spo2))

        else:
            dispatcher.utter_message(template="utter_no_data", no_data="No data available")


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "validate_diagnosis_forms"

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
        vital_signs = fetch_vital_signs()
        vital_aggr_signs = fetch_aggr_signs()
        if len(vital_signs) > 0:
            tempr = str(vital_signs[0]["tempr"])
            resp = str(vital_signs[0]["resp"])
            hr = str(vital_signs[0]["hr"])
            spo2 = str(vital_signs[0]["spo2"])
        else:
            tempr = "No data"
            resp = "No data"
            hr = "No Data"
            spo2 = "No data"
        if tracker.get_slot('vital_signs') == "temperature":
            maxtempr = str(vital_aggr_signs[0]["maxtempr"])
            mintempr = str(vital_aggr_signs[0]["mintempr"])
            avgtempr = str(vital_aggr_signs[0]["avgtempr"])
            dispatcher.utter_message(template="utter_temperature", temperature=tempr, maxtempr=maxtempr,
                                     mintempr=mintempr, avgtempr=avgtempr)

        elif tracker.get_slot('vital_signs') == "heart":
            maxhr = str(vital_aggr_signs[0]["maxhr"])
            minhr = str(vital_aggr_signs[0]["minhr"])
            avghr = str(vital_aggr_signs[0]["avghr"])
            dispatcher.utter_message(template="utter_heart", heart=hr, maxhr=maxhr, minhr=minhr, avghr=avghr)

        elif tracker.get_slot('vital_signs') == "pressure":
            maxspo2 = str(vital_aggr_signs[0]["maxspo2"])
            minspo2 = str(vital_aggr_signs[0]["minspo2"])
            avgspo2 = str(vital_aggr_signs[0]["avgspo2"])
            dispatcher.utter_message(template="utter_pressure", pressure=spo2, maxspo2=maxspo2, minspo2=minspo2,
                                     avgspo2=avgspo2)

        elif tracker.get_slot('vital_signs') == "respiration":
            maxresp = str(vital_aggr_signs[0]["maxresp"])
            minresp = str(vital_aggr_signs[0]["minresp"])
            avgresp = str(vital_aggr_signs[0]["avgresp"])
            dispatcher.utter_message(template="utter_respiration", respiration=resp, maxresp=maxresp, minresp=minresp,
                                     avgresp=avgresp)

        elif tracker.get_slot('vital_signs') == "all":
            dispatcher.utter_message(template="utter_all",
                                     all="Temp: " + tempr + " Pressure: " + spo2 + " Heart rate: " + hr + " Respiration: " + resp)

        else:
            dispatcher.utter_message(template="utter_none",
                                     none="No vital sign selected")

        return [SlotSet("requested_slot", None)]
