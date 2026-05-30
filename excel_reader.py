import pandas as pd

def load_data(file_path="students.xlsx"):
    df = pd.read_excel(file_path)

    # تنظيف البيانات من القيم الفارغة
    df = df.fillna("")

    return df
