import google.generativeai as genai
import requests
import streamlit as st

# Configure Gemini API with the correct key
api_key = "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)

# Load the model
model = genai.GenerativeModel('gemini-1.5-pro-001')

# Function to communicate with Gemini API for mental health insights
def mental_health_chat(user_input):
    try:
        prompt = f"User input: {user_input}. Provide insights and support for mental health in a supportive, conversational manner."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error fetching AI response: {str(e)}"

# Function to analyze nutrition information
def analyze_nutrition(food_item, quantity):
    try:
        prompt = f"Analyze the nutritional content of {quantity} of {food_item}. Provide information on fiber, protein, etc., and give an overview of whether it is healthy."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error fetching nutrition data: {str(e)}"

# Function to track fitness activities
def analyze_fitness(activity, duration):
    try:
        prompt = f"Evaluate the fitness impact of doing {activity} for {duration} minutes. Provide feedback on whether it's on track for fitness goals."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error fetching fitness analysis: {str(e)}"
