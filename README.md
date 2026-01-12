# CNC Round Stock Taper G-Code Generator

A Python program that generates G-code for cutting tapered cylinders on a 4th axis CNC machine. The program creates continuous spiral cuts with configurable pitch and feed rates, automatically calculating the number of passes needed based on maximum depth constraints.

## Features

- **Continuous Spiral Cutting**: Creates helical toolpaths that advance along the Y-axis while rotating the A-axis
- **Automatic Pass Calculation**: Determines the number of passes needed based on a maximum radial depth of 0.25" per pass
- **Cleanup Circles**: Adds cleanup passes at the start and end positions for each depth pass
- **Configurable Parameters**: Supports custom pitch and feed rate settings
- **TAP File Output**: Generates industry-standard .tap files ready for CNC machines

## Requirements

- Python 3.x
- No external dependencies required (uses only standard library)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/marksundt/CNCRoundStock.git
cd CNCRoundStock
```

2. The program is ready to use - no installation needed!

## Usage

### Basic Usage (Default Settings)

```bash
python taper_gcode_generator.py <start_diameter> <end_diameter> <length>
```

**Default values:**
- Pitch: 0.125" (1/8 inch per turn)
- Feed Rate: 40.0 IPM (inches per minute)

### Advanced Usage (Custom Settings)

```bash
python taper_gcode_generator.py <start_diameter> <end_diameter> <length> [pitch] [feed_rate]
```

### Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `start_diameter` | Yes | Starting diameter in inches | - |
| `end_diameter` | Yes | Ending diameter in inches | - |
| `length` | Yes | Length of cylinder in inches | - |
| `pitch` | No | Pitch per turn in inches | 0.125 |
| `feed_rate` | No | Feed rate in IPM | 40.0 |

## Examples

### Example 1: Basic Taper
Cut from 2" diameter to 1.5" diameter over 6" length using default settings:

```bash
python taper_gcode_generator.py 2.0 1.5 6.0
```

**Output:**
```
Generating G-code:
  Start diameter: 2.0"
  End diameter: 1.5"
  Length: 6.0"
  Pitch: 0.125" per turn
  Feed rate: 40.0 IPM
  Total radial depth: 0.2500"
  Number of passes: 1
  Depth per pass: 0.2500"
  Number of turns: 48.00
  Output file: taper_2.0to1.5_6.0L.tap
```

### Example 2: Steep Taper with Multiple Passes
Cut from 3" diameter to 1" diameter over 2" length:

```bash
python taper_gcode_generator.py 3.0 1.0 2.0
```

**Output:**
```
Generating G-code:
  Start diameter: 3.0"
  End diameter: 1.0"
  Length: 2.0"
  Pitch: 0.125" per turn
  Feed rate: 40.0 IPM
  Total radial depth: 1.0000"
  Number of passes: 4
  Depth per pass: 0.2500"
  Number of turns: 16.00
  Output file: taper_3.0to1.0_2.0L.tap
```

### Example 3: Custom Pitch
Use a 0.25" pitch per turn:

```bash
python taper_gcode_generator.py 2.0 1.5 6.0 0.25
```

### Example 4: Custom Pitch and Feed Rate
Use 0.25" pitch and 50 IPM feed rate:

```bash
python taper_gcode_generator.py 2.0 1.5 6.0 0.25 50.0
```

## Generated G-Code Structure

Each pass in the generated G-code follows this sequence:

1. **Return to start position** (Y=0, A=0)
2. **Engage at fixed Z depth** (radial depth for this pass)
3. **Cleanup circle at start** (360° rotation at Y=0)
4. **Helical cut** (simultaneous Y advance and A rotation)
5. **Cleanup circle at end** (360° rotation at final Y position)
6. **Retract to safe Z height**

### Key G-Code Features

- **G20**: Inch mode
- **G90**: Absolute positioning
- **G94**: Feed per minute mode
- **Fixed Z per pass**: Z depth remains constant during each pass (maximum 0.25" radial depth)
- **Coordinated motion**: Y and A axes move simultaneously for spiral cut

## Output Files

Output files are automatically named using the pattern:
```
taper_{start_dia}to{end_dia}_{length}L.tap
```

Examples:
- `taper_2.0to1.5_6.0L.tap`
- `taper_3.0to1.0_2.0L.tap`

## Technical Details

### Maximum Depth Per Pass
The program automatically calculates the number of passes needed based on a maximum radial depth of **0.25 inches** per pass. This ensures safe cutting without overloading the tool.

### Pitch Calculation
The pitch determines how far the tool advances along the Y-axis for each complete rotation (360°) of the A-axis. The default 1/8" (0.125") pitch creates a fine spiral.

### Coordinate System
- **Y-axis**: Length of the cylinder
- **A-axis**: Rotational axis (degrees)
- **Z-axis**: Radial depth (negative values cut into the material)

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.