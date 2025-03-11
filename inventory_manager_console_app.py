# Using separate lists for inventory data
product_ids = ["P001", "P002", "P003"]
names = ["Rice 5kg", "Wheat Flour 1kg", "Mobile Charger"]
categories = ["Grocery", "Grocery", "Electronics"]
quantities = [45, 8, 15]
prices = [250.00, 60.00, 300.00]

def find_low_stock_items(low_stock):
    """
    Find all items with quantity less than or equal to low_stock threshold
    Return: Lists of product details for low stock items
    """
    if low_stock is None: 
        raise TypeError("Low stock threshold cannot be None")
        
    if not isinstance(low_stock, int):
        raise TypeError("Low stock threshold must be an integer")
    if low_stock <= 0:
        raise ValueError("Low stock threshold must be positive")
    
    low_stock_ids = []
    low_stock_names = []
    low_stock_categories = []
    low_stock_quantities = []
    low_stock_prices = []
    
    for i in range(len(product_ids)):
        if quantities[i] <= low_stock:
            low_stock_ids.append(product_ids[i])
            low_stock_names.append(names[i])
            low_stock_categories.append(categories[i])
            low_stock_quantities.append(quantities[i])
            low_stock_prices.append(prices[i])
            
    return low_stock_ids, low_stock_names, low_stock_categories, low_stock_quantities, low_stock_prices

def search_products(search_term):
    """
    Search for products where name contains search_term (case-insensitive)
    Return: Lists of product details for matching items
    """
    if search_term is None:
        raise TypeError("Search term cannot be None")
    if not isinstance(search_term, str):
        raise TypeError("Search term must be a string")
    
    if not search_term:
        return product_ids[:], names[:], categories[:], quantities[:], prices[:]
    
    matching_ids = []
    matching_names = []
    matching_categories = []
    matching_quantities = []
    matching_prices = []
    
    search_term = search_term.lower()
    for i in range(len(names)):
        if search_term in names[i].lower():
            matching_ids.append(product_ids[i])
            matching_names.append(names[i])
            matching_categories.append(categories[i])
            matching_quantities.append(quantities[i])
            matching_prices.append(prices[i])
            
    return matching_ids, matching_names, matching_categories, matching_quantities, matching_prices

def summarize_categories():
    """
    Group items by category and count them
    Return: Lists of categories and their counts
    """
    category_set = set(categories)
    unique_categories = list(category_set)
    category_counts = []
    
    for cat in unique_categories:
        count = 0
        for i in range(len(categories)):
            if categories[i] == cat:
                count += 1
        category_counts.append(count)
        
    return unique_categories, category_counts

def calculate_inventory_value():
    """
    Calculate total value of inventory (quantity * price for each item)
    Return: Float representing total value
    """
    total_value = 0.0
    
    for i in range(len(product_ids)):
        if not isinstance(quantities[i], int):
            raise TypeError("Quantity must be an integer")
        if not isinstance(prices[i], (int, float)):
            raise TypeError("Price must be a number")
        if prices[i] < 0:
            raise ValueError("Price cannot be negative")
        if quantities[i] < 0:
            raise ValueError("Quantity cannot be negative")
            
        total_value += quantities[i] * prices[i]
        
    return total_value

def generate_reorder_list(low_stock):
    """
    Generate list of items to reorder based on low_stock threshold
    Return: Lists with item names and reorder quantities
    """
    if low_stock <= 0:
        raise ValueError("Low stock threshold must be positive")
    
    reorder_names = []
    reorder_quantities = []
    
    for i in range(len(product_ids)):
        if quantities[i] <= low_stock:
            reorder_quantity = (3 * low_stock) - quantities[i]
            reorder_names.append(names[i])
            reorder_quantities.append(reorder_quantity)
            
    return reorder_names, reorder_quantities

