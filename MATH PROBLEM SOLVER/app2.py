import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# Configure Streamlit app
st.set_page_config(page_title="Math Solver & Data Assistant")
st.title("Text to Math Problem Solver Using Google Gemma2")

# Sidebar for Groq API key input
groq_api_key = st.sidebar.text_input("Enter Groq API key", type="password")

# Stop execution if no key provided
if not groq_api_key:
    st.info("Please add your Groq API key to continue.")
    st.stop()

# Initialize LLM
llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

# Set up Wikipedia tool
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Search Wikipedia for general information about any topic."
)

# Set up math solving tool
math_chain = LLMMathChain(llm=llm, verbose=False)
calculator_tool = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Solve math expressions. Only use for pure mathematical computations."
)

# Custom prompt for logic/reasoning questions
prompt = """
You are a math assistant that solves user questions.
Provide a detailed step-by-step solution, point by point.

Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

# Chain to handle reasoning tasks
reasoning_chain = LLMChain(llm=llm, prompt=prompt_template)
reasoning_tool = Tool(
    name="Reasoning Tool",
    func=reasoning_chain.run,
    description="Handles logic-based or descriptive math questions."
)

# Initialize agent with tools
agent_executor = initialize_agent(
    tools=[wikipedia_tool, calculator_tool, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I'm your math assistant. Ask me any question involving calculations or concepts."}
    ]

# Render past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input area
question = st.text_area("Type your math or reasoning question here:")

# Handle submission
if st.button("Solve"):
    if question.strip():
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        with st.spinner("Thinking..."):
            callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            try:
                response = agent_executor.run(question, callbacks=[callback])
            except Exception as e:
                response = f"An error occurred while processing your question: {e}"

        # Clean response from smart unicode characters
        response = response.replace("’", "'").replace("“", '"').replace("”", '"')

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
        st.success("Here is your answer!")
    else:
        st.warning("Please enter a question before clicking the solve button.")
