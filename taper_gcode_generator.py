#!/usr/bin/env python3
"""
G-code Generator for Tapered Cylinders on 4th Axis CNC
Generates a continuous spiral cut with specified pitch and depth constraints.
"""

import math
import sys


def generate_taper_gcode(start_diameter, end_diameter, length, pitch=0.125, feed_rate=40.0, output_file="output.tap"):
    """
    Generate G-code for cutting a tapered cylinder on a 4th axis CNC.

    Parameters:
    - start_diameter: Starting diameter in inches
    - end_diameter: Ending diameter in inches
    - length: Length of the cylinder in inches
    - pitch: Pitch per turn in inches (default: 0.125 = 1/8 inch)
    - feed_rate: Feed rate in inches per minute (default: 40.0)
    - output_file: Output filename (default: output.tap)
    """

    # Constants
    MAX_DEPTH_PER_PASS = 0.25  # 1/4 inch maximum depth of cut

    # Calculate key values
    start_radius = start_diameter / 2.0
    end_radius = end_diameter / 2.0
    total_radial_depth = abs(start_radius - end_radius)

    # Determine number of passes needed
    num_passes = math.ceil(total_radial_depth / MAX_DEPTH_PER_PASS)
    if num_passes == 0:
        num_passes = 1

    # Depth per pass
    z_depth_per_pass = total_radial_depth / num_passes

    # Number of complete turns needed
    num_turns = length / pitch

    print(f"Generating G-code:")
    print(f"  Start diameter: {start_diameter}\"")
    print(f"  End diameter: {end_diameter}\"")
    print(f"  Length: {length}\"")
    print(f"  Pitch: {pitch}\" per turn")
    print(f"  Feed rate: {feed_rate} IPM")
    print(f"  Total radial depth: {total_radial_depth:.4f}\"")
    print(f"  Number of passes: {num_passes}")
    print(f"  Depth per pass: {z_depth_per_pass:.4f}\"")
    print(f"  Number of turns: {num_turns:.2f}")
    print(f"  Output file: {output_file}")

    # Generate G-code
    with open(output_file, 'w') as f:
        # Header
        f.write("%\n")
        f.write("(Tapered Cylinder G-code)\n")
        f.write(f"(Start Diameter: {start_diameter}\")\n")
        f.write(f"(End Diameter: {end_diameter}\")\n")
        f.write(f"(Length: {length}\")\n")
        f.write(f"(Pitch: {pitch}\" per turn)\n")
        f.write(f"(Feed Rate: {feed_rate} IPM)\n")
        f.write(f"(Passes: {num_passes})\n")
        f.write("\n")

        # Initialize
        f.write("G90 (Absolute positioning)\n")
        f.write("G94 (Feed per minute)\n")
        f.write("G20 (Inches)\n")
        f.write("G17 (XY plane)\n")
        f.write("\n")

        # Home and setup
        f.write("G28 (Home)\n")
        f.write("G0 Z0.5 (Rapid to safe Z)\n")
        f.write("G0 Y0.0 A0.0 (Move to start position)\n")
        f.write("\n")

        # Spindle start
        f.write("M3 S1000 (Start spindle - adjust RPM as needed)\n")
        f.write("G4 P2.0 (Dwell 2 seconds)\n")
        f.write("\n")

        # Generate passes
        for pass_num in range(1, num_passes + 1):
            f.write(f"(Pass {pass_num} of {num_passes})\n")

            # Calculate current Z depth for this pass (fixed throughout the pass)
            # Each pass removes z_depth_per_pass radially
            z_pos = -(z_depth_per_pass * pass_num)

            # Total rotation and Y distance for this pass
            total_rotation = num_turns * 360.0
            final_y = length

            # Move to start position for this pass
            f.write("G0 Y0.0 A0.0 (Return to start)\n")

            # Engage at Z depth
            f.write(f"G1 Z{z_pos:.4f} F{feed_rate} (Engage at depth)\n")

            # Cleanup circle at start (before helical cut)
            f.write(f"G1 A360.0000 F{feed_rate} (Cleanup circle at start)\n")

            # Single continuous helical cut - Y advances while A rotates
            f.write(f"G1 Y{final_y:.4f} A{total_rotation + 360.0:.4f} F{feed_rate} (Helical cut)\n")

            # Cleanup circle at end
            f.write(f"G1 A{total_rotation + 720.0:.4f} F{feed_rate} (Cleanup circle at end)\n")

            # Retract after pass
            f.write("G0 Z0.5 (Retract)\n")
            f.write("\n")

        # Cleanup
        f.write("(Cleanup)\n")
        f.write("G0 Z0.5 (Retract to safe Z)\n")
        f.write("G0 Y0.0 A0.0 (Return to start)\n")
        f.write("M5 (Stop spindle)\n")
        f.write("M30 (Program end)\n")
        f.write("%\n")

    print(f"\nG-code generated successfully: {output_file}")


def main():
    """Main entry point for the program."""

    if len(sys.argv) >= 4:
        try:
            start_dia = float(sys.argv[1])
            end_dia = float(sys.argv[2])
            length = float(sys.argv[3])

            # Optional parameters
            pitch = float(sys.argv[4]) if len(sys.argv) > 4 else 0.125
            feed_rate = float(sys.argv[5]) if len(sys.argv) > 5 else 40.0

            # Validate inputs
            if start_dia <= 0 or end_dia <= 0 or length <= 0:
                print("Error: All dimensions must be positive numbers")
                sys.exit(1)

            if pitch <= 0:
                print("Error: Pitch must be a positive number")
                sys.exit(1)

            if feed_rate <= 0:
                print("Error: Feed rate must be a positive number")
                sys.exit(1)

            # Generate output filename
            output_file = f"taper_{start_dia}to{end_dia}_{length}L.tap"
            generate_taper_gcode(start_dia, end_dia, length, pitch, feed_rate, output_file)

        except ValueError:
            print("Error: Invalid number format")
            sys.exit(1)
    else:
        print("Tapered Cylinder G-code Generator")
        print("=" * 50)
        print("\nUsage: python taper_gcode_generator.py <start_diameter> <end_diameter> <length> [pitch] [feed_rate]")
        print("\nRequired Parameters:")
        print("  start_diameter : Starting diameter in inches")
        print("  end_diameter   : Ending diameter in inches")
        print("  length         : Length of cylinder in inches")
        print("\nOptional Parameters:")
        print("  pitch          : Pitch per turn in inches (default: 0.125 = 1/8\")")
        print("  feed_rate      : Feed rate in IPM (default: 40.0)")
        print("\nExamples:")
        print("  python taper_gcode_generator.py 2.0 1.5 6.0")
        print("  python taper_gcode_generator.py 2.0 1.5 6.0 0.25")
        print("  python taper_gcode_generator.py 2.0 1.5 6.0 0.25 50.0")
        print("\nThis will generate a .tap file with G-code for a 4th axis CNC")
        print("that cuts a continuous spiral, taking max 1/4\" depth per pass.")
        sys.exit(0)


if __name__ == "__main__":
    main()
