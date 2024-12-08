import pandas as pd
import numpy as np
import pymysql
from pymysql.cursors import DictCursor

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = pymysql.connect(
            host='localhost',
            database='DIC',
            user='root',
            password='qwerty1234',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def handle_nan_values(df):
    """
    Replace NaN values with None for compatibility with MySQL.
    """
    return df.replace({np.nan: None})

def drop_table(table_name='movies'):
    """
    Drop the existing table to recreate it.
    """
    try:
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return
        
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        connection.commit()
        print(f"Table '{table_name}' dropped successfully!")

    except Exception as e:
        print(f"Error dropping table: {e}")
    
    finally:
        if connection:
            connection.close()

def create_table_from_csv(csv_file_path, table_name='movies'):
    """
    Create a MySQL table based on the structure of the CSV file.
    """
    try:
        df = pd.read_csv(csv_file_path)
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return
        
        cursor = connection.cursor()

        # Generate column definitions
        column_definitions = []
        for column, dtype in df.dtypes.items():
            if pd.api.types.is_integer_dtype(dtype):
                sql_type = 'INT'
            elif pd.api.types.is_float_dtype(dtype):
                sql_type = 'FLOAT'
            else:
                sql_type = 'VARCHAR(500)'  # Default for string types
            
            null_constraint = 'NULL' if df[column].isnull().any() else 'NOT NULL'
            column_definitions.append(f"{column} {sql_type} {null_constraint}")

        # Table creation query
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(column_definitions)}
        )
        """
        
        print("Table creation query:")
        print(create_table_query)
        
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully!")

    except Exception as e:
        print(f"Error creating table: {e}")
    
    finally:
        if connection:
            connection.close()

def insert_csv_to_db(csv_file_path, table_name='movies'):
    """
    Insert CSV data into MySQL database.
    """
    try:
        # Read and clean the CSV
        df = pd.read_csv(csv_file_path)
        df_cleaned = handle_nan_values(df)

        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return

        cursor = connection.cursor()

        # Prepare and execute insert query
        columns_str = ', '.join([f"{col}" for col in df_cleaned.columns])
        placeholders = ', '.join(['%s'] * len(df_cleaned.columns))
        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        data_to_insert = df_cleaned.values.tolist()
        try:
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
            print(f"Successfully inserted {len(data_to_insert)} rows into {table_name}")
        except Exception as bulk_insert_error:
            print(f"Bulk insert failed: {bulk_insert_error}")
            print("Falling back to row-by-row insertion...")
            
            successful_inserts = 0
            failed_inserts = 0
            for index, row in enumerate(data_to_insert):
                try:
                    cursor.execute(insert_query, row)
                    successful_inserts += 1
                    if successful_inserts % 100 == 0:
                        print(f"Inserted {successful_inserts} rows...")
                except Exception as row_error:
                    print(f"Error inserting row {index + 1}: {row_error}")
                    failed_inserts += 1
            connection.commit()
            print(f"\nData Import Summary:")
            print(f"Total rows processed: {len(data_to_insert)}")
            print(f"Successfully inserted: {successful_inserts}")
            print(f"Failed inserts: {failed_inserts}")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

def main():
    # Path to your CSV file
    csv_file_path = r'./cleaned_movies_dataset.csv'
    
    # Step 1: Drop existing table (if needed)
    drop_table(table_name='movies')
    
    # Step 2: Create table based on CSV structure
    create_table_from_csv(csv_file_path, table_name='movies')
    
    # Step 3: Insert CSV data into the table
    insert_csv_to_db(csv_file_path, table_name='movies')

if __name__ == "__main__":
    main()