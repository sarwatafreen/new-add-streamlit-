import os
import asyncio
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from whatsapp import send_whatsapp_message

# Load environment variables
load_dotenv(find_dotenv())
set_tracing_disabled(True)

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash"

# External Gemini LLM client
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    # base_url="https://generativelanguage.googleapis.com/v1beta/"
    base_url=  "https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv&gid=<SHEET_TAB_ID>"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model=MODEL_NAME
)

# Static rishta database
all_boys = [
    {"name": "Muneeb", "age": 22, "city": "Karachi"},
    {"name": "Muhammad Ubaid Hussain", "age": 25, "city": "Lahore"},
    {"name": "Azan", "age": 19, "city": "Islamabad"},
    {"name": "Samar", "age": 40, "city": "Islamabad"},
    {"name": "Ali", "age": 55, "profession": "IT & Engineering", "city": "Lahore"},
]

all_girls = [
    {"name": "Ayesha", "age": 21, "city": "Karachi"},
    {"name": "Sara", "age": 24, "city": "Lahore"},
    {"name": "Hina", "age": 20, "city": "Islamabad"},
]

# Tool function for filtered search
@function_tool



def get_user_data(min_age: int) -> list[dict]:
    """Retrieve user data based on a minimum age."""
    return [user for user in all_boys + all_girls if user["age"] >= min_age]

# Create Auntie Agent
rishtey_wali_agent = Agent(
    name="Auntie",
    model=model,
    instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
    tools=[get_user_data, send_whatsapp_message]
)

# Streamlit UI
st.set_page_config(page_title="💌 Rishtey Wali Auntie", page_icon="💌")
st.title("💌 Rishtey Wali Auntie")
st.write("Salamz beta! Main hoon tumhari Rishtey Wali Auntie. Apni details do, main tumhein rishtay doongi!")

# Initialize session history
if "history" not in st.session_state:
    st.session_state.history = []

# ---- All Rishtay Button ----
if st.button("📂 All Rishtay (Boys & Girls)"):
    st.subheader("👦 Boys")
    for boy in all_boys:
        details = f"- **{boy['name']}**, Age: {boy['age']}, City: {boy['city']}"
        if "profession" in boy:
            details += f", Profession: {boy['profession']}"
        st.markdown(details)

    st.subheader("👧 Girls")
    for girl in all_girls:
        st.markdown(f"- **{girl['name']}**, Age: {girl['age']}, City: {girl['city']}")

# ---- Rishtey Form ----
with st.expander("📋 Rishtey Ki Details Fill Karein"):
    with st.form("rishtay_form"):
        name = st.text_input("Apka Naam")
        age = st.number_input("Apki Age", min_value=18, max_value=70)
        whatsapp = st.text_input("WhatsApp Number")
        requirements = st.text_area("Apki Pasand / Requirements")
        submitted = st.form_submit_button("Details Submit Karein")

    if submitted:
        form_message = f"Naam: {name}, Age: {age}, WhatsApp: {whatsapp}, Pasand: {requirements}"
        st.session_state.history.append({"role": "user", "content": form_message})

        matches = get_user_data(age)
        if matches:
            match_list = "\n".join([
                f"{m['name']} (Age: {m['age']}, City: {m['city']})"
                for m in matches
            ])
            rishtay_message = f"Beta {name}, tumhare liye ye rishtay milay hain:\n{match_list}"
        else:
            rishtay_message = f"Beta {name}, afsos abhi tumhari age group ka rishta nahi mila."

        st.session_state.history.append({"role": "assistant", "content": rishtay_message})
        st.success("Aapki details save ho gayi hain! Neeche Auntie se baat karein.")

# ---- Chat Section ----
user_input = st.text_input("Auntie ko kuch puchho:")

if st.button("Send") and user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        Runner.run(
            starting_agent=rishtey_wali_agent,
            input=st.session_state.history
        )
    )
    loop.close()

    st.session_state.history.append({"role": "assistant", "content": result.final_output})

# ---- Chat history display ----
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**Auntie:** {chat['content']}")



# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv, find_dotenv
# from openai import AsyncOpenAI
# from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
# from whatsapp import send_whatsapp_message

# # Load environment variables
# load_dotenv(find_dotenv())
# set_tracing_disabled(True)

# # Gemini API setup
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"

# # External Gemini LLM client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/"
# )

# model = OpenAIChatCompletionsModel(
#     openai_client=external_client,
#     model=MODEL_NAME
# )

