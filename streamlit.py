import streamlit as st
import requests

API_URL="http://localhost:8000"

st.title("To-Do List")


#fetch task from backend
response=requests.get(f'{API_URL}/notes')
if response.status_code==200:
    tasks=response.json()
else:
    st.error('failed to load error')
    tasks=[]


#add new task
title=st.text_input("enter Title",placeholder="Groceries")
content=st.text_area("Enter content")
new_task={'title':title,'content':content}
btn=st.button("Add Task")

if btn:
    if new_task:
        res=requests.post(f'{API_URL}/notes',json=new_task)
        if res.status_code==200:
            st.success("task added")
            st.experimental_rerun()
        else:
            st.error("failed to add task")



#show task
for task in tasks:
    col1, col2, col3 = st.columns([0.7,0.15,0.15])
    with col1:
        st.write(f"{task['task']}")
        st.caption(f"{task['content']}") 
    with col2:
        if st.button("",key=f"done_{task['id']}"):
            requests.put(f"{API_URL}/notes/{task['id']}")
            st.experimental_rerun()

    with col3:
        if st.button("",key=f"delete_{task['id']}"):
            requests.delete(f"{API_URL}/notes/{task['id']}")
            st.experimental_rerun()