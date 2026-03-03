import numpy as np
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
    df["Позначка часу"] = pd.to_datetime(df["Позначка часу"], format="%d.%m.%Y %H:%M:%S", errors="coerce")

    mask_date = df["Позначка часу"] > "22.02.2026"
    mask_empty_taken = (df["Хто взяв"].isna()) | (df["Хто взяв"].astype(str).str.strip() == "")
    mask_can_take = (
        (df["Можна брати?"].astype(str).str.strip() == "Так") | 
        (df["Можна брати?"].isna()) | 
        (df["Можна брати?"].astype(str).str.strip() == "") 
    )
    final_mask = mask_date & mask_can_take & mask_empty_taken

    matching_rows = df[final_mask]
    if matching_rows.empty:
        return None
    
    row = matching_rows.iloc[0]
    return ContactFound(
        name=row["Твоє ім'я"],
        telegram=row["Твій нік в тг"],
        grade=row["Твій курс"],
        comments=row["Твої коментарі (за бажанням)"],
        row_number=matching_rows.index[0] + 2, # one for counting starts from 0 and one for header  
    )
