from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import os

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

# 1. Create the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Function to send a message to GPT
def chat_with_ai(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a highly personalized fitness and nutrition assistant. Provide detailed and specific plans."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# 3. Function to build a smart prompt
def build_prompt(user_info, choice_type):
    if choice_type == "diet":
        return (
            f"Create a highly personalized diet plan for a {user_info['age']} year old {user_info['gender']}, "
            f"{user_info['height']} ft tall, {user_info['weight']} lbs, "
            f"who is {user_info['activity']} active. "
            f"Their goal is to {user_info['goal']}. "
            f"Dietary preferences: {user_info['diet']}. "
            f"Provide a detailed breakfast, lunch, dinner, and snack plan for one day, "
            f"with estimated calories per meal."
        )
    elif choice_type == "workout":
        return (
            f"Create a {user_info['fitness_level']} workout routine for a {user_info['age']} year old {user_info['gender']}, "
            f"{user_info['height']} ft tall, {user_info['weight']} lbs. "
            f"Their goal is to {user_info['goal']}, with an activity level of {user_info['activity']}. "
            f"Design a weekly schedule (5 days of training), "
            f"and specify exercises, sets, and reps for each day."
        )

# 4. Web routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # collect data from form
        user_info = {
            "age": request.form["age"],
            "gender": request.form["gender"],
            "height": request.form["height"],
            "weight": request.form["weight"],
            "activity": request.form["activity"],
            "diet": request.form["diet"],
            "goal": request.form["goal"],
            "fitness_level": request.form["fitness_level"],
        }
        plan_type = request.form["plan_type"]

        prompt = build_prompt(user_info, choice_type=plan_type)
        ai_response = chat_with_ai(prompt)

        return render_template("result.html", ai_response=ai_response)

    return render_template("index.html")

# 5. Run server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
