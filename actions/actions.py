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
from actions.vital_sign_rest_api import fetch_vital_signs, check_anomalies, \
    check_anomaly_recommendations
# from actions.db import add_user, authenticate_user
from typing import Dict, Text, List, Optional, Any
from rasa_sdk.forms import FormValidationAction


# class ActionCheckStatus(Action):
#     def name(self) -> Text:
#         return "check_heath_status_action"
#
#     def run(
#             self,
#             dispatcher,
#             tracker: Tracker,
#             domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#         vital_signs = fetch_vital_signs()
#         if len(vital_signs) > 0:
#             tempr = vital_signs[0]["tempr"]
#             resp = vital_signs[0]["resp"]
#             hr = vital_signs[0]["hr"]
#             spo2 = vital_signs[0]["spo2"]
#             # output = prediction(hr, spo2, resp, tempr)
#             output = check_anomalies(check_anomalies)
#             dispatcher.utter_message(template="utter_health_status",
#                                      health_status=str(output))
#             if output == "Abnormal":
#                 if tempr >= 37.5:
#                     dispatcher.utter_message(template="utter_exceed_tempr",
#                                              tempr=str(tempr))
#                 elif tempr <= 36:
#                     dispatcher.utter_message(template="utter_less_tempr",
#                                              tempr=str(tempr))
#
#                 if resp >= 20:
#                     dispatcher.utter_message(template="utter_exceed_resp",
#                                              resp=str(resp))
#                 elif resp <= 12:
#                     dispatcher.utter_message(template="utter_less_resp",
#                                              resp=str(resp))
#                 if hr >= 80:
#                     dispatcher.utter_message(template="utter_exceed_hr",
#                                              hr=str(hr))
#                 elif hr <= 60:
#                     dispatcher.utter_message(template="utter_less_hr",
#                                              hr=str(hr))
#                 if spo2 <= 90:
#                     dispatcher.utter_message(template="utter_high_pressure",
#                                              spo2=str(spo2))
#                 # elif spo2 <= 60:
#                 #     dispatcher.utter_message(template="utter_low_pressure",
#                 #                              spo2=str(spo2))
#
#         else:
#             dispatcher.utter_message(template="utter_no_data", no_data="No data available")


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
        output = check_anomalies()
        if len(output) > 0:
            if output == "Abnormal":
                 dispatcher.utter_message(template="utter_abnormal_response", abnormal_response="The Patient condition is not normal. The patient needs an agent medical attention")
            elif output == "Normal":
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

        recommendations = check_anomaly_recommendations()
        if len(recommendations):
            temp_reco, temp = "", 1
            spo2_reco, spo2 = "", 1
            resp_reco, resp = "", 1
            heart_reco, heart = "", 1
            for reco in recommendations:
                if len(reco) > 1:
                    if reco["recoType"] == "Temperature":
                        temp_reco = temp_reco + str(temp)+ "-"+ reco["recoDescription"] + "\n"
                        temp+=1
                    elif reco["recoType"] == "Spo2":
                        spo2_reco = spo2_reco  + str(spo2)+ "-"+ reco["recoDescription"] + "\n"
                        spo2+=1
                    elif reco["recoType"] == "Respiration":
                        resp_reco = resp_reco  + str(resp)+ "-"+  reco["recoDescription"] + "\n"
                        resp+=1
                    elif reco["recoType"] == "Heart Rate":
                        heart_reco = heart_reco  + str(heart)+ "-"+  reco["recoDescription"] + "\n"
                        heart+=1
            if len(temp_reco)>0:
                dispatcher.utter_message(template="utter_temp_suggest",
                                         tempr_suggest="Below are the best Practice for body temperature at Home\n" + temp_reco)

            if len(resp_reco)>0:
                dispatcher.utter_message(template="utter_resp_suggest",
                                         resp_suggest="The following are the best practice for breathing relaxation\n" + resp_reco)
            if len(heart_reco)>0:
                dispatcher.utter_message(template="utter_hr_suggest",
                                         hr_suggest="The following are the best practice to relieve the heart beating\n" + heart_reco)

            if len(spo2_reco)>0:
                dispatcher.utter_message(template="utter_pressure_suggest",
                                         spo2_suggest="Please follow the steps bellow to increase the Oxygen "
                                                      "saturaton in blood\n" + spo2_reco)


