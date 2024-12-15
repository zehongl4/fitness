#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 21:41:50 2024

@author: xuan
"""

import datetime
from enum import Enum
import openai

# Initialize OpenAI client with a hardcoded API key
client = openai.OpenAI(
    api_key=""  # Replace with your actual API key
)

class TimeOfDay(Enum):
    MORNING = "morning"
    MIDDAY = "midday" 
    EVENING = "evening"

def get_time_of_day() -> TimeOfDay:
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return TimeOfDay.MORNING
    elif 12 <= current_hour < 17:
        return TimeOfDay.MIDDAY
    return TimeOfDay.EVENING

class UserProfile:
    def __init__(self, name: str = None, age: int = None, weight: float = None,
                 height: float = None, medical_conditions: list = None,
                 preferences: list = None, goals: list = None):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.medical_conditions = medical_conditions or []
        self.preferences = preferences or []
        self.goals = goals or []

    def get_missing_attributes(self):
        missing = []
        if not self.name: missing.append("name")
        if not self.age: missing.append("age")
        if not self.weight: missing.append("weight")
        if not self.height: missing.append("height")
        if not self.medical_conditions: missing.append("medical conditions")
        return missing

    def update_attribute(self, attribute, value):
        if attribute != "medical conditions":
            setattr(self, attribute, value)
        else:
            self.medical_conditions.append(value)

class FitnessAssistant:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def ask_for_missing_attributes(self):
        missing_attributes = self.user_profile.get_missing_attributes()
        if missing_attributes:
            for attr in missing_attributes:
                response = input(f"Please enter your {attr}: ")
                self.user_profile.update_attribute(attr, response)
    
    def generate_time_based_questions(self):
        time_of_day = get_time_of_day().value
        messages = [
            {"role": "system", "content": "You are a fitness assistant."},
            {"role": "user", "content": f"It is now {time_of_day}, what are suitable fitness activities for this time of day?"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

    def generate_preference_questions(self):
        prompt = f"Generate a fitness-related question to know users' preference for a user named {self.user_profile.name}, aged {self.user_profile.age}, weighing {self.user_profile.weight} kg, height {self.user_profile.height} cm, with medical conditions {', '.join(self.user_profile.medical_conditions)}. Previous preferences: {', '.join(self.user_profile.preferences)}."
        messages = [
            {"role": "system", "content": "You are a fitness assistant."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

    def generate_goal_questions(self):
        prompt = f"Generate a fitness goal-oriented question for the same user. Past goals: {', '.join(self.user_profile.goals)}."
        messages = [
            {"role": "system", "content": "You are a fitness assistant."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

# Usage
user_profile = UserProfile(name="Alice", age=30, weight=65.0, height=165.0, preferences=['jogging', 'yoga'], goals=['increase stamina'])
assistant = FitnessAssistant(user_profile)
assistant.ask_for_missing_attributes()  # Query and update missing attributes
time_questions = assistant.generate_time_based_questions()
preferences = assistant.generate_preference_questions()
goals = assistant.generate_goal_questions()

user_profile.preferences.append(preferences)
user_profile.goals.append(goals)

print("Time-Sensitive Fitness Questions:", time_questions)
print("Generated Questions based on user preferences:", preferences)
print("Generated Goals based on past goals:", goals)







