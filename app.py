import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis 1896-2016")
st.sidebar.image(
   'https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
   'Select an Option',
   ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
   st.sidebar.header("Medal Tally")
   years, country = helper.country_year_list(df)

   selected_year = st.sidebar.selectbox("Select Year", years)
   selected_country = st.sidebar.selectbox("Select Country", country)

   medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
   if selected_year == 'Overall' and selected_country == 'Overall':
       st.title("Overall Tally")
   if selected_year != 'Overall' and selected_country == 'Overall':
       st.title("Medal Tally in " + str(selected_year) + " Olympics")
   if selected_year == 'Overall' and selected_country != 'Overall':
       st.title(selected_country + " overall performance")
   if selected_year != 'Overall' and selected_country != 'Overall':
       st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
   st.table(medal_tally)

if user_menu == 'Overall Analysis':
   editions = df['Year'].unique().shape[0] - 1
   cities = df['City'].unique().shape[0]
   sports = df['Sport'].unique().shape[0]
   events = df['Event'].unique().shape[0]
   athletes = df['Name'].unique().shape[0]
   nations = df['region'].unique().shape[0]

   st.title("Top Statistics")
   col1, col2, col3 = st.columns(3)
   with col1:
       st.header("Editions")
       st.title(editions)
   with col2:
       st.header("Hosts")
       st.title(cities)
   with col3:
       st.header("Sports")
       st.title(sports)

   col1, col2, col3 = st.columns(3)
   with col1:
       st.header("Events")
       st.title(events)
   with col2:
       st.header("Nations")
       st.title(nations)
   with col3:
       st.header("Athletes")
       st.title(athletes)

   nations_over_time = helper.data_over_time(df, 'region')
   fig = px.line(nations_over_time, x="Edition", y="region")
   st.title("Participating Nations over the years")
   st.plotly_chart(fig)

   events_over_time = helper.data_over_time(df, 'Event')
   fig = px.line(events_over_time, x="Edition", y="Event")
   st.title("Events over the years")
   st.plotly_chart(fig)

   athlete_over_time = helper.data_over_time(df, 'Name')
   fig = px.line(athlete_over_time, x="Edition", y="Name")
   st.title("Athletes over the years")
   st.plotly_chart(fig)

   # Assuming you want to plot the number of events for each sport over the years
   st.title("No. of Events over time (Every Sport)")

   # Create figure and axis
   fig, ax = plt.subplots(figsize=(20, 20))  # Unpack the figure and axis

   # Prepare your data
   x = df.drop_duplicates(['Year', 'Sport', 'Event'])

   # Create a pivot table for the heatmap
   heatmap_data = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')

   # Plot heatmap using the axis 'ax'
   sns.heatmap(heatmap_data, annot=True, ax=ax)

   # Pass only the figure object to Streamlit for rendering
   st.pyplot(fig)  # fig is the figure object, not the tuple

   st.title("Most successful Athletes Top 20")
   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')



   selected_sport = st.selectbox('Select a Sport', sport_list)
   x = helper.most_successful(df, selected_sport)
   if x is not None and not x.empty:
       st.table(x)
   else:
       st.warning("No data available for the selected sport.")



if user_menu == 'Country-wise Analysis':
   st.sidebar.title('Country-wise Analysis')

   country_list = df['region'].dropna().unique().tolist()
   country_list.sort()

   selected_country = st.sidebar.selectbox('Select a Country', country_list)

   country_df = helper.yearwise_medal_tally(df, selected_country)
   fig = px.line(country_df, x="Year", y="Medal")
   st.title(selected_country + " Medal Tally over the years")
   st.plotly_chart(fig)

   st.title(selected_country + " excels in the following sports")
   pt = helper.country_event_heatmap(df, selected_country)
   # Changes Made Here
   fig, ax = plt.subplots(figsize=(20, 20))
   sns.heatmap(pt, annot=True, ax=ax)
   st.pyplot(fig)

   st.title("Top 10 athletes of " + selected_country)
   # Call the most_successful_countrywise function
   top_athletes = helper.most_successful_countrywise(df, selected_country)

   # Check if the result is valid and display it
   if top_athletes is not None and not top_athletes.empty:
       st.table(top_athletes)
   else:
       st.warning("No data available for the selected country.")

if user_menu == 'Athlete wise Analysis':
   athlete_df = df.drop_duplicates(subset=['Name', 'region'])

   x1 = athlete_df['Age'].dropna()
   x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
   x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
   x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

   fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
   fig.update_layout(autosize=False, width=1000, height=600)
   st.title("Distribution of Age")
   st.plotly_chart(fig)

   x = []
   name = []
   famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                    'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens',
                    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
   for sport in famous_sports:
       temp_df = athlete_df[athlete_df['Sport'] == sport]
       x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
       name.append(sport)

   fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
   fig.update_layout(autosize=False, width=1000, height=600)
   st.title("Distribution of Age wrt Sports (Gold Medalist)")
   st.plotly_chart(fig)

   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')

   st.title("Men vs Women Athletes (1896 to 2016)")

   # Call the men_vs_women function
   gender_counts = helper.men_vs_women(df)

   # Display the results
   if gender_counts is not None and not gender_counts.empty:
       # Create a line plot
       plt.figure(figsize=(12, 6))
       plt.plot(gender_counts['Year'], gender_counts['Male'], label='Male', marker='o')
       plt.plot(gender_counts['Year'], gender_counts['Female'], label='Female', marker='o')

       # Customizing the plot
       plt.title('Number of Male and Female Athletes (1896 to 2016)')
       plt.xlabel('Year')
       plt.ylabel('Number of Athletes')
       plt.xticks(gender_counts['Year'], rotation=45)  # Ensure years are displayed
       plt.legend()
       plt.grid()

       # Show the plot in Streamlit
       st.pyplot(plt)
   else:
       st.warning("No data available for the selected criteria.")

   st.title("Height vs Weight Analysis(Filtered- NA & No Medal)")

   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')

   selected_sport = st.selectbox('Select a Sport', sport_list)

   # Call the weight_v_height function
   filtered_data = helper.weight_v_height(df, selected_sport)

   # Display the filtered data
   if filtered_data is not None and not filtered_data.empty:
       st.table(filtered_data)
   else:
       st.warning("No data available for the selected sport or all data has missing height/weight or 'No Medal'.")

