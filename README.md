# Text-to-Math-Problem-Solver-Using-Google-Gemma2

This is a Streamlit web application that allows users to input math and reasoning-based questions. The app uses **Google Gemma2** via **Langchain** and integrates multiple tools including a calculator, a Wikipedia search utility, and a custom reasoning engine to provide accurate and detailed solutions.

## Features

* **Math Solver**: Solves pure math expressions using LLMMathChain.
* **Wikipedia Search**: Retrieves relevant information for general knowledge and conceptual queries.
* **Reasoning Engine**: Handles logic-based or descriptive math problems with step-by-step explanations.
* **Streamlit UI**: Simple and interactive user interface for easy question submission and real-time responses.

## Technologies Used

* [Streamlit](https://streamlit.io/)
* [LangChain](https://www.langchain.com/)
* [Groq API](https://console.groq.com/)
* [Google Gemma2 Model (via LangChain Groq)](https://groq.com/)
* WikipediaAPIWrapper from Langchain Community Tools

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/math-solver-app.git
   cd math-solver-app
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**

   ```bash
   streamlit run app.py
   ```

4. **Enter Groq API Key**

   * Provide your [Groq API key](https://console.groq.com/) in the sidebar to start using the application.

## Usage

* Input your math or logic question in the provided text area.
* Click the "Solve" button.
* The assistant will return a detailed answer using one or more integrated tools.

## Notes

* This application uses **Groq's Gemma2 model**. Ensure you have a valid API key.
* Wikipedia is used for factual lookup and may occasionally return approximate results.