def get_data_from_file(file_name: str) -> str:
    with open("file_name", "r", encoding="utf-8") as file:
        return file.read().strip()