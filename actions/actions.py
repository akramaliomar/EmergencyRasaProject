# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# from rasa_sdk import tensorflow
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from actions.vital_sign_rest_api import fetch_vital_signs, fetch_aggr_signs, fetch_heath_status, prediction
# from actions.db import add_user, authenticate_user
from typing import Dict, Text, List, Optional, Any
from rasa_sdk.forms import FormValidationAction

#
# class ActionAddUser(Action):
#     def name(self) -> Text:
#         return "add_user_action"
#
#     def run(
#             self,
#             dispatcher,
#             tracker: Tracker,
#             domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#         # users = add_user("ali", 2345)
#         users = add_user("ali", 2345)
#         if users == "success":
#             dispatcher.utter_message(template="utter_user_success", user_name="user_name")
#         else:
#             dispatcher.utter_message(template="utter_user_fail", user_name="user_name")


class ValidateAuthenticationForm(Action):
    def name(self) -> Text:
        return "validate_authentication_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        required_slots = slots_mapped_in_domain + ["auth_name"]
        return required_slots

    async def extract_auth_name(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        text_of_last_user_message = tracker.latest_message.get("text")
        # sit_outside = "outdoor" in text_of_last_user_message

        return {"auth_name": text_of_last_user_message}


# class ValidateRestaurantForm(Action):
#     def name(self) -> Text:
#         return "validate_authentication_form"
#
#     def run(
#             self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[EventType]:
#         required_slots = ["auth_code"]
#
#         for slot_name in required_slots:
#             if tracker.slots.get(slot_name) is None:
#                 # The slot is not filled yet. Request the user to fill this slot next.
#                 return [SlotSet("requested_slot", slot_name)]
#
#         # All slots are filled.
#         return [SlotSet("requested_slot", None)]



class ActionCheckPrediction(Action):
    def name(self) -> Text:
        return "check_prediction_action"
    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(template="utter_prediction", prediction = prediction())


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_authentication_submit"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # ucount = authenticate_user(tracker.get_slot("auth_name"), tracker.get_slot("auth_code"))
        ucount = 1
        if ucount == 1:
            dispatcher.utter_message(template="utter_auth_success",
                                     auth_code=tracker.get_slot("auth_code"), uth_name=tracker.get_slot("auth_name"))
        else:
            dispatcher.utter_message(template="utter_auth_fail",
                                     auth_code=tracker.get_slot("auth_code"), auth_name=tracker.get_slot("auth_name"))
        # dispatcher.utter_message(template="utter_details_thanks",
        #                          code=tracker.get_slot("auth_code"))


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
            if output == str("Abnormal"):
                vital_signs = fetch_vital_signs()
                tempr = vital_signs[0]["tempr"]
                resp = vital_signs[0]["resp"]
                hr = vital_signs[0]["hr"]
                spo2 = vital_signs[0]["spo2"]
                if tempr >= 30:
                    dispatcher.utter_message(template="utter_exceed_tempr",
                                             tempr=str(tempr))
                elif tempr <= 20:
                    dispatcher.utter_message(template="utter_less_tempr",
                                             tempr=str(tempr))

                if resp >= 30:
                    dispatcher.utter_message(template="utter_exceed_resp",
                                             resp=str(resp))
                elif resp <= 20:
                    dispatcher.utter_message(template="utter_less_resp",
                                             resp=str(resp))

                if hr >= 30:
                    dispatcher.utter_message(template="utter_exceed_hr",
                                             hr=str(hr))
                elif hr <= 20:
                    dispatcher.utter_message(template="utter_less_hr",
                                             hr=str(hr))
                if spo2 >= 90:
                    dispatcher.utter_message(template="utter_high_pressure",
                                             spo2=str(spo2))
                elif spo2 <= 60:
                    dispatcher.utter_message(template="utter_low_pressure",
                                             spo2=str(spo2))

        else:
            dispatcher.utter_message(template="utter_no_data", no_data="No data available")


class ActionCheckAbnormalStatus(Action):
    def name(self) -> Text:
        return "check_abnormal_vital_signs_action"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        vital_signs = fetch_vital_signs()
        if len(vital_signs):
            tempr = vital_signs[0]["tempr"]
            resp = vital_signs[0]["resp"]
            hr = vital_signs[0]["hr"]
            spo2 = vital_signs[0]["spo2"]
            tempStatus = "Normal"
            hrStatus = "Normal"
            spo2Status = "Normal"
            respStatus = "Normal"
            if tempr >= 30 or tempr <= 20:
                tempStatus = "Abnormal"
            dispatcher.utter_message(template="utter_exceed_tempr",
                                         tempr=str(tempr), tempStatus=tempStatus)

            if resp >= 30 or resp <= 20:
                respStatus = "Abnormal"
            dispatcher.utter_message(template="utter_exceed_resp",
                                         resp=str(resp), respStatus=respStatus)
            if hr >= 30 or hr <= 20:
                hrStatus = "Abnormal"

            dispatcher.utter_message(template="utter_exceed_hr",
                                         hr=str(hr), hrStatus=hrStatus)

            if spo2 >= 90 or spo2 <= 60:
                spo2Status = "Abnormal"

            dispatcher.utter_message(template="utter_high_pressure",
                                         spo2=str(spo2), spo2Status=spo2Status)

            return {"temp_reading": tempr, "sop2_reading": spo2, "heart_reading": hr, "resp_reading": resp}
        else:
            dispatcher.utter_message(template="utter_no_data", no_data="No data available")



class ActionDiagnosticResponseAction(Action):
    def name(self) -> Text:
        return "diagnostic_response_action"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        prediction = fetch_heath_status()
        if len(prediction) > 0:
            output = prediction[0]["output"]

            if output == str("Abnormal"):
                dispatcher.utter_message(template="utter_abnormal_response",
                                         abnormal_response=str(
                                             "The Patient condition is not normal. The patient needs an agent medical "
                                             "attention"))
            elif output == str("Normal"):
                dispatcher.utter_message(template="utter_normal_response",
                                         normal_response=str("The Patient condition is Normal."))
        else:
            dispatcher.utter_message(template="utter_no_data", no_data="No data available")


class ActionSuggestion(Action):
    def name(self) -> Text:
        return "suggested_action"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        vital_signs = fetch_vital_signs()
        if len(vital_signs):
            tempr = vital_signs[0]["tempr"]
            resp = vital_signs[0]["resp"]
            hr = vital_signs[0]["hr"]
            spo2 = vital_signs[0]["spo2"]
            if tempr >= 30:
                dispatcher.utter_message(template="utter_temp_suggest",
                                         tempr_suggest="Please follow the steps below to reduce the body heat")
            elif tempr <= 20:
                dispatcher.utter_message(template="utter_temp_suggest",
                                         tempr_suggest="Please follow the steps below to increase the body heat")
            if resp >= 30:
                dispatcher.utter_message(template="utter_resp_suggest",
                                         resp_suggest="Please follow the steps for breathing relaxation")
            elif resp <= 20:
                dispatcher.utter_message(template="utter_resp_suggest",
                                         resp_suggest="Please follow the steps for breathing relaxation")
            if hr >= 30:
                dispatcher.utter_message(template="utter_hr_suggest",
                                         hr_suggest="Please follow the steps to lower the heart rate")
            elif hr <= 20:
                dispatcher.utter_message(template="utter_hr_suggest",
                                         hr_suggest="Please follow the steps for improving the heart rate")
            if spo2 >= 90:
                dispatcher.utter_message(template="utter_pressure_suggest",
                                         spo2_suggest="Please follow the steps bellow to lower the pressure to the safe value")
            elif spo2 <= 60:
                dispatcher.utter_message(template="utter_pressure_suggest",
                                         spo2_suggest="Please follow the steps bellow to increase the pressure to save value")



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
                                     all="Temp: " + tempr + " C Oxygen Saturation: " + spo2 + " % Heart rate: " + hr + " bpm Respiration: " + resp+" bpm")

        else:
            dispatcher.utter_message(template="utter_none",
                                     none="No vital sign selected")

        return [SlotSet("requested_slot", None)]
