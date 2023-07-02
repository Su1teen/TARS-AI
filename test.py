# -*- coding: utf-8 -*-
# from youtube_transcript_api import YouTubeTranscriptApi
# import openai
# import streamlit as st
# from streamlit_chat import message
# openai.api_key = "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"

# def get_transcript(video_id):
#     before, sep, after = video_id.partition('=')
#     if len(after) > 0:
#         video_id = after
#     outls=[]
#     tx=YouTubeTranscriptApi.get_transcript(video_id)
#     for i in tx:
#         outtxt=(i['text'])
#         outls.append(outtxt)
#     whole=' '.join(outls)
#     print(whole.replace("\n", ""),'\n')
#     return (whole.replace("\n", ""))

# def get_summary(url):
#     transcript=get_transcript(url)
#     prompt=f"I am gonna give you transcript of video, you have to summarize it and create brief explanation of main points. Here is the text:{transcript}, After that ask me, whether I have questions and wait for my response. If only I understood everything, try to check my understanding of the video by suggesting to give me practice questions based on the video. After that ask me to give you answers and wait for my response, and then check them for correctness. If I don't understand the content of video try to ask what was difficult. Wait for my response and after that, explain them in more detail."
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt }]
#     )
#     output_text = response['choices'][0]['message']['content']
#     return output_text
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []
# if 'past' not in st.session_state:
#     st.session_state['past'] = []
# def chat_completion(request):
#     messages = [
#         {"role": "system", "content": "You are now chatting with the TARS Assistant. Enjoy your conversation!"}
#     ]

#     # Append past messages to the conversation
#     if st.session_state['past']:
#         for past_input in st.session_state['past'][::-1]:
#             if "youtube.com" not in past_input:
#                 messages.append({"role": "user", "content": past_input})
#      # Check if there is a video URL in the user's input
#     if "youtube.com" in request:
#         summary = get_summary(request)  # Get the summary of the video
#         messages.append({"role": "assistant", "content": summary})
#         return summary  # Early return here if YouTube URL is detected

#     messages.append({"role": "user", "content": request})

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )

#     output_text = response['choices'][0]['message']['content']
#     return output_text
# st.title("TARS Assistant")
# # Storing the chat
# if st.checkbox("Tutor Mode"):
#     st.write("Assistant now in Tutor mode")
# else:
#     st.write("Assistant now in ChatGPT mode")
    
# user_input = st.text_input("You:", key='input')
# if user_input:
#     output = chat_completion(user_input)
#     # Store the output
#     st.session_state['past'].append(user_input)
#     st.session_state['generated'].append(output)
#     user_input=("")
# if st.session_state['generated']:
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         message(st.session_state["generated"][i], key=str(i))
#         message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
# -*- coding: utf-8 -*-
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = "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"
def get_transcript(video_id):
    before, sep, after = video_id.partition('=')
    if len(after) > 0:
        video_id = after
    outls=[]
    tx=YouTubeTranscriptApi.get_transcript(video_id)
    for i in tx:
        outtxt=(i['text'])
        outls.append(outtxt)
    whole=' '.join(outls)
    print(whole.replace("\n", ""),'\n')
    return (whole.replace("\n", ""))

def chat_completion(request, tutor_mode):
    messages = [
        {"role": "system", "content": "You are now chatting with the TARS Assistant. Enjoy your conversation!"}
    ]

    # Append past messages to the conversation
    if st.session_state['past']:
        for past_input in st.session_state['past'][::-1]:
            if "youtube.com" not in past_input:
                messages.append({"role": "user", "content": past_input})
    if st.session_state['generated']:
        for past_generated in st.session_state['generated'][::-1]:
                messages.append({"role": "system", "content": past_generated})
    
    if "youtube.com" in request:
        transcript = get_transcript(request)
        request = f"I am gonna give you transcript of video, you have to summarize it and create brief explanation of main points. Here is the text:{transcript}. After that ask me, whether I have questions and wait for my response. If I don't understand the content of video try to ask what was difficult. Wait for my response and after that, explain them in more detail."
        messages.append({"role": "assistant", "content": request})
        messages.append({"role": "user", "content": request})
    elif "analogue" in request or "alternative" in request or "similar" in request or "correlat" in request:
        request=f"Give me analogues by description I provide to the study resources. They must be at the same topic and idea, field, link is not neccesary. If I will tell you to give free ones, collect only free onces, you have permission to do so. The source is: {request}. Start response with the Phrase: There are analogues close by description or genre, they are:\n"
        messages.append({"role": "assistant", "content": request})
        messages.append({"role": "user", "content": request})    
    elif "practice" in request or "test" in request or "exam" in request or "exercise" in request:
        request=f"Give me about 5 or 10 exercies or questions related to topic I requested. If you summarized the transcript before you may also use information from that summary to create a question. You should, check my answers for correctness, and if I made a mistake then correct me. Now here is request: {request}. Start response with the Phrase: Let's start a test"
        messages.append({"role": "assistant", "content": request})
        messages.append({"role": "user", "content": request})    
    else:
        if tutor_mode:
            # Provide clues instead of direct answers
            request=f"Do not give me a direct answer, only give me some sort of advice or clue so that I can figure out the question myself. If I struggle, try to help me to figure out the problem and its solution. Now here is request: {request}"
            messages.append({"role": "assistant", "content": request})
            messages.append({"role": "user", "content": request})    
        else:
            request=f"Just give me a direct answer to my response. Be friendly. Now here is request: {request}"
            messages.append({"role": "assistant", "content": request})
            messages.append({"role": "user", "content": request})
            
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    output_text = response['choices'][0]['message']['content']
    return output_text


st.title("TARS Assistant")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []


tutor_mode = st.checkbox("Tutor Mode")
user_input = st.text_input("You:", key='input')

if user_input:
    output = chat_completion(user_input, tutor_mode)
    # Store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
    user_input = ""

if tutor_mode:
    st.write("Assistant is now in Tutor mode")
    if st.session_state['generated']:
        for i in range(len(st.session_state['past'])-1, -1, -1): 
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
else:
    st.write("Assistant is now in ChatGPT mode")
    if st.session_state['generated']:
        for i in range(len(st.session_state['past'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')