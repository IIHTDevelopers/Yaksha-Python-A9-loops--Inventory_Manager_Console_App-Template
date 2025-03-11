import pytest
import inspect
from test.TestUtils import TestUtils
import inventory_manager_console_app as inventory_module

test_obj = TestUtils()

def test_input_validation():
    """Test validation of function input parameters"""
    try:
        # Check if required functions exist
        required_functions = ['find_low_stock_items', 'search_products', 
                            'generate_reorder_list', 'display_report']
        
        for func_name in required_functions:
            if not hasattr(inventory_module, func_name):
                test_obj.yakshaAssert("TestInputValidation", False, "exception")
                return
        
        find_low_stock_items = getattr(inventory_module, 'find_low_stock_items')
        search_products = getattr(inventory_module, 'search_products')
        generate_reorder_list = getattr(inventory_module, 'generate_reorder_list')
        display_report = getattr(inventory_module, 'display_report')
        
        # Test find_low_stock_items with invalid inputs
        with pytest.raises(TypeError):
            find_low_stock_items(None)
        
        with pytest.raises(TypeError):
            find_low_stock_items("10")  # String instead of int
        
        with pytest.raises(ValueError):
            find_low_stock_items(-5)  # Negative value
        
        # Test search_products with invalid inputs
        with pytest.raises(TypeError):
            search_products(None)
        
        with pytest.raises(TypeError):
            search_products(10)  # Integer instead of string
        
        # Test generate_reorder_list with invalid inputs
        with pytest.raises(ValueError):
            generate_reorder_list(-5)  # Negative value
        
        with pytest.raises(ValueError):
            generate_reorder_list(0)  # Zero value
        
        # Test display_report with invalid inputs
        with pytest.raises(ValueError):
            display_report("invalid_type", None)
        
        with pytest.raises(TypeError):
            display_report("low_stock", None)
        
        test_obj.yakshaAssert("TestInputValidation", True, "exception")
    except Exception:
        test_obj.yakshaAssert("TestInputValidation", False, "exception")

def test_inventory_data_validation():
    """Test validation of inventory data in functions"""
    try:
        # Check if required function exists
        if not hasattr(inventory_module, 'calculate_inventory_value'):
            test_obj.yakshaAssert("TestInventoryDataValidation", False, "exception")
            return
        
        calculate_inventory_value = getattr(inventory_module, 'calculate_inventory_value')
        
        # Backup original values
        quantities = inventory_module.quantities.copy()
        prices = inventory_module.prices.copy()
        
        # Test calculate_inventory_value with invalid quantities
        inventory_module.quantities[0] = "invalid"  # String instead of int
        with pytest.raises(TypeError):
            calculate_inventory_value()
        
        # Restore and test with invalid price
        inventory_module.quantities[0] = quantities[0]
        inventory_module.prices[0] = "invalid"  # String instead of number
        with pytest.raises(TypeError):
            calculate_inventory_value()
        
        # Restore and test with negative quantity
        inventory_module.prices[0] = prices[0]
        inventory_module.quantities[0] = -10
        with pytest.raises(ValueError):
            calculate_inventory_value()
        
        # Restore and test with negative price
        inventory_module.quantities[0] = quantities[0]
        inventory_module.prices[0] = -100.0
        with pytest.raises(ValueError):
            calculate_inventory_value()
        
        # Restore original values
        inventory_module.quantities[0] = quantities[0]
        inventory_module.prices[0] = prices[0]
        
        test_obj.yakshaAssert("TestInventoryDataValidation", True, "exception")
    except Exception:
        # Ensure original values are restored in case of exception
        if 'quantities' in locals() and 'prices' in locals():
            inventory_module.quantities[0] = quantities[0]
            inventory_module.prices[0] = prices[0]
        test_obj.yakshaAssert("TestInventoryDataValidation", False, "exception")

def test_display_report_validation():
    """Test validation in display_report function"""
    try:
        # Check if required function exists
        if not hasattr(inventory_module, 'display_report'):
            test_obj.yakshaAssert("TestDisplayReportValidation", False, "exception")
            return
        
        display_report = getattr(inventory_module, 'display_report')
        
        # Test display_report with different report types
        
        # Valid report type but invalid data
        with pytest.raises(TypeError):
            display_report("low_stock", None)
        
        # Invalid report type
        with pytest.raises(ValueError):
            display_report("invalid_type", ([], [], [], [], []))
        
        # Test data validation with empty results
        empty_data = ([], [], [], [], [])
        # This should not raise an exception
        display_report("low_stock", empty_data)
        
        # Test with mismatch input lists (different lengths)
        mismatched_data = (["P001"], ["Item1"], ["Cat1"], [10], [100.0, 200.0])  # Extra price
        try:
            display_report("low_stock", mismatched_data)
            # The function should handle this gracefully or raise an appropriate exception
            # We're not specifically testing for an exception here, but for graceful handling
            display_handles_mismatched = True
        except IndexError:
            # If the function doesn't handle the mismatch, we'll get an IndexError
            display_handles_mismatched = False
        
        test_obj.yakshaAssert("TestDisplayReportValidation", display_handles_mismatched, "exception")
    except Exception:
        test_obj.yakshaAssert("TestDisplayReportValidation", False, "exception")

def test_user_input_validation():
    """Test validation in user input handling function"""
    try:
        # Check if required function exists
        if not hasattr(inventory_module, 'get_valid_integer_input'):
            test_obj.yakshaAssert("TestUserInputValidation", False, "exception")
            return
        
        get_valid_integer_input = getattr(inventory_module, 'get_valid_integer_input')
        
        # We can't directly test the interactive input function with pytest
        # But we can check if the function exists and handles exceptions
        
        # Check if get_valid_integer_input function exists
        assert callable(get_valid_integer_input), "get_valid_integer_input function should exist"
        
        # Check function signature to ensure it accepts min/max parameters
        sig = inspect.signature(get_valid_integer_input)
        has_min_max = "min_value" in sig.parameters and "max_value" in sig.parameters
        
        # Check if the prompt parameter exists
        has_prompt = "prompt" in sig.parameters
        
        test_obj.yakshaAssert("TestUserInputValidation", has_min_max and has_prompt, "exception")
    except Exception:
        test_obj.yakshaAssert("TestUserInputValidation", False, "exception")