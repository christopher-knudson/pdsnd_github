import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# These variables are for validating user inputs
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
daysofweek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      try:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower().strip()
        if city not in CITY_DATA: 
          raise ValueError
        break
      except ValueError:
        print('\nThat was not a valid input. Please type the city exactly as it appears above.')

    # TO DO: get user input for month (all, january, february, ... , june)
    print('\nNow, which month would you like to see data for?')
    while True:
      try:
        month = input('Enter the full name of the month (e.g. "January") or enter \"all.\"\n').lower().strip()
        if month not in months and month.lower() != 'all':
          raise ValueError
        break
      except ValueError:
        print('\nThat was not a valid input. Please spell out the entire month or enter \"all.\"')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nFinally, which day of the week would you like to see data for?')
    while True:
      try:
        day = input('Enter the full day of week (e.g. "Monday") or enter \"all.\"\n').lower().strip()
        if day not in daysofweek and day != 'all':
          raise ValueError
        break
      except ValueError:
        print('\nThat was not a valid input. Please spell out the entire day of week or enter \"all.\"')
    
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month # returns numerical month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1
    
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
    start_time = time.time() # This is for tracking how long this function takes.

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {months[most_common_month-1].title()}") 

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {most_common_day}") 

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common hour: {most_common_hour}") 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {most_common_start_station}")

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"Most common end station: {most_common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + " - " + df['End Station']
    most_common_station_combo = df['Station Combo'].mode()[0]
    print(f"Most common start and end station combo: {most_common_station_combo}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time:,} minutes")


    # TO DO: display mean travel time
    average_travel_time = int(round(df['Trip Duration'].mean(), 0))
    print(f"Average travel time: {average_travel_time} minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].nunique()
    print(f"Count of user types: {user_types}")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
      gender_types = df['Gender'].nunique()
      print(f"Count of gender types: {gender_types}")
    else:
      print('Gender stats not available for this city.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
      earliest_birth_year = int(df['Birth Year'].min())
      latest_birth_year = int(df['Birth Year'].max())
      most_common_birth_year = int(df['Birth Year'].mode())
      print(f"Earliest birth year: {earliest_birth_year}")
      print(f"Latest birth year: {latest_birth_year}")
      print(f"Most common birth year: {most_common_birth_year}")
    else:
      print('Birth year stats not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Prompts the user if they want to see 5 lines of raw data.
    Display that data if the answer is 'yes.'
    Continues iterating these prompts and displaying the next 5 lines of raw data at each iteration.
    Stop when the user says 'no' or there is no more raw data to display.
    """
    
    # Ensures all columns are printed.
    pd.set_option('display.max_columns', None) 

    while True:
      try:
        raw_data = input('\nWould you like to see 5 rows of raw data? Please type yes or no. ').lower().strip()
        if raw_data == 'yes':
          location = 5
          print()
          print(df[location-5:location])
          while location<len(df.index)+5: #ensures every last row can be returned before loop breaks
            try:
              cont = input('\nWould you like to see 5 more rows? Please type yes or no. ').lower().strip()
              if cont == 'yes':
                location += 5 #location > df length is not a problem
                print(df[location-5:location]) 
              elif cont == 'no':
                break
              else:
                raise ValueError
            except ValueError:
              print('\nThat was not a valid input. Please type yes or no. ')
          break
        elif raw_data == 'no':
          break
        else:
          raise ValueError
      except ValueError:
        print('\nThat was not a valid input. Please type yes or no. ')

def main():
    """
    Calls the other functions in the module, 
    then asks the user if they want to run the function again.
    """

    while True:
      city, month, day = get_filters()
      df = load_data(city, month, day)
      
      time_stats(df)
      station_stats(df)
      trip_duration_stats(df)
      user_stats(df)
      raw_data(df)
      
      restart = input('\nWould you like to restart? Enter yes or no.\n')
      if restart.lower() != 'yes':
          break
      else:
        print()

if __name__ == "__main__":
	main()