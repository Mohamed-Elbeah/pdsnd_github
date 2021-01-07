# -*- coding: utf-8 -*-
"""
@Edited by: Mohamed Elbeah ™
"""

# Import Necessary Packages
import time
import pandas as pd
import numpy as np

# Three data files available
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to explore? [Chicago, New York City or Washington] ")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("invalid input. Please enter a valid input")

    # get user input for month (all, january, february, ... , june)
    while True:    
        month = input("Which month would you like to filter by? [January, February, March, April, May, June] or type 'all' for all months ")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("invalid input. Please enter a valid input")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Are you looking for a particular day? If so, enter the day as follows: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday] or type 'all' for all days ")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("invalid input. Please enter a valid input")

    print('-'*40)
    return city, month, day

# Note: Washington's lack of user data
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The Most Common Month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The Most Common Day of Week: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The Most Common Start Hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The Most Commonly Used Start Station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The Most Commonly Used End Station: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The Most Frequent Trip:', popular_start_end[0], " --> ", popular_start_end[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: {:.2f} hours".format(total_travel_time/3600))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time: {:.2f} minutes".format(mean_travel_time/60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:')
    print(user_types)

    # Display counts of gender
    try:
      gender_types = df['Gender'].value_counts()
      print('\nCounts of Gender Types: ')
      print(gender_types)
    except KeyError:
      print("No data available for Gender Types.")    

    # Display earliest, most recent, and most common year of birth
    try:
      earliest_year = df['Birth Year'].min()
      recent_year = df['Birth Year'].max()
      common_year = df['Birth Year'].value_counts().idxmax()
      print('\nEarliest Year of Birth:', earliest_year)
      print('Recent Year of Birth:', recent_year)
      print('Common Year of Birth:', common_year)
    except KeyError:
      print("No data available for Birth of Year.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    """Displays individual trip data."""
    r = 0
    while True:
        response = input("Would you like to see 5 lines of raw data? Type yes or no ")
        response = response.lower()

        if response != 'yes':
            break
        else:
            print("Displaying individual trip data: \n")
            print(df.iloc[r: r+5])
            r += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
