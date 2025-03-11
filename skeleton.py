# DO NOT MODIFY THE SECTIONS MARKED AS "DO NOT MODIFY"
# Sample inventory data - DO NOT MODIFY
product_ids = ["P001", "P002", "P003"]
names = ["Rice 5kg", "Wheat Flour 1kg", "Mobile Charger"]
categories = ["Grocery", "Grocery", "Electronics"]
quantities = [45, 8, 15]
prices = [250.00, 60.00, 300.00]

def find_low_stock_items(threshold):
    """
    TODO: Use a loop to find items with quantity below threshold
    Return lists of product details for low stock items
    """
    # Validation - DO NOT MODIFY
    if threshold is None: 
        raise TypeError("Threshold cannot be None")
    if not isinstance(threshold, int):
        raise TypeError("Threshold must be an integer")
    if threshold <= 0 or threshold > 100:
        raise ValueError("Threshold must be between 1 and 100")
    
    # TODO: Implement the following using a for loop
    # 1. Create empty result lists (for ids, names, quantities)
    # 2. Loop through the inventory using range(len(product_ids))
    # 3. If an item's quantity is <= threshold, add its details to result lists
    # 4. Return the result lists
    pass

def search_products(term):
    """
    TODO: Use a loop to find items where name contains term (case-insensitive)
    Return lists of product details for matching items
    """
    # Validation - DO NOT MODIFY
    if term is None:
        raise TypeError("Search term cannot be None")
    if not isinstance(term, str):
        raise TypeError("Search term must be a string")
    
    # TODO: Implement the following using a for loop
    # 1. Create empty result lists (for ids, names)
    # 2. Convert search term to lowercase
    # 3. Loop through the inventory using range(len(names))
    # 4. If term is in item's name (case-insensitive), add to result lists
    # 5. Return the result lists
    pass

def count_by_category():
    """
    TODO: Use nested loops to count items in each category
    Return lists of categories and their counts
    """
    # TODO: Implement the following using nested loops
    # 1. Create a list for unique categories
    # 2. Loop through categories to find unique ones
    # 3. Create a list for category counts
    # 4. For each unique category, loop through all categories to count occurrences
    # 5. Return both lists (unique categories and counts)
    pass

def calculate_total_value():
    """
    TODO: Use a loop to calculate total value (quantity * price) of all items
    Return the total value as a float
    """
    # TODO: Implement the following using a for loop
    # 1. Initialize total value as 0
    # 2. Loop through the inventory using range(len(quantities))
    # 3. Calculate item_value = quantities[i] * prices[i]
    # 4. Add item_value to total
    # 5. Return the total value
    pass

def main():
    """
    TODO: Implement the main menu loop
    """
    # TODO: Implement the following:
    # 1. Create a loop to repeatedly show menu
    # 2. Show options (1-5)
    # 3. Get user choice
    # 4. Based on choice:
    #    - For low stock items: Get threshold, call function, display results
    #    - For search: Get search term, call function, display results
    #    - For category count: Call function, display results
    #    - For total value: Call function, display result
    #    - For exit: Break the loop
    # 5. Handle invalid inputs
    pass

if __name__ == "__main__":
    main()