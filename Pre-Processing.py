import pandas as pd
import os

class Colors:
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    END = '\033[0m'

# Load the data
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'Input\Recorded_Business_Tasks.csv')
df = pd.read_csv(file_path)

# Display initial data information
print(Colors.PURPLE + "--The initial data--" + Colors.END)
df.info()
print("-----------------------------------------------------------------")

# Inspect unique step and event names
print(Colors.PURPLE +  "--Inspect the step names and event names to decide on activity--" + Colors.END)
print(Colors.BLUE + "Step Names:" + Colors.END)
print(Colors.GREEN + "It has 19 unique activities" + Colors.END)
unique_step_names = df['StepName'].value_counts()
unique_event_names = df['label_EventName'].value_counts()

print(Colors.BLUE + "Event Names:" + Colors.END)
print(Colors.GREEN + "It has 619 unique activities which is too many activities and makes it unfit to be the chosen activity" + Colors.END)
print(unique_step_names)
print(unique_event_names)
print("-----------------------------------------------------------------")


# Drop unnecessary columns
print(Colors.PURPLE + "--Data after dropping columns--" + Colors.END)
print(Colors.GREEN + "We can see that the ApplicationProcessName column has the most missing values.\nTo drop all these rows will be a big loss of data" + Colors.END)
unwanted_cols = ['StepId', 'NextStepId', 'AutomationStep', 'ApplicationParentWindowName', 'label_EventName', 'label_EventId']
df = df.drop(unwanted_cols, axis=1)
df.info()
print("-----------------------------------------------------------------")

# Drop duplicate rows
print(Colors.PURPLE + "--Data after dropping duplicate rows--" + Colors.END)
df = df.drop_duplicates()
df.info()
print("-----------------------------------------------------------------")

# Check and handle missing values in ApplicationProcessName
print(Colors.PURPLE + "--Check ApplicationProcessName empty values--" + Colors.END)
print(Colors.GREEN + "For the empty values, we want to look at the column ApplicationParentWindowName to see which application the empty ApplicationProcessName belongs to" + Colors.END)
print(Colors.GREEN + "We previously dropped this column since it was un-useful, so we load it in newly to investigate" + Colors.END)
print(Colors.GREEN + "The parent window names for the empty ApplicationProcessName seem to be Task Switcher and Destination, these window names belong to the operating system of the PC e.g., Windows/Mac/Linux" + Colors.END)
# Create a copy to investigate missing values
df_copy = pd.read_csv(file_path)
empty_rows = df_copy[df_copy['ApplicationProcessName'].isnull()]
investigate_column = ['ApplicationParentWindowName']
print(empty_rows[investigate_column].value_counts())
print("-----------------------------------------------------------------")

# Fill in missing values
print(Colors.PURPLE + "--Populate missing ApplicationProcessName where the ApplicationParentWindowName is Task Switcher or Destination--" + Colors.END)
print(Colors.GREEN + "Filling the empty data with OS (Operating System)" + Colors.END)
condition = (df_copy['ApplicationParentWindowName'].isin(['Task Switcher', 'Destination'])) & df_copy['ApplicationProcessName'].isna()
df.loc[condition, 'ApplicationProcessName'] = 'OS'
df.info()
print("-----------------------------------------------------------------")

# Drop rows with any remaining missing values
print(Colors.PURPLE + "--Data after dropping missing value rows--" + Colors.END)
df = df.dropna()
df.info()
print("-----------------------------------------------------------------")

# Combine StepName with ApplicationProcessName
print(Colors.PURPLE + "--Data after concatenating StepName and ApplicationProcessName--" + Colors.END)
print(Colors.GREEN + "It has 95 unique activities" + Colors.END)
df['New_StepName'] = df['StepName'] + ' / ' + df['ApplicationProcessName']
unique_concatenated_names = df['New_StepName'].value_counts()
print(unique_concatenated_names)
print("-----------------------------------------------------------------")
print(Colors.PURPLE + "--Final columns--" + Colors.END)
df.info()

# Save the processed data to a new CSV file
output_file_path = os.path.join(current_directory,'Output\output-recorded-business-tasks.csv')
df.to_csv(output_file_path, sep=';', index=False, encoding='utf-8')