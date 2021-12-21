import pandas
import plotly.express as px
from pandas import DataFrame

if __name__ == '__main__':
    path = "result.csv"
    df = pandas.read_csv(path)

    new_df = DataFrame()

    cnt = 0
    for idx in df.index:
        for col in df.columns:
            if col == "file" or col == "vertices":
                continue
            new_df.at[cnt, "Filetype"] = col
            new_df.at[cnt, "Input file name"] = df.at[idx, "file"]
            new_df.at[cnt, "File size [KB]"] = df.at[idx, col]
            cnt += 1

    fig = px.scatter(new_df, x="Input file name", y="File size [KB]", color="Filetype",  template="plotly_dark", title="Absolute Size Comparison")
    fig.update_traces(marker=dict(size=16))
    fig.write_html("absolute.html")
