#!/usr/bin/env python3
"""
FIT to Claude Knowledge Converter

Converts .fit files from Apple Watch/Garmin devices into structured,
Claude-compatible format for training analysis.
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import fitparse
from pathlib import Path


class FitToClaudeConverter:
    """Converts FIT files to Claude-compatible format"""
    
    def __init__(self, input_dir: str = "input", output_dir: str = "output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_workout_data(self, fitfile: fitparse.FitFile) -> Dict[str, Any]:
        """Extracts structured workout data from FIT file"""
        workout_data = {
            "metadata": {},
            "session_summary": {},
            "records": [],
            "laps": [],
            "events": []
        }
        
        # Parse all messages
        for record in fitfile.get_messages():
            msg_type = record.name
            
            if msg_type == 'file_id':
                time_created = record.get_value('time_created')
                workout_data["metadata"].update({
                    "file_type": record.get_value('type'),
                    "manufacturer": record.get_value('manufacturer'),
                    "product": record.get_value('product'),
                    "serial_number": record.get_value('serial_number'),
                    "time_created": time_created.isoformat() if time_created else None
                })
            
            elif msg_type == 'session':
                start_time = record.get_value('start_time')
                workout_data["session_summary"].update({
                    "start_time": start_time.isoformat() if start_time else None,
                    "total_elapsed_time": record.get_value('total_elapsed_time'),
                    "total_timer_time": record.get_value('total_timer_time'),
                    "total_distance": record.get_value('total_distance'),
                    "total_calories": record.get_value('total_calories'),
                    "avg_speed": record.get_value('avg_speed'),
                    "max_speed": record.get_value('max_speed'),
                    "avg_heart_rate": record.get_value('avg_heart_rate'),
                    "max_heart_rate": record.get_value('max_heart_rate'),
                    "avg_cadence": record.get_value('avg_cadence'),
                    "max_cadence": record.get_value('max_cadence'),
                    "sport": record.get_value('sport'),
                    "sub_sport": record.get_value('sub_sport'),
                    "total_ascent": record.get_value('total_ascent'),
                    "total_descent": record.get_value('total_descent'),
                    "min_altitude": record.get_value('min_altitude'),
                    "max_altitude": record.get_value('max_altitude')
                })
            
            elif msg_type == 'record':
                timestamp = record.get_value('timestamp')
                record_data = {
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "position_lat": record.get_value('position_lat'),
                    "position_long": record.get_value('position_long'),
                    "altitude": record.get_value('altitude'),
                    "heart_rate": record.get_value('heart_rate'),
                    "cadence": record.get_value('cadence'),
                    "distance": record.get_value('distance'),
                    "speed": record.get_value('speed'),
                    "power": record.get_value('power'),
                    "temperature": record.get_value('temperature')
                }
                # Remove None values
                record_data = {k: v for k, v in record_data.items() if v is not None}
                workout_data["records"].append(record_data)
            
            elif msg_type == 'lap':
                start_time = record.get_value('start_time')
                lap_data = {
                    "start_time": start_time.isoformat() if start_time else None,
                    "total_elapsed_time": record.get_value('total_elapsed_time'),
                    "total_timer_time": record.get_value('total_timer_time'),
                    "total_distance": record.get_value('total_distance'),
                    "avg_speed": record.get_value('avg_speed'),
                    "max_speed": record.get_value('max_speed'),
                    "avg_heart_rate": record.get_value('avg_heart_rate'),
                    "max_heart_rate": record.get_value('max_heart_rate'),
                    "total_calories": record.get_value('total_calories'),
                    "lap_trigger": record.get_value('lap_trigger')
                }
                lap_data = {k: v for k, v in lap_data.items() if v is not None}
                workout_data["laps"].append(lap_data)
            
            elif msg_type == 'event':
                timestamp = record.get_value('timestamp')
                event_data = {
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "event": record.get_value('event'),
                    "event_type": record.get_value('event_type'),
                    "data": record.get_value('data')
                }
                event_data = {k: v for k, v in event_data.items() if v is not None}
                workout_data["events"].append(event_data)
        
        return workout_data
    
    def generate_training_summary(self, workout_data: Dict[str, Any]) -> str:
        """Generates compact factual summary without evaluation for Claude"""
        summary = []
        session = workout_data.get("session_summary", {})
        
        # Basic information
        start_time = session.get("start_time")
        if start_time:
            dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            summary.append(f"# Training from {dt.strftime('%d.%m.%Y')}")
            summary.append(f"**Start time:** {dt.strftime('%H:%M:%S')}")
            summary.append(f"**Weekday:** {dt.strftime('%A')}")
        
        # Training duration and distance
        if session.get("total_timer_time"):
            total_seconds = session["total_timer_time"]
            duration = timedelta(seconds=total_seconds)
            summary.append(f"**Total time:** {duration} ({total_seconds/60:.1f} minutes)")
            
        if session.get("total_elapsed_time"):
            elapsed_seconds = session["total_elapsed_time"] 
            if elapsed_seconds != session.get("total_timer_time"):
                summary.append(f"**Elapsed time:** {timedelta(seconds=elapsed_seconds)}")
        
        if session.get("total_distance"):
            distance_km = session["total_distance"] / 1000
            summary.append(f"**Distance:** {distance_km:.2f} km")
        
        # Pace and speed
        if session.get("avg_speed"):
            avg_speed_kmh = session["avg_speed"] * 3.6
            summary.append(f"**Average speed:** {avg_speed_kmh:.2f} km/h")
            
            # Calculate pace
            avg_pace_per_km = 1000 / session["avg_speed"]
            pace_minutes = int(avg_pace_per_km // 60)
            pace_seconds = int(avg_pace_per_km % 60)
            summary.append(f"**Average pace:** {pace_minutes}:{pace_seconds:02d} min/km")
        
        if session.get("max_speed"):
            max_speed_kmh = session["max_speed"] * 3.6
            summary.append(f"**Maximum speed:** {max_speed_kmh:.2f} km/h")
        
        # Heart rate
        if session.get("avg_heart_rate"):
            summary.append(f"**Average heart rate:** {session['avg_heart_rate']} bpm")
        if session.get("max_heart_rate"):
            summary.append(f"**Maximum heart rate:** {session['max_heart_rate']} bpm")
        
        # Elevation data
        if session.get("total_ascent"):
            summary.append(f"**Total ascent:** {session['total_ascent']} m")
        if session.get("total_descent"):
            summary.append(f"**Total descent:** {session['total_descent']} m")
        if session.get("min_altitude") is not None:
            summary.append(f"**Minimum altitude:** {session['min_altitude']:.0f} m")
        if session.get("max_altitude") is not None:
            summary.append(f"**Maximum altitude:** {session['max_altitude']:.0f} m")
        
        # Additional metrics
        if session.get("total_calories"):
            summary.append(f"**Calories:** {session['total_calories']} kcal")
        if session.get("avg_cadence"):
            summary.append(f"**Average cadence:** {session['avg_cadence']} spm")
        if session.get("max_cadence"):
            summary.append(f"**Maximum cadence:** {session['max_cadence']} spm")
        
        # Interval information with speeds
        laps = workout_data.get("laps", [])
        if laps:
            summary.append(f"\n## Intervals ({len(laps)} intervals)")
            
            # Detailed interval statistics
            lap_times = [lap.get("total_timer_time", 0) for lap in laps if lap.get("total_timer_time")]
            lap_distances = [lap.get("total_distance", 0) for lap in laps if lap.get("total_distance")]
            lap_speeds = [lap.get("avg_speed", 0) for lap in laps if lap.get("avg_speed")]
            lap_hr = [lap.get("avg_heart_rate", 0) for lap in laps if lap.get("avg_heart_rate")]
            
            if lap_times:
                avg_lap_time = sum(lap_times) / len(lap_times)
                summary.append(f"**Average interval time:** {timedelta(seconds=avg_lap_time)}")
                summary.append(f"**Shortest interval:** {timedelta(seconds=min(lap_times))}")
                summary.append(f"**Longest interval:** {timedelta(seconds=max(lap_times))}")
            
            if lap_distances:
                avg_lap_dist = sum(lap_distances) / len(lap_distances) / 1000
                summary.append(f"**Average interval distance:** {avg_lap_dist:.3f} km")
            
            if lap_speeds:
                # Speeds per interval in km/h and as pace
                avg_lap_speed_kmh = sum(speed * 3.6 for speed in lap_speeds) / len(lap_speeds)
                min_speed_kmh = min(lap_speeds) * 3.6
                max_speed_kmh = max(lap_speeds) * 3.6
                summary.append(f"**Average interval speed:** {avg_lap_speed_kmh:.2f} km/h")
                summary.append(f"**Slowest interval speed:** {min_speed_kmh:.2f} km/h")
                summary.append(f"**Fastest interval speed:** {max_speed_kmh:.2f} km/h")
                
                # Paces for intervals
                avg_pace_per_km = 1000 / (sum(lap_speeds) / len(lap_speeds))
                min_pace_per_km = 1000 / max(lap_speeds)
                max_pace_per_km = 1000 / min(lap_speeds)
                
                avg_pace_min, avg_pace_sec = int(avg_pace_per_km // 60), int(avg_pace_per_km % 60)
                min_pace_min, min_pace_sec = int(min_pace_per_km // 60), int(min_pace_per_km % 60)
                max_pace_min, max_pace_sec = int(max_pace_per_km // 60), int(max_pace_per_km % 60)
                
                summary.append(f"**Average interval pace:** {avg_pace_min}:{avg_pace_sec:02d} min/km")
                summary.append(f"**Fastest interval pace:** {min_pace_min}:{min_pace_sec:02d} min/km")
                summary.append(f"**Slowest interval pace:** {max_pace_min}:{max_pace_sec:02d} min/km")
            
            if lap_hr:
                avg_lap_hr = sum(lap_hr) / len(lap_hr)
                min_hr = min(lap_hr)
                max_hr = max(lap_hr)
                summary.append(f"**Average heart rate in intervals:** {avg_lap_hr:.0f} bpm")
                summary.append(f"**Lowest interval heart rate:** {min_hr} bpm")
                summary.append(f"**Highest interval heart rate:** {max_hr} bpm")
            
            # List individual intervals
            summary.append(f"\n### Individual intervals:")
            for i, lap in enumerate(laps[:10], 1):  # Show only the first 10 intervals
                lap_time = lap.get("total_timer_time", 0)
                lap_dist = lap.get("total_distance", 0) / 1000
                lap_speed = lap.get("avg_speed", 0)
                lap_hr_val = lap.get("avg_heart_rate", 0)
                
                if lap_time and lap_speed:
                    speed_kmh = lap_speed * 3.6
                    pace_per_km = 1000 / lap_speed if lap_speed > 0 else 0
                    pace_min, pace_sec = int(pace_per_km // 60), int(pace_per_km % 60)
                    
                    interval_info = f"**Interval {i}:** {timedelta(seconds=lap_time)}, {lap_dist:.2f}km, {speed_kmh:.1f}km/h ({pace_min}:{pace_sec:02d}min/km)"
                    if lap_hr_val:
                        interval_info += f", {lap_hr_val}bpm"
                    summary.append(interval_info)
            
            if len(laps) > 10:
                summary.append(f"... and {len(laps) - 10} more intervals")
        
        # Device information
        metadata = workout_data.get("metadata", {})
        if metadata.get("manufacturer"):
            summary.append(f"\n## Device information")
            summary.append(f"**Manufacturer:** {metadata.get('manufacturer')}")
            if metadata.get("product"):
                summary.append(f"**Product:** {metadata.get('product')}")
            if metadata.get("serial_number"):
                summary.append(f"**Serial number:** {metadata.get('serial_number')}")
        
        # Data point information
        records_count = len(workout_data.get("records", []))
        if records_count > 0:
            summary.append(f"\n**Data points:** {records_count}")
            
            # Estimate recording frequency
            if session.get("total_timer_time") and records_count > 1:
                recording_interval = session["total_timer_time"] / records_count
                summary.append(f"**Recording interval:** approx. {recording_interval:.1f} seconds")
        
        return "\n".join(summary)
    
    def convert_file(self, fit_file_path: Path) -> Dict[str, str]:
        """Converts a FIT file"""
        try:
            # Parse FIT file
            fitfile = fitparse.FitFile(str(fit_file_path))
            workout_data = self.extract_workout_data(fitfile)
            
            # Create output files
            base_name = fit_file_path.stem
            
            # Compact JSON file with essential data only (without raw data)
            json_path = self.output_dir / f"{base_name}.json"
            compact_data = {
                "metadata": workout_data.get("metadata", {}),
                "session_summary": workout_data.get("session_summary", {}),
                "lap_summary": {
                    "count": len(workout_data.get("laps", [])),
                    "laps": workout_data.get("laps", [])[:10]  # Only first 10 laps
                },
                "record_count": len(workout_data.get("records", [])),
                "events_count": len(workout_data.get("events", []))
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(compact_data, f, indent=2, ensure_ascii=False)
            
            # Markdown file for factual training summary
            markdown_path = self.output_dir / f"{base_name}.md"
            summary = self.generate_training_summary(workout_data)
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            return {
                "status": "success",
                "json_file": str(json_path),
                "markdown_file": str(markdown_path)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "file": str(fit_file_path)
            }
    
    def convert_all(self) -> List[Dict[str, str]]:
        """Converts all FIT files in the input directory"""
        results = []
        
        if not self.input_dir.exists():
            print(f"Input directory {self.input_dir} does not exist!")
            return results
        
        fit_files = list(self.input_dir.glob("*.fit"))
        if not fit_files:
            print(f"No .fit files found in {self.input_dir}!")
            return results
        
        # Sort files by date
        fit_files.sort()
        
        print(f"Converting {len(fit_files)} FIT files...")
        
        for fit_file in fit_files:
            print(f"Processing: {fit_file.name}")
            result = self.convert_file(fit_file)
            results.append(result)
            
            if result["status"] == "success":
                print(f"  ✓ Successfully converted")
            else:
                print(f"  ✗ Error: {result['error']}")
        
        return results
    


def main():
    parser = argparse.ArgumentParser(description="Converts FIT files to Claude-compatible format")
    parser.add_argument("--input", "-i", default="input", help="Input directory (default: input)")
    parser.add_argument("--output", "-o", default="output", help="Output directory (default: output)")
    parser.add_argument("--file", "-f", help="Convert only a specific file")
    
    args = parser.parse_args()
    
    converter = FitToClaudeConverter(args.input, args.output)
    
    if args.file:
        fit_file = Path(args.file)
        if not fit_file.exists():
            print(f"File {fit_file} does not exist!")
            return
        result = converter.convert_file(fit_file)
        if result["status"] == "success":
            print(f"Successfully converted: {result['markdown_file']}")
        else:
            print(f"Error: {result['error']}")
    else:
        results = converter.convert_all()
        
        success_count = sum(1 for r in results if r["status"] == "success")
        print(f"\nConversion completed: {success_count}/{len(results)} successful")
        
        if success_count > 0:
            print(f"\nOutput files available in: {converter.output_dir}")


if __name__ == "__main__":
    main()