# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
# from rasa_sdk import tensorflow
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from actions.vital_sign_rest_api import fetch_vital_signs, check_anomalies, check_anomaly_recommendations, \
    authenticate_device, optimize_slots
# from actions.db import add_user, authenticate_user
from typing import Dict, Text, List, Optional, Any
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset


# class ActionAge(Action):
#     def name(self) -> Text:
#         return "action_device_code"
#
#     def run(
#             self,
#             dispatcher,
#             tracker: Tracker,
#             domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(template="utter_device_code", device_key=tracker.get_slot('auth_code'),
#                                  device_number=tracker.get_slot('device_number'))
#         return []
#

class ActionCheckAbnormalStatus(Action):
    def name(self) -> Text:
        return "check_abnormal_vital_signs_action"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot('device_number') is None or tracker.get_slot(
                'is_authenticated') is None or tracker.get_slot('is_authenticated') == "No" or tracker.get_slot(
            'auth_code') is None:
            dispatcher.utter_message(template="utter_authentication_msg", msg="2- Device is not authenticated")
            # dispatcher.utter_message(template="utter_device_code", device_key=tracker.get_slot('auth_code'),
            #                          is_authenticated=tracker.get_slot('is_authenticated'),
            #                          device_number=optimize_slots(tracker.get_slot('device_number')))

            return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'),
                    SlotSet("device_number", None), SlotSet("device_code", None)]

            # dispatcher.utter_message(template="utter_device_number", sms="ABVS- Device Number is not Set. Please")
        else:
            vital_signs = fetch_vital_signs(optimize_slots(tracker.get_slot('device_number')))
            if len(vital_signs):
                tempr = vital_signs[0][0]["tempr"]
                resp = vital_signs[0][0]["resp"]
                hr = vital_signs[0][0]["hr"]
                spo2 = vital_signs[0][0]["spo2"]
                tempStatus = vital_signs[1][0]["btName"]
                hrStatus = vital_signs[1][0]["hrName"]
                spo2Status = vital_signs[1][0]["spName"]
                respStatus = vital_signs[1][0]["respName"]
                dispatcher.utter_message(template="utter_exceed_tempr",
                                         tempr=str(tempr), tempStatus=tempStatus)
                dispatcher.utter_message(template="utter_exceed_resp",
                                         resp=str(resp), respStatus=respStatus)
                dispatcher.utter_message(template="utter_exceed_hr",
                                         hr=str(hr), hrStatus=hrStatus)
                dispatcher.utter_message(template="utter_high_pressure",
                                         spo2=str(spo2), spo2Status=spo2Status)

                # return {"temp_reading": tempr, "sop2_reading": spo2, "heart_reading": hr, "resp_reading": resp}
            else:
                dispatcher.utter_message(template="utter_no_data", no_data="No data available")
        return [SlotSet("state_machine", "logged")]


class ActionDiagnosticResponseAction(Action):
    def name(self) -> Text:
        return "diagnostic_response_action"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot('device_number') is None or tracker.get_slot(
                'is_authenticated') is None or tracker.get_slot('is_authenticated') == "No" or tracker.get_slot(
            'auth_code') is None:
            dispatcher.utter_message(template="utter_authentication_msg", msg="3-Device is not authenticated")

            return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'),
                    SlotSet("device_number", None), SlotSet("device_code", None)]
        else:
            output = check_anomalies(optimize_slots(tracker.get_slot('device_number')))
            if len(output) > 0:
                if output == "Abnormal":
                    dispatcher.utter_message(template="utter_abnormal_response",
                                             abnormal_response="The Patient condition is not normal. The patient needs an agent medical attention")
                elif output == "Normal":
                    dispatcher.utter_message(template="utter_normal_response",
                                             normal_response=str("The Patient condition is Normal."))
            else:
                dispatcher.utter_message(template="utter_no_data", no_data="No data available")
        return [SlotSet("state_machine", "logged")]


