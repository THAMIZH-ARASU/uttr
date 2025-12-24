#!/usr/bin/env python3
"""
UTTR Test Runner
Runs all test files in the tests directory and reports results.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return success status."""
    try:
        result = subprocess.run(
            ['python', 'shell.py', test_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Test timed out"
    except Exception as e:
        return False, "", str(e)

def main():
    """Main test runner function."""
    print("=" * 60)
    print("  UTTR Language Test Suite Runner")
    print("=" * 60)
    print()
    
    # Get tests directory
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob('test_*.uttr'))
    
    if not test_files:
        print("No test files found in tests/ directory")
        return 1
    
    print(f"Found {len(test_files)} test files")
    print()
    
    # Run each test
    passed = 0
    failed = 0
    results = []
    
    for i, test_file in enumerate(test_files, 1):
        test_name = test_file.stem
        print(f"[{i}/{len(test_files)}] Running {test_name}...", end=' ')
        
        success, stdout, stderr = run_test(test_file)
        
        if success:
            print("✓ PASS")
            passed += 1
            results.append((test_name, True, None))
        else:
            print("✗ FAIL")
            failed += 1
            results.append((test_name, False, stderr))
    
    # Print summary
    print()
    print("=" * 60)
    print("  Test Summary")
    print("=" * 60)
    print(f"Total Tests: {len(test_files)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_files)*100):.1f}%")
    print()
    
    # Print failed tests details
    if failed > 0:
        print("Failed Tests:")
        for name, success, error in results:
            if not success:
                print(f"  - {name}")
                if error:
                    print(f"    Error: {error[:100]}")
        print()
    
    # Return exit code
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
