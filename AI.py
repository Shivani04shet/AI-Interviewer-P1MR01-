import os
import time
import elevenlabs
import google.generativeai as genai
from playsound import playsound  # Simple audio playback
from elevenlabs.client import ElevenLabs

# Set API Keys (Replace with your actual keys)
genai.configure(api_key=" ")  #Insert your Gemini API key
client = ElevenLabs(
  api_key='', 
) # Insert your Elevelabs API  key



def generate_interview_questions(topic, num_questions=5):
    """Generate interview questions using Google Gemini AI."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Generate {num_questions} interview questions for a {topic} role."

    try:
        response = model.generate_content(prompt)
        questions = response.text.split("\n") if response.text else ["No questions generated."]
        return questions
    except Exception as e:
        print(f"An error occurred: {e}")
        return ["An error occurred while generating questions."]

# Topic of the interview
topic = "Software Engineer"
questions = generate_interview_questions(topic)

# Specify the voice ID from ElevenLabs
VOICE_ID = " "  # Replace with an actual ElevenLabs voice ID

if questions:
    for i, question in enumerate(questions):
        question = question.strip()
        if question:
            print(f"Q{i+1}: {question}")

            try:
                # Generate audio using ElevenLabs with voice ID
                audio = elevenlabs.generate(
                    text=question, 
                    voice=VOICE_ID,  # Use voice ID instead of name
                    model="eleven_multilingual_v1"
                )
                filename = f"question_{i}.mp3"

                # Save audio file
                with open(filename, "wb") as f:
                    f.write(audio)

                # Check if file exists before playing
                if not os.path.exists(filename):
                    print(f"Error: {filename} not found.")
                    continue

                # Play audio using playsound
                playsound(filename)

                # Wait before the next question
                time.sleep(2)

                # Delete the file after playback
                os.remove(filename)
            except Exception as e:
                print(f"Error processing audio: {e}")
else:
    print("No questions were generated.")