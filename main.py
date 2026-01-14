from dotenv import load_dotenv

load_dotenv()

from graph.graph_flow import app

if __name__ == "__main__":

    user_query = input("Enter a question about AI in Finance?\n")
    answer = app.invoke(input={"question": user_query})
    print(answer['generation'])