import pandas
import plotly.express as px
from pandas import DataFrame

if __name__ == '__main__':
    path = "result.csv"
    df = pandas.read_csv(path)

    new_df = DataFrame()

    mode = "vertices"  # else "original"

    cnt = 0
    for idx in df.index:
        for col in df.columns:
            if col == "file" or col == "vertices" or col == "original":
                continue
            new_df.at[cnt, "type"] = col
            new_df.at[cnt, "input"] = df.at[idx, "file"]
            new_df.at[cnt, "size"] = df.at[idx, col] / df.at[idx, mode]
            cnt += 1

    fig = px.box(new_df, x="type", y="size", color="type",  template="plotly_dark",
                 title="Relative Size Comparison (compared to baseline)" if mode == "original" else "Relative Size Comparison (compared to number of vertices)",
                 labels={
                     "input": "File format",
                     "size": "Baseline factor (compared to input .obj)" if mode == "original" else "File size (KB) / vertices",
                     "type": "File type"
                 },
                 points="all"
                 )
    if mode == "original":
        fig.add_hline(y=1, annotation_text="Input file base line", annotation_position="bottom right")
        fig.update_yaxes(range=[0, 13.5])
    else:
        fig.update_yaxes(range=[0, 1])
    fig.write_html(f"relative_{mode}.html")
