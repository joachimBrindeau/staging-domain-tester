# Staging domain Tester

Staging domain Tester is a Python script that tests all URLs in an XML sitemap using a specified staging domain. It retrieves the sitemap, extracts all URLs, replaces the original domain in these URLs with the input staging domain, and tests each URL while providing updates on progress in the terminal. The HTTP status code for each URL is recorded.

The test results, including the URL and the HTTP status code, are saved in a CSV file named after the sitemap's domain. If a CSV file for the sitemap's domain already exists, the script offers the option to either retest all URLs or only retest URLs that previously returned a specific status code, like 404 or 301. 

The new test results are then saved, and the CSV file is updated accordingly.

## Prerequisites

- MacOS
- Python 3
- Python packages: `requests` and `beautifulsoup4`

## Features

- **Retrieves a sitemap from a given URL**: The script starts by asking for the sitemap's URL and the staging domain.
- **Replaces the original domain with a staging domain**: The script replaces the original domain in the extracted URLs with your specified staging domain.
- **Tests each URL individually**: The script sends a GET request to each URL and obtains the HTTP status code.
- **Updates progress in terminal**: You can monitor the script's progress in real-time in your terminal.
- **Saves all the results in a CSV file**: The CSV file will be named after the sitemap's domain, and will contain all tested URLs along with their HTTP status codes.
- **Partial retest option**: If an existing CSV file for that domain is found, the script asks whether to retest all URLs or only those that previously returned a specific status code.

## Installation on MacOS

Here are the steps to get the script up and running:

1. Open Terminal.

2. Install Xcode Command Line Tools with the following command:

   ```bash
   xcode-select --install
   ```
   
   Click "Install" and agree to the Terms of Service when prompted.

3. Install Homebrew, a package manager for MacOS, by pasting the following command and hitting Enter:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

4. Install Python 3 using Homebrew:

   ```bash
   brew install python3
   ```

   Verify the installation by checking the version of Python installed:

   ```bash
   python3 --version
   ```

5. Pip, a package installer for Python, should be installed with Python 3. Verify it's installed with:

   ```bash
   pip3 --version
   ```

6. Install required Python packages using pip:

   ```bash
   pip3 install requests beautifulsoup4
   ```

7. Download the script. Replace "https://path_to_the_script/sitemap_tester.py" with the actual URL of the script:

   ```bash
   curl -O https://path_to_the_script/sitemap_tester.py
   ```

## How to Run the Script

1. Navigate to the directory with the script.
2. Run the script using Python 3:

   ```bash
   python3 sitemap_tester.py
   ```

3. When prompted, enter the sitemap URL and the staging domain.

## Results

The script creates a CSV file in the current directory, named after the sitemap's domain (e.g., `example.com.csv`). Each line in the CSV file contains a URL and the HTTP status code returned when testing the URL.

If a CSV file for the sitemap's domain already exists, the script will ask whether to retest all URLs or only the URLs with a specific status code. The script then updates the existing CSV file with the new test results.

## Note

This script sends a GET request to every URL in the sitemap. Depending on the size of the sitemap, running this script could generate substantial network traffic. Please ensure you have appropriate permissions to make multiple requests to the target URLs.
