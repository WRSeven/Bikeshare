import time
import pandas as pd
import numpy as np
import os

# Valid data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

WEEK_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # User input for city, month, day with validation
    while True:
        city = str(input("Enter city name (chicago, new york city, washington): ").lower().strip())
        if city in CITY_DATA:
            print(f"Valid: {city}")
            break
        else:
            print("Invalid. Please choose chicago, new york city, or washington")
    while True:
        month = str(input("Enter month (all, january, february, ... , june): ").lower().strip())
        if month in MONTH_DATA:
            print(f"Valid: {month}")
            break
        else:
            print("Invalid: Enter month (all, january, february, ... , june): ")
    while True:
        day = str(input("Enter day of week (all, monday, tuesday, ... sunday): ").lower().strip())
        if day in WEEK_DATA:
            print(f"Valid: {day}")
            break
        else:
            print("Invalid: Enter day of week (all, monday, tuesday, ... sunday): ")
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
    # Check path of the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.normpath(os.path.join(script_dir, '..', 'data'))  # Navigate to the data directory
    file_path = os.path.join(data_dir, CITY_DATA[city])

    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Remove NaN values
    if df.isnull().values.any():
        print("Warning: DataFrame had NaN values. NaN values removed.")
        df = df.dropna()
    else:
        print("No NaN values.")

    # Convert Start Time in datetime-format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract Month and Day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
                                
    # Filter Month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter Day
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]
    
    print("DataFrame loaded and filtered.")
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # Displays statistics on the most frequent times of travel
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month_name = ['January', 'February', 'March', 'April', 'May', 'June'][most_common_month - 1]
    print(f"Most common month: {most_common_month_name}")
    
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day: {most_common_day}")
    
    # display the most common start hour
    most_comon_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"Most common hour: {most_comon_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    #Displays statistics on the most popular stations and trip.
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {most_common_start_station}")

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {most_common_end_station}")

    # display most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    most_common_start_end_station = df['Start-End Combination'].mode()[0]
    print(f"Most common trip from start to end station: {most_common_start_end_station}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    #Displays statistics on the total and average trip duration.
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    #Displays statistics on bikeshare users.
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    print('\nCalculating Type...\n')
    user_types = df['User Type'].value_counts()
    print("Usertype:", user_types)

    # Gender and Birth Year data only available for Chicago and New York City
    if city == "washington":
        print("No gender data available for washington")
    else:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("Gender:", gender_counts)
        # Display earliest, most recent, and most common year of birth
        min_year = df['Birth Year'].min()
        print(f"Earliest year of birth: {min_year}")
        max_year = df['Birth Year'].max()
        print(f"Most recent year of birth: {max_year}")
        most_year = df['Birth Year'].mode()[0]
        print(f"Most common year of birth: {most_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays 5 lines of raw data upon user request."""
    i = 0
    pd.set_option('display.max_columns', 200)

    while True:
        raw = input("\nWould you like to see 5 lines of raw data? Enter yes or no.\n").strip().lower()
        if raw == 'no':
            print("Exiting raw data display.")
            break
        elif raw == 'yes':
            # Check if there are enough rows left to display
            if i >= len(df):
                print("No more data to display.")
                break
            print(df.iloc[i:i+5])  # Display 5 rows of data
            i += 5
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
            if restart in ['yes', 'no']:
                if restart == 'no':
                    print("Exiting the program. Goodbye!")
                    break
                else:
                    print("Restarting the program...")
                    break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        
        if restart == 'no':
            break

if __name__ == "__main__":
	main()