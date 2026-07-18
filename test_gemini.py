from ai.gemini_chat import ask_teachtwin

notes = """
Database Management System is software used to store and manage data.
"""

question = "What is DBMS?"

answer = ask_teachtwin(notes, question)

print(answer)
