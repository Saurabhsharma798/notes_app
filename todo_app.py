import streamlit as st
import requests

API_URL="http://localhost:8000"

st.title("To-Do List")

if 'token' not in st.session_state:
    st.session_state['token']=None

if  st.session_state['token'] is None:
    st.subheader('Log In  or Sign Up')
    mode=st.radio("choose action",['Login','Signup'])
    username=st.text_input("username")
    password=st.text_input("password",type='password')
    
    
    if mode=="Login":

        if st.button('login'):
            res=requests.post(f"{API_URL}/auth/login",data={'username':username,'password':password})
            if res.status_code==200:
                token=res.json()['access_token']
                st.session_state['token']=token
                st.success("logged in successfully")
                st.rerun()
            else:
                st.error('login failed')
        st.stop()
    else:
        if st.button('Signup'):
            res=requests.post(f"{API_URL}/auth/signup",json={'username':username,'password':password})
            if res.status_code == 200:
                # st.success("Account Created! Please Login.")
                login_res=requests.post(f"{API_URL}/auth/login",data={'username':username,'password':password})
                if login_res.status_code==200:
                    token=res.json()['access_token']
                    st.session_state['token']=token
                    st.success("logged in successfully")
                    st.rerun()
                else:
                    st.error("user registered! please try logging in")
            
            else:
                st.error("sign up failed username may already exist")
        st.stop()
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'token': None}))

#fetch task from backend
headers={'Authorization':f"Bearer {st.session_state['token']}"}
response=requests.get(f'{API_URL}/notes',headers=headers)


if response.status_code==200:
    tasks=response.json()
else:
    st.error('failed to load error')
    tasks=[]
    st.stop()


#add new task
title=st.text_input("enter Title",placeholder="Groceries")
content=st.text_area("Enter content",placeholder="2 kilo aalo,1 kilo tamatar")
new_task={'title':title,'content':content}
btn=st.button("Add Task")

if btn:
    if title and content:
        res=requests.post(f'{API_URL}/notes',json=new_task,headers=headers)
        if res.status_code==200:
            st.success("task added")
            st.rerun()
        else:
            st.error("failed to add task")
    else:
        st.warning('title and content cannot be empty')


if 'edit_id' not in st.session_state:
    st.session_state['edit_id']=None
#show task
for task in tasks:
    col1, col2, col3 = st.columns([0.7,0.15,0.15])
    with col1:
        st.write(f"{task['title']}")
        st.caption(f"{task['content']}") 
    with col2:
        if st.button("Edit✏️",key=f"edit_{task['id']}"):
            st.session_state.edit_id=task['id']
            st.session_state.edit_title=task['title']
            st.session_state.edit_content=task['content']

    with col3:
        if st.button("Del🗑️",key=f"delete_{task['id']}"):
            requests.delete(f"{API_URL}/notes/{task['id']}",headers=headers)
            st.rerun()


if st.session_state.edit_id:
    st.subheader("Update Task")
    new_title=st.text_input("update title",value=st.session_state.edit_title)
    new_content=st.text_area("update content",value=st.session_state.edit_content)
    if st.button("Update"):
        update_data={'title':new_title,'content':new_content}
        res=requests.put(f"{API_URL}/notes/{st.session_state.edit_id}",json=update_data,headers=headers)

        if res.status_code == 200:
            st.success("task updated")
            st.session_state.edit_id=None
            st.rerun()
        else:
            st.error("failed to update task")
    if st.button("Cancel"):
        st.session_state.edit_id=None
        st.rerun()