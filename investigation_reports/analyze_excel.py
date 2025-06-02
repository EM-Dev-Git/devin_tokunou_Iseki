import pandas as pd
import sys

try:
    df = pd.read_excel('/home/ubuntu/attachments/2d3164a1-1a1b-4b10-b157-e4338f160502/UkeharaiDB_Matsuyama.xlsx', sheet_name=None)
    print('UkeharaiDB_Matsuyama.xlsx sheets:', list(df.keys()))
    for sheet_name, sheet_df in df.items():
        print(f'Sheet {sheet_name}: {sheet_df.shape} rows/cols')
        if len(sheet_df) > 0:
            print(f'Columns: {list(sheet_df.columns)[:10]}')  # First 10 columns
            print()
except Exception as e:
    print(f'Error reading UkeharaiDB_Matsuyama.xlsx: {e}')

try:
    df2 = pd.read_excel('/home/ubuntu/attachments/6d1b4af2-6c03-47af-90e8-53037be92735/.xlsx', sheet_name=None)
    print('Error screenshot file sheets:', list(df2.keys()))
    for sheet_name, sheet_df in df2.items():
        print(f'Sheet {sheet_name}: {sheet_df.shape} rows/cols')
        if len(sheet_df) > 0:
            print(f'Columns: {list(sheet_df.columns)[:10]}')
            print()
except Exception as e:
    print(f'Error reading screenshot file: {e}')
