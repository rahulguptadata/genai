from email import message
from turtle import st


import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB",page_icon="KLK")
st.title(" CHat with SQL DB")
INJECTION_WARNING="""sql agents can be vulnerable , use proper roles check [here](https://python.langchain.com/docs/security)
"""

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"
radio_opt=["use SQLLITE3 databse - Student.db","connect to your SQL database"]

selected_opt=st.sidebar.radio(label="Chose the DB which you want to chat",options=radio_opt)
if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("provide my sql host")
    mysql_user=st.sidebar.text_input("provide my sql user")
    mysql_pass=st.sidebar.text_input("provide my sql password")
    mysql_db=st.sidebar.text_input("my sql dabases name")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="Groq api key",type="password")

if not db_uri:
    st.info("please enter db_uri")

if not api_key:
    st.info("provide groq api key")

## llm model

llm=ChatGroq(groq_api_key="",model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")

def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_pass=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"student.db").absolute()
        print(dbfilepath)
        creator=lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri==MYSQL:
        if not(mysql_host and mysql_user and mysql_pass and mysql_db):
            print("please provde details")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}/{mysql_db}"))

if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_pass,mysql_db)
else:
    db=configure_db(db_uri)

##tool kit
toolkit=SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(llm=llm,toolkit=toolkit,verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"]=[{"role":"assistant","content":"How can i help you ?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query=st.chat_input(placeholder="ask anythng from the database")

if user_query:
    st.session_state.messages.append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({"role":"assistent","content":response})
        st.write(response)

