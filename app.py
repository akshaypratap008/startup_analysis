import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('startup_clean.csv')
df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
df['month'] = df['date'].dt.month_name()
df['year'] = df['date'].dt.year
# st.dataframe(df)

# st.set_page_config(layout='wide', page_title='Startup Analysis')
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investors'])

st.set_page_config(layout='wide', page_title='Satrtup Analysis')


def load_investor_details(investor):
    st.title(investor)

    #load recent 5 investments for the investor
    st.subheader('Most Recent Investments')    
    last5_df = df[df['investor'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    #load biggest investment
    with col1: 
        st.subheader('Biggest Investments')
        big_series = df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots(figsize =(8,6))
        ax.bar(big_series.index, big_series.values)
        fig.tight_layout()
        plt.xlabel('Startup Name')
        plt.ylabel('Price in crores')
        st.pyplot(fig)  

    #load investment sectors
    with col2:
        vertical_series = df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots(figsize =(8,6))
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.2f%%")
        fig1.tight_layout()
        # ax1.legend()
        st.pyplot(fig1)

    #load investment round and city
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Investment round')
        round_series = df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum()
        fig, ax = plt.subplots(figsize =(7,5))
        ax.pie(round_series, autopct='%0.2f%%', labels=round_series.index)
        
        st.pyplot(fig)

    with col2:
        st.subheader('Invested in cities')
        cities_series = df[df['investor'].str.contains(investor)].groupby('city')['amount'].sum()
        fig, ax = plt.subplots(figsize =(7,5))
        ax.pie(cities_series, autopct='%0.2f%%', labels=cities_series.index)
        # fig.tight_layout()
        # plt.legend()
        st.pyplot(fig)

    #yoy investment
    st.subheader('Year on Year Total Investment')
    year_investment = df[df['investor'].str.contains(investor)].groupby(df['date'].dt.year)['amount'].sum()
    fig, ax = plt.subplots(figsize=(8,6))
    ax.plot(year_investment.index, year_investment.values)
    fig.tight_layout()
    
    plt.xlabel('Year')
    plt.ylabel('Amount in Crores(INR)')
    st.pyplot(fig)
    
    #similar investor as per the sector
    st.subheader('Similar Investor')

    filtered_df = df[df['investor'] == investor]

    if not filtered_df.empty:
        vertical_counts = filtered_df['vertical'].value_counts()
        if not vertical_counts.empty:
            popular_vertical = vertical_counts.idxmax()
            similar_df = df[(df['vertical'] == popular_vertical) & (df['investor'] != investor)]
            if not similar_df.empty:
                similar_investor = similar_df['investor'].value_counts().head(3).index.tolist()
                st.write(similar_investor)
            else:
                st.write("No similar investors found for this vertical.")
        else:
            st.write("No vertical data found for this investor.")
    else:
        st.write("Investor not found in dataset.")

def load_overall_analysis():

    # total amount invested
    total = round(df['amount'].sum())

    #companies with max funding
    max_funding = round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()[0])

    #avg funding 
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())

    #total startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max Funding',  str(max_funding) + ' Cr')
    with col3:
        st.metric('Avg Funding', str(avg_funding) + ' Cr')
    with col4:
        st.metric('Funded Startups', num_startups)

    # MoM chart --> Total + count
    st.header('Month on Month Graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)

    fig3, ax3 = plt.subplots(figsize = (10,6))
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    plt.setp(ax3.get_xticklabels(), rotation=90)
    st.pyplot(fig3)



def load_startup_details(startup):
    st.title(startup)

if option == 'Overall Analysis':
    st.title('Overall Analysis')
    load_overall_analysis()


elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)

    st.title('Startup Analysis')

elif option == 'Investors':
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select an investor', sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
