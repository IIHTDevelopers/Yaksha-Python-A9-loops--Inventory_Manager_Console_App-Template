import pytest
import re
import inspect
import sys
from test.TestUtils import TestUtils
import importlib

# Import the module directly
import inventory_manager_console_app as inventory_module

test_obj = TestUtils()

def test_function_definitions():
    """Test if required functions are defined and callable"""
    try:
        required_functions = [
            'find_low_stock_items', 
            'search_products', 
            'summarize_categories', 
            'calculate_inventory_value', 
            'generate_reorder_list'
        ]
        
        all_funcs_found = True
        for func_name in required_functions:
            if not hasattr(inventory_module, func_name) or not callable(getattr(inventory_module, func_name)):
                all_funcs_found = False
                break
        
        test_obj.yakshaAssert("TestFunctionDefinitions", all_funcs_found, "functional")
    except Exception:
        test_obj.yakshaAssert("TestFunctionDefinitions", False, "functional")

def test_loop_implementations():
    """Test if required loop structures are implemented correctly"""
    try:
        # Check filtering loop in find_low_stock_items
        has_filtering_loop = False
        try:
            if hasattr(inventory_module, 'find_low_stock_items'):
                low_stock_code = inspect.getsource(getattr(inventory_module, 'find_low_stock_items'))
                has_filtering_loop = ("for" in low_stock_code and 
                                     "range(len(" in low_stock_code and
                                     "if" in low_stock_code and
                                     "append" in low_stock_code)
        except:
            pass
        
        # Check search loop in search_products
        has_search_loop = False
        try:
            if hasattr(inventory_module, 'search_products'):
                search_code = inspect.getsource(getattr(inventory_module, 'search_products'))
                has_search_loop = ("for" in search_code and 
                                  "range(len(" in search_code and
                                  "lower()" in search_code and
                                  "append" in search_code)
        except:
            pass
        
        # Check nested loops in summarize_categories
        has_nested_loops = False
        try:
            if hasattr(inventory_module, 'summarize_categories'):
                category_code = inspect.getsource(getattr(inventory_module, 'summarize_categories'))
                has_nested_loops = category_code.count("for") >= 2 and "set" in category_code
        except:
            pass
        
        # Check accumulation loop in calculate_inventory_value
        has_accumulation_loop = False
        try:
            if hasattr(inventory_module, 'calculate_inventory_value'):
                value_code = inspect.getsource(getattr(inventory_module, 'calculate_inventory_value'))
                has_accumulation_loop = ("for" in value_code and 
                                        "range(len(" in value_code and
                                        "+=" in value_code)
        except:
            pass
        
        all_loops_present = (has_filtering_loop and 
                            has_search_loop and 
                            has_nested_loops and 
                            has_accumulation_loop)
        
        test_obj.yakshaAssert("TestLoopImplementations", all_loops_present, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestLoopImplementations", False, "functional")

def test_business_logic():
    """Test if business logic is implemented correctly"""
    try:
        # Check required functions exist
        required_functions = ['find_low_stock_items', 'search_products', 
                             'summarize_categories', 'calculate_inventory_value', 
                             'generate_reorder_list']
        
        for func_name in required_functions:
            if not hasattr(inventory_module, func_name):
                test_obj.yakshaAssert("TestBusinessLogic", False, "functional")
                return
                
        # Test find_low_stock_items function
        try:
            find_low_stock_items = getattr(inventory_module, 'find_low_stock_items')
            low_stock_ids, _, _, low_stock_quantities, _ = find_low_stock_items(10)
            low_stock_correct = "P002" in low_stock_ids and 8 in low_stock_quantities
        except:
            low_stock_correct = False
        
        # Test search_products function
        try:
            search_products = getattr(inventory_module, 'search_products')
            search_ids, search_names, _, _, _ = search_products("rice")
            search_correct = "P001" in search_ids and "Rice 5kg" in search_names
        except:
            search_correct = False
        
        # Test summarize_categories function
        try:
            summarize_categories = getattr(inventory_module, 'summarize_categories')
            unique_categories, category_counts = summarize_categories()
            category_correct = "Grocery" in unique_categories and 2 in category_counts
        except:
            category_correct = False
        
        # Test calculate_inventory_value function
        try:
            calculate_inventory_value = getattr(inventory_module, 'calculate_inventory_value')
            expected_value = (45 * 250.00) + (8 * 60.00) + (15 * 300.00)
            actual_value = calculate_inventory_value()
            value_correct = abs(actual_value - expected_value) < 0.01
        except:
            value_correct = False
        
        # Test generate_reorder_list function
        try:
            generate_reorder_list = getattr(inventory_module, 'generate_reorder_list')
            reorder_names, reorder_quantities = generate_reorder_list(10)
            reorder_item = "Wheat Flour 1kg"
            reorder_correct = reorder_item in reorder_names 
            
            # Also check reorder quantity formula (3*low_stock - current_qty)
            if reorder_correct:
                idx = reorder_names.index(reorder_item)
                wheat_qty = 8  # Known quantity from the data
                expected_qty = (3 * 10) - wheat_qty
                reorder_correct = reorder_quantities[idx] == expected_qty
        except:
            reorder_correct = False
        
        all_logic_correct = (low_stock_correct and search_correct and 
                            category_correct and value_correct and
                            reorder_correct)
        
        test_obj.yakshaAssert("TestBusinessLogic", all_logic_correct, "functional")
    except Exception:
        test_obj.yakshaAssert("TestBusinessLogic", False, "functional")

def test_parallel_list_handling():
    """Test if the functions correctly handle parallel lists"""
    try:
        # Check required functions exist
        required_functions = ['find_low_stock_items', 'search_products', 
                             'summarize_categories', 'generate_reorder_list']
        
        for func_name in required_functions:
            if not hasattr(inventory_module, func_name):
                test_obj.yakshaAssert("TestParallelListHandling", False, "functional")
                return
        
        # Test that all functions return correct number of results
        try:
            find_low_stock_items = getattr(inventory_module, 'find_low_stock_items')
            low_ids, low_names, low_cats, low_quants, low_prices = find_low_stock_items(10)
            parallel_low_stock = (len(low_ids) == len(low_names) == len(low_cats) == 
                                len(low_quants) == len(low_prices))
        except:
            parallel_low_stock = False
        
        try:
            search_products = getattr(inventory_module, 'search_products')
            search_ids, search_names, search_cats, search_quants, search_prices = search_products("rice")
            parallel_search = (len(search_ids) == len(search_names) == len(search_cats) == 
                              len(search_quants) == len(search_prices))
        except:
            parallel_search = False
        
        try:
            summarize_categories = getattr(inventory_module, 'summarize_categories')
            cats, counts = summarize_categories()
            parallel_categories = len(cats) == len(counts)
        except:
            parallel_categories = False
        
        try:
            generate_reorder_list = getattr(inventory_module, 'generate_reorder_list')
            reorder_names, reorder_quantities = generate_reorder_list(10)
            parallel_reorder = len(reorder_names) == len(reorder_quantities)
        except:
            parallel_reorder = False
        
        all_parallel_correct = (parallel_low_stock and parallel_search and 
                               parallel_categories and parallel_reorder)
        
        test_obj.yakshaAssert("TestParallelListHandling", all_parallel_correct, "functional")
    except Exception:
        test_obj.yakshaAssert("TestParallelListHandling", False, "functional")