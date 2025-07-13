import pandas as pd

df = pd.read_csv("OLA.csv")

#Show preview
print(" Original Columns:\n", df.columns.tolist())
print("\nSample Before Transformation:\n", df[['Date', 'Time', 'Booking Status']].head())

#Combine Date and Time
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

#Extract Hour of Day
df['Hour'] = df['Datetime'].dt.hour

#Extract Day of Week
df['DayOfWeek'] = df['Datetime'].dt.day_name()
df['WeekType'] = df['DayOfWeek'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')

#Define Cancellation flags
def determine_cancel_type(row):
    if row['Booking Status'] == 'Cancelled by Customer':
        return 'Customer'
    elif row['Booking Status'] == 'Cancelled by Driver':
        return 'Driver'
    elif row['Booking Status'] == 'Incomplete':
        return 'Incomplete'
    elif row['Booking Status'] == 'Success':
        return 'None'
    else:
        return 'Unknown'

df['Is_Cancelled'] = df['Booking Status'].apply(lambda x: x != 'Success')
df['Cancellation_Type'] = df.apply(determine_cancel_type, axis=1)

#Show new columns
print("\nNew Columns Added: ['Datetime', 'Hour', 'DayOfWeek', 'WeekType', 'Is_Cancelled', 'Cancellation_Type']\n")
print(df[['Datetime', 'Hour', 'DayOfWeek', 'WeekType', 'Is_Cancelled', 'Cancellation_Type']].head())

#Show missing values
missing_booking_value = df['Booking Value'].isna().sum()
print(f"\nRows with missing 'Booking Value': {missing_booking_value}")

#Export cleaned data
df.to_csv("cleaned_booking_data.csv", index=False)
print("\nCleaned data saved to 'cleaned_booking_data.csv'")




#Splitting Data
#Completed Bookings
bookings = df.copy()

#Cancelled rides
cancelled = bookings[bookings['Is_Cancelled'] == True]

#Rides with ratings
ratings = bookings.dropna(subset=['Driver Ratings', 'Customer Rating'])

#Valid rides for value analysis
valid_rides = bookings.dropna(subset=['Booking Value'])




#Unified Reason Column
df_reason = df.copy()

# Map correct reason based on Cancellation_Type
df_reason['Unified_Reason'] = df_reason.apply(
    lambda row: row['Reason for Cancelling by Driver'] if row['Cancellation_Type'] == 'Driver'
    else row['Reason for Cancelling by Customer'] if row['Cancellation_Type'] == 'Customer'
    else row['Incomplete Rides Reason'] if row['Cancellation_Type'] == 'Incomplete'
    else 'Unknown',
    axis=1
)

# Drop the individual reason columns
df_reason.drop(['Reason for Cancelling by Driver', 'Reason for Cancelling by Customer', 'Incomplete Rides Reason'], axis=1, inplace=True)

# Save final cleaned version
df_reason.to_csv("/mnt/data/cleaned_cancellations.csv", index=False)
df_reason[['Booking ID', 'Cancellation_Type', 'Unified_Reason']].head()
