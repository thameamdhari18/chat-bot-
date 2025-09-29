# This example uses OpenAI's GPT-3.5/4 via openai package for demonstration.
# You can swap with any LLM provider.
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple in-memory user state (expand for production)
user_states = {}

def wellness_conversation(user_id, user_message):
    # Maintain basic context
    if user_id not in user_states:
        user_states[user_id] = {"history": []}
    state = user_states[user_id]
    state["history"].append({"role": "user", "content": user_message})

    # LangGraph-like flow: check for mood, give tips/quotes, answer questions
    if "sad" in user_message.lower() or "not good" in user_message.lower():
        bot_message = (
            "I'm sorry you're feeling down. Here's a motivational quote:\n"
            "\"Keep your face always toward the sunshine—and shadows will fall behind you.\" — Walt Whitman\n"
            "Would you like a tip to improve your mood?"
        )
    elif "tip" in user_message.lower() or "yes" in user_message.lower():
        bot_message = (
            "Tip: Take a short walk, listen to your favorite music, or chat with a friend. "
            "Self-care is important! How are you feeling now?"
        )
    else:
        # Use LLM for general chat
        chat_history = [{"role": msg["role"], "content": msg["content"]} for msg in state["history"][-5:]]
        chat_history.insert(0, {"role": "system", "content": "You are a friendly wellness assistant."})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            max_tokens=150,
        )
        bot_message = completion.choices[0].message["content"].strip()

    state["history"].append({"role": "assistant", "content": bot_message})
    return bot_message