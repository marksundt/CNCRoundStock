# CNCRoundStock

A Python program that generates G-code (.tap files) for rounding square stock on a CNC machine with a 4th axis (rotary axis).

## Overview

This tool automates the creation of CNC toolpaths to convert square stock into cylindrical round stock. The program calculates the necessary cuts and rotations to remove material from the corners of square stock, creating a smooth cylindrical surface.

## Features

- Generates complete G-code programs with header and footer
- Configurable roughing and finishing passes
- Supports both imperial (inches) and metric (mm) units
- Adjustable cutting parameters (feedrate, spindle speed, depth of cut)
- Multiple rotational positions for smooth surface finish
- Safety features with configurable safe Z heights

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Installation

Simply clone this repository:

```bash
git clone https://github.com/marksundt/CNCRoundStock.git
cd CNCRoundStock
chmod +x round_stock.py
```

## Usage

### Basic Usage

```bash
python3 round_stock.py -s STOCK_SIZE -d DIAMETER -l LENGTH -o OUTPUT_FILE
```

### Required Arguments

- `-s, --stock-size`: Side dimension of the square stock
- `-d, --diameter`: Target diameter of the finished round stock
- `-l, --length`: Length of stock to round

### Optional Arguments

- `-t, --tool-diameter`: Diameter of cutting tool (default: 0.25)
- `-f, --feedrate`: Cutting feedrate in units per minute (default: 100.0)
- `-r, --spindle-speed`: Spindle RPM (default: 1000)
- `--stepover`: Depth of cut per pass (default: 0.1)
- `--safe-z`: Safe Z height for rapid moves (default: 1.0)
- `-o, --output`: Output filename (default: round_stock.tap)

### Examples

#### Example 1: Basic operation (imperial units)
```bash
python3 round_stock.py -s 1.0 -d 0.75 -l 6.0 -o output.tap
```
This converts 1" square stock to 0.75" diameter over a 6" length.

#### Example 2: Metric units with custom parameters
```bash
python3 round_stock.py -s 25.4 -d 19.0 -l 150 -f 150 -r 1500 -o metric_stock.tap
```
This converts 25.4mm square stock to 19mm diameter over 150mm length.

#### Example 3: Fine finishing with smaller stepover
```bash
python3 round_stock.py -s 1.0 -d 0.75 -l 6.0 --stepover 0.05 -o fine_finish.tap
```
This uses a smaller stepover for a finer finish (more passes).

## How It Works

The program works by:

1. **Calculating the material to remove**: Determines how much material needs to be removed from the corners of the square stock
2. **Generating roughing passes**: Creates multiple passes at different depths to remove bulk material efficiently
3. **Rotating the stock**: Uses the 4th axis (A-axis) to rotate the stock to different angular positions
4. **Taking finishing passes**: Performs a final pass with more rotational positions for a smooth surface
5. **Output formatting**: Writes properly formatted G-code to a .tap file

The G-code includes:
- Program header with setup commands
- Spindle control (start/stop)
- Coordinated X-axis (tool position) and A-axis (rotation) movements
- Z-axis movements for cutting and retracting
- Safety rapids and returns to origin

## G-code Output

The generated .tap file contains standard G-code commands:
- `G00`: Rapid positioning
- `G01`: Linear feed move
- `M03`: Start spindle
- `M05`: Stop spindle
- `M30`: Program end
- `A`: 4th axis (rotary) positioning

## Safety Considerations

⚠️ **Important**: Always verify generated G-code in a simulator before running on actual CNC equipment.

- Review all rapids and feed moves
- Ensure stock is properly secured in a 4th axis chuck or fixture
- Verify tool clearances
- Check spindle speeds and feedrates are appropriate for your material
- Perform a dry run with the spindle off

## Limitations

- The finished diameter must be less than the square stock size
- The finished diameter cannot exceed the diagonal of the square stock
- Tool diameter is specified but not currently used in toolpath calculations (assumes tool radius compensation in CNC control)

## License

This project is open source and available for use and modification.

## Contributing

Contributions, issues, and feature requests are welcome!