import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS =  ["january", "february", "march", "april", "may", "june"]
CITIES = ["chicago", "washington", "new york city"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while(not city in CITIES):
        print('Please enter the city (chicago, washington, new york city)');
        city = input().lower()
    

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    while(not month in MONTHS):
        print('Please enter a month (  {} )'.format(', '.join(MONTHS)));
        month = input().lower();

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while(not day in DAYS):
        print('Please enter a day (  {} )'.format(', '.join(DAYS)))
        day = input().lower()

    print('#'*40)
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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    
    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour is {}'.format(common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station_mode = df['Start Station'].mode()[0]
    print('Most commonly used start station is {}'.format(common_start_station_mode))

    # TO DO: display most commonly used end station
    common_end_station_mode = df['End Station'].mode()[0]
    print('Most commonly used end station is {}'.format(common_end_station_mode))

    # TO DO: display most frequent combination of start station and end station trip
    combination = df['Start Station'].append(df['End Station'], ignore_index=True)
    print('Most frequent combination of start station and end station trip is {}'.format(combination.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is {}'.format(total_travel_time))
    
    # TO DO: display mean travel time
    total_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is {}'.format(total_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df['User Type'].value_counts()
    user_types = len(df['User Type'].unique())
    print('The number of user types is {}'.format(user_types))

    if not city.lower() == "washington":
         # TO DO: Display counts of gender
        gender = len(df['Gender'].unique())
        print('The genders are {}'.format(gender))

        # TO DO: Display earliest, most recent, and most common year of birth
        common_year_of_birth = df['Birth Year'].mode()[0]
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        print('The earliest year of birth is {}'.format(int(earliest)))
        print('The most recent year of birth is {}'.format(int(recent)))
        print('The most common year of birth is {}'.format(int(common_year_of_birth)))
    else:
        print("There is no gender and birth year for this city")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    current_index = 0

    while True:
        user_answer = input('\n Do you want to see raw data? Enter yes or no.\n').lower()
        if user_answer in ["yes", "no"]:
            if user_answer == "yes":
                if current_index >= df.size:
                    print("No more data to display")
                    break;
                else:
                    print(df.iloc[current_index: min(current_index + 5, df.size)])
                    current_index += 5
                
            else:
                break;
        else:
            print("")
     
def main():
    while True:
        city, month, day = get_filters()
        #print("{} {} {}".format(city, day, month))
        df = load_data(city, month, day)
        df.head()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


