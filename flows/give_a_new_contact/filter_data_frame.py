import pandas as pd
from collections import namedtuple


ContactFound = namedtuple(
    "ContactFound",
    [
        "name",
        "telegram",
        "grade",
        "comments",
        "row_number",
    ]
)


def filter_data_frame(df: pd.DataFrame) -> ContactFound | None:
    df["Позначка часу"] = pd.to_datetime(df["Позначка часу"], format='%d.%m.%Y %H:%M:%S')
    time_framed = df.loc[df["Позначка часу"] > "22.02.2026"]
    first_empty_index = time_framed[time_framed["Хто взяв"].isna() | (time_framed['Хто взяв'].astype(str).str.strip() == "")].index[0]

    for idx, row in time_framed.loc[first_empty_index:].iterrows():
        if row["Можна брати?"] == "Так":
            return ContactFound(
                name=row["Твоє ім'я"],
                telegram=row["Твій нік в тг"],
                grade=row["Твій курс"],
                comments=row["Твої коментарі (за бажанням)"],
                row_number=idx + 2 if isinstance(idx, int) else None,
            )