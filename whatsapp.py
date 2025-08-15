import os
import requests
from agents import function_tool

@function_tool
def send_whatsapp_message(number: str, message: str) -> str:
    """
    Use the UltraMSG API to send a custom WhatsApp message to the specified phone number.
    Returns a success message if sent successfully, or an error if the request fails.
    """
    instance_id = os.getenv("INSTANCE_ID")  # Make sure matches .env
    token = os.getenv("API_TOKEN")          # Make sure matches .env
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

    payload = {
        "token": token,
        "to": number,
        "body": message
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return f"Message sent successfully to {number}"
    else:
        return f"Failed to send message. Error: {response.text}"

############################################chainlit code##################
# 
# import chainlit as cl
# import os
# # import chainlit as cl
# from agents import Agent, function_tool
# import requests

# @function_tool
# def send_whatsapp_message(number: str, message: str) -> str:
#     """
#     Use the UltraMSG API to send a custom WhatsApp message to the specified phone number.
#     Returns a success message if sent successfully, or an error if the request fails.
#     """
#     instance_id = os.getenv("instance_ID")  # Make sure env var name matches your .env
#     token = os.getenv("API_TOKEN")  # Corrected spelling
#     url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

#     payload = {
#         "token": token,
#         "to": number,
#         "body": message
#     }

#     response = requests.post(url, data=payload)

#     if response.status_code == 200:
#         return f"Message sent successfully to {number}"
#     else:
#         return f"Failed to send message. Error: {response.text}"



###################################chainlit code oper wala#############################

# import chainlit as cl
# from agents import Agent,function_tool
# import requests

# @function_tool
# def send_whatsapp_message(number: str,message:str) ->str:
#     """
#     User the UltraMSG API to  send a custom whatsapp message to the specified phone number, 
#     Rerurns a success message if sent successfully , a or an error if the request dails,
#     """
#    instance_id = os.getenv("instance_ID")
#     token =os.getenv("APU_TOKEN") 
#     url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
#     payload ={
#         "token": token,
#         "to":number,
#         "body":message
#     }
#   response = requests.post(url,data=payload)
#   ifresponse.status_code == 200:
#   return f"Message senr successfuly to {number}"
#   else:
#     return f"Failed to send message. error: {response.text}"