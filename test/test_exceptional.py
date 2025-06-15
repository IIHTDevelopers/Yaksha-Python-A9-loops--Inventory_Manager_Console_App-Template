import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
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
    
    def test_exceptional_cases(self):
        """Test validation and exception handling for skeleton functions"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
                return
            
            # Check required functions (skeleton functions only)
            required_functions = [
                'find_low_stock_items',
                'search_products',
                'count_by_category',
                'calculate_total_value'
            ]
            
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                    print("TestErrorHandling = Failed")
                    return
            
            # Access functions directly
            find_low_stock_items = getattr(self.module_obj, 'find_low_stock_items')
            search_products = getattr(self.module_obj, 'search_products')
            count_by_category = getattr(self.module_obj, 'count_by_category')
            calculate_total_value = getattr(self.module_obj, 'calculate_total_value')
            
            # Track test results
            test_results = {}
            
            # Input validation tests for find_low_stock_items
            
            # Test 1: find_low_stock_items with None (skeleton has this validation)
            try:
                find_low_stock_items(None)
                test_results["none_threshold"] = False
            except TypeError:
                test_results["none_threshold"] = True
            except Exception:
                test_results["none_threshold"] = False
            
            # Test 2: find_low_stock_items with string (skeleton has this validation)
            try:
                find_low_stock_items("10")
                test_results["string_threshold"] = False
            except TypeError:
                test_results["string_threshold"] = True
            except Exception:
                test_results["string_threshold"] = False
            
            # Test 3: find_low_stock_items with negative value (skeleton validation: <= 0)
            try:
                find_low_stock_items(-5)
                test_results["negative_threshold"] = False
            except ValueError:
                test_results["negative_threshold"] = True
            except Exception:
                test_results["negative_threshold"] = False
            
            # Test 4: find_low_stock_items above range (skeleton validation: > 100)
            try:
                find_low_stock_items(150)
                test_results["above_range_threshold"] = False
            except ValueError:
                test_results["above_range_threshold"] = True
            except Exception:
                test_results["above_range_threshold"] = False
            
            # Input validation tests for search_products
            
            # Test 5: search_products with None (skeleton has this validation)
            try:
                search_products(None)
                test_results["none_search"] = False
            except TypeError:
                test_results["none_search"] = True
            except Exception:
                test_results["none_search"] = False
            
            # Test 6: search_products with number (skeleton has this validation)
            try:
                search_products(10)
                test_results["number_search"] = False
            except TypeError:
                test_results["number_search"] = True
            except Exception:
                test_results["number_search"] = False
            
            # Function existence and basic functionality tests
            
            # Test 7: count_by_category can be called (no parameters expected)
            try:
                result = count_by_category()
                test_results["category_callable"] = True
            except Exception:
                test_results["category_callable"] = False
            
            # Test 8: calculate_total_value can be called (no parameters expected)
            try:
                result = calculate_total_value()
                test_results["total_value_callable"] = True
            except Exception:
                test_results["total_value_callable"] = False
            
            # Test 9: find_low_stock_items with valid input works
            try:
                result = find_low_stock_items(10)
                test_results["valid_low_stock"] = True
            except Exception:
                test_results["valid_low_stock"] = False
            
            # Test 10: search_products with valid input works
            try:
                result = search_products("rice")
                test_results["valid_search"] = True
            except Exception:
                test_results["valid_search"] = False
            
            # Data type validation (basic checks)
            
            # Test 11: Functions return appropriate data types
            try:
                low_stock_result = find_low_stock_items(10)
                search_result = search_products("test")
                category_result = count_by_category()
                value_result = calculate_total_value()
                
                # Check that results are reasonable data types
                valid_types = (
                    isinstance(low_stock_result, (list, tuple)) and
                    isinstance(search_result, (list, tuple)) and
                    isinstance(category_result, (list, tuple, dict)) and
                    isinstance(value_result, (int, float))
                )
                test_results["return_types"] = valid_types
            except Exception:
                test_results["return_types"] = False
            
            # Check if all tests passed
            all_passed = all(test_results.values())
            
            if not all_passed:
                self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
                print("TestErrorHandling = Failed")
            else:
                self.test_obj.yakshaAssert("TestErrorHandling", True, "exception")
                print("TestErrorHandling = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestErrorHandling", False, "exception")
            print("TestErrorHandling = Failed")

if __name__ == '__main__':
    unittest.main()