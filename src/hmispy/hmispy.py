"""Main module."""

import pandas as pd
import sys
from .utils import list_codes
from .utils import list_states
from .utils import rename_states


def extract_numbers_from_html_df(
    df,
    metric_colname,
    metric_code,
    total_colnames=["Total [(A+B) or (C+D)]"],
    verbose=False,
):
    code_df = list_codes()
    metric_desc = code_df[code_df["code"] == metric_code]["description"].values[0]
    row_index_df = df[metric_colname] == metric_code

    row_index = row_index_df.reset_index(drop=True).iloc[:, 0].tolist()
    all_cols = list(sorted(set(list(map(lambda x: x[1], df.columns.tolist())))))
    index_lengths = list(sorted(set(list(map(lambda x: len(x), df.columns.tolist())))))
    assert len(index_lengths) == 1
    states = list_states()
    all_df = list()
    for state in states:
        if index_lengths[0] < 3:
            try:
                value = df.loc[row_index, ("State", state)].values[0]
            except KeyError:
                continue
            value = df.loc[row_index, ("State", state)].values[0]
            all_df.append(
                {
                    "state": state,
                    "metric_code": metric_code,
                    "metric_desc": metric_desc,
                    "value": value,
                    "value_type": "Total [(A+B) or (C+D)]",
                    "read_mode": "html",
                }
            )
        else:
            for value_type in total_colnames:
                try:
                    value = df.loc[row_index, ("State", state, value_type)].values[0]
                    all_df.append(
                        {
                            "state": state,
                            "metric_code": metric_code,
                            "metric_desc": metric_desc,
                            "value": value,
                            "value_type": value_type,
                            "read_mode": "html",
                        }
                    )
                except KeyError:
                    if verbose:
                        sys.stderr.write(
                            "Skipping",
                            {
                                "state": state,
                                "metric_code": metric_code,
                                "metric_desc": metric_desc,
                            },
                        )
    return all_df


def extract_numbers_from_excel_df(
    df,
    metric_colname,
    metric_code,
    total_colnames=["Total [(A+B) or (C+D)]"],
    verbose=False,
):
    code_df = list_codes()
    metric_desc = code_df[code_df["code"] == metric_code]["description"].values[0]

    row_index = df[metric_colname] == metric_code
    states = list_states()
    all_df = list()
    for state in states:
        for value_type in total_colnames:
            try:
                state_index = df.columns.tolist().index(state + " " + value_type)
                value = df.loc[row_index].values[0][state_index]
                all_df.append(
                    {
                        "state": state,
                        "metric_code": metric_code,
                        "metric_desc": metric_desc,
                        "value": value,
                        "value_type": value_type,
                        "read_mode": "excel",
                    }
                )
            except ValueError:
                if verbose:
                    sys.stderr.write("Skipping {} {}\n".format(state, value_type))
    return all_df


def read_hmis_xls(
    filepath,
    codes=["4.1.1.a", "4.1.1.b"],
    total_colnames=["Total [(A+B) or (C+D)]", "Urban [C]", "Rural [D]"],
    verbose=False,
):
    month = (
        filepath.replace(" ", "")
        .replace(".xlsx", "")
        .replace(".xls", "")
        .split("-")[-1]
    )
    states = list_states()

    try:
        df = pd.read_html(filepath)[0]
        df = df.replace({"\\'": ""}, regex=True)

        metric_colname = ["Unnamed: 1_level_0"]
        df[metric_colname] = df[metric_colname].replace({"\\'": ""}, regex=True)

    except UnicodeDecodeError:
        sys.stderr.write("Got unicode error with {}\n".format(filepath))

        df = pd.read_excel(filepath, skiprows=6)  # [0]
        df = df.replace({"\\'": ""}, regex=True)
        df.columns = list(df.columns)
        df.columns.values[0] = "x"
        df.columns.values[1] = "metric"
        df.columns.values[2] = "value_type"
        df["metric"] = df["metric"].replace({"\\'": ""}, regex=True)
        metric_colname = "metric"
    df = rename_states(df)
    parsed_results = list()
    for code in codes:
        if metric_colname == "metric":
            result_df = extract_numbers_from_excel_df(
                df,
                metric_colname=metric_colname,
                metric_code=code,
                total_colnames=total_colnames,
                verbose=verbose,
            )
            parsed_results += result_df
        else:
            result_df = extract_numbers_from_html_df(
                df,
                metric_colname=metric_colname,
                metric_code=code,
                total_colnames=total_colnames,
                verbose=verbose,
            )
            parsed_results += result_df
    df = pd.DataFrame(parsed_results)
    df["month"] = month
    df["filepath"] = filepath
    return df
