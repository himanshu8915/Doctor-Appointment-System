# from fastapi import FastAPI
# from pydantic import BaseModel
# from agents import DoctorAppointmentAgent
# from langchain_core.messages import HumanMessage
# import os

# from utils.mongo_handler import load_from_mongo, load_to_mongo
# load_from_mongo()




# #os.environ.pop("SSL_CERT_FILE", None)


# app = FastAPI()

# # Define Pydantic model to accept request body
# class UserQuery(BaseModel):
#     id_number: int
#     messages: str


# agent = DoctorAppointmentAgent()

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}


# @app.post("/execute")
# def execute_agent(user_input: UserQuery):
#     app_graph = agent.workflow()
    
#     # Prepare agent state as expected by the workflow
#     input = [
#         HumanMessage(content=user_input.messages)
#     ]
#     query_data = {
#         "messages": input,
#         "id_number": user_input.id_number,
#         "next": "",
#         "query": "",
#         "current_reasoning": "",
#     }

#     config = {"configurable": {"user_id": f"{user_input.id_number}","thread_id":f"{user_input.id_number}-convo1", "recursion_limit": 100}}  

#     response = app_graph.invoke(query_data,config=config)
#     return {"messages": response["messages"]}

# @app.post('/save-to-mongo')
# def save_data_to_mongo():
#     load_to_mongo()
#     return{"status":"Data saved to MongoDB sucessfully"}   

# @app.post("/personal-assistant")
# def personal_assistant(user_input: UserQuery):
#     from reports_agent import PersonalReportAgent  # 👈 new file/class
#     agent = PersonalReportAgent()
#     app_graph = agent.workflow()

#     input_msg = [HumanMessage(content=user_input.messages)]
#     query_data = {
#         "messages": input_msg,
#         "id_number": user_input.id_number,
#         "query": "",
#         "current_reasoning": "",
#     }

#     config = {"configurable": {"user_id": f"{user_input.id_number}","thread_id":f"{user_input.id_number}-convo2", "recursion_limit": 100}}
#     response = app_graph.invoke(query_data, config=config)
#     return {"messages": response["messages"]}

from fastapi import FastAPI
from pydantic import BaseModel
from agents import DoctorAppointmentAgent
from langchain_core.messages import HumanMessage
import os


#os.environ.pop("SSL_CERT_FILE", None)


app = FastAPI()

# Define Pydantic model to accept request body
class UserQuery(BaseModel):
    id_number: int
    messages: str

agent = DoctorAppointmentAgent()

@app.post("/execute")
def execute_agent(user_input: UserQuery):
    app_graph = agent.workflow()
    
    # Prepare agent state as expected by the workflow
    input = [
        HumanMessage(content=user_input.messages)
    ]
    query_data = {
        "messages": input,
        "id_number": user_input.id_number,
        "next": "",
        "query": "",
        "current_reasoning": "",
    }
    config = {"configurable": {"user_id": f"{user_input.id_number}","thread_id":f"{user_input.id_number}-convo1", "recursion_limit": 100}}   

    response = app_graph.invoke(query_data,config=config)
    return {"messages": response["messages"]}