# FIT File to Claude Converter

A Python tool that converts FIT files from Apple Watch, Garmin, and other fitness devices into structured, Claude-compatible format for training analysis.

## Features

- **Interval-focused Analysis**: Detailed speed, pace, and heart rate analysis per interval
- **Multiple Output Formats**: JSON for data analysis, Markdown for human-readable reports  
- **Device Support**: Apple Watch, Garmin, and other FIT-compatible devices
- **Batch Processing**: Convert multiple files at once
- **Comprehensive Metrics**: Time, distance, elevation, heart rate, cadence, and more

## Installation

1. Clone this repository:
```bash
git clone https://github.com/skempken/fit-file-reporter.git
cd fit-file-reporter
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your `.fit` files in the `input/` directory
2. Run the converter:
```bash
python fit_to_claude.py
```
3. Find your converted files in the `output/` directory

### Command Line Options

```bash
# Convert all files in input directory
python fit_to_claude.py

# Convert single file
python fit_to_claude.py -f path/to/file.fit

# Custom input/output directories
python fit_to_claude.py -i custom_input -o custom_output
```

## Output

### JSON Files
Structured data perfect for further analysis:
- Session metadata and device information
- Complete training metrics and statistics
- Interval data with timing and performance metrics

### Markdown Files
Human-readable training reports including:
- Training summary with key metrics
- Detailed interval analysis
- Speed, pace, and heart rate breakdowns
- Device information and data quality metrics

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development documentation, architecture overview, and contribution guidelines.

## Privacy

- All processing is done locally - no data is sent to external servers
- Your fitness data stays on your machine
- Generated files can be safely shared (they contain only the metrics you choose to export)

## License

Open source - free for research and personal use.