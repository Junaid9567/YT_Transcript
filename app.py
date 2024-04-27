import streamlit as st
from dotenv import load_dotenv
load_dotenv() ## load all the environment variables
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

# getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try: 
        video_id  = youtube_video_url.split("=")[1]
        # transcript_text is in form of list 
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        # since this is in a list lets append it together
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return   transcript   

        pass
    except Exception as e:
        raise e




genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

# create a function to generate summary from gemini by giving 
# input as the transcript 

prompt = """You are Youtube Video summarizer, you will be taking the transcript text and summarizing the entire video And providing the important summary in points within 250 words. Please provide the summary of the text given here:  """
def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube  Video Link:")

transcript_text = ""
# botom will give the entire youtube transcript link
if st.button("Get Detailed Notes"):
    transcript_text =  extract_transcript_details(youtube_link)

if transcript_text:
    summary =  generate_gemini_content(transcript_text,prompt)
    st.markdown("## Detailed Notes:")
    st.write(summary)
