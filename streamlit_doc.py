import streamlit as st
import pandas as pd
import time

email = st.text_input('Enter email')
password = st.number_input('Enter password')
gender = st.selectbox('Select Gender', ['Male', 'Female'])

btn = st.button('Login')

#if btn is clicked
if btn:
    if email == 'akshay@gmail.com' and password == 12345:
        st.success('Login successfull')
        st.write(gender)
        st.balloons()
    else:
        st.error('Login Failed')

# title
st.title('Startup Dashboard')

# header and subheader
st.header('I am learning Streamlit')
st.subheader('I am loving it!')

# write -- to write things like a paragraph as normal text
st.write('Normal text.. Aksha.. ')

# markdown
st.markdown('''
        ### My favorite movies
        - Race 3
        - Humshakals
        - Akshay
        - Housefull
''')

# code in streamlit 
st.code('''
        def foo(input):
            return foo**2

        x = foo(2)
''')

# Latex -- design language(helpful in mathematical equations)
st.latex('x^2 + y^2 = 1')

## Display elements 
# Dataframe
df = pd.DataFrame({
    'name': ['nitish', 'akshay', 'Preet'],
    'marks': [22, 33, 45]
})

st.dataframe(df)

#Metrics
st.metric('Revenue', 'Rs 3L', '-3%')

#json
st.json({
    'name': ['nitish', 'akshay', 'Preet'],
    'marks': [22, 33, 45]
})

#displaying media- image, audio and video
st.image('streamlit-logo.png')

## creating layouts
# creating a sidebar
st.sidebar.title('Side bar title')

#creating column
col1 , col2 = st.columns(2)
with col1:
    st.metric('Age', '+7%')

with col2:
    st.metric('Revenue', '-5%')

## showing status
st.error('Login Failed')
st.success('Login Successfully')
st.warning('Not valid')
st.info('only integers ')

#progress bar
bar = st.progress(0)

# for i in range(1, 101):
#     time.sleep(0.1)
#     bar.progress(i)

#file uploader
file = st.file_uploader('Upload a csv file')

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())