def display_report(report_type, data):
    """
    Display the report in tabular format based on report type
    """
    if report_type not in ["low_stock", "search", "categories", "value", "reorder"]:
        raise ValueError("Invalid report type")
    if data is None:
        raise TypeError("Report data cannot be None")
    
    if report_type == "low_stock":
        ids, item_names, item_categories, item_quantities, item_prices = data
        print("\nLow Stock Items Report:")
        print("-" * 60)
        if len(ids) == 0:
            print("No items below the specified threshold.")
        else:
            print(f"{'Product ID':<12}{'Name':<20}{'Category':<15}{'Quantity':<10}{'Price':<10}")
            print("-" * 60)
            for i in range(len(ids)):
                print(f"{ids[i]:<12}{item_names[i]:<20}{item_categories[i]:<15}{item_quantities[i]:<10}{item_prices[i]:<10.2f}")

    elif report_type == "search":
        ids, item_names, item_categories, item_quantities, item_prices = data
        print("\nSearch Results:")
        print("-" * 60)
        if len(ids) == 0:
            print("No matching items found.")
        else:
            print(f"{'Product ID':<12}{'Name':<20}{'Category':<15}{'Quantity':<10}{'Price':<10}")
            print("-" * 60)
            for i in range(len(ids)):
                print(f"{ids[i]:<12}{item_names[i]:<20}{item_categories[i]:<15}{item_quantities[i]:<10}{item_prices[i]:<10.2f}")

    elif report_type == "categories":
        unique_categories, category_counts = data
        print("\nCategory Summary Report:")
        print("-" * 30)
        print(f"{'Category':<20}{'Count':<10}")
        print("-" * 30)
        for i in range(len(unique_categories)):
            print(f"{unique_categories[i]:<20}{category_counts[i]:<10}")

    elif report_type == "value":
        total_value = data
        print("\nTotal Inventory Value Report:")
        print("-" * 30)
        print(f"Total Value: ${total_value:,.2f}")

    elif report_type == "reorder":
        reorder_names, reorder_quantities = data
        print("\nReorder List Report:")
        print("-" * 40)
        if len(reorder_names) == 0:
            print("No items need reordering.")
        else:
            print(f"{'Product Name':<25}{'Reorder Quantity':<15}")
            print("-" * 40)
            for i in range(len(reorder_names)):
                print(f"{reorder_names[i]:<25}{reorder_quantities[i]:<15}")

def get_valid_integer_input(prompt, min_value=None, max_value=None):
    """Get a valid integer input from the user"""
    while True:
        try:
            value = input(prompt)
            value = int(value)
            
            if min_value is not None and value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}.")
                continue
                
            if max_value is not None and value > max_value:
                print(f"Please enter a number less than or equal to {max_value}.")
                continue
                
            return value
        except ValueError:
            print("Please enter a valid number.")

def show_help():
    """Display help information for the user"""
    print("\n--- HELP INFORMATION ---")
    print("This program helps you manage your inventory:")
    print("1. View Low Stock Items: Shows items with quantity below a threshold")
    print("   - You'll need to enter a threshold number (like 10)")
    print("2. Search Products: Find products by name")
    print("   - Enter part of a product name (like 'rice')")
    print("3. View Category Summary: Shows count of items by category")
    print("4. Calculate Total Inventory Value: Shows total value of all items")
    print("5. Generate Reorder List: Creates a list of items to reorder")
    print("   - You'll need to enter a threshold number")
    print("6. Exit: Quit the program")
    print("H. Help: Show this help information")
    input("\nPress Enter to continue...")

def main():
    """
    Main function to run the inventory management system
    """
    print("\nWelcome to the Inventory Management System!")
    print("Enter 'H' at any time to get help.")
    
    while True:
        print("\nInventory Management System - Main Menu")
        print("1. View Low Stock Items")
        print("2. Search Products")
        print("3. View Category Summary")
        print("4. Calculate Total Inventory Value")
        print("5. Generate Reorder List")
        print("6. Exit")
        print("H. Help")
        
        choice = input("\nEnter your choice (1-6 or H): ").strip().upper()
        
        if choice == 'H':
            show_help()
            continue
        
        if choice == '1':
            print("\n--- View Low Stock Items ---")
            print("This shows items with quantity below your specified threshold.")
            low_stock = get_valid_integer_input("Enter low stock threshold (1-100): ", 1, 100)
            data = find_low_stock_items(low_stock)
            display_report("low_stock", data)
            
        elif choice == '2':
            print("\n--- Search Products ---")
            print("This searches for products containing your search term.")
            search_term = input("Enter search term (leave empty to show all): ")
            results = search_products(search_term)
            display_report("search", results)
            
        elif choice == '3':
            print("\n--- View Category Summary ---")
            print("This shows the count of items in each category.")
            data = summarize_categories()
            display_report("categories", data)
            
        elif choice == '4':
            print("\n--- Calculate Total Inventory Value ---")
            print("This shows the total value of all inventory items.")
            total_value = calculate_inventory_value()
            display_report("value", total_value)
            
        elif choice == '5':
            print("\n--- Generate Reorder List ---")
            print("This creates a list of items to reorder based on your threshold.")
            low_stock = get_valid_integer_input("Enter low stock threshold (1-100): ", 1, 100)
            data = generate_reorder_list(low_stock)
            display_report("reorder", data)
            
        elif choice == '6':
            print("Thank you for using the Inventory Management System!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 6, or H for help.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()