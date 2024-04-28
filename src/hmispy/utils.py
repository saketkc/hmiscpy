import pandas as pd
import os


def rename_states(df):
    df = df.rename(
        columns={
            "Andaman & Nicobar Islands": "A & N Islands",
            "Andhra Pradesh Old": "Andhra Pradesh",
            "Jammu And Kashmir": "Jammu & Kashmir",
        }
    )


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


def list_codes():
    csv_file_path = os.path.join(
        os.path.dirname(__file__), "data", "code_description.csv"
    )
    df = pd.read_csv(csv_file_path)
    return df


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