class ActionSuggestion(Action):
    def name(self) -> Text:
        return "suggested_action"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        if tracker.get_slot('device_number') is None or tracker.get_slot(
                'is_authenticated') is None or tracker.get_slot('is_authenticated') == "No" or tracker.get_slot(
            'auth_code') is None:
            dispatcher.utter_message(template="utter_authentication_msg", msg="Device is not authenticated")

            return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'),
                    SlotSet("device_number", None), SlotSet("device_code", None)]
        # elif tracker.get_slot('context') is None:
        #     dispatcher.utter_message(template="utter_context", con_sms="")
        # elif tracker.get_slot('age') is None:
        #     dispatcher.utter_message(template="utter_age", con_sms="Age is not set. Please")
        # elif tracker.get_slot('health_status') is None:
        #     dispatcher.utter_message(template="utter_ask_for_health", h_sms="")
        elif tracker.get_slot('health_status') is None or tracker.get_slot('age') is None and tracker.get_slot(
                'context') is None:
            return [SlotSet("state_machine", "suggestion"), FollowupAction('activity_tracking_action')]

        else:
            recommendations = check_anomaly_recommendations(optimize_slots(tracker.get_slot('device_number')),
                                                            tracker.get_slot('age'), tracker.get_slot('context'),
                                                            tracker.get_slot('health_status'))
            if len(recommendations):
                temp_reco, temp = "", 1
                spo2_reco, spo2 = "", 1
                resp_reco, resp = "", 1
                heart_reco, heart = "", 1
                for reco in recommendations:
                    if len(reco) > 1:
                        if reco["recoType"] == "Temperature":
                            temp_reco = temp_reco + str(temp) + "-" + reco["recoDescription"] + "\n"
                            temp += 1
                        elif reco["recoType"] == "Spo2":
                            spo2_reco = spo2_reco + str(spo2) + "-" + reco["recoDescription"] + "\n"
                            spo2 += 1
                        elif reco["recoType"] == "Respiration":
                            resp_reco = resp_reco + str(resp) + "-" + reco["recoDescription"] + "\n"
                            resp += 1
                        elif reco["recoType"] == "Heart Rate":
                            heart_reco = heart_reco + str(heart) + "-" + reco["recoDescription"] + "\n"
                            heart += 1
                if len(temp_reco) > 0:
                    dispatcher.utter_message(template="utter_temp_suggest",
                                             tempr_suggest="Below are the best Practice for body temperature at Home\n" + temp_reco)

                if len(resp_reco) > 0:
                    dispatcher.utter_message(template="utter_resp_suggest",
                                             resp_suggest="The following are the best practice for breathing relaxation\n" + resp_reco)
                if len(heart_reco) > 0:
                    dispatcher.utter_message(template="utter_hr_suggest",
                                             hr_suggest="The following are the best practice to relieve the heart beating\n" + heart_reco)

                if len(spo2_reco) > 0:
                    dispatcher.utter_message(template="utter_pressure_suggest",
                                             spo2_suggest="Please follow the steps bellow to increase the Oxygen "
                                                          "saturaton in blood\n" + spo2_reco)
        return [SlotSet("state_machine", "logged")]


"""
class ActionRequestAge(Action):
    def name(self) -> Text:
        return "action_request_age"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot('device_number') is None:
            dispatcher.utter_message(template="utter_ask_for_help1", age=tracker.get_slot('age'),
                                     device="no value")
        else:
            dispatcher.utter_message(template="utter_ask_for_help1", age=tracker.get_slot('age'), device="Value exist")


class ActionRequestContext(Action):
    def name(self) -> Text:
        return "action_request_context"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_ask_for_context", context=tracker.get_slot('context'))
        return []


class ActionRequestHealth(Action):
    def name(self) -> Text:
        return "action_request_health"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_health_status", health_status=tracker.get_slot('health_status'))
        return []
"""


class ValidateAuthenticationForm(Action):
    def name(self) -> Text:
        return "validate_simple_activation_form"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["auth_code", "device_number"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]


class ActionExist(Action):
    def name(self) -> Text:
        return "exit_action"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        # All slots are filled.
        return [AllSlotsReset(), FollowupAction('activity_tracking_action')]


class ActionTracking(Action):
    def name(self) -> Text:
        return "activity_tracking_action"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot('state_machine') == "start" and tracker.get_slot('is_authenticated') == "No":
            dispatcher.utter_template("utter_service_list", tracker)
            return [FollowupAction('simple_activation_form')]
        elif tracker.get_slot('state_machine') in ["start", "logged", "suggestion"]:
            if int(tracker.get_slot('needed'))>1:
                response = "utter_more_info_needed"
            else:
                response = "utter_info_needed"
            if tracker.get_slot('health_status') is not None and tracker.get_slot(
                    'age') is not None and tracker.get_slot('context') is not None:
                if tracker.get_slot('state_machine') in ["start"]:
                    dispatcher.utter_template("utter_ask_for_help", tracker)
                else:
                    dispatcher.utter_template("utter_ask_for_more_help", tracker)

            elif tracker.get_slot('age') is None:

                dispatcher.utter_template(response, tracker)
                dispatcher.utter_template("utter_age", tracker)
                return [SlotSet("needed", int(tracker.get_slot('needed'))+1)]
            elif tracker.get_slot('health_status') is None:
                dispatcher.utter_template(response, tracker)
                dispatcher.utter_template("utter_ask_for_health", tracker)
                return [SlotSet("needed", int(tracker.get_slot('needed'))+1)]
            elif tracker.get_slot('context') is None:
                dispatcher.utter_template(response, tracker)
                dispatcher.utter_template("utter_context", tracker)
                return [SlotSet("needed", int(tracker.get_slot('needed'))+1)]
            elif tracker.get_slot('state_machine') in ["suggestion"]:
                return [FollowupAction('suggested_action')]

