import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import os
import torch
torch.classes.__path__ = []
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import HumanMessage
from io import StringIO
from PIL import Image
import streamlit.components.v1 as components
from agentic import AgenticWorkflow
from dotenv import load_dotenv
import us_states
import traceback

st.set_page_config(page_title="Simple GenAI App", page_icon="🤖")

load_dotenv()

print(os.getenv('GRANITE_LLM_NAME'))

tab1, tab2 = st.tabs(["Chat", "Agentic"])

try:
    llm = ChatOpenAI(
        model=os.getenv('GRANITE_LLM_NAME'), 
        temperature=0.1,
    )
            
    embed_llm = OpenAIEmbeddings(
        api_key=os.getenv('EMBED_API_KEY'),
        base_url=os.getenv('EMBED_API_BASE'),
        dimensions=768,
        model=os.getenv('EMBED_LLM_NAME'),
    )
except Exception as e:
    st.error(f"An error occurred during model initialization: {str(e)}")
    st.info("Please check your API key and try again.")

with tab1:
    st.title("🤖 Simple Chat App")
    st.write("This app demonstrates integrating with InstructLab-tuned LLMs for various generative AI tasks.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me a question!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message(name="assistant",avatar="images/redhat.png"):
            with st.spinner("Thinking..."):
                try:
                    response = llm.invoke([HumanMessage(content=prompt)])
                    response_content = response.content
                    st.markdown(response_content)
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
with tab2:
    st.title("🤖 Simple Agentic App")
    st.write("This section allows you to search for scholarships, grants, and other state and federal student aid.")
    
    if "messages2" not in st.session_state:
        st.session_state.messages2 = []
        
    with st.sidebar:
        with st.expander("View Agentic Workflow"):
            st.image("images/agentic.png")
            
    if prompt := st.selectbox("Select your state of residence",
                              [""] + us_states.STATES,):
        
        with st.spinner("Working on it..."):

            st.session_state.messages2.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
                
            try:
                workflow = AgenticWorkflow(llm, embed_llm)
                workflow.run(f"I live in {prompt}.", st)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                traceback.print_exc()
    
    