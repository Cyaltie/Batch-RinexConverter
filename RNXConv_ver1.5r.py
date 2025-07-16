import os
import sys
import logging
import zipfile
import subprocess
import shutil
import glob
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

class RINEXConverter:
    def __init__(self):
        self.setup_directories()
        self.setup_logging()
        self.hour_letters = {i: chr(ord('a') + i) for i in range(24)}
        self.navigation_types = ['n', 'g', 'l', 'q', 'c', 'j', 'i', 'h', 'f']

    def setup_directories(self):
        self.base_dir = Path("C:/RNXConverter")
        self.input_dir = self.base_dir / "Input"
        self.input_raw_dir = self.base_dir / "Input" / "Raw"
        self.temp_dir = self.input_raw_dir / "temp"
        self.final_dir = self.base_dir / "Output" / "Final"
        self.final_temp_dir = self.final_dir / "temp"
        
        # Create directories
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.input_raw_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.final_dir.mkdir(parents=True, exist_ok=True)
        self.final_temp_dir.mkdir(parents=True, exist_ok=True)

    def setup_logging(self):
        log_file = self.base_dir / "rinex_converter.log"
        self.logger = logging.getLogger('RINEXConverter')
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.logger.addHandler(console_handler)

        self.logger.info("================ RINEX CONVERTER START ================")

    def get_user_input(self) -> dict:
        config = {}
        
        # Get station inputs
        leica_sites = input("Leica site/s (comma-separated, lowercase): ").strip()
        config['leica_sites'] = [site.strip() for site in leica_sites.split(',') if site.strip()]
        
        trimble_sites = input("Trimble site/s (comma-separated, uppercase): ").strip()
        config['trimble_sites'] = [site.strip() for site in trimble_sites.split(',') if site.strip()]

        # Get date range
        start_date = input("Start date (dd mm yyyy): ").strip()
        end_date = input("End date (dd mm yyyy): ").strip()
        config['start_date'] = datetime.strptime(start_date, "%d %m %Y")
        config['end_date'] = datetime.strptime(end_date, "%d %m %Y")

        # Get time range
        start_time = input("UTC start time (hhmm): ").strip()
        end_time = input("UTC end time (hhmm): ").strip()
        config['start_hour'] = int(start_time[:2])
        config['start_minute'] = int(start_time[2:])
        config['end_hour'] = int(end_time[:2])
        config['end_minute'] = int(end_time[2:])

        # Get processing options
        config['logging_interval'] = int(input("Logging interval in seconds: ").strip())
        config['rinex_version'] = input("RINEX version (2/3): ").strip()
        config['include_nav'] = input("Include navigation files? (y/n): ").strip().lower() == 'y'
        config['hatanaka_compression'] = input("Apply Hatanaka compression? (y/n): ").strip().lower() == 'y'
        
        return config

    def scan_for_zip_files(self):
        """Scan and list all zip files in input directories for debugging"""
        self.logger.info("=== SCANNING FOR ZIP FILES ===")
        
        # Check main input directory
        input_files = list(self.input_dir.glob("*.zip"))
        self.logger.info(f"Files in {self.input_dir}:")
        for file in input_files:
            self.logger.info(f"  - {file.name}")
        
        # Check input/raw directory
        raw_files = list(self.input_raw_dir.glob("*.zip"))
        self.logger.info(f"Files in {self.input_raw_dir}:")
        for file in raw_files:
            self.logger.info(f"  - {file.name}")
        
        # Check if files are in Raw directory and move them to Input
        if raw_files and not input_files:
            self.logger.info("Found zip files in Raw directory, moving to Input directory...")
            for file in raw_files:
                new_location = self.input_dir / file.name
                shutil.move(str(file), str(new_location))
                self.logger.info(f"Moved {file.name} to Input directory")
        
        self.logger.info("=== END SCAN ===")

    def find_and_extract_zip_files(self, config: dict) -> List[dict]:
        """Find and extract zip files matching the criteria"""
        extracted_files = []
        
        current_date = config['start_date']
        end_date = config['end_date']
        
        while current_date <= end_date:
            doy = current_date.timetuple().tm_yday
            year = current_date.year
            
            # Determine hour range for this day
            if current_date == config['start_date']:
                start_hour = config['start_hour']
            else:
                start_hour = 0
                
            if current_date == config['end_date']:
                end_hour = config['end_hour']
                if config['end_minute'] == 0:
                    end_hour -= 1
            else:
                end_hour = 23
            
            # Process each hour
            for hour in range(start_hour, end_hour + 1):
                hour_letter = self.hour_letters[hour]
                doy_str = f"{doy:03d}"
                
                # Check for Leica files
                for site in config['leica_sites']:
                    if site:  # Only process if site is not empty
                        zip_pattern = f"{site}{doy_str}{hour_letter}.zip"
                        self.logger.info(f"Looking for Leica pattern: {zip_pattern}")
                        zip_files = list(self.input_dir.glob(zip_pattern))
                        
                        if not zip_files:
                            # Also try with different extensions or patterns
                            alt_patterns = [
                                f"{site}{doy_str}{hour_letter}.*.zip",
                                f"{site.upper()}{doy_str}{hour_letter}.zip",
                                f"{site.lower()}{doy_str}{hour_letter}.zip"
                            ]
                            for alt_pattern in alt_patterns:
                                alt_files = list(self.input_dir.glob(alt_pattern))
                                if alt_files:
                                    self.logger.info(f"Found files with alternative pattern: {alt_pattern}")
                                    zip_files.extend(alt_files)
                                    break
                        
                        for zip_file in zip_files:
                            self.logger.info(f"Extracting Leica file: {zip_file.name}")
                            with zipfile.ZipFile(zip_file, 'r') as z:
                                z.extractall(self.input_raw_dir)
                            
                            extracted_files.append({
                                'site': site,
                                'doy': doy,
                                'hour': hour,
                                'year': year,
                                'type': 'leica',
                                'zip_file': zip_file
                            })
                
                # Check for Trimble files
                for site in config['trimble_sites']:
                    if site:  # Only process if site is not empty
                        zip_pattern = f"{site}{doy_str}{hour_letter}.zip"
                        self.logger.info(f"Looking for Trimble pattern: {zip_pattern}")
                        zip_files = list(self.input_dir.glob(zip_pattern))
                        
                        if not zip_files:
                            # Also try with different extensions or patterns
                            alt_patterns = [
                                f"{site}{doy_str}{hour_letter}.*.zip",
                                f"{site.upper()}{doy_str}{hour_letter}.zip",
                                f"{site.lower()}{doy_str}{hour_letter}.zip"
                            ]
                            for alt_pattern in alt_patterns:
                                alt_files = list(self.input_dir.glob(alt_pattern))
                                if alt_files:
                                    self.logger.info(f"Found files with alternative pattern: {alt_pattern}")
                                    zip_files.extend(alt_files)
                                    break
                        
                        for zip_file in zip_files:
                            self.logger.info(f"Extracting Trimble file: {zip_file.name}")
                            with zipfile.ZipFile(zip_file, 'r') as z:
                                z.extractall(self.input_raw_dir)
                            
                            extracted_files.append({
                                'site': site,
                                'doy': doy,
                                'hour': hour,
                                'year': year,
                                'type': 'trimble',
                                'zip_file': zip_file
                            })
            
            current_date += timedelta(days=1)
        
        self.logger.info(f"Total extracted files: {len(extracted_files)}")
        return extracted_files

    def merge_t02_files(self, site: str, doy: int, year: int):
        """Merge T02 files of the same station and DOY"""
        doy_str = f"{doy:03d}"
        pattern = f"{site}{doy_str}*.T02"
        t02_files = list(self.input_raw_dir.glob(pattern))
        
        if len(t02_files) > 1:
            self.logger.info(f"Merging {len(t02_files)} T02 files for {site} DOY {doy}")
            merged_file = self.input_raw_dir / f"{site}{doy_str}.T02"
            
            with open(merged_file, 'wb') as outfile:
                for t02_file in sorted(t02_files):
                    with open(t02_file, 'rb') as infile:
                        outfile.write(infile.read())
                    t02_file.unlink()  # Delete original file
            
            self.logger.info(f"Merged T02 file created: {merged_file.name}")
            return merged_file
        elif len(t02_files) == 1:
            return t02_files[0]
        else:
            self.logger.warning(f"No T02 files found for {site} DOY {doy}")
            return None

    def process_leica_files(self, site: str, doy: int, year: int):
        """Process Leica MDB files - concatenate all hour files for a full day"""
        doy_str = f"{doy:03d}"
        
        # Look for all MDB files for this site and DOY (all hours)
        mdb_pattern = f"{site}{doy_str}*.m*"
        mdb_files = list(self.input_raw_dir.glob(mdb_pattern))
        
        if not mdb_files:
            self.logger.warning(f"No MDB files found for pattern: {mdb_pattern}")
            return
        
        self.logger.info(f"Processing {len(mdb_files)} Leica MDB files for {site} DOY {doy}")
        for mdb_file in mdb_files:
            self.logger.info(f"  - {mdb_file.name}")
        
        # Create a space-separated string of all MDB filenames for the command
        mdb_filenames = " ".join([mdb_file.name for mdb_file in mdb_files])
        
        # Run mdb2rinex with all files to create a concatenated full-day file
        cmd = f"mdb2rinex -f {mdb_filenames} -o temp"
        
        try:
            result = subprocess.run(cmd, shell=True, cwd=self.input_raw_dir, 
                                  capture_output=True, text=True, check=True)
            self.logger.info(f"mdb2rinex completed for {site} DOY {doy} (full day)")
            if result.stdout:
                self.logger.info(f"STDOUT: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running mdb2rinex: {e}")
            self.logger.error(f"STDERR: {e.stderr}")
            # Fallback: try processing files individually if batch processing fails
            self.logger.info("Attempting to process files individually as fallback...")
            for mdb_file in mdb_files:
                try:
                    cmd_individual = ["mdb2rinex", "-f", mdb_file.name, "-o", "temp"]
                    result = subprocess.run(cmd_individual, cwd=self.input_raw_dir, 
                                          capture_output=True, text=True, check=True)
                    self.logger.info(f"Individual processing completed for {mdb_file.name}")
                except subprocess.CalledProcessError as e_individual:
                    self.logger.error(f"Error processing {mdb_file.name}: {e_individual}")

    def process_trimble_files(self, site: str, doy: int, year: int):
        """Process Trimble T02 files"""
        doy_str = f"{doy:03d}"
        
        # First merge T02 files if multiple exist
        t02_file = self.merge_t02_files(site, doy, year)
        
        if not t02_file:
            return
        
        self.logger.info(f"Processing Trimble file: {t02_file.name}")
        
        cmd = ["convertToRinex", t02_file.name, "-v", "3.02", "-p", "temp"]
        
        try:
            result = subprocess.run(cmd, cwd=self.input_raw_dir, 
                                  capture_output=True, text=True, check=True)
            self.logger.info(f"convertToRinex completed for {t02_file.name}")
            if result.stdout:
                self.logger.info(f"STDOUT: {result.stdout}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running convertToRinex: {e}")
            self.logger.error(f"STDERR: {e.stderr}")

    def convert_rinex_version_and_logging(self, site: str, doy: int, year: int, target_version: str, logging_interval: int):
        """Convert RINEX version and apply logging interval as the first step"""
        doy_str = f"{doy:03d}"
        year_str = f"{year % 100:02d}"
        
        temp_dir =  self.temp_dir
        if not temp_dir.exists():
            self.logger.warning(f"Temp directory not found: {temp_dir}")
            return
        
        # Find RINEX files in temp directory
        rinex_pattern = f"{site}{doy_str}*.{year_str}o"
        rinex_files = list(temp_dir.glob(rinex_pattern))
        
        if not rinex_files:
            self.logger.warning(f"No RINEX files found for pattern: {rinex_pattern}")
            return
        
        for rinex_file in rinex_files:
            output_file = self.final_temp_dir / rinex_file.name
            
            if target_version == "2":
                # For version 2: convert to version 2
                cmd = ["gfzrnx", "-finp", rinex_file.name, "-fout", str(output_file), "-smp", str(logging_interval), "-q", "-vo", "2", "-f"]
                self.logger.info(f"Converting to RINEX v2 and setting up for {rinex_file.name}")
            else:
                # For version 3: apply logging interval
                cmd = ["gfzrnx", "-finp", rinex_file.name, "-fout", str(output_file), "-smp", str(logging_interval), "-q", "-kv", "-f"]
                self.logger.info(f"Applying logging interval {logging_interval}s to {rinex_file.name}")
            
            try:
                result = subprocess.run(cmd, cwd=temp_dir, 
                                      capture_output=True, text=True, check=True)
                self.logger.info(f"Version/logging conversion completed for {rinex_file.name}")
                if result.stdout:
                    self.logger.info(f"STDOUT: {result.stdout}")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error in version/logging conversion: {e}")
                self.logger.error(f"STDERR: {e.stderr}")
                # Copy original file if conversion fails
                shutil.copy2(rinex_file, output_file)
                self.logger.warning(f"Copied original file due to conversion error: {rinex_file.name}")

    def fix_rinex_headers(self, site: str, doy: int, year: int):
        """Fix RINEX headers using gfzrnx - now operates on files in final temp directory"""
        doy_str = f"{doy:03d}"
        year_str = f"{year % 100:02d}"
        
        if not self.final_temp_dir.exists():
            self.logger.warning(f"Final temp directory not found: {self.final_temp_dir}")
            return
        
        # Find RINEX files in final temp directory
        rinex_pattern = f"{site}{doy_str}*.{year_str}o"
        rinex_files = list(self.final_temp_dir.glob(rinex_pattern))
        
        if not rinex_files:
            self.logger.warning(f"No RINEX files found for pattern: {rinex_pattern}")
            return
        
        header_file = self.base_dir / "pagenetHDR.txt"
        
        for rinex_file in rinex_files:
            output_file = self.final_temp_dir / f"fixed_{rinex_file.name}"
            
            if header_file.exists():
                cmd = ["gfzrnx", "-finp", rinex_file.name, "-fout", output_file.name,
                       "-crux", str(header_file), "-hded", "-q", "-kv"]
                
                try:
                    result = subprocess.run(cmd, cwd=self.final_temp_dir, 
                                          capture_output=True, text=True, check=True)
                    self.logger.info(f"Header fixed for {rinex_file.name}")
                    if result.stdout:
                        self.logger.info(f"STDOUT: {result.stdout}")
                    
                    # Replace original with fixed version
                    rinex_file.unlink()
                    output_file.rename(rinex_file)
                    
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Error fixing headers for {rinex_file.name}: {e}")
                    self.logger.error(f"STDERR: {e.stderr}")
                    # Remove the failed output file if it exists
                    if output_file.exists():
                        output_file.unlink()
            else:
                self.logger.warning("Header file not found, skipping header fix")

    def create_zip_files(self, site: str, doy: int, year: int, include_nav: bool):
        """Create zip files with RINEX data using the new naming convention"""
        doy_str = f"{doy:03d}"
        year_str = f"{year % 100:02d}"
        
        temp_dir = self.input_raw_dir / "temp"
        
        # Find observation files in final temp directory
        obs_pattern = f"{site}{doy_str}*.{year_str}o"
        obs_files = list(self.final_temp_dir.glob(obs_pattern))
        
        for obs_file in obs_files:
            # Create new zip name in format: sitenamedoy.yro.zip (e.g., PAPI0950.23o.zip)
            # Extract site name (first 4 characters) and use uppercase
            site_name = site[:4].upper()
            zip_name = f"{site_name}{doy_str}0.{year_str}o.zip"
            zip_path = self.final_dir / zip_name
            
            files_to_zip = [obs_file]
            
            if include_nav:
                # Find corresponding navigation files in temp directory
                base_name = obs_file.stem
                for nav_type in self.navigation_types:
                    nav_pattern = f"{base_name}.{year_str}{nav_type}"
                    nav_files = list(temp_dir.glob(nav_pattern))
                    files_to_zip.extend(nav_files)
            
            # Create zip file using 7zip for better compression
            # First try 7zip, fallback to Python zipfile if 7zip is not available
            try:
                # Create file list for 7zip
                file_list = []
                working_dir = None
                
                for file_path in files_to_zip:
                    if file_path.exists():
                        # Use relative path and set working directory
                        if working_dir is None:
                            working_dir = file_path.parent
                        file_list.append(file_path.name)
                
                if file_list and working_dir:
                    # Use 7zip command
                    cmd = ["7z", "a", "-tzip", str(zip_path)] + file_list
                    result = subprocess.run(cmd, cwd=working_dir, 
                                          capture_output=True, text=True, check=True)
                    self.logger.info(f"Created zip file with 7zip: {zip_path.name}")
                    for file_name in file_list:
                        self.logger.info(f"Added to zip: {file_name}")
                        
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                # Fallback to Python zipfile if 7zip fails or is not available
                self.logger.warning(f"7zip not available or failed: {e}. Using Python zipfile as fallback.")
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in files_to_zip:
                        if file_path.exists():
                            zipf.write(file_path, file_path.name)
                            self.logger.info(f"Added to zip: {file_path.name}")
                
                self.logger.info(f"Created zip file with Python zipfile: {zip_path.name}")

    def apply_hatanaka_compression(self, site: str, doy: int, year: int):
        """Apply Hatanaka compression to RINEX files"""
        doy_str = f"{doy:03d}"
        year_str = f"{year % 100:02d}"
        
        # Find zip files in final directory using the new naming convention
        site_name = site[:4].upper()
        zip_pattern = f"{site_name}{doy_str}0.{year_str}o.zip"
        zip_files = list(self.final_dir.glob(zip_pattern))
        
        for zip_file in zip_files:
            # Extract zip file temporarily
            temp_extract_dir = self.final_dir / "temp_extract"
            temp_extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_file, 'r') as zipf:
                zipf.extractall(temp_extract_dir)
            
            # Find observation files and compress them
            obs_files = list(temp_extract_dir.glob(f"*.{year_str}o"))
            
            for obs_file in obs_files:
                compressed_file = temp_extract_dir / f"{obs_file.stem}.{year_str}d"
                
                # Apply Hatanaka compression
                cmd = f"gfzrnx -finp {obs_file.name} | rnx2crx > {compressed_file.name}"
                
                try:
                    result = subprocess.run(cmd, shell=True, cwd=temp_extract_dir, 
                                          capture_output=True, text=True, check=True)
                    self.logger.info(f"Applied Hatanaka compression: {obs_file.name}")
                    
                    # Remove uncompressed file
                    obs_file.unlink()
                    
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"Error applying Hatanaka compression: {e}")
                    self.logger.error(f"STDERR: {e.stderr}")
            
            # Create new zip file with compressed data using the same naming convention
            compressed_zip_name = zip_file.name.replace('.zip', '_compressed.zip')
            compressed_zip_path = self.final_dir / compressed_zip_name
            
            # Try to create compressed zip with 7zip first, fallback to Python zipfile
            try:
                # Create file list for 7zip
                file_list = []
                for file_path in temp_extract_dir.glob("*"):
                    if file_path.is_file():
                        file_list.append(file_path.name)
                
                if file_list:
                    # Use 7zip command
                    cmd = ["7z", "a", "-tzip", str(compressed_zip_path)] + file_list
                    result = subprocess.run(cmd, cwd=temp_extract_dir, 
                                          capture_output=True, text=True, check=True)
                    self.logger.info(f"Created compressed zip with 7zip: {compressed_zip_path.name}")
                    
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                # Fallback to Python zipfile if 7zip fails or is not available
                self.logger.warning(f"7zip not available or failed: {e}. Using Python zipfile as fallback.")
                
                with zipfile.ZipFile(compressed_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in temp_extract_dir.glob("*"):
                        if file_path.is_file():
                            zipf.write(file_path, file_path.name)
                
                self.logger.info(f"Created compressed zip with Python zipfile: {compressed_zip_path.name}")
            
            # Remove original zip and temp directory
            zip_file.unlink()
            shutil.rmtree(temp_extract_dir)

    def cleanup_temporary_files(self):
        """Clean up all temporary files"""
        self.logger.info("Cleaning up temporary files...")
        
        # Clean Input/Raw directory
        for file_path in self.input_raw_dir.glob("*"):
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
        
        # Clean temp directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        
        # Clean final temp directory
        if self.final_temp_dir.exists():
            shutil.rmtree(self.final_temp_dir)
        
        self.logger.info("Cleanup completed")

    def run(self):
        config = self.get_user_input()
        
        # Step 1: Find and extract zip files
        self.logger.info("Step 1: Finding and extracting zip files...")
        extracted_files = self.find_and_extract_zip_files(config)
        
        if not extracted_files:
            self.logger.warning("No files found for processing")
            self.logger.info("Please check:")
            self.logger.info("1. Zip files are in C:\\RNXConverter\\Input\\")
            self.logger.info("2. File names follow the pattern: sitenameDOYhour.zip")
            self.logger.info("3. DOY is 3 digits (e.g., 095 for day 95)")
            self.logger.info("4. Hour is a letter (a-x for hours 0-23)")
            self.logger.info("5. Date range and stations match your input")
            return
        
        # Group files by site and DOY for processing
        site_groups = {}
        for file_info in extracted_files:
            key = (file_info['site'], file_info['doy'], file_info['year'], file_info['type'])
            if key not in site_groups:
                site_groups[key] = []
            site_groups[key].append(file_info)
        
        # Process each site group
        for (site, doy, year, site_type), files in site_groups.items():
            self.logger.info(f"Processing {site} DOY {doy} ({site_type})")
            
            # Step 2-4: Process raw files
            if site_type == 'leica':
                self.process_leica_files(site, doy, year)
            elif site_type == 'trimble':
                self.process_trimble_files(site, doy, year)
            
            # Step 5: Convert RINEX version and apply logging interval FIRST
            self.logger.info(f"Step 5: Converting RINEX version and applying logging interval for {site} DOY {doy}")
            self.convert_rinex_version_and_logging(site, doy, year, config['rinex_version'], config['logging_interval'])
            
            # Step 6: Fix headers AFTER version/logging conversion
            self.logger.info(f"Step 6: Fixing RINEX headers for {site} DOY {doy}")
            self.fix_rinex_headers(site, doy, year)
            
            # Step 7: Create zip files
            self.logger.info(f"Step 7: Creating zip files for {site} DOY {doy}")
            self.create_zip_files(site, doy, year, config['include_nav'])
            
            # Step 8: Apply Hatanaka compression if requested
            if config['hatanaka_compression']:
                self.logger.info(f"Step 8: Applying Hatanaka compression for {site} DOY {doy}")
                self.apply_hatanaka_compression(site, doy, year)
        
        # Step 9: Cleanup temporary files
        self.logger.info("Step 9: Cleaning up temporary files...")
        self.cleanup_temporary_files()
        
        self.logger.info("================ RINEX CONVERTER COMPLETE ================")
        self.logger.info(f"Processed {len(site_groups)} site/day combinations")
        self.logger.info(f"Output files are in: {self.final_dir}")


def main():
    """Main function to run the RINEX converter"""
    try:
        converter = RINEXConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()