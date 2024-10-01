import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):
   medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
   flag = 0
   temp_df = pd.DataFrame()

   if year == 'Overall' and country == 'Overall':
       temp_df = medal_df
   if year == 'Overall' and country != 'Overall':
       flag = 1
       temp_df = medal_df[medal_df['region'] == country]
   if year != 'Overall' and country == 'Overall':
       temp_df = medal_df[medal_df['Year'] == int(year)]
   if year != 'Overall' and country != 'Overall':
       temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

   if flag == 1:
       x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
   else:
       x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

   x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

   x['Gold'] = x['Gold'].astype('int')
   x['Silver'] = x['Silver'].astype('int')
   x['Bronze'] = x['Bronze'].astype('int')
   x['total'] = x['total'].astype('int')

   return x


def country_year_list(df):
   years = df['Year'].unique().tolist()
   years.sort()
   years.insert(0, 'Overall')

   country = np.unique(df['region'].dropna().values).tolist()
   country.sort()
   country.insert(0, 'Overall')

   return years,country


def data_over_time(df, col):
   nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()

   # Check column names after reset_index()
   nations_over_time.columns = ['Edition', col]  # Explicitly naming the columns

   return nations_over_time.sort_values('Edition')


def most_successful(df, sport):
   # Filter for rows with medals
   temp_df = df.dropna(subset=['Medal'])

   # If a specific sport is selected, filter by that sport
   if sport != 'Overall':
      temp_df = temp_df[temp_df['Sport'] == sport]

   # Count the number of medals for each athlete (Name)
   medal_counts = temp_df['Name'].value_counts().reset_index()

   # Rename columns for clarity
   medal_counts.columns = ['Name', 'Medals']  # Set correct column names directly

   # Get the top 20 athletes based on the number of medals
   top_20 = medal_counts.head(20)

   # Debugging: Check the columns and content before merging
   print("Top 20 medal_counts columns:", top_20.columns)
   print("Top 20 medal_counts head:", top_20.head())

   # Merge with the original DataFrame to get additional details
   result = top_20.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

   # Debugging: Check the result after merging
   print("Result columns:", result.columns)
   print("Result head:", result.head())

   return result




def yearwise_medal_tally(df,country):
   temp_df = df.dropna(subset=['Medal'])
   temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

   new_df = temp_df[temp_df['region'] == country]
   final_df = new_df.groupby('Year').count()['Medal'].reset_index()

   return final_df

def country_event_heatmap(df,country):
   temp_df = df.dropna(subset=['Medal'])
   temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

   new_df = temp_df[temp_df['region'] == country]

   pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
   return pt


def most_successful_countrywise(df, country):
   # Filter for rows with medals and the selected country
   temp_df = df.dropna(subset=['Medal'])
   temp_df = temp_df[temp_df['region'] == country]

   # Count the number of medals for each athlete (Name)
   medal_counts = temp_df['Name'].value_counts().reset_index()
   medal_counts.columns = ['Name', 'Medals']  # Set correct column names

   # Get the top 10 athletes
   top_10 = medal_counts.head(10)

   # Merge with the original DataFrame to get additional details
   result = top_10.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

   return result


def weight_v_height(df, sport):
   # Drop duplicates based on athlete's name and region
   athlete_df = df.drop_duplicates(subset=['Name', 'region'])

   # Fill NaN values in the 'Medal' column with 'No Medal'
   athlete_df['Medal'].fillna('No Medal', inplace=True)

   # Filter based on the selected sport
   if sport != 'Overall':
      temp_df = athlete_df[athlete_df['Sport'] == sport]
   else:
      temp_df = athlete_df

   # Filter out athletes where either Height or Weight is NaN and those with 'No Medal'
   temp_df = temp_df.dropna(subset=['Height', 'Weight'])
   temp_df = temp_df[temp_df['Medal'] != 'No Medal']

   # Ensure we return only relevant columns
   return temp_df[['Name', 'Height', 'Weight', 'Medal', 'Sport', 'region']]


def men_vs_women(df):
   # Drop duplicates based on athlete's name and region
   athlete_df = df.drop_duplicates(subset=['Name', 'region'])

   # Count male athletes by year
   men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
   men.rename(columns={'Name': 'Male'}, inplace=True)

   # Count female athletes by year
   women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
   women.rename(columns={'Name': 'Female'}, inplace=True)

   # Merge male and female counts
   final = men.merge(women, on='Year', how='outer')
   final.fillna(0, inplace=True)  # Replace NaN values with 0

   # Filter for years from 1896 to 2016
   final = final[(final['Year'] >= 1896) & (final['Year'] <= 2016)]

   return final

