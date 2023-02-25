import pandas as pd

def xls_to_csv(xls_file, csv_file):
    df = pd.read_excel(xls_file)
    df.to_csv(csv_file, index=False)
    return df

if __name__ == '__main__':
    xls_file = 'köyler_tıbbi_yardım.xls'
    csv_file = 'köyler_tıbbi_yardım.csv'
    xls_to_csv(xls_file, csv_file)