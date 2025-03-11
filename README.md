# System Requirements Specification
# Loop-Focused Inventory Management System (Version 1.0)

## TABLE OF CONTENTS
1. Project Abstract
2. Core Requirements
3. Loop Implementation Constraints
4. Program Structure
5. Execution Steps

## 1. PROJECT ABSTRACT
This Python console application demonstrates effective loop implementation for inventory management tasks. The program processes parallel lists containing product information to perform filtering, searching, counting, and calculation operations. The focus is on proper loop implementation for data manipulation.

## 2. CORE REQUIREMENTS
1. Process multiple inventory items stored in parallel lists
2. Find items below specified stock thresholds using loops
3. Search products by name using loops and conditionals
4. Count items by category using nested loops
5. Calculate total inventory value using accumulation loops

## 3. LOOP IMPLEMENTATION CONSTRAINTS

### 3.1 DATA STRUCTURE
- Inventory must be stored as parallel lists:
  ```python
  product_ids = ["P001", "P002", "P003"]
  names = ["Rice 5kg", "Wheat Flour 1kg", "Mobile Charger"]
  categories = ["Grocery", "Grocery", "Electronics"]
  quantities = [45, 8, 15]
  prices = [250.00, 60.00, 300.00]
  ```

### 3.2 REQUIRED LOOP IMPLEMENTATIONS

1. **Filtering Loop** (find_low_stock_items):
   - Must use a `for` loop with `range()` to iterate through indices
   - Must use conditional (`if`) inside loop to check values
   - Must append matching items to result lists
   - Example: 
     ```python
     for i in range(len(quantities)):
         if quantities[i] <= threshold:
             # append to results
     ```

2. **Search Loop** (search_products):
   - Must use a `for` loop to iterate through product names
   - Must perform case-insensitive string comparison
   - Must append matching items to result lists
   - Example:
     ```python
     for i in range(len(names)):
         if term.lower() in names[i].lower():
             # append to results
     ```

3. **Nested Loops** (count_by_category):
   - First loop: Must gather unique categories
   - Second loop: Must count occurrences of each category
   - Must handle duplicate categories correctly
   - Example:
     ```python
     for cat in unique_cats:
         count = 0
         for item_cat in categories:
             if item_cat == cat:
                 count += 1
     ```

4. **Accumulation Loop** (calculate_total_value):
   - Must use a `for` loop to iterate through indices
   - Must perform multiplication inside loop
   - Must accumulate a running total
   - Example:
     ```python
     for i in range(len(quantities)):
         total += quantities[i] * prices[i]
     ```

## 4. PROGRAM STRUCTURE

1. **Data Definition**:
   - Define parallel lists for inventory data

2. **Processing Functions**:
   - `find_low_stock_items(threshold)`: Returns filtered product information
   - `search_products(term)`: Returns matching product information
   - `count_by_category()`: Returns unique categories and their counts
   - `calculate_total_value()`: Returns total inventory value

3. **Main Function**:
   - Display menu options
   - Get user input
   - Call appropriate processing function
   - Display results

## 5. EXECUTION STEPS

1. Run the program
2. Select a function from the menu (1-5)
3. Enter required inputs when prompted
4. View the results
5. Continue or exit