# # Static rishta database
# all_boys = [
#     {"name": "Muneeb", "age": 22, "city": "Karachi"},
#     {"name": "Muhammad Ubaid Hussain", "age": 25, "city": "Lahore"},
#     {"name": "Azan", "age": 19, "city": "Islamabad"},
#     { "name": "samar", "Age": 40," city": "Islamabad", "Pakistan"},
#      {"name": "ali","Age: 55","Designer : IT & Engineering","city":"Lahore, Pakistan"}



# ]

# all_girls = [
#     {"name": "Ayesha", "age": 21, "city": "Karachi"},
#     {"name": "Sara", "age": 24, "city": "Lahore"},
#     {"name": "Hina", "age": 20, "city": "Islamabad"},
# ]

# # Tool function for filtered search
# @function_tool
# def get_user_data(min_age: int) -> list[dict]:
#     """Retrieve user data based on a minimum age."""
#     return [user for user in all_boys + all_girls if user["age"] >= min_age]

# # Create Auntie Agent
# rishtey_wali_agent = Agent(
#     name="Auntie",
#     model=model,
#     instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
#     tools=[get_user_data, send_whatsapp_message]
# )

# # Streamlit UI
# st.set_page_config(page_title="💌 Rishtey Wali Auntie", page_icon="💌")
# st.title("💌 Rishtey Wali Auntie")
# st.write("Salamz beta! Main hoon tumhari Rishtey Wali Auntie. Apni details do, main tumhein rishtay doongi!")

# # Initialize session history
# if "history" not in st.session_state:
#     st.session_state.history = []

# # ---- All Rishtay Button ----
# if st.button("📂 All Rishtay (Boys & Girls)"):
#     st.subheader("👦 Boys")
#     for boy in all_boys:
#         st.markdown(f"- **{boy['name']}**, Age: {boy['age']}, City: {boy['city']}")

#     st.subheader("👧 Girls")
#     for girl in all_girls:
#         st.markdown(f"- **{girl['name']}**, Age: {girl['age']}, City: {girl['city']}")

# # ---- Rishtey Form ----
# with st.expander("📋 Rishtey Ki Details Fill Karein"):
#     with st.form("rishtay_form"):
#         name = st.text_input("Apka Naam")
#         age = st.number_input("Apki Age", min_value=18, max_value=70)
#         whatsapp = st.text_input("WhatsApp Number")
#         requirements = st.text_area("Apki Pasand / Requirements")
#         submitted = st.form_submit_button("Details Submit Karein")

#     if submitted:
#         form_message = f"Naam: {name}, Age: {age}, WhatsApp: {whatsapp}, Pasand: {requirements}"
#         st.session_state.history.append({"role": "user", "content": form_message})

#         matches = get_user_data(age)
#         if matches:
#             match_list = "\n".join([f"{m['name']} (Age: {m['age']}, City: {m['city']})" for m in matches])
#             rishtay_message = f"Beta {name}, tumhare liye ye rishtay milay hain:\n{match_list}"
#         else:
#             rishtay_message = f"Beta {name}, afsos abhi tumhari age group ka rishta nahi mila."

#         st.session_state.history.append({"role": "assistant", "content": rishtay_message})
#         st.success("Aapki details save ho gayi hain! Neeche Auntie se baat karein.")

# # ---- Chat Section ----
# user_input = st.text_input("Auntie ko kuch puchho:")

