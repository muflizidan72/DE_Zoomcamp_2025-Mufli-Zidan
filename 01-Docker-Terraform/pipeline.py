import argparse,os,sys
from sqlalchemy import create_engine
import pandas as pd
import pyarrow.parquet as pq
from time import time

def main(args):
    user = args.user
    password = args.password
    host = args.host
    port = args.port
    db = args.db
    tb = args.tb
    url = args.url

    # Read a link of CSV/Parquet data
    file_name = url.rsplit('/', 1)[-1].strip()
    print(f'Downloading {file_name} ...')
    # Download the CSV/Parquet data
    os.system(f'curl {url.strip()} -o {file_name}')
    print('\n')

    # Create engine of SQL
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    # Proccess the CSV/Parquet Data
    if ".csv" in file_name:
        df = pd.read_csv(file_name, nrows=10)
        df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
    elif ".parquet" in file_name:
        file = pq.ParquetFile(file_name)
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else:
        print(f'Error because only supporting CSV/Parquet format data')
        sys.exit()
    
    # Create the table in the Postgresql
    df.head(0).to_sql(name=tb, con=engine, if_exists='replace')

    # Insert value of CSV/Parquet data
    t_start = time()
    count = 0
    for batch in df_iter:
        count += 1

        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch

        print(f'Inserting ! Batch {count}\n')

        #Push the data to Postgres
        b_start = time()
        batch_df.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time()
        print(f'It taken {b_end - b_start: 0.3f} seconds\n')

    t_end = time()
    print(f'Finished! It taken {t_end - t_start: 0.3f} seconds to push all of data')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingestion of CSV/Parquet Data to Postgresql.')
    parser.add_argument('--user', help='Username of Postgres')
    parser.add_argument('--password', help='Password of Postgres')
    parser.add_argument('--host', help='Host name of Postgres')
    parser.add_argument('--port', help='Port of Postgres')
    parser.add_argument('--db', help='Database name of Postgres')
    parser.add_argument('--tb', help='Table name of Postgres')
    parser.add_argument('--url', help='Link of CSV/Parquet Data')

    args = parser.parse_args()
    main(args)