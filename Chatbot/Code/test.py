from assistant import AssistantManager


manager = AssistantManager()
manager.create_assistant(
           name = "News Summarizer",
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
    content=f"summarize the news on this topic OpenAI"
)
manager.run_assistant(instructions="Summarize the news")


# Wait for completion and process message
manager.wait_for_completed()
summary = manager.get_summary()

