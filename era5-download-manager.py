import pandas as pd
import numpy as np
from pathlib import Path
import time
import logging
from datetime import datetime
import calendar
import cdsapi
import xarray as xr
import zipfile
import concurrent.futures
from typing import Optional, Dict, List, Union

class ERA5DownloadManager:
    """Manages batch downloads of ERA5 climate data with robust error handling and tracking."""
    
    def __init__(self, base_dir: Path, max_retries: int = 3, retry_delay: int = 300):
        """
        Initialize the download manager.
        
        Parameters:
        -----------
        base_dir : Path
            Base directory for storing climate data
        max_retries : int
            Maximum number of retry attempts for failed downloads
        retry_delay : int
            Delay in seconds between retry attempts
        """
        self.base_dir = Path(base_dir)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize directories
        self.raw_dir = self.base_dir / 'raw'
        self.log_dir = self.base_dir / 'logs'
        self.temp_dir = self.base_dir / 'temp'
        
        # Create necessary directories
        for directory in [self.raw_dir, self.log_dir, self.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize CDS API client
        self.client = cdsapi.Client()
    
    def _setup_logging(self):
        """Configure logging with both file and console handlers."""
        log_file = self.log_dir / f'era5_download_{datetime.now():%Y%m%d_%H%M%S}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _get_download_status(self) -> pd.DataFrame:
        """Load or create the download status tracking DataFrame."""
        status_file = self.log_dir / 'download_status.csv'
        
        if status_file.exists():
            return pd.read_csv(status_file)
        else:
            df = pd.DataFrame(columns=[
                'year', 'month', 'status', 'attempts', 
                'last_attempt', 'error_message', 'file_path'
            ])
            df.to_csv(status_file, index=False)
            return df
    
    def _save_download_status(self, status_df: pd.DataFrame):
        """Save the current download status."""
        status_file = self.log_dir / 'download_status.csv'
        status_df.to_csv(status_file, index=False)
    
    def _download_month(self, year: int, month: int) -> Dict[str, Union[str, str]]:
        """
        Download ERA5 data for a specific year and month.
        
        Returns:
        --------
        Dict containing download status and details
        """
        zip_filename = self.raw_dir / f'{year}' / f'era5_daily_india_{year}_{month:02d}.zip'
        zip_filename.parent.mkdir(exist_ok=True)
        
        result = {
            'status': 'failed',
            'error_message': '',
            'file_path': str(zip_filename)
        }
        
        try:
            # Define ERA5 variables (same as in your original code)
            variables = [
                'maximum_2m_temperature_since_previous_post_processing',
                'minimum_2m_temperature_since_previous_post_processing',
                'total_precipitation',
                'surface_net_solar_radiation',
                '2m_dewpoint_temperature'
            ]
            
            num_days = calendar.monthrange(year, month)[1]
            
            self.client.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'variable': variables,
                    'year': str(year),
                    'month': f'{month:02d}',
                    'day': [f'{day:02d}' for day in range(1, num_days + 1)],
                    'time': ['00:00', '12:00'],
                    'area': [38, 68, 8, 98],  # India bounding box
                    'format': 'netcdf',
                },
                zip_filename
            )
            
            # Verify the download by attempting to open it
            with zipfile.ZipFile(zip_filename, 'r') as zf:
                zf.testzip()
            
            result['status'] = 'success'
            
        except Exception as e:
            result['status'] = 'failed'
            result['error_message'] = str(e)
            
            if zip_filename.exists():
                zip_filename.unlink()
        
        return result
    
    def batch_download(self, start_year: int, end_year: int, 
                      start_month: Optional[int] = None, 
                      end_month: Optional[int] = None):
        """
        Execute batch download of ERA5 data with robust error handling.
        
        Parameters:
        -----------
        start_year : int
            Starting year for download
        end_year : int
            Ending year for download
        start_month : Optional[int]
            Starting month (1-12), defaults to 1
        end_month : Optional[int]
            Ending month (1-12), defaults to 12
        """
        start_month = start_month or 1
        end_month = end_month or 12
        
        status_df = self._get_download_status()
        
        for year in range(start_year, end_year + 1):
            year_dir = self.raw_dir / str(year)
            year_dir.mkdir(exist_ok=True)
            
            month_range = range(1, 13)
            if year == start_year:
                month_range = range(start_month, 13)
            elif year == end_year:
                month_range = range(1, end_month + 1)
            
            for month in month_range:
                # Check if already successfully downloaded
                existing = status_df[
                    (status_df['year'] == year) & 
                    (status_df['month'] == month)
                ]
                
                if not existing.empty and existing.iloc[-1]['status'] == 'success':
                    self.logger.info(f"Skipping {year}-{month:02d}, already downloaded")
                    continue
                
                attempts = 0
                while attempts < self.max_retries:
                    self.logger.info(f"Downloading {year}-{month:02d}, attempt {attempts + 1}")
                    
                    result = self._download_month(year, month)
                    
                    # Update status
                    new_status = pd.DataFrame([{
                        'year': year,
                        'month': month,
                        'status': result['status'],
                        'attempts': attempts + 1,
                        'last_attempt': datetime.now().isoformat(),
                        'error_message': result['error_message'],
                        'file_path': result['file_path']
                    }])
                    
                    status_df = pd.concat([status_df, new_status], ignore_index=True)
                    self._save_download_status(status_df)
                    
                    if result['status'] == 'success':
                        break
                    
                    attempts += 1
                    if attempts < self.max_retries:
                        self.logger.warning(
                            f"Download failed for {year}-{month:02d}, "
                            f"retrying in {self.retry_delay} seconds..."
                        )
                        time.sleep(self.retry_delay)
                    else:
                        self.logger.error(
                            f"Maximum retries reached for {year}-{month:02d}. "
                            f"Error: {result['error_message']}"
                        )
                
                # Add delay between months to avoid API rate limits
                time.sleep(5)

if __name__ == "__main__":
    # Example usage
    base_dir = Path("data/climate")
    manager = ERA5DownloadManager(base_dir)
    
    # Download data for test period
    manager.batch_download(
        start_year=1970,
        end_year=1970,  # Test with one year first
        start_month=1,
        end_month=2     # Test with two months
    )
