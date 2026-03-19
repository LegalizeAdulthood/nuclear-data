#!/usr/bin/env python3
"""
Test runner for ND812 disassembler.

Usage:
    python run-test.py <test-name>

Runs the disassembler on test/<test-name>.bin and compares
the output to test/<test-name>.asm.
"""

import argparse
import os
import subprocess
import sys


def run_test(test_name):
    """Run a single disassembler test and compare output."""
    # Construct paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    disasm_script = os.path.join(project_dir, "disassemble.py")
    bin_file = os.path.join(script_dir, f"{test_name}.bin")
    asm_file = os.path.join(script_dir, f"{test_name}.asm")

    # Check if test files exist
    if not os.path.exists(bin_file):
        print(f"ERROR: Test binary file not found: {bin_file}")
        return False

    if not os.path.exists(asm_file):
        print(f"ERROR: Expected output file not found: {asm_file}")
        return False

    # Run disassembler
    try:
        result = subprocess.run(
            [sys.executable, disasm_script, bin_file],
            capture_output=True,
            text=True,
            check=True
        )
        actual_output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Disassembler failed with exit code {e.returncode}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to run disassembler: {e}")
        return False

    # Read expected output
    try:
        with open(asm_file, 'r') as f:
            expected_output = f.read()
    except Exception as e:
        print(f"ERROR: Failed to read expected output: {e}")
        return False

    # Compare outputs
    actual_lines = actual_output.splitlines()
    expected_lines = expected_output.splitlines()

    if actual_lines == expected_lines:
        print(f"PASS: {test_name}")
        return True
    else:
        print(f"FAIL: {test_name}")
        print(f"\nExpected {len(expected_lines)} lines, got {len(actual_lines)} lines")
        
        # Show differences
        max_lines = max(len(expected_lines), len(actual_lines))
        diff_count = 0
        for i in range(max_lines):
            if i >= len(expected_lines):
                print(f"  Line {i+1}: EXTRA in actual output")
                print(f"    Actual:   '{actual_lines[i]}'")
                diff_count += 1
                if diff_count >= 10:
                    print(f"  ... ({max_lines - i - 1} more lines)")
                    break
            elif i >= len(actual_lines):
                print(f"  Line {i+1}: MISSING from actual output")
                print(f"    Expected: '{expected_lines[i]}'")
                diff_count += 1
                if diff_count >= 10:
                    print(f"  ... ({max_lines - i - 1} more lines)")
                    break
            elif expected_lines[i] != actual_lines[i]:
                print(f"  Line {i+1}: MISMATCH")
                print(f"    Expected: '{expected_lines[i]}'")
                print(f"    Actual:   '{actual_lines[i]}'")
                diff_count += 1
                if diff_count >= 10:
                    remaining_diffs = sum(1 for j in range(i+1, max_lines) 
                                         if j >= len(expected_lines) or j >= len(actual_lines) 
                                         or expected_lines[j] != actual_lines[j])
                    if remaining_diffs > 0:
                        print(f"  ... ({remaining_diffs} more differences)")
                    break
        
        return False


def main():
    parser = argparse.ArgumentParser(description="ND812 disassembler test runner")
    parser.add_argument("test_name", help="Name of test to run (without .bin/.asm extension)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    success = run_test(args.test_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
