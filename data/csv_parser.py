   
import csv

with open('test_csv.csv') as csvfile:
     reader = csv.reader(csvfile, delimiter=' ')
     def enter_stock_csv(pharmacy_id, file_path, cursor):
        for row in reader:
            insert_stock(pharmacy_id, amount, pzn, product_name, ingredient, supplier, quantity, x, y, z, cooling_p, recipe_p, cursor)
            print(', '.join(row))