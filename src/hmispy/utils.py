import os
import pandas as pd


def rename_states(df):
    df = df.rename(
        columns={
            "Andaman & Nicobar Islands": "A & N Islands",
            "Andhra Pradesh Old": "Andhra Pradesh",
            "Jammu And Kashmir": "Jammu & Kashmir",
        }
    )
    return df


def list_states():
    states = [
        "A & N Islands",
        "All India",
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chandigarh",
        "Chhattisgarh",
        "Dadra & Nagar Haveli",
        "Daman & Diu",
        "Delhi",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jammu & Kashmir",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Ladakh",
        "Lakshadweep",
        "M/O Defence",
        "M/O Railways",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Puducherry",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
    ]
    return states


def list_codes():
    csv_file_path = os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")),
        "data",
        "code_description.csv",
    )
    df = pd.read_csv(csv_file_path, index_col=0)
    return df


def search_codes(pattern):
    pattern = pattern.lower()
    df = list_codes()
    return df.loc[df["description"].str.lower().str.contains(pattern)]


def format_excel_df(df):
    states = list_states()
    for index in range(4, len(df.iloc[0])):
        existing_col = df.columns[index]
        existing_row = df.iloc[0][index]
        if existing_col in states:
            statex = existing_col
            df.columns.values[index] = existing_col.strip() + " " + existing_row.strip()
        elif "Unnamed" in existing_col:
            df.columns.values[index] = statex.strip() + " " + existing_row.strip()
    return df
