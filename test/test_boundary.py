import pytest
from test.TestUtils import TestUtils
import inventory_manager_console_app as inventory_module

test_obj = TestUtils()

def test_zero_and_large_values():
    """Test for zero values and large value handling"""
    try:
        # Check if required functions exist
        if not hasattr(inventory_module, 'find_low_stock_items') or not hasattr(inventory_module, 'generate_reorder_list'):
            test_obj.yakshaAssert("TestZeroAndLargeValues", False, "boundary")
            return

        find_low_stock_items = getattr(inventory_module, 'find_low_stock_items')
        generate_reorder_list = getattr(inventory_module, 'generate_reorder_list')
        
        # Test with threshold equal to zero (should raise ValueError)
        with pytest.raises(ValueError):
            find_low_stock_items(0)
        
        # Test with very large threshold that exceeds all quantities
        quantities = inventory_module.quantities
        product_ids = inventory_module.product_ids
        max_quantity = max(quantities)
        large_threshold = max_quantity + 10
        
        ids, names, cats, quants, prices = find_low_stock_items(large_threshold)
        all_items_returned = (len(ids) == len(product_ids) and 
                             len(names) == len(product_ids) and
                             len(cats) == len(product_ids))
        
        # Test reorder calculations with large threshold
        reorder_names, reorder_quantities = generate_reorder_list(large_threshold)
        correct_reorder_calculation = True
        for i in range(len(reorder_names)):
            name_idx = inventory_module.names.index(reorder_names[i])
            expected_quantity = (3 * large_threshold) - quantities[name_idx]
            if reorder_quantities[i] != expected_quantity:
                correct_reorder_calculation = False
                break
        
        test_obj.yakshaAssert("TestZeroAndLargeValues", 
                             all_items_returned and correct_reorder_calculation, 
                             "boundary")
    except Exception:
        test_obj.yakshaAssert("TestZeroAndLargeValues", False, "boundary")

def test_empty_and_edge_searches():
    """Test search function with empty and edge case search terms"""
    try:
        # Check if required function exists
        if not hasattr(inventory_module, 'search_products'):
            test_obj.yakshaAssert("TestEmptyAndEdgeSearches", False, "boundary")
            return

        search_products = getattr(inventory_module, 'search_products')
        product_ids = inventory_module.product_ids
        
        # Test with empty search string (should return all items)
        ids, names, cats, quants, prices = search_products("")
        empty_search_returns_all = len(ids) == len(product_ids)
        
        # Test with search term that matches nothing
        ids, names, cats, quants, prices = search_products("xyz123nonexistent")
        no_match_returns_empty = len(ids) == 0
        
        # Test with search term that is part of multiple items
        ids, names, cats, quants, prices = search_products("r")
        partial_match_works = len(ids) >= 2  # Should match "Rice" and "Charger"
        
        # Test with case variations
        ids1, _, _, _, _ = search_products("rice")
        ids2, _, _, _, _ = search_products("RICE")
        ids3, _, _, _, _ = search_products("Rice")
        case_insensitive = ids1 == ids2 == ids3
        
        test_obj.yakshaAssert("TestEmptyAndEdgeSearches", 
                             empty_search_returns_all and no_match_returns_empty and 
                             partial_match_works and case_insensitive, 
                             "boundary")
    except Exception:
        test_obj.yakshaAssert("TestEmptyAndEdgeSearches", False, "boundary")

def test_category_edge_cases():
    """Test category summarization with edge cases"""
    try:
        # Check if required function exists
        if not hasattr(inventory_module, 'summarize_categories'):
            test_obj.yakshaAssert("TestCategoryEdgeCases", False, "boundary")
            return

        summarize_categories = getattr(inventory_module, 'summarize_categories')
        
        # Backup original categories
        categories = inventory_module.categories.copy()
        product_ids = inventory_module.product_ids
        
        # Test with single category type (temporarily modify global list)
        for i in range(len(inventory_module.categories)):
            inventory_module.categories[i] = "SingleCategory"
        
        try:
            unique_cats, counts = summarize_categories()
            single_category_works = (len(unique_cats) == 1 and 
                                    unique_cats[0] == "SingleCategory" and 
                                    counts[0] == len(product_ids))
        finally:
            # Restore original categories
            for i in range(len(inventory_module.categories)):
                inventory_module.categories[i] = categories[i]
        
        # Test with normal categories (now restored)
        unique_cats, counts = summarize_categories()
        normal_categories_work = (len(unique_cats) == len(set(categories)) and
                                 sum(counts) == len(product_ids))
        
        test_obj.yakshaAssert("TestCategoryEdgeCases", 
                             single_category_works and normal_categories_work, 
                             "boundary")
    except Exception as e:
        # Ensure original categories are restored in case of exception
        if 'categories' in locals():
            for i in range(len(inventory_module.categories)):
                inventory_module.categories[i] = categories[i]
        test_obj.yakshaAssert("TestCategoryEdgeCases", False, "boundary")

def test_value_calculation_boundary():
    """Test inventory value calculation with boundary cases"""
    try:
        # Check if required function exists
        if not hasattr(inventory_module, 'calculate_inventory_value'):
            test_obj.yakshaAssert("TestValueCalculationBoundary", False, "boundary")
            return

        calculate_inventory_value = getattr(inventory_module, 'calculate_inventory_value')
        
        # Backup original values
        quantities = inventory_module.quantities.copy()
        prices = inventory_module.prices.copy()
        
        # Test with all zero quantities
        for i in range(len(inventory_module.quantities)):
            inventory_module.quantities[i] = 0
        
        try:
            total_value = calculate_inventory_value()
            zero_quantities_gives_zero = total_value == 0
        finally:
            # Restore original quantities
            for i in range(len(inventory_module.quantities)):
                inventory_module.quantities[i] = quantities[i]
        
        # Test with one very large value
        large_quantity = 1000000
        inventory_module.quantities[0] = large_quantity
        
        try:
            large_total = calculate_inventory_value()
            expected_large_total = (large_quantity * prices[0])
            for i in range(1, len(quantities)):
                expected_large_total += quantities[i] * prices[i]
            
            large_value_calculated_correctly = abs(large_total - expected_large_total) < 0.01
        finally:
            # Restore original quantities
            inventory_module.quantities[0] = quantities[0]
        
        test_obj.yakshaAssert("TestValueCalculationBoundary", 
                             zero_quantities_gives_zero and large_value_calculated_correctly, 
                             "boundary")
    except Exception:
        # Ensure original values are restored in case of exception
        if 'quantities' in locals() and 'prices' in locals():
            for i in range(len(inventory_module.quantities)):
                inventory_module.quantities[i] = quantities[i]
            for i in range(len(inventory_module.prices)):
                inventory_module.prices[i] = prices[i]
        test_obj.yakshaAssert("TestValueCalculationBoundary", False, "boundary")