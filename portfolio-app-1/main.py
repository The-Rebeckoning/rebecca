import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt

# Create dataframe
df = pd.read_csv('drug-use-by-age.csv')
df = df.rename(columns={'alcohol-use':'Alcohol',
                                'marijuana-use':'Marijuana',
                                'cocaine-use':'Cocaine',
                                'crack-use':'Crack',
                                'heroin-use':'Heroin',
                                'hallucinogen-use':'Hallucinogen',
                                'oxycotin-use':'Oxycotin',
                                'meth-use':'Meth'})

drugs =['Alcohol','Marijuana','Cocaine','Crack','Heroin','Meth']


st.title("Understanding addiction")
st.markdown('''
    This is an interactive dashboard that invites users to analyze substance use by age with the goal of preventing addiction. 

    This data is from the National Survey on Drug Use and Health (NSDUH). The survey asked participants whether they used a particular substance at least once in the last 12 months.

    The substances included in the study are alcohol, meth, cocaine, marijuana, heroin and crack.

    **Source**: [National Survey on Drug Use and Health from the Substance Abuse and Mental Health Data Archive](https://www.samhsa.gov/data/report/2020-nsduh-detailed-tables).
    ''')

st.header("Key takeways")
st.subheader("Alcohol is the most widely used substance")
st.metric(label="Percent of 15 year olds who have used alcohol in the last 12 months", value="29.2%")

# Create line graph for key takeway one

df_columns = ["age"]

for drug in drugs:
    df_columns.append(drug)


semi_final_frame_data = df[df_columns]

final_frame_data = semi_final_frame_data.melt(id_vars=["age"],var_name="Drug",value_name="Value")

final_frame_data = final_frame_data.rename(columns={'Value':'Percentage'})

chart = alt.Chart(final_frame_data).mark_line().encode(
x=alt.X('age'),
y=alt.Y('Percentage'),
color='Drug:N'
).properties(title = "Substance use estimates for all respondents")
st.altair_chart(chart, use_container_width=True) 


st.markdown('''
To prevent addiction, policymakers should consider when and why young people drink. Marijuana, crack and cocaine make up a much smaller percentage of substance usage. 
''')

st.subheader("Early twenties have the highest substance use rates")


st.metric(label="Percent of 21 year olds who have used cocaine", value="4.8%")



# Create a dataframe with just the columns we need
segemented_df=df[['age','Alcohol','Marijuana','Cocaine','Crack', 'Heroin','Meth']]

# Create chart data for 21 year old substance use
twenty_one_df = segemented_df.query("age == '21'")

# Melt the dataframe so that the drug use values are organized by column and data can be created as a histogram.

twenty_one_df = pd.melt(twenty_one_df, id_vars =['age'], value_vars = drugs)

# Set the index to the drug

twenty_one_df = twenty_one_df.set_index('variable')

# Rename the columns for readibility

twenty_one_df = twenty_one_df.rename(columns={'value':'Percentage'}).rename_axis("Drug")

fig=px.bar(twenty_one_df , x="Percentage", orientation='h')

# Update title

fig.update_layout(title_text='Substance use for 21 year olds')

st.write(fig)

st.markdown('''
Health practioners should consider why people in the early twenties use substances and what makes them choose to stop as they get older. 
''')

st.subheader("Illegal drug use is erratic")

df_columns = ["age"]

illegal_drugs = ["Cocaine","Meth","Crack"]

for drug in illegal_drugs:
    df_columns.append(drug)


semi_final_frame_data = df[df_columns]

final_frame_data = semi_final_frame_data.melt(id_vars=["age"],var_name="Drug",value_name="Value")

final_frame_data = final_frame_data.rename(columns={'Value':'Percentage'})

chart = alt.Chart(final_frame_data).mark_line().encode(
x=alt.X('age'),
y=alt.Y('Percentage'),
color='Drug:N'
).properties(title = "Illegal substance use estimates for all respondents")
st.altair_chart(chart, use_container_width=True) 



st.markdown('''Comparing cocaine, crack and meth use varies greatly so preventing usage will require a specialized approach.
''')

st.header("Interactive dashboards")

# First interactive line plot

st.subheader("Compare drug use by age")

drug_selection = st.multiselect(
    label = 'Pick the drugs to compare', options =
    drugs, default=["Alcohol"])

st.subheader("You selected:")

for i in drug_selection:
    st.write(i)

df_columns = ["age"]
for drug in drug_selection:
    df_columns.append(drug)

# Second interactive histogram

semi_final_frame_data = df[df_columns]

final_frame_data = semi_final_frame_data.melt(id_vars=["age"],var_name="Drug",value_name="Value")

final_frame_data = final_frame_data.rename(columns={'Value':'Percentage'})

chart = alt.Chart(final_frame_data).mark_line().encode(
x=alt.X('age'),
y=alt.Y('Percentage'),
color='Drug:N'
)
st.altair_chart(chart, use_container_width=True) 






st.subheader("Drug use by age")
age_group_list = list(df['age'].unique())

# Interactive dashboards showing substance use by age group

age_group_selection = st.selectbox(label = "Choose an age group", options = age_group_list)

chart_data = segemented_df[ (segemented_df['age'] == age_group_selection )]
del chart_data[chart_data.columns[0]]
values = np.array(chart_data)
values = values.tolist()
final_values = values[0]

dict_from_list = {k: v for k, v in zip(drugs, final_values)}


final_frame_data = pd.DataFrame(dict_from_list, index = range(1))

result = final_frame_data.transpose()
result = result.rename(columns={0:'Percentage'}).rename_axis("Drug")

st.write(result)

fig=px.bar(result, x="Percentage",orientation='h')
st.write(fig)

st.header("About the data")
st.markdown("""

    SAMHSA suspended in-person data collection on the 2020 NSDUH on March 16, 2020 because of the
    COVID-19 pandemic. With administrative approval, a small-scale data collection effort was conducted during Quarter 3 from July 16 to 22, 2020.

    To reduce the impact on NSDUH data collection due to the COVID-19 pandemic, SAMHSA approved the addition of web-based data collection on September 11, 2020. 

    In Quarter 4 of 2020 (i.e., October to December), web-based interviewing became the primary form
    of NSDUH data collection. Conventional in-person data collection was carried out wherever it
    was considered safe to do so based on county- and state-level COVID-19 metrics. 

    """)

st.subheader("Survey Design")

st.markdown("""
    The coordinated sample design is state based with an independent, multistage area probability sample.
    States are viewed as the first level of stratification. Each state is further stratified into approximately equally populated state sampling regions (SSRs). Creation of each year’s multistage area probability sample then involves selecting census tracts within each SSR, census block groups within census tracts, and area
    segments (i.e., a collection of census blocks) within census block groups. Finally, dwelling units
    (DUs) are selected within segments, and within each selected DU, up to two residents who are at
    least 12 years old are selected for interviewing.

    """)
st.subheader("The raw data")
st.write(df)

