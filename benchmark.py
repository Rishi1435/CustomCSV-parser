import timeit
import csv
import os
import random
import string
from custom_csv import CustomCsvReader, CustomCsvWriter

# Constants for Benchmarking
FILENAME = "benchmark_data.csv"
ROWS = 10000
COLS = 5

def generate_data(rows, cols):
    """Generates a list of lists with random string data, including edge cases."""
    data = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            # 10% chance to include a comma, quote, or newline to test edge cases
            special = random.random()
            if special < 0.1:
                content = f'Data, "with" \n edge case {random.randint(1,100)}'
            else:
                content = ''.join(random.choices(string.ascii_letters, k=10))
            row.append(content)
        data.append(row)
    return data

def benchmark_standard_write(data):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def benchmark_custom_write(data):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = CustomCsvWriter(f)
        writer.writerows(data)

def benchmark_standard_read():
    with open(FILENAME, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for _ in reader:
            pass

def benchmark_custom_read():
    with open(FILENAME, 'r', newline='', encoding='utf-8') as f:
        reader = CustomCsvReader(f)
        for _ in reader:
            pass

def run_benchmark():
    print(f"Generating synthetic data: {ROWS} rows, {COLS} columns...")
    data = generate_data(ROWS, COLS)
    
    print("-" * 40)
    print("Starting Write Benchmark (Average of 5 runs)")
    
    t_std_write = timeit.timeit(lambda: benchmark_standard_write(data), number=5) / 5
    print(f"Standard csv.writer: {t_std_write:.4f} seconds")
    
    t_cust_write = timeit.timeit(lambda: benchmark_custom_write(data), number=5) / 5
    print(f"CustomCsvWriter:     {t_cust_write:.4f} seconds")
    
    print("-" * 40)
    print("Starting Read Benchmark (Average of 5 runs)")
    
    # Ensure file exists from write test
    benchmark_standard_write(data) 
    
    t_std_read = timeit.timeit(benchmark_standard_read, number=5) / 5
    print(f"Standard csv.reader: {t_std_read:.4f} seconds")
    
    t_cust_read = timeit.timeit(benchmark_custom_read, number=5) / 5
    print(f"CustomCsvReader:     {t_cust_read:.4f} seconds")
    
    print("-" * 40)
    print("Performance Ratios (Standard / Custom)")
    print(f"Write Speed: Custom is {t_cust_write/t_std_write:.1f}x slower")
    print(f"Read Speed:  Custom is {t_cust_read/t_std_read:.1f}x slower")

    # Cleanup
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

if __name__ == "__main__":
    run_benchmark()