# class ActionSuggestion(Action):
#     def name(self) -> Text:
#         return "suggested_action"
#
#     def run(
#             self,
#             dispatcher,
#             tracker: Tracker,
#             domain: "DomainDict",
#     ) -> List[Dict[Text, Any]]:
#
#         vital_signs = fetch_vital_signs()
#         if len(vital_signs):
#             tempr = vital_signs[0]["tempr"]
#             resp = vital_signs[0]["resp"]
#             hr = vital_signs[0]["hr"]
#             spo2 = vital_signs[0]["spo2"]
#             if tempr >= 30:
#                 dispatcher.utter_message(template="utter_temp_suggest",
#                                          tempr_suggest="Below are the best Practice to low body temperature at Home\n"
#                                                        "1- getting plenty of rest\n"
#                                                        "2- drinking water and juices to stay hydrated \n"
#                                                        "3- wearing comfortable, loose clothes\n"
#                                                        "4- keeping rooms at a cool, comfortable temperature"
#                                                        "")
#             elif tempr <= 20:
#                 dispatcher.utter_message(template="utter_temp_suggest",
#                                          tempr_suggest="Below are the best Practice to handle lower body temperature at Home\n"
#                                                        "1- Recognize the signs of hypothermia\n"
#                                                        "2- Get out of the cold. If your body temperature is dropping dramatically, you need to get out of the cold. If you are outdoors, find a warm room or shelter\n"
#                                                        "3- Remove wet clothes. If your clothes are wet, then remove them and put on some dry clothes.\n"
#                                                        "4- Rely on skin-to-skin contact. If you can't get indoors, curl up with another person under loose, dry layers of blankets or clothing\n"
#                                                        "5- Warm the center of the body first")
#             if resp >= 30:
#                 dispatcher.utter_message(template="utter_resp_suggest",
#                                          resp_suggest="The following are the best practice for breathing relaxation\n"
#                                                       "1- Deep breathing: Breathing in deeply through the abdomen can help someone manage their breathlessness\n"
#                                                       "2- Pursed lip breathing: helps reduce breathlessness by slowing the pace of a person’s breathing\n"
#                                                       "3- Finding a comfortable and supported position\n"
#                                                       "4- Using a fan: using a handheld fan to blow air across the nose and face could reduce the sensation of breathlessness\n"
#                                                       "5- Inhaling steam: help keep a person’s nasal passages clear, which can help them breathe more easily\n"
#                                                       "6- Drinking black coffee: help ease breathlessness, as the caffeine in it can reduce tightness in the muscles in a person’s airway\n"
#                                                       "7- Eating fresh ginger: Eating fresh ginger, or adding some to hot water as a drink, may help reduce shortness of breath that occurs due to a respiratory infection")
#             elif resp <= 20:
#                 dispatcher.utter_message(template="utter_resp_suggest",
#                                          resp_suggest="The following are best practicies to reduce rapid or deep breathing\n"
#                                                       "1- Breathe through pursed lips\n"
#                                                       "2- Breathe slowly into a paper bag or cupped hands\n"
#                                                       "3- Attempt to breathe into your belly (diaphragm) rather than your chest\n"
#                                                       "4- Hold your breath for 10 to 15 seconds at a time")
#             if hr >= 30:
#                 dispatcher.utter_message(template="utter_hr_suggest",
#                                          hr_suggest="The following are the best practice to relieve the fast heart beating\n"
#                                                     "1- Manage your stress through relaxation\n"
#                                                     "2- Drink enough water\n"
#                                                     "3- Avoid stimulants like tobacco products, heavy alcohol\n"
#                                                     "4- Eat a banalanced diet\n"
#                                                     "5- Exercise regularly")
#             elif hr <= 20:
#                 dispatcher.utter_message(template="utter_hr_suggest",
#                                          hr_suggest="Please follow the steps for improving the heart rate\n"
#                                                     "1- Eat Cayenne pepper: It is a natural blood regulator and a heart tonic. It also helps remove congestion in the circulatory system as well as stimulate the body\n"
#                                                     "2- Eat Ginger: The stimulant properties that a ginger contains are quite similar to that of a cayenne pepper\n"
#                                                     "3- Stress Reduction: You can reduce stress by meditating, having excellent sleep patterns, and engaging in physical activity\n"
#                                                     "4- Garlic contains natural properties that enable it to reduce body cholesterol, high blood pressure, and improve coronary heart diseases.")
#             if spo2 <= 90:
#                 dispatcher.utter_message(template="utter_pressure_suggest",
#                                          spo2_suggest="Please follow the steps bellow to lower the pressure to the safe value\n"
#                                                       "1- Lie down in the prone position. Proning is the best position to increase the oxygen level of your body\n"
#                                                       "2- Include more antioxidants in your diet. Antioxidants allow your body to use oxygen more efficiently\n"
#                                                       "3- Practice slow and deep breathing. our breathing pattern can have a vast effect on your blood's oxygen saturation level. By changing your breathing style, you can provide a significant boost to your blood's SpO2 level\n"
#                                                       "4- Drink lots of fluid. Keeping yourself hydrated is another important method to improve your blood's oxygen saturation level")
#

class ActionRequestVitalSigns(Action):
    def name(self) -> Text:
        return "action_request_vital_signs"

    def run(
            self,
            dispatcher,
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        vital_signs = fetch_vital_signs()
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

        elif tracker.get_slot('vital_signs') in ["oxygen"]:
            maxspo2 = vital_signs[2][0]["maxspo2"]
            minspo2 = vital_signs[2][0]["minspo2"]
            avgspo2 = vital_signs[2][0]["avgspo2"]
            dispatcher.utter_message(template="utter_oxygen", oxygen=spo2, maxspo2=maxspo2, minspo2=minspo2,
                                     avgspo2=avgspo2)

        elif tracker.get_slot('vital_signs') in ["respiration", "resp", "breath"]:
            maxresp = vital_signs[2][0]["maxresp"]
            minresp = vital_signs[2][0]["minresp"]
            avgresp = vital_signs[2][0]["avgresp"]
            dispatcher.utter_message(template="utter_respiration", respiration=resp, maxresp=maxresp, minresp=minresp,
                                     avgresp=avgresp)

        elif tracker.get_slot('vital_signs') in ["all"]:
            dispatcher.utter_message(template="utter_all",
                                     all="Temp: " + tempr + " C Oxygen Saturation: " + spo2 + " % Heart rate: " + hr + " bpm Respiration: " + resp + " bpm")

        else:
            dispatcher.utter_message(template="utter_none",
                                     none="No vital sign selected")
