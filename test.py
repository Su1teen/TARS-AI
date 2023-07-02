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
    messages = []

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
        request = f"I am gonna give you transcript of video, you have to summarize it and create brief explanation of main points. Here is the text:{transcript}, After that ask me, whether I have questions and wait for my response. If only I understood everything, try to check my understanding of the video by suggesting to give me practice questions based on the video. After that ask me to give you answers and wait for my response, and then check them for correctness. If I don't understand the content of video try to ask what was difficult. Wait for my response and after that, explain them in more detail."
        messages.append({"role": "assistant", "content": request})
        messages.append({"role": "user", "content": request})
    else:
        if tutor_mode:
            # Provide clues instead of direct answers
            if "questions" in request.lower():
                clue = "Ask me about specific topics or details from the video, and I will try to provide more information."
                messages.append({"role": "assistant", "content": clue})
            elif "answers" in request.lower():
                clue = "Think about the information presented in the video and try to come up with your answers. Once you have them, let me know, and we can check them together."
                messages.append({"role": "assistant", "content": clue})
            elif "difficult" in request.lower():
                clue = "Tell me which specific parts of the video you found challenging, and I will explain them in more detail."
                messages.append({"role": "assistant", "content": clue})
            else:
                messages.append({"role": "user", "content": request})
        else:
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