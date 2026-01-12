#!/usr/bin/env python3
"""
CNC Round Stock G-code Generator

This program generates G-code (.tap) files for rounding square stock
on a CNC machine with a 4th axis (rotary axis).

The program calculates the toolpath to remove material from the corners
of square stock to create cylindrical round stock.
"""

import math
import argparse
import sys
from typing import List


class GCodeGenerator:
    """Generates G-code for rounding square stock using a 4th axis."""
    
    def __init__(self, stock_size: float, finished_diameter: float, 
                 stock_length: float, tool_diameter: float, 
                 feedrate: float = 100.0, spindle_speed: int = 1000,
                 stepover: float = 0.1, safe_z: float = 1.0):
        """
        Initialize the G-code generator.
        
        Args:
            stock_size: Side dimension of square stock (inches or mm)
            finished_diameter: Target diameter of round stock (inches or mm)
            stock_length: Length of stock to round (inches or mm)
            tool_diameter: Diameter of cutting tool (inches or mm)
            feedrate: Cutting feedrate (units per minute)
            spindle_speed: Spindle RPM
            stepover: Depth of cut per pass (inches or mm)
            safe_z: Safe Z height for rapid moves (inches or mm)
        """
        self.stock_size = stock_size
        self.finished_diameter = finished_diameter
        self.stock_length = stock_length
        self.tool_diameter = tool_diameter
        self.feedrate = feedrate
        self.spindle_speed = spindle_speed
        self.stepover = stepover
        self.safe_z = safe_z
        
        # Validate inputs
        if finished_diameter > stock_size * math.sqrt(2):
            raise ValueError("Finished diameter cannot exceed diagonal of square stock")
        
        if finished_diameter >= stock_size:
            raise ValueError("Finished diameter must be less than stock size")
            
    def generate_header(self) -> List[str]:
        """Generate G-code header."""
        return [
            "% ",
            "(CNC Round Stock Generator)",
            f"(Square Stock: {self.stock_size})",
            f"(Finished Diameter: {self.finished_diameter})",
            f"(Length: {self.stock_length})",
            "()",
            "G90 G54 G17 G20 (Absolute, Work Coords, XY Plane, Inches)",
            "G21 (Metric - change to G20 for inches)",
            f"M03 S{self.spindle_speed} (Start spindle)",
            "G04 P2.0 (Wait for spindle to reach speed)",
            f"G00 Z{self.safe_z} (Rapid to safe Z)",
            ""
        ]
    
    def calculate_cut_depth(self) -> float:
        """Calculate the maximum depth of cut needed."""
        # Maximum depth is from the flat of the square to the final radius
        max_radius = self.finished_diameter / 2.0
        stock_half = self.stock_size / 2.0
        return stock_half - max_radius
    
    def generate_roughing_passes(self) -> List[str]:
        """Generate roughing passes to remove bulk material."""
        gcode = ["(Roughing passes)"]
        
        max_depth = self.calculate_cut_depth()
        num_passes = math.ceil(max_depth / self.stepover)
        
        # Number of rotational positions (more positions = smoother finish)
        num_positions = 16
        angle_step = 360.0 / num_positions
        
        for pass_num in range(num_passes):
            current_depth = min((pass_num + 1) * self.stepover, max_depth)
            cutting_radius = (self.stock_size / 2.0) - current_depth
            
            gcode.append(f"(Pass {pass_num + 1}, Depth: {current_depth:.4f})")
            
            # Calculate X position (distance from center)
            # Tool cuts at the cutting radius
            x_pos = cutting_radius
            
            for pos in range(num_positions):
                angle = pos * angle_step
                
                # Rotate to position
                gcode.append(f"G00 A{angle:.3f} (Rotate to {angle:.1f} degrees)")
                
                # Rapid to start of cut
                gcode.append(f"G00 X{x_pos:.4f} Z{self.safe_z}")
                
                # Feed down to cutting depth
                gcode.append(f"G01 Z-0.1 F{self.feedrate}")
                
                # Make the cut along the length
                gcode.append(f"G01 Z-{self.stock_length:.4f}")
                
                # Retract
                gcode.append(f"G00 Z{self.safe_z}")
            
            gcode.append("")
        
        return gcode
    
    def generate_finishing_pass(self) -> List[str]:
        """Generate finishing pass for smooth surface."""
        gcode = ["(Finishing pass)"]
        
        # Finishing pass at final diameter
        final_radius = self.finished_diameter / 2.0
        x_pos = final_radius
        
        # More positions for smoother finish
        num_positions = 32
        angle_step = 360.0 / num_positions
        
        for pos in range(num_positions + 1):  # +1 to complete the circle
            angle = pos * angle_step
            
            gcode.append(f"G00 A{angle:.3f}")
            
            if pos == 0:
                gcode.append(f"G00 X{x_pos:.4f} Z{self.safe_z}")
                gcode.append(f"G01 Z-0.1 F{self.feedrate}")
            
            # Make the cut along the length
            gcode.append(f"G01 Z-{self.stock_length:.4f}")
            
            # Return to start
            gcode.append(f"G00 Z{self.safe_z}")
        
        gcode.append("")
        return gcode
    
    def generate_footer(self) -> List[str]:
        """Generate G-code footer."""
        return [
            "(End of program)",
            f"G00 Z{self.safe_z}",
            "G00 A0 (Return rotary axis to 0)",
            "G00 X0 Y0 (Return to origin)",
            "M05 (Stop spindle)",
            "M30 (Program end)",
            "%"
        ]
    
    def generate(self) -> str:
        """Generate complete G-code program."""
        gcode_lines = []
        
        gcode_lines.extend(self.generate_header())
        gcode_lines.extend(self.generate_roughing_passes())
        gcode_lines.extend(self.generate_finishing_pass())
        gcode_lines.extend(self.generate_footer())
        
        return "\n".join(gcode_lines)
    
    def save_to_file(self, filename: str):
        """Save G-code to a .tap file."""
        if not filename.endswith('.tap'):
            filename += '.tap'
        
        gcode = self.generate()
        
        with open(filename, 'w') as f:
            f.write(gcode)
        
        print(f"G-code saved to: {filename}")
        print(f"Total lines: {len(gcode.splitlines())}")


