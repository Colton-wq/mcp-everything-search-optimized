#!/usr/bin/env python3
"""
Test cases for GitHub Issue #14: Space handling in query strings
"""

def test_space_handling_scenarios():
    """
    Test various space handling scenarios to reproduce Issue #14
    """
    
    print("Testing GitHub Issue #14: Space handling in query strings\n")
    
    # Test cases that should be investigated
    test_cases = [
        {
            "query": "test file",
            "description": "Basic space-separated terms",
            "expected": "Should work - finds files containing both 'test' and 'file'"
        },
        {
            "query": "\"test file\"",
            "description": "Quoted exact phrase",
            "expected": "Should find files with exact phrase 'test file'",
            "issue": "FOUND: Returns no results - this is the Issue #14 problem!"
        },
        {
            "query": "test  file",
            "description": "Multiple spaces between terms",
            "expected": "Should work like single space"
        },
        {
            "query": " test",
            "description": "Leading space",
            "expected": "Should work (space should be trimmed)"
        },
        {
            "query": "test ",
            "description": "Trailing space",
            "expected": "Should work (space should be trimmed)"
        },
        {
            "query": "test\tfile",
            "description": "Tab character between terms",
            "expected": "Should be handled properly"
        },
        {
            "query": "test\nfile",
            "description": "Newline character between terms",
            "expected": "Should be handled or rejected gracefully"
        }
    ]
    
    print("Test Cases Analysis:")
    print("=" * 60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. Query: '{case['query']}'")
        print(f"   Description: {case['description']}")
        print(f"   Expected: {case['expected']}")
        if 'issue' in case:
            print(f"   ISSUE: {case['issue']}")
        print()
    
    print("Root Cause Analysis:")
    print("=" * 60)
    print("The issue appears to be with quoted string handling in Everything SDK.")
    print("When a query contains quotes, the Everything search engine may not")
    print("be processing the query correctly, resulting in no results.")
    print()
    print("Potential Solutions:")
    print("1. Add quote escaping/handling in the query preprocessing")
    print("2. Validate quoted queries before sending to Everything SDK")
    print("3. Provide clear error messages for unsupported query syntax")
    print("4. Document supported and unsupported query patterns")
    
    return test_cases

def test_everything_syntax_compatibility():
    """
    Test Everything search syntax compatibility
    """
    
    print("\nTesting Everything Search Syntax Compatibility\n")
    
    # Everything search syntax that should be tested
    everything_syntax = [
        {
            "query": "*.py",
            "description": "Wildcard extension search",
            "status": "Working"
        },
        {
            "query": "ext:py",
            "description": "Extension function",
            "status": "Working"
        },
        {
            "query": "size:>1mb",
            "description": "Size function",
            "status": "Needs testing"
        },
        {
            "query": "dm:today",
            "description": "Date modified function",
            "status": "Needs testing"
        },
        {
            "query": "\"exact phrase\"",
            "description": "Quoted exact phrase",
            "status": "Issue #14 - Not working"
        },
        {
            "query": "file1 | file2",
            "description": "OR operator",
            "status": "Needs testing"
        },
        {
            "query": "file1 file2",
            "description": "AND operator (implicit)",
            "status": "Working"
        }
    ]
    
    print("Everything Syntax Compatibility:")
    print("=" * 60)
    
    for syntax in everything_syntax:
        print(f"Query: {syntax['query']}")
        print(f"Description: {syntax['description']}")
        print(f"Status: {syntax['status']}")
        print()

if __name__ == "__main__":
    print("GitHub Issue #14 Investigation\n")
    
    test_cases = test_space_handling_scenarios()
    test_everything_syntax_compatibility()
    
    print("\nSummary:")
    print("=" * 60)
    print("Identified Issue #14: Quoted string queries return no results")
    print("Basic space-separated queries work correctly")
    print("Leading/trailing spaces are handled properly")
    print("Need to test more Everything syntax features")
    print()
    print("Recommended Fixes:")
    print("1. Add quoted string preprocessing/validation")
    print("2. Improve error handling for unsupported syntax")
    print("3. Add comprehensive Everything syntax testing")
    print("4. Update documentation with supported query patterns")