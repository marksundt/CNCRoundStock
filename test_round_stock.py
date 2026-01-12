#!/usr/bin/env python3
"""
Simple tests for the CNC Round Stock G-code Generator
"""

import os
import sys
import tempfile
from round_stock import GCodeGenerator


def test_basic_generation():
    """Test basic G-code generation."""
    print("Test 1: Basic G-code generation...")
    
    generator = GCodeGenerator(
        stock_size=1.0,
        finished_diameter=0.75,
        stock_length=6.0,
        tool_diameter=0.25
    )
    
    gcode = generator.generate()
    
    # Check that G-code was generated
    assert len(gcode) > 0, "G-code should not be empty"
    assert gcode.startswith("%"), "G-code should start with %"
    assert gcode.endswith("%"), "G-code should end with %"
    assert "M03" in gcode, "G-code should contain spindle start command"
    assert "M05" in gcode, "G-code should contain spindle stop command"
    assert "M30" in gcode, "G-code should contain program end command"
    
    print("  ✓ Basic generation works")


def test_file_output():
    """Test file output."""
    print("Test 2: File output...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.tap")
        
        generator = GCodeGenerator(
            stock_size=1.0,
            finished_diameter=0.75,
            stock_length=6.0,
            tool_diameter=0.25
        )
        
        generator.save_to_file(output_file)
        
        # Check file was created
        assert os.path.exists(output_file), "Output file should exist"
        
        # Check file has content
        with open(output_file, 'r') as f:
            content = f.read()
        
        assert len(content) > 0, "Output file should not be empty"
        assert content.startswith("%"), "File should start with %"
        assert content.endswith("%"), "File should end with %"
    
    print("  ✓ File output works")


def test_validation():
    """Test input validation."""
    print("Test 3: Input validation...")
    
    # Test diameter too large
    try:
        generator = GCodeGenerator(
            stock_size=1.0,
            finished_diameter=1.5,  # Too large
            stock_length=6.0,
            tool_diameter=0.25
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  ✓ Correctly rejects diameter larger than stock")
    
    # Test diameter equal to stock
    try:
        generator = GCodeGenerator(
            stock_size=1.0,
            finished_diameter=1.0,  # Equal to stock
            stock_length=6.0,
            tool_diameter=0.25
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  ✓ Correctly rejects diameter equal to stock")


def test_cut_depth_calculation():
    """Test cut depth calculation."""
    print("Test 4: Cut depth calculation...")
    
    generator = GCodeGenerator(
        stock_size=1.0,
        finished_diameter=0.75,
        stock_length=6.0,
        tool_diameter=0.25
    )
    
    cut_depth = generator.calculate_cut_depth()
    
    # Expected: (1.0/2) - (0.75/2) = 0.5 - 0.375 = 0.125
    expected = 0.125
    assert abs(cut_depth - expected) < 0.001, f"Cut depth should be {expected}, got {cut_depth}"
    
    print(f"  ✓ Cut depth calculated correctly: {cut_depth}")


def test_different_units():
    """Test with different unit sizes (metric-like values)."""
    print("Test 5: Different unit values...")
    
    generator = GCodeGenerator(
        stock_size=25.4,
        finished_diameter=19.0,
        stock_length=150.0,
        tool_diameter=6.0,
        feedrate=200.0,
        spindle_speed=2000
    )
    
    gcode = generator.generate()
    
    assert "25.4" in gcode, "Stock size should appear in header"
    assert "19.0" in gcode, "Finished diameter should appear in header"
    assert "150.0" in gcode, "Length should appear in header"
    
    print("  ✓ Works with different unit values")


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running CNC Round Stock Generator Tests")
    print("="*50 + "\n")
    
    try:
        test_basic_generation()
        test_file_output()
        test_validation()
        test_cut_depth_calculation()
        test_different_units()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50 + "\n")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