def main():
    """Main entry point for the program."""
    parser = argparse.ArgumentParser(
        description='Generate G-code for rounding square stock on a CNC with 4th axis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -s 1.0 -d 0.75 -l 6.0 -o output.tap
  %(prog)s --stock-size 25.4 --diameter 19.0 --length 150 --output round_stock.tap
        """
    )
    
    parser.add_argument('-s', '--stock-size', type=float, required=True,
                        help='Side dimension of square stock')
    parser.add_argument('-d', '--diameter', type=float, required=True,
                        help='Target diameter of round stock')
    parser.add_argument('-l', '--length', type=float, required=True,
                        help='Length of stock to round')
    parser.add_argument('-t', '--tool-diameter', type=float, default=0.25,
                        help='Diameter of cutting tool (default: 0.25)')
    parser.add_argument('-f', '--feedrate', type=float, default=100.0,
                        help='Cutting feedrate (default: 100.0)')
    parser.add_argument('-r', '--spindle-speed', type=int, default=1000,
                        help='Spindle RPM (default: 1000)')
    parser.add_argument('--stepover', type=float, default=0.1,
                        help='Depth of cut per pass (default: 0.1)')
    parser.add_argument('--safe-z', type=float, default=1.0,
                        help='Safe Z height for rapid moves (default: 1.0)')
    parser.add_argument('-o', '--output', type=str, default='round_stock.tap',
                        help='Output filename (default: round_stock.tap)')
    
    args = parser.parse_args()
    
    try:
        generator = GCodeGenerator(
            stock_size=args.stock_size,
            finished_diameter=args.diameter,
            stock_length=args.length,
            tool_diameter=args.tool_diameter,
            feedrate=args.feedrate,
            spindle_speed=args.spindle_speed,
            stepover=args.stepover,
            safe_z=args.safe_z
        )
        
        generator.save_to_file(args.output)
        
        print("\nProgram parameters:")
        print(f"  Square stock size: {args.stock_size}")
        print(f"  Finished diameter: {args.diameter}")
        print(f"  Length: {args.length}")
        print(f"  Material to remove: {generator.calculate_cut_depth():.4f}")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
