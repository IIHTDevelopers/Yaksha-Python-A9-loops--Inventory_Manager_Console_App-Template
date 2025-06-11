import unittest
import os
import importlib
import sys
import io
import contextlib
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
    
    def test_boundary_cases(self):
        """Test all boundary and edge cases for inventory functions (skeleton-aligned)"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return
            
            # Check required functions (matching skeleton)
            required_functions = [
                'find_low_stock_items',
                'search_products',
                'count_by_category',
                'calculate_total_value'
            ]
            
            for func_name in required_functions:
                if not check_function_exists(self.module_obj, func_name):
                    self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                    print("TestBoundaryScenarios = Failed")
                    return
            
            # Access functions directly (skeleton names)
            find_low_stock_items = getattr(self.module_obj, 'find_low_stock_items')
            search_products = getattr(self.module_obj, 'search_products')
            count_by_category = getattr(self.module_obj, 'count_by_category')
            calculate_total_value = getattr(self.module_obj, 'calculate_total_value')
            
            # Get data lists
            product_ids = self.module_obj.product_ids
            quantities = self.module_obj.quantities
            categories = self.module_obj.categories
            prices = self.module_obj.prices
            
            test_results = {}
            
            # Test 1: Zero threshold handling (skeleton validation: <= 0 or > 100)
            try:
                find_low_stock_items(0)
                test_results["zero_threshold"] = False
            except ValueError:
                test_results["zero_threshold"] = True
            except Exception:
                test_results["zero_threshold"] = False
            
            # Test 2: Above range threshold (skeleton validation: <= 0 or > 100)  
            try:
                find_low_stock_items(101)
                test_results["above_range_threshold"] = False
            except ValueError:
                test_results["above_range_threshold"] = True
            except Exception:
                test_results["above_range_threshold"] = False
            
            # Test 3: Valid threshold in range returns appropriate items
            try:
                result = find_low_stock_items(50)  # Within skeleton's 1-100 range
                # Skeleton expects "lists of product details" - format flexible
                valid_result = False
                if isinstance(result, (list, tuple)) and len(result) > 0:
                    valid_result = True
                test_results["valid_threshold"] = valid_result
            except Exception:
                test_results["valid_threshold"] = False
            
            # Test 4: Empty search term handling
            try:
                result = search_products("")
                # Should handle empty string appropriately
                valid_empty_search = isinstance(result, (list, tuple))
                test_results["empty_search"] = valid_empty_search
            except Exception:
                test_results["empty_search"] = False
            
            # Test 5: Non-matching search
            try:
                result = search_products("xyz123nonexistent")
                # Should return empty or no results
                no_matches = True
                if isinstance(result, (list, tuple)):
                    if isinstance(result, tuple) and len(result) > 0:
                        no_matches = len(result[0]) == 0 if hasattr(result[0], '__len__') else False
                    elif isinstance(result, list):
                        no_matches = len(result) == 0
                test_results["nonmatch_search"] = no_matches
            except Exception:
                test_results["nonmatch_search"] = False
            
            # Test 6: Case insensitive search
            try:
                result1 = search_products("rice")
                result2 = search_products("RICE") 
                # Should return same results regardless of case
                case_insensitive = (str(result1) == str(result2))
                test_results["case_search"] = case_insensitive
            except Exception:
                test_results["case_search"] = False
            
            # Test 7: Category counting basic functionality
            try:
                unique_categories, category_counts = count_by_category()
                # Should return proper category data: 2 Grocery, 1 Electronics
                valid_categories = (
                    isinstance(unique_categories, list) and 
                    isinstance(category_counts, list) and
                    "Grocery" in unique_categories and
                    "Electronics" in unique_categories and
                    2 in category_counts and 1 in category_counts
                )
                test_results["category_count"] = valid_categories
            except Exception:
                test_results["category_count"] = False
            
            # Test 8: Total value calculation
            try:
                result = calculate_total_value()
                # Should return a numeric value
                valid_total = isinstance(result, (int, float)) and result >= 0
                test_results["total_value"] = valid_total
            except Exception:
                test_results["total_value"] = False
            
            # Test 9: Large threshold (edge case within valid range)
            try:
                result = find_low_stock_items(100)  # Max valid value per skeleton
                # Should handle max valid threshold
                valid_max = isinstance(result, (list, tuple))
                test_results["max_threshold"] = valid_max
            except Exception:
                test_results["max_threshold"] = False
            
            # Test 10: Minimum threshold (edge case within valid range)
            try:
                result = find_low_stock_items(1)  # Min valid value per skeleton
                # Should handle min valid threshold
                valid_min = isinstance(result, (list, tuple))
                test_results["min_threshold"] = valid_min
            except Exception:
                test_results["min_threshold"] = False
            
            all_passed = all(test_results.values())
            
            if not all_passed:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
            else:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
                print("TestBoundaryScenarios = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            print("TestBoundaryScenarios = Failed")

if __name__ == '__main__':
    unittest.main()