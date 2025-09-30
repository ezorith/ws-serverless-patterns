#!/usr/bin/env python3
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import subprocess
import sys
import os

def run_unit_tests():
    """Run unit tests"""
    print("Running unit tests...")
    result = subprocess.run([
        "python3", "-m", "pytest", 
        "tests/unit/", 
        "-v", 
        "--tb=short"
    ], cwd=os.path.dirname(__file__))
    return result.returncode == 0

def run_integration_tests():
    """Run integration tests"""
    print("Running integration tests...")
    if not os.getenv('API_ENDPOINT'):
        print("Skipping integration tests - API_ENDPOINT not set")
        return True
    
    result = subprocess.run([
        "python3", "-m", "pytest", 
        "tests/integration/", 
        "-v", 
        "--tb=short"
    ], cwd=os.path.dirname(__file__))
    return result.returncode == 0

def main():
    """Run all tests"""
    print("=" * 50)
    print("Running Users API Test Suite")
    print("=" * 50)
    
    unit_success = run_unit_tests()
    integration_success = run_integration_tests()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Unit Tests: {'PASSED' if unit_success else 'FAILED'}")
    print(f"Integration Tests: {'PASSED' if integration_success else 'FAILED'}")
    print("=" * 50)
    
    if not (unit_success and integration_success):
        sys.exit(1)

if __name__ == "__main__":
    main()