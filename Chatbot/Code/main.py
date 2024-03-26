from assistant import AssistantManager
import streamlit as st

manager = AssistantManager()
st.title("News Summarizer")

with st.form(key='user_input_form'):
    instructions = st.text_input("Enter topic:")
    summit_button = st.form_submit_button(label="Run Assistant")
    
    if summit_button:
       manager.create_assistant(
           name = "News Summarier",
           instructions = "You are a personal article summarizer Assistant who knows how to take a list of article's titles and description and the write a short summary of all the news articles.",
           tools=[
               {
                   "type": "function",
                   "function": {
                       "name": "get_news",
                       "description": "Get the list of articles/news for the given topic.",
                       "parameters": {
                           "type": "object",
                           "properties": {
                               "topic": {
                                   "type": "string", 
                                   "description": "The topic for the news, e.g. bitcoin",
                               }
                           },
                           "required": ["topic"],
                       }
                   }
               }
           ]
       )
       manager.create_thread()
       
       # Add the message and run the assistant
       manager.add_message_to_thread(
           role="user",
           content=f"List and summarize the news on this topic {instructions}"
       )
       manager.run_assistant(instructions="Summarize the news")
       
       
       # Wait for completion and process message
       manager.wait_for_completed()
       summary = manager.get_summary()
       news = manager.get_news()
       #st.json(news)
       st.write(summary)
       st.text("Run Steps:")
       st.code(manager.run_step(), line_numbers=True)
       

