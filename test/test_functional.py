import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
import re
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_function_definitions(self):
        """Test if required skeleton functions are defined and callable"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestRequiredFunctionNames", False, "functional")
                print("TestRequiredFunctionNames = Failed")
                return
            
            # Check if required skeleton functions exist
            required_functions = [
                'find_low_stock_items', 
                'search_products', 
                'count_by_category', 
                'calculate_total_value'
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not hasattr(self.module_obj, func_name) or not callable(getattr(self.module_obj, func_name, None)):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestRequiredFunctionNames", False, "functional")
                print("TestRequiredFunctionNames = Failed")
                return
            
            self.test_obj.yakshaAssert("TestRequiredFunctionNames", True, "functional")
            print("TestRequiredFunctionNames = Passed")
            
        except Exception as e:
            self.test_obj.yakshaAssert("TestRequiredFunctionNames", False, "functional")
            print("TestRequiredFunctionNames = Failed")
    
    def test_loop_implementations(self):
        """Test if required loop structures are implemented correctly"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestLambdaUsage", False, "functional")
                print("TestLambdaUsage = Failed")
                return
            
            # Check if all required functions are defined
            required_functions = [
                'find_low_stock_items', 
                'search_products', 
                'count_by_category', 
                'calculate_total_value'
            ]
            
            missing_functions = []
            for func_name in required_functions:
                if not hasattr(self.module_obj, func_name) or not callable(getattr(self.module_obj, func_name, None)):
                    missing_functions.append(func_name)
            
            if missing_functions:
                self.test_obj.yakshaAssert("TestLambdaUsage", False, "functional")
                print("TestLambdaUsage = Failed")
                return
            
            # Check if functions can execute (indicating implementation exists)
            functions_implemented = 0
            
            # Test find_low_stock_items implementation
            try:
                find_low_stock_items = getattr(self.module_obj, 'find_low_stock_items')
                result = find_low_stock_items(10)
                if result is not None:
                    functions_implemented += 1
            except Exception:
                pass
            
            # Test search_products implementation
            try:
                search_products = getattr(self.module_obj, 'search_products')
                result = search_products("rice")
                if result is not None:
                    functions_implemented += 1
            except Exception:
                pass
            
            # Test count_by_category implementation
            try:
                count_by_category = getattr(self.module_obj, 'count_by_category')
                result = count_by_category()
                if result is not None:
                    functions_implemented += 1
            except Exception:
                pass
            
            # Test calculate_total_value implementation
            try:
                calculate_total_value = getattr(self.module_obj, 'calculate_total_value')
                result = calculate_total_value()
                if result is not None and isinstance(result, (int, float)):
                    functions_implemented += 1
            except Exception:
                pass
            
            # All 4 skeleton functions should be implemented
            all_implemented = (functions_implemented == 4)
            
            self.test_obj.yakshaAssert("TestLambdaUsage", all_implemented, "functional")
            if all_implemented:
                print("TestLambdaUsage = Passed")
            else:
                print("TestLambdaUsage = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestLambdaUsage", False, "functional")
            print("TestLambdaUsage = Failed")
    
    def test_business_logic(self):
        """Test if business logic is implemented correctly per skeleton requirements"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFunctionLogic", False, "functional")
                print("TestFunctionLogic = Failed")
                return
            
            # Check required functions exist
            required_functions = ['find_low_stock_items', 'search_products', 
                                 'count_by_category', 'calculate_total_value']
            
            for func_name in required_functions:
                if not hasattr(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestFunctionLogic", False, "functional")
                    print("TestFunctionLogic = Failed")
                    return
            
            logic_tests_passed = 0
            
            # Test find_low_stock_items business logic
            try:
                find_low_stock_items = getattr(self.module_obj, 'find_low_stock_items')
                # Looking for items with quantity <= 10: P002 (Wheat Flour, qty=8)
                result = find_low_stock_items(10)
                
                # Check if it identifies low stock items correctly
                found_low_stock = False
                if isinstance(result, (list, tuple)):
                    # Format may vary, but should include wheat flour info
                    result_str = str(result).lower()
                    if "wheat" in result_str or "8" in result_str or "p002" in result_str:
                        found_low_stock = True
                
                if found_low_stock:
                    logic_tests_passed += 1
            except Exception:
                pass
            
            # Test search_products business logic
            try:
                search_products = getattr(self.module_obj, 'search_products')
                # Should find "Rice 5kg" when searching for "rice"
                result = search_products("rice")
                
                found_rice = False
                if isinstance(result, (list, tuple)):
                    result_str = str(result).lower()
                    if "rice" in result_str or "p001" in result_str:
                        found_rice = True
                
                if found_rice:
                    logic_tests_passed += 1
            except Exception:
                pass
            
            # Test count_by_category business logic
            try:
                count_by_category = getattr(self.module_obj, 'count_by_category')
                # Should identify 2 Grocery items and 1 Electronics item
                unique_categories, category_counts = count_by_category()
                
                correct_categories = False
                if isinstance(unique_categories, list) and isinstance(category_counts, list):
                    # Check if we have the right categories and counts
                    grocery_idx = -1
                    electronics_idx = -1
                    
                    for i, cat in enumerate(unique_categories):
                        if cat == "Grocery":
                            grocery_idx = i
                        elif cat == "Electronics":
                            electronics_idx = i
                    
                    if (grocery_idx >= 0 and electronics_idx >= 0 and
                        category_counts[grocery_idx] == 2 and
                        category_counts[electronics_idx] == 1):
                        correct_categories = True
                
                if correct_categories:
                    logic_tests_passed += 1
            except Exception:
                pass
            
            # Test calculate_total_value business logic
            try:
                calculate_total_value = getattr(self.module_obj, 'calculate_total_value')
                # Expected: (45*250) + (8*60) + (15*300) = 11250 + 480 + 4500 = 16230
                result = calculate_total_value()
                
                correct_total = False
                if isinstance(result, (int, float)):
                    expected = (45 * 250.0) + (8 * 60.0) + (15 * 300.0)
                    if abs(result - expected) < 0.01:
                        correct_total = True
                
                if correct_total:
                    logic_tests_passed += 1
            except Exception:
                pass
            
            # All 4 business logic tests should pass
            all_logic_correct = (logic_tests_passed == 4)
            
            self.test_obj.yakshaAssert("TestFunctionLogic", all_logic_correct, "functional")
            if all_logic_correct:
                print("TestFunctionLogic = Passed")
            else:
                print("TestFunctionLogic = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestFunctionLogic", False, "functional")
            print("TestFunctionLogic = Failed")
    
    def test_data_structure_handling(self):
        """Test if functions correctly handle the parallel list data structure"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestDataStructures", False, "functional")
                print("TestDataStructures = Failed")
                return
            
            # Check if data structures exist
            required_data = ['product_ids', 'names', 'categories', 'quantities', 'prices']
            
            for data_name in required_data:
                if not hasattr(self.module_obj, data_name):
                    self.test_obj.yakshaAssert("TestDataStructures", False, "functional")
                    print("TestDataStructures = Failed")
                    return
            
            # Verify data consistency (parallel lists should have same length)
            product_ids = self.module_obj.product_ids
            names = self.module_obj.names
            categories = self.module_obj.categories
            quantities = self.module_obj.quantities
            prices = self.module_obj.prices
            
            data_consistent = (len(product_ids) == len(names) == len(categories) == 
                             len(quantities) == len(prices) == 3)
            
            # Verify expected sample data exists
            expected_data = (
                "P001" in product_ids and
                "Rice 5kg" in names and
                "Grocery" in categories and
                45 in quantities and
                250.00 in prices
            )
            
            # Test if functions use the data structure correctly
            functions_use_data = 0
            
            # Test find_low_stock_items uses data
            try:
                find_low_stock_items = getattr(self.module_obj, 'find_low_stock_items')
                result = find_low_stock_items(50)  # Should return all items
                if result is not None:
                    functions_use_data += 1
            except Exception:
                pass
            
            # Test search_products uses data
            try:
                search_products = getattr(self.module_obj, 'search_products')
                result = search_products("Rice")
                if result is not None:
                    functions_use_data += 1
            except Exception:
                pass
            
            # Test count_by_category uses data
            try:
                count_by_category = getattr(self.module_obj, 'count_by_category')
                result = count_by_category()
                if result is not None:
                    functions_use_data += 1
            except Exception:
                pass
            
            # Test calculate_total_value uses data
            try:
                calculate_total_value = getattr(self.module_obj, 'calculate_total_value')
                result = calculate_total_value()
                if result is not None and result > 0:
                    functions_use_data += 1
            except Exception:
                pass
            
            all_data_correct = (data_consistent and expected_data and functions_use_data == 4)
            
            self.test_obj.yakshaAssert("TestDataStructures", all_data_correct, "functional")
            if all_data_correct:
                print("TestDataStructures = Passed")
            else:
                print("TestDataStructures = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestDataStructures", False, "functional")
            print("TestDataStructures = Failed")
    
    def test_main_function_structure(self):
        """Test if main function exists and has basic structure"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestDemonstrationFunctions", False, "functional")
                print("TestDemonstrationFunctions = Failed")
                return
            
            # Check if main function exists
            if not hasattr(self.module_obj, 'main') or not callable(getattr(self.module_obj, 'main', None)):
                self.test_obj.yakshaAssert("TestDemonstrationFunctions", False, "functional")
                print("TestDemonstrationFunctions = Failed")
                return
            
            # Check if main function can be called (basic structure test)
            main_function_exists = True
            
            try:
                # Try to get the source code to check for basic structure
                main_func = getattr(self.module_obj, 'main')
                source = inspect.getsource(main_func)
                
                # Check for basic menu structure elements
                has_loop = "while" in source or "for" in source
                has_menu = "print" in source and ("choice" in source or "input" in source)
                has_function_calls = any(func in source for func in [
                    "find_low_stock_items", "search_products", 
                    "count_by_category", "calculate_total_value"
                ])
                
                main_structure_correct = has_loop and has_menu and has_function_calls
                
            except Exception:
                # If we can't inspect source, just check if main exists and is callable
                main_structure_correct = callable(main_func)
            
            # Test data structure initialization
            data_initialized = True
            try:
                # Check if required data exists and has correct initial values
                expected_products = ["P001", "P002", "P003"]
                expected_names = ["Rice 5kg", "Wheat Flour 1kg", "Mobile Charger"]
                
                actual_ids = getattr(self.module_obj, 'product_ids', [])
                actual_names = getattr(self.module_obj, 'names', [])
                
                data_initialized = (
                    actual_ids == expected_products and
                    actual_names == expected_names
                )
            except Exception:
                data_initialized = False
            
            all_demo_correct = main_function_exists and main_structure_correct and data_initialized
            
            self.test_obj.yakshaAssert("TestDemonstrationFunctions", all_demo_correct, "functional")
            if all_demo_correct:
                print("TestDemonstrationFunctions = Passed")
            else:
                print("TestDemonstrationFunctions = Failed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestDemonstrationFunctions", False, "functional")
            print("TestDemonstrationFunctions = Failed")

if __name__ == '__main__':
    unittest.main()