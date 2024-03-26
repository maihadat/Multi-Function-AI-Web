from openai import OpenAI
import os
import time
import logging
from datetime import datetime
import json
from functions import get_news


client = OpenAI()
model="gpt-3.5-turbo-0125"


class AssistantManager():
    thread_id = None
    assistant_id = None
    
    def __init__(self, model:str = model):
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None
        self.news = None
        
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )
    
    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=tools,
                model=self.model
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            
    def create_thread(self, ):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            
    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )
    
    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            self.run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                instructions=instructions
            )
    
    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread_id
            )
            summary = []
            
            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)
            
            self.summary = '\n'.join(summary)
            #print(f"SUMMARY-----------> {role.capitalize()}: ==> {response}")
            
            for msg in messages:
                role = msg.role
                content = msg.content[0].text.value
                
            
                #print(f"SUMMARY-----------> {role.capitalize()}: ==> {content}")

    def wait_for_completed(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id, run_id=self.run.id
                )
                print(f"RUN STATUS:: {run_status.model_dump_json(indent=4)}")
                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("FUNCTION CALLING NOW....")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )
                    
    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tools_outputs = []
        
        for action in required_actions['tool_calls']:
            func_name = action['function']['name']
            arguments = json.loads(action['function']['arguments'])
            
            if func_name == 'get_news':
                output = get_news(topic=arguments['topic'])
                final_str = ""
                for item in output:
                    final_str += "".join(item)
                
                tools_outputs.append({'tool_call_id': action['id'],
                                      'output': final_str})
            else:
                raise ValueError('Unknown function ' + func_name)
        print("Submitting outputs back to assistant.....")
        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread_id,
            run_id=self.run.id,
            tool_outputs=tools_outputs
        )
        self.news = final_str
            
    # for streamlit
    def get_summary(self):
        return self.summary
    
    def get_news(self):
        return self.news
    
    def run_step(self):
        run_steps = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread_id,
            run_id=self.run.id
        )
        print(f"Run Steps:::", run_steps)
        
                    
                
    
        
        
            
        
        
