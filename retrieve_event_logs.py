import pandas as pd
import pm4py

def get_logs_df(csv_logs_path, sep):
    csv_df = pd.read_csv(csv_logs_path, sep=sep)
    # filtering the columns required
    csv_df = csv_df[["RecordingId", "TimeStamp", "New_StepName", "StepDescription"]]
    return csv_df

def format_event_logs(csv_logs_df):
    xes_columns = ["case:concept:name", "time:timestamp", "concept:name", "activity"]
    #rename columns to fit into xes format
    csv_logs_df.columns = xes_columns
    # ensuring the datatypes
    csv_logs_df["case:concept:name"] = csv_logs_df["case:concept:name"].astype(str)
    csv_logs_df["time:timestamp"] = pd.to_datetime(csv_logs_df["time:timestamp"])
    csv_logs_df["concept:name"] = csv_logs_df["concept:name"].astype(str)
    csv_logs_df["activity"] = csv_logs_df["activity"].astype(str)
    event_log = pm4py.convert_to_event_log(csv_logs_df)
    return event_log

if __name__ == "__main__":
    csv_logs_path = "Output\output-recorded-business-tasks.csv"
    sep = ";"
    xes_logs_path = "Output\event_logs.xes"
    csv_logs_df = get_logs_df(csv_logs_path, sep)
    event_logs = format_event_logs(csv_logs_df)
    pm4py.write_xes(event_logs, xes_logs_path)
    
    
