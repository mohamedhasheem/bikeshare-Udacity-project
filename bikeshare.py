'''

                            bikeshare project for udacity
                            data analysis nanodegree by ITIDA
                            by Mohamed Hashem


'''
import time
import pandas as pd
import numpy as np
from scipy import stats

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS_LIST = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

ROW_ANS_LIST = ['yes', 'no']

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
        city = input("Please enter a city (chicago, new york city, washington)? ").lower()
        if city not in CITY_DATA:
            print("Please enter a valid city.")
        else:
            print("Your selected city is: ", city)
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter a month (all, january, february, ... , june)? ").lower()
        if month not in MONTHS_LIST:
            print("Please enter a valid month.")
        else:
            print("Your selected month is: ", month)
            break
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter a day of week (all, monday, tuesday, ... sunday)? ").lower()
        if day not in DAYS_LIST:
            print("Please enter a valid day of week.")
        else:
            print("Your selected day of week: ", day)
            break

    print('-'*40)
    return city, month, day


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

    try:
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month_number'] = df['Start Time'].dt.month
        df['weekday_name'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour

        if month != 'all':
            month_number = MONTHS_LIST.index(month) + 1
            df = df[df['month_number'] == month_number]

        if day != 'all':
            df = df[df['weekday_name'].str.lower() == day]
            
        return df
    
    except Exception as e:
        print("Error occurred while loading the file")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        most_common_month_number = df['month_number'].mode()[0]
        most_common_month_name = MONTHS_LIST[most_common_month_number - 1]
        print('The most common month in the selected city is: ', most_common_month_name)
        
    except Exception as e:
        print('Error occurred while calculating the most common month')

    # display the most common day of week
    try:
        most_common_weekday_name = df['weekday_name'].mode()[0]
        print('The most common weekday in the selected city is: ', most_common_weekday_name)
        
    except Exception as e:
        print('Error occurred while calculating the most common weekday')


    # display the most common start hour
    try:
        most_common_start_hour = df['hour'].mode()[0]
        print('The most common start hour in the selected city is: ', most_common_start_hour)
        
    except Exception as e:
        print('Error occurred while calculating the most common start hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_common_start_station = df['Start Station'].mode()[0]
        start_station_use_count = df['Start Station'].value_counts(sort=True, ascending=False)[0]
        print('The most commonly used start station in the selected city is: ', most_common_start_station, ' and was used: ', start_station_use_count, ' times')
        
    except Exception as e:
        print('Error occurred while calculating the most commonly used start station')

    # display most commonly used end station
    try:
        most_common_end_station = df['End Station'].mode()[0]
        end_station_use_count = df['End Station'].value_counts(sort=True, ascending=False)[0]
        print('The most commonly used end station in the selected city is: ', most_common_end_station, ' and was used: ', end_station_use_count, ' times')
        
    except Exception as e:
        print('Error occurred while calculating the most commonly used end station')

    # display most frequent combination of start station and end station trip
    try:
        most_common_trip = (df["Start Station"] + " TO " + df["End Station"]).mode()[0]
        most_common_trip_count = (df["Start Station"] + df["End Station"]).value_counts(sort=True, ascending=False)[0]
        print('The most frequent trip is: ', most_common_trip, '\n and was used: ', most_common_trip_count,' times')
        
    except Exception as e:
        print('Error occurred while calculating the most frequent combination of start station and end station trip')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    try:
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['trip_duration'] = df['End Time'] - df['Start Time']
        total_trips_duration = df['trip_duration'].sum()
        print('The total trips duration in the selected city is:', total_trips_duration)
        
    except Exception as e:
        print('Error occured while calculaing the total trips duration')

    # display mean travel time
    try:
        trip_duration_mean = df['trip_duration'].mean()
        print('The mean travel time in the selected city is:', trip_duration_mean)
        
    except Exception as e:
        print('Error occured while calculaing the mean travel time')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        user_types_and_counts = df['User Type'].value_counts()
        print('User types and corresponding counts in the selected city are: \n', user_types_and_counts)
        
    except Exception as e:
        print('Error occured while calculating the user types and counts')

    # Display counts of gender
    try:
        gende_counts = df['Gender'].value_counts()
        print('User types and corresponding counts in the selected city are: \n', gende_counts)
        
    except Exception as e:
        print('Error occured while calculating the user gender counts')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The earliest birth year is: ', int(earliest_birth_year))
        print('The most recent_birth_year birth year is: ', int(most_recent_birth_year))
        print('The most common birth year is: ', int(most_common_birth_year))
        
    except Exception as e:
        print('Error occured while calculating the earliest, most recent, and most common year of birth')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    #solving a code review issue as it's required
    #Function to display the row data as per user's request 
def display_data(df):
    row_data = ''
    rows = 0
    while row_data not in ROW_ANS_LIST:
        row_data = input("Do you want to see raw data, yes or no?\n").lower()
        if row_data == "yes":
            print(df.head())
        elif row_data == "no":
            print("no row data displayed as per user entry")
        elif row_data not in ROW_ANS_LIST:
            print("please check your entry and enter a valid option")

    #while loop to check if user want to see extra 5 rows as required in code review
    while row_data == 'yes':
        rows += 5
        row_data = input("Do you want to see extra 5 raws data?\n").lower()
        if row_data == "yes":
            print(df[rows:rows+5])
        elif row_data != "yes":
            print("no more row data displayed as per user entry")
            break

    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
