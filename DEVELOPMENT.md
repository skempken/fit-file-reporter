# FIT to Claude Converter - Development Documentation

## Overview

This tool converts FIT files (fitness tracking data) from Apple Watch and similar devices into a structured, Claude-compatible format. The focus is on **interval analysis** for running training.

## Current Functionality

### Input
- **FIT files** in the `input/` directory
- Supports Apple Watch and other FIT-compatible devices
- Automatic batch processing of all `.fit` files

### Output
- **JSON files**: Structured data with metadata, session summary, and compact lap information
- **Markdown files**: Human-readable training reports with focus on interval analysis

### Core Features
1. **Interval-centered Analysis**
   - Speed per interval (km/h and pace)
   - Heart rate per interval
   - Detailed statistics (min/max/average)
   - Individual listing of the first 10 intervals

2. **Comprehensive Metrics**
   - Time data (total time, interval times)
   - Distances (total and per interval)
   - Speeds and paces
   - Heart rate data
   - Elevation profile and calorie consumption

## Technical Architecture

### Class: `FitToClaudeConverter`
- **Initialization**: Configures input/output directories
- **`extract_workout_data()`**: Parses FIT files and extracts structured data
- **`generate_training_summary()`**: Creates human-readable markdown reports
- **`convert_file()`**: Converts individual files
- **`convert_all()`**: Batch processing

### Data Structure
```json
{
  "metadata": { /* Device information */ },
  "session_summary": { /* Overall statistics */ },
  "lap_summary": {
    "count": 11,
    "laps": [ /* Interval details */ ]
  },
  "record_count": 1234,
  "events_count": 5
}
```

## Future Development Possibilities

### Short-term Improvements

1. **Extended Interval Analysis**
   - Automatic detection of stress/recovery phases
   - Heart rate zone analysis per interval
   - Pace variability within intervals

2. **Additional Output Formats**
   - CSV export for spreadsheets
   - Extended JSON structure for data analysis
   - GPX export for mapping tools

3. **Improved User Experience**
   - Configuration file for output preferences
   - Automatic backup functionality
   - Input file validation

### Medium-term Extensions

4. **Training Analysis**
   - Comparison between training sessions
   - Progress tracking over time
   - Automatic training type recognition (interval, endurance run, etc.)

5. **Data Visualization**
   - Integration with plotting libraries
   - HTML reports with interactive graphics
   - Heart rate and pace charts

6. **Multi-Sport Support**
   - Cycling, swimming, other sports
   - Sport-specific metrics
   - Customizable output templates

### Long-term Visions

7. **AI Integration**
   - Automatic training recommendations
   - Anomaly detection in training data
   - Personalized performance analysis

8. **Cloud Integration**
   - API for external training systems
   - Synchronization with fitness platforms
   - Collaborative training features

## Technical Requirements

### Dependencies
- **fitparse**: FIT file parsing
- **Python 3.8+**: Base runtime
- **pathlib, datetime, json**: Standard libraries

### Installation
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Nutzung
```bash
# Convert all files
python fit_to_claude.py

# Convert single file
python fit_to_claude.py -f path/to/file.fit

# Custom directories
python fit_to_claude.py -i custom_input -o custom_output
```

## Data Quality and Validation

### Current Validation
- Checking for None values
- Basic data type validation
- Error handling for corrupted FIT files

### Improvement Possibilities
- Outlier detection in heart rate data
- Plausibility checks for speeds
- GPS data validation
- Automatic data cleaning

## Performance Optimization

### Current Implementation
- Sequential processing
- Memory-efficient JSON output (only first 10 laps)
- Compact markdown generation

### Optimization Potential
- Parallel processing for batch conversion
- Streaming parser for large FIT files
- Caching for recurring calculations
- Compressed output options

## Testing and Quality Assurance

### Recommended Test Suite
```bash
# Unit tests
pytest tests/test_converter.py
pytest tests/test_data_extraction.py
pytest tests/test_markdown_generation.py

# Integration tests
pytest tests/test_full_workflow.py

# Performance tests
pytest tests/test_performance.py
```

### Test Data
- Various device types (Apple Watch, Garmin, etc.)
- Different training types
- Edge cases (very short/long trainings)
- Corrupted or incomplete files

## Contributing to Development

### Code Style
- PEP 8 compliant
- Use type hints
- Comprehensive docstrings
- Meaningful variable names

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/neue-funktionalität

# Commits with descriptive messages
git commit -m "Add: Herzfrequenz-Zonen-Analyse"

# Run tests before push
pytest
git push origin feature/neue-funktionalität
```

## License and Usage

- **Open Source**: Freely available for research and personal use
- **Privacy**: Local processing, no cloud transmission
- **Compatibility**: Runs on Windows, macOS, Linux

---

*This documentation is continuously expanded. For questions or improvement suggestions, please create an issue or submit a pull request.*