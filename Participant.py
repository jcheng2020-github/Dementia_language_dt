#Author: Junfu Cheng

import openai
class Participant:
    def __init__(self, patient_id, conversations, api_key):

        self.patient_id = patient_id
        self.conversations = conversations
        self.message = []
        self.api_key = api_key
        
        # Set the OpenAI API key
        openai.api_key = api_key
        # Prepare the prompt for instruction-tuning
        system_prompt = (#refer to title={A-CONECT: Designing AI-based Conversational Chatbot for Early Dementia Intervention}, author={Hong, Junyuan and Zheng, Wenqing and Meng, Han and Liang, Siqi and Chen, Anqing and H. Dodge, Hiroko and Zhou, Jiayu and Wang, Zhangyang},
f"""
You are an old person with Mild Cognitive Impairment.
You will talk to an interviewer.
Based on the past conversations delimited by triple backticks,\
your task is to play the role as 'Participant' in the past conversation and\
response to the interviewer\
while maintaining a consistent style with the 'Participant' in the past conversation\n
"""
        )
        # Add the patient's conversations to the prompt
        for i, conv in enumerate(conversations):
            system_prompt += f"Past Conversation {i + 1}: \n```{conv}\n```\n"

        system_prompt += "Now, simulate your response to the interviewer:\n"
        # Generate a response using the instruction-tuned model
        print("System Prompt:")
        print(system_prompt)
        print()
        self.message.append({'role': 'system', 'content': system_prompt})
        
        
    def chat_with_gpt(self, prompt):
        self.message.append({'role': 'user', 'content': prompt})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # or 'gpt-4' if you have access
            messages=self.message,
            temperature=0
        )

        self.message.append({'role': 'assistant', 'content': response['choices'][0]['message']['content']})
        #print(self.message)
        return response['choices'][0]['message']['content']
