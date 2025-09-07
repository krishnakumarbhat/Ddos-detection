import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the CSV file
data = pd.read_csv('output.csv')

# Check the column names in the data DataFrame
print(data.columns)

# Verify if the columns exist in the DataFrame
required_columns = ['File Name', 'Protocol', 'Source IP', 'Destination IP', 'Source Port',
                    'Destination Port', 'Payload', 'Time Taken']
if not all(column in data.columns for column in required_columns):
    raise KeyError("Required columns not found in the DataFrame.")

# Replace missing values (NaN) with zeros
data = data.fillna(0)

# Preprocessing steps
# Convert categorical columns to numeric using one-hot encoding
data = pd.get_dummies(data, columns=['Protocol'])

# Split the data into features (X) and target (y)
X = data.drop(['File Name', 'Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Payload', 'Time Taken'], axis=1)
y = data['File Name']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the Random Forest classifier
rf = RandomForestClassifier()

# Train the classifier
rf.fit(X_train, y_train)

# Make predictions on the testing data
predictions = rf.predict(X_test)

# Find the indices of the rows corresponding to DDoS attacks
ddos_indices = y_test[y_test.isin(predictions)].index

# Get the IP addresses responsible for DDoS attacks
ddos_ips = data.loc[ddos_indices, 'Source IP']

# Store the IP addresses in a new CSV file
ddos_ips.to_csv('ddosip.csv', index=False)

