from dotenv import load_dotenv
from typing import Any, Dict, List
from graph.graph_flow import app
import streamlit_app as st


load_dotenv()

if __name__ == "__main__":

    user_query = input("Enter a question about AI in Finance?\n")
    answer = app.invoke(input={"question": user_query})
    print(answer['generation'])