# if st.button("Send") and user_input:
#     st.session_state.history.append({"role": "user", "content": user_input})

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(
#         Runner.run(
#             starting_agent=rishtey_wali_agent,
#             input=st.session_state.history
#         )
#     )
#     loop.close()

#     st.session_state.history.append({"role": "assistant", "content": result.final_output})

# # ---- Chat history display ----
# for chat in st.session_state.history:
#     if chat["role"] == "user":
#         st.markdown(f"**You:** {chat['content']}")
#     else:
#         st.markdown(f"**Auntie:** {chat['content']}")


# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv, find_dotenv
# from openai import AsyncOpenAI
# from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
# from whatsapp import send_whatsapp_message

# # Load environment variables
# load_dotenv(find_dotenv())
# set_tracing_disabled(True)

# # Gemini API setup
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"

# # External Gemini LLM client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/"
# )

# model = OpenAIChatCompletionsModel(
#     openai_client=external_client,
#     model=MODEL_NAME
# )

# # Tool function
# @function_tool
# def get_user_data(min_age: int) -> list[dict]:
#     """Retrieve user data based on a minimum age."""
#     users = [
#         {"name": "Muneeb", "age": 22},
#         {"name": "Muhammad Ubaid Hussain", "age": 25},
#         {"name": "Azan", "age": 19},
#     ]
#     return [user for user in users if user["age"] >= min_age]

# # Create Auntie Agent
# rishtey_wali_agent = Agent(
#     name="Auntie",
#     model=model,
#     instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
#     tools=[get_user_data, send_whatsapp_message]
# )

# # Streamlit UI
# st.set_page_config(page_title="💌 Rishtey Wali Auntie", page_icon="💌")
# st.title("💌 Rishtey Wali Auntie")
# st.write("Salamz beta! Main hoon tumhari Rishtey Wali Auntie. Apni age aur WhatsApp number do, main tumhein rishtay doongi!")

# # Initialize session history
# if "history" not in st.session_state:
#     st.session_state.history = []

# # ---- Rishtey Form ----
# with st.expander("📋 Rishtey Ki Details Fill Karein"):
#     with st.form("rishtay_form"):
#         name = st.text_input("Apka Naam")
#         age = st.number_input("Apki Age", min_value=18, max_value=70)
#         whatsapp = st.text_input("WhatsApp Number")
#         requirements = st.text_area("Apki Pasand / Requirements")
#         submitted = st.form_submit_button("Details Submit Karein")

#     if submitted:
#         form_message = f"Naam: {name}, Age: {age}, WhatsApp: {whatsapp}, Pasand: {requirements}"
#         st.session_state.history.append({"role": "user", "content": form_message})
#         st.success("Aapki details save ho gayi hain! Neeche Auntie se baat karein.")

# # ---- Chat Section ----
# user_input = st.text_input("Auntie ko kuch puchho:")

# if st.button("Send") and user_input:
#     st.session_state.history.append({"role": "user", "content": user_input})

#     # Async call in Streamlit (safe way)
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(
#         Runner.run(
#             starting_agent=rishtey_wali_agent,
#             input=st.session_state.history
#         )
#     )
#     loop.close()

#     st.session_state.history.append({"role": "assistant", "content": result.final_output})

# # ---- Chat history display ----
# for chat in st.session_state.history:
#     if chat["role"] == "user":
#         st.markdown(f"**You:** {chat['content']}")
#     else:
#         st.markdown(f"**Auntie:** {chat['content']}")


# import os
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv, find_dotenv
# from openai import AsyncOpenAI
# from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
# from whatsapp import send_whatsapp_message

# # Load environment variables
# load_dotenv(find_dotenv())
# set_tracing_disabled(True)

# # Gemini API setup
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"

# # External Gemini LLM client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/"
# )

# model = OpenAIChatCompletionsModel(
#     openai_client=external_client,
#     model=MODEL_NAME
# )

# # Tool function
# @function_tool
# def get_user_data(min_age: int) -> list[dict]:
#     """Retrieve user data based on a minimum age."""
#     users = [
#         {"name": "Muneeb", "age": 22},
#         {"name": "Muhammad Ubaid Hussain", "age": 25},
#         {"name": "Azan", "age": 19},
#     ]
#     return [user for user in users if user["age"] >= min_age]

# # Create Auntie Agent
# rishtey_wali_agent = Agent(
#     name="Auntie",
#     model=model,
#     instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
#     tools=[get_user_data, send_whatsapp_message]
# )

# # Streamlit UI
# st.set_page_config(page_title="💌 Rishtey Wali Auntie", page_icon="💌")
# st.title("💌 Rishtey Wali Auntie")
# st.write("Salamz beta! Main hoon tumhari Rishtey Wali Auntie. Apni age aur WhatsApp number do, main tumhein rishtay doongi!")

# if "history" not in st.session_state:
#     st.session_state.history = []

# user_input = st.text_input("Auntie ko kuch puchho:")

# if st.button("Send") and user_input:
#     st.session_state.history.append({"role": "user", "content": user_input})

#     # Async call in Streamlit (safe way)
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(
#         Runner.run(
#             starting_agent=rishtey_wali_agent,
#             input=st.session_state.history
#         )
#     )
#     loop.close()

#     st.session_state.history.append({"role": "assistant", "content": result.final_output})

# # Chat history display
# for chat in st.session_state.history:
#     if chat["role"] == "user":
#         st.markdown(f"**You:** {chat['content']}")
#     else:
#         st.markdown(f"**Auntie:** {chat['content']}")




#######################################chainlit###############################
# import chainlit as cl
# import asyncio
# import os
# from dotenv import find_dotenv, load_dotenv
# from openai import AsyncOpenAI
# from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
# # import chainlit as cl
# from whatsapp import send_whatsapp_message
# # Load environment variables
# load_dotenv(find_dotenv())
# set_tracing_disabled(True)  # Function call, not variable assignment

# # Gemini API setup
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"

# # External Gemini LLM client
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/"
# )

# model = OpenAIChatCompletionsModel(
#     openai_client=external_client,
#     model=MODEL_NAME
# )

# # Tool function
# @function_tool
# def get_user_data(min_age: int) -> list[dict]:
#     """Retrieve user data based on a minimum age."""
#     users = [
#         {"name": "Muneeb", "age": 22},
#         {"name": "Muhammad Ubaid Hussain", "age": 25},
#         {"name": "Azan", "age": 19},
#     ]
#     return [user for user in users if user["age"] >= min_age]

# # Rishtey wali Auntie Agent
# rishtey_wali_agent = Agent(
#     name="Auntie",
#     model=model,
#     instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches.",
#     tools=[get_user_data,send_whatsapp_message]  # WebSearchTool() ka use sirf OpenAI API key ke sath hoga
# )

# # On Chat Start
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(
#         content="Salamz beta! Main hoon tumhari Rishtey wali Auntie. Apni age aur WhatsApp number do, main tumhein rishtay doongi!"
#     ).send()

# # On Message
# @cl.on_message
# async def main(message: cl.Message):
#     await cl.Message(content="Thinking...").send()

#     history = cl.user_session.get("history") or []
#     history.append({"role": "user", "content": message.content})

#     result = Runner.run_sync(
#         starting_agent=rishtey_wali_agent,
#         input=history
#     )

#     history.append({"role": "assistant", "content": result.final_output})
#     cl.user_session.set("history", history)

#     await cl.Message(content=result.final_output).send()



#############################################chainlit code oper wala

# import asyncio
# import os
# from dotenv import find_dotenv, load_dotenv
# from openai import AsyncOpenAI
# from openai.types.responses import ResponseTextDeltaEvent
# from agents import Agent, Runner, OpenAIChatCompletionsModel,set_tracing_disabled,functiontool
# import chainlit  as cl


# load_dotenv(find_dotenv())
#  set_tracing_disabled = True

#  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0-flash"

# # 🔹 Step 2: Gemini LLM setup
# external_client = AsyncOpenAI(
#     api_key=GEMINI_API_KEY,
#     base_url="https://generativelanguage.googleapis.com/v1beta/"
# )

# model = OpenAIChatCompletionsModel(
#     openai_client=external_client,
#     model=MODEL_NAME
# )
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # external_client =AsyncOpenAI(
# #     api_key = API_KEY,
# #     BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# # )
# # model = OpenAIchatCompletionsMODEL(
# # MODEL = "gemini-2.0-flash"
# # openai_client=external_client
# # )

# @function_tool
# def get_user_data(min_age: int) -> list[dict]:
#     "Retrieve user data based on a minimum age"
#     users = [
#         {"name": "Muneeb", "age": 22},
#         {"name": "Muhammad Ubaid Hussain", "age": 25},
#         {"name": "Azan", "age": 19},
#     ]

#     for user in users:
#         if user["age"] < min_age:
#             users.remove(user)
    
#     return users
#     rishtey_wali_agent = Agent(
#     name="Auntie",
#     model=model,
#     instructions="You are a warm and wise 'Rishtey Wali Auntie' who helps people find matches",
#     tools=[get_user_data, WebSearchTool()]   # WebSearchTool will only work with OpenAI API key, 
#     # if you want to use any other free llm use "browser-use"
#     @cl.on_chat_start
#     async def on_chat_start():
#         await cl.message("Salamz! beta!, I am your Rishtey wali Auntie. Give meyour full details age our whatsapp number and i give  you rishty!")
# )
# @cl.on_message
# async def main(message :cl.Message):
#     awiat cl.Message("t=Thinking..."). send()
#     history = cl.user_session.get("history")or[]
#     history.append({"role":"user","content":message.content}) 

#     result = Runner.run_sync(
#         starting_agent= rishtey_wali_agent,
#         input = history
#     )
# history.append({"role":"assistant","content":result.final_output})
# cl.user_session.set(("history",history))
# await cl.Message(content=result.final_output).send()


# def main():
#     print("Hello from rishty-wali-anutie-streamlit!")


# if __name__ == "__main__":
#     main()