class ActionDeviceAuthentication(Action):
    def name(self) -> Text:
        return "action_device_code"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(template="utter_device_code", device_key=tracker.get_slot('auth_code'), device_number=optimize_slots(tracker.get_slot('device_number')))

        if not (tracker.get_slot('auth_code') is None) and not (tracker.get_slot('device_number') is None):
            result = authenticate_device(optimize_slots(tracker.get_slot('device_number')),
                                         tracker.get_slot('auth_code'))
            if len(result) > 0:
                if int(result["msg"]) == 2:
                    # SlotSet("is_authenticated", True)
                    dispatcher.utter_message(template="utter_authentication_msg", msg="Your device is successfully "
                                                                                      "authenticated ")
                    # dispatcher.utter_message(template="utter_device_code", device_key=tracker.get_slot('auth_code'),
                    #                          is_authenticated="hhhh",
                    #                          device_number=optimize_slots(tracker.get_slot('device_number')))
                    # dispatcher.utter_template("utter_ask_for_help", tracker)
                    return [SlotSet("is_authenticated", "Yes"), SlotSet("state_machine", "start"),
                            FollowupAction('activity_tracking_action')]
                elif int(result["msg"]) == 1:
                    dispatcher.utter_message(template="utter_authentication_msg", msg="Device (" + optimize_slots(
                        tracker.get_slot('device_number')) + ") is not registered ")
                    return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'), AllSlotsReset()]
                elif int(result["msg"]) == 3:
                    dispatcher.utter_message(template="utter_authentication_msg", msg="Device Key is Incorrect ")
                    return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'), AllSlotsReset()]
                else:
                    dispatcher.utter_message(template="utter_authentication_msg", msg="Authentication fail")
                    return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'), AllSlotsReset()]


class ActionRequestVitalSigns(Action):
    def name(self) -> Text:
        return "action_request_vital_signs"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot('device_number') is None or tracker.get_slot(
                'is_authenticated') is None or tracker.get_slot('is_authenticated') is "No" or tracker.get_slot(
            'auth_code') is None:
            dispatcher.utter_message(template="utter_authentication_msg", msg="1-Device is not authenticated")

            return [SlotSet("is_authenticated", "No"), FollowupAction('simple_activation_form'),
                    SlotSet("device_number", None), SlotSet("device_code", None)]
        else:
            vital_signs = fetch_vital_signs(optimize_slots(tracker.get_slot('device_number')))
            # vital_aggr_signs = fetch_aggr_signs()
            if len(vital_signs) > 0:
                tempr = vital_signs[0][0]["tempr"]
                resp = vital_signs[0][0]["resp"]
                hr = vital_signs[0][0]["hr"]
                spo2 = vital_signs[0][0]["spo2"]
            else:
                tempr = "No data"
                resp = "No data"
                hr = "No Data"
                spo2 = "No data"
            if tracker.get_slot('vital_signs') in ["temperature", "temp"]:
                maxtempr = vital_signs[2][0]["maxtempr"]
                mintempr = vital_signs[2][0]["mintempr"]
                avgtempr = vital_signs[2][0]["avgtempr"]
                dispatcher.utter_message(template="utter_temperature", temperature=tempr, maxtempr=maxtempr,
                                         mintempr=mintempr, avgtempr=avgtempr)

            elif tracker.get_slot('vital_signs') in ["heart", "heart rate"]:
                maxhr = vital_signs[2][0]["maxhr"]
                minhr = vital_signs[2][0]["minhr"]
                avghr = vital_signs[2][0]["avghr"]
                dispatcher.utter_message(template="utter_heart", heart=hr, maxhr=maxhr, minhr=minhr, avghr=avghr)

            elif tracker.get_slot('vital_signs') in ["oxygen", "spo2"]:
                maxspo2 = vital_signs[2][0]["maxspo2"]
                minspo2 = vital_signs[2][0]["minspo2"]
                avgspo2 = vital_signs[2][0]["avgspo2"]
                dispatcher.utter_message(template="utter_oxygen", oxygen=spo2, maxspo2=maxspo2, minspo2=minspo2,
                                         avgspo2=avgspo2)

            elif tracker.get_slot('vital_signs') in ["respiration", "resp", "breath"]:
                maxresp = vital_signs[2][0]["maxresp"]
                minresp = vital_signs[2][0]["minresp"]
                avgresp = vital_signs[2][0]["avgresp"]
                dispatcher.utter_message(template="utter_respiration", respiration=resp, maxresp=maxresp,
                                         minresp=minresp,
                                         avgresp=avgresp)

            elif tracker.get_slot('vital_signs') in ["all"]:
                dispatcher.utter_message(template="utter_all",
                                         all="Temp: " + tempr + " C Oxygen Saturation: " + spo2 + " % Heart rate: " + hr + " bpm Respiration: " + resp + " bpm")

            else:
                dispatcher.utter_message(template="utter_none",
                                         none="No vital sign selected")
        return [SlotSet("state_machine", "logged")]
