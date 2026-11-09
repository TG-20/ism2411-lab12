# ISM2411 Lab 12 - Read a Sales CSV, Write a Cleaned Report
#
# Reflection 1:
# Python and Excel can both do this ETL work, but Excel is faster for a one-time
# look at the data because you can see it and click through it. Python is better
# when the same steps must be repeated on new or very large files, since the script
# runs them the same way every time. Excel is still easier for quick charts and for
# sharing with people who don't code.
#
# Reflection 2:
# A store could log each day's closing sales total from its register system to a
# text file. Append mode is the right tool because it adds a new line and keeps the
# earlier days, while write mode would erase the history on every run. The result
# is a simple record that managers can use to review sales over time.

import csv
import os
from datetime import datetime

INPUT_FILE = "data/sales.csv"
OUTPUT_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"

# Exercise 1: confirm the file exists and has the expected structure
print("--- Exercise 1 ---")
print("File exists:", os.path.exists(INPUT_FILE))
with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)
    row_count = sum(1 for row in reader)
print("Columns:", header)
print("Data rows:", row_count)

# Exercise 2: read and print raw rows (every value is a string)
print("\n--- Exercise 2 ---")
with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Exercise 3: skip the header
print("\n--- Exercise 3 ---")
with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)

# Exercise 4: compute totals
print("\n--- Exercise 4 ---")
total_revenue = 0
with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")

# Exercise 5: filter orders over $100 and write them to a new CSV
print("\n--- Exercise 5 ---")
original_count = 0
written_count = 0
with open(INPUT_FILE, "r", newline="") as infile, open(OUTPUT_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        original_count += 1
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        if line_total > 100:
            writer.writerow([row[0], f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} of {original_count} rows to {OUTPUT_FILE}")

# Exercise 6: same totals using csv.DictReader
# csv.reader is fine for small files with a fixed column order, and it is shorter.
# csv.DictReader is clearer and keeps working if the columns are moved around.
print("\n--- Exercise 6 ---")
dict_total = 0
with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${dict_total:.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))

# Exercise 7: revenue summary by product
print("\n--- Exercise 7 ---")
summary = {}
with open(INPUT_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        line_total = float(row["price"]) * int(row["quantity"])
        summary[row["product"]] = summary.get(row["product"], 0) + line_total
for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")

# Exercise 8: append one line to the log on every run
print("\n--- Exercise 8 ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{timestamp} - Total revenue: ${total_revenue:.2f}\n")
print(f"Added a line to {LOG_FILE}")
