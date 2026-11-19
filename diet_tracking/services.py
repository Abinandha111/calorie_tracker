from google import genai

import os
import json
gemini_api_key = os.getenv("gemini_api_key")

client = genai.Client(api_key=gemini_api_key)

def scan_food_image(image):

    image_bytes = image.read()
 
    
    prompt = """
    Analyze the uploaded food image.

    Extract the following information:
    1. Title of the food item.
    2. Estimated calories (in kcal).
    3. Meal type.

    Instructions:
    - Identify the food item from the image.
    - If multiple food items are visible, consider all items together.
    - Provide a suitable title describing the food.
    - Estimate the total calories based on the visible food portions.
    - Do not invent exact nutritional values. Provide reasonable estimates.
    - Automatically determine the meal type based on the food items and visible meal context.
    - Do not ask the user to specify the meal type.

    Available meal types:
    - breakfast
    - lunch
    - dinner
    - snack

    Choose only one meal type.
    If the meal type cannot be determined confidently, choose the most appropriate category.

    Return only valid JSON with exactly these fields:
    title, calorie, meal_type.

    Example output:
    {
        "title": "Chicken Biriyani",
        "calorie": 450,
        "meal_type": "lunch"
    }
    """


    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[
            prompt,
            {
                "inline_data": {
                    "mime_type": image.content_type,
                    "data": image_bytes
                }
            }
        ],
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)

    
    