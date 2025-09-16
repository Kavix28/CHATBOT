from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import re

class ActionHandleNameResponse(Action):
    def name(self) -> Text:
        return "action_handle_name_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract name from entities first
        name = next(tracker.get_latest_entity_values("user_name"), None)
        
        # If no entity found, try to extract from text
        if not name:
            text = tracker.latest_message.get('text', '').strip().lower()
            
            # Common patterns for name responses
            patterns = [
                r'my name is (\w+)',
                r'i am (\w+)',
                r'this is (\w+)',
                r'call me (\w+)',
                r'you can call me (\w+)',
                r'name is (\w+)',
                r"i'm (\w+)",
                r"it's (\w+)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    name = match.group(1)
                    break
            
            # If no pattern matched, use the whole text (assuming it's just a name)
            if not name and len(text.split()) <= 2:
                name = text.title()
        
        if name:
            # Clean up the name
            name = name.strip().title()
            dispatcher.utter_message(text=f"Nice to meet you, {name}!")
            return [SlotSet("user_name", name), FollowupAction("utter_ask_user_email")]
        else:
            dispatcher.utter_message(text="I didn't catch your name. Could you please tell me your name?")
            return []

class ActionHandleEmailResponse(Action):
    def name(self) -> Text:
        return "action_handle_email_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract email from entities or text
        email = next(tracker.get_latest_entity_values("user_email"), None)
        if not email:
            email = tracker.latest_message.get('text')
        
        # Simple email validation
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            dispatcher.utter_message(text="Thank you! Your inquiry has been submitted. We'll contact you soon.")
            return [SlotSet("user_email", email)]
        else:
            dispatcher.utter_message(text="Please provide a valid email address.")
            return [SlotSet("user_email", None)]

class ActionShowFees(Action):
    def name(self) -> Text:
        return "action_show_fees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course = tracker.get_slot("inquiry_course")
        if course:
            if "computer" in course.lower():
                dispatcher.utter_message(text="The fee for Computer Science B.Tech is ₹1,20,000 per year.")
            elif "electrical" in course.lower():
                dispatcher.utter_message(text="The fee for Electrical Engineering B.Tech is ₹1,10,000 per year.")
            elif "mechanical" in course.lower():
                dispatcher.utter_message(text="The fee for Mechanical Engineering B.Tech is ₹1,15,000 per year.")
            else:
                dispatcher.utter_message(text=f"The fee for {course} B.Tech is approximately ₹1,00,000 - ₹1,20,000 per year.")
        else:
            dispatcher.utter_message(text="B.Tech fees range from ₹1,00,000 to ₹1,20,000 per year depending on the department.")
        
        return []

# actions.py - Update the show_department_info action
class ActionShowDepartmentInfo(Action):
    def name(self) -> Text:
        return "action_show_department_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course = tracker.get_slot("course_name")
        if course:
            department_heads = {
                "computer science": "Dr. Sharma",
                "electrical": "Dr. Gupta", 
                "mechanical": "Dr. Patel",
                "civil": "Dr. Kumar",
                "electronics": "Dr. Singh",
                "chemical": "Dr. Reddy"
            }
            
            head_name = department_heads.get(course.lower(), "the department head")
            
            if "head" in tracker.latest_message.get('intent', {}).get('name', ''):
                dispatcher.utter_message(text=f"The head of {course} department is {head_name}.")
            else:
                if "computer" in course.lower():
                    dispatcher.utter_message(text="Computer Science Department offers cutting-edge programs in AI, ML, and software engineering with state-of-the-art labs.")
                elif "electrical" in course.lower():
                    dispatcher.utter_message(text="Electrical Engineering Department focuses on power systems, electronics, and electrical machines with modern laboratories.")
                elif "mechanical" in course.lower():
                    dispatcher.utter_message(text="Mechanical Engineering Department provides comprehensive training in design, manufacturing, and thermal sciences.")
                else:
                    dispatcher.utter_message(text=f"The {course} department offers excellent B.Tech programs with experienced faculty and modern facilities.")
        else:
            dispatcher.utter_message(text="Please specify which department you're interested in.")
        
        return []

class ActionShowEligibility(Action):
    def name(self) -> Text:
        return "action_show_eligibility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course = tracker.get_slot("course_name")
        if course:
            dispatcher.utter_message(text=f"For {course} B.Tech, you need 12th grade with PCM and minimum 75% marks with valid JEE Main score.")
        else:
            dispatcher.utter_message(text="For B.Tech programs, you need 12th grade with Physics, Chemistry, Mathematics and minimum 75% marks with valid JEE Main score.")
        
        return []

class ActionFallbackKnowledgeBase(Action):
    def name(self) -> Text:
        return "action_fallback_knowledge_base"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="I'm not sure I understand. Could you please rephrase your question or ask about admission, courses, fees, or hostel facilities?")
        
        return []