# Pulling Census Demographic Data Using the Census API and User-Defined State Inputs

## Overview
This project allows for the retrieval and customization of recent Census ACS demographic data in CSV format for integration into Python, SQL, or geospatial analysis workflows.

## Objective
The Census Bureau provides demographic data through the ACS API, but retrieving and formatting it for repeatable analysis requires custom scripting. This project retrieves user-defined demographic categories for every county or county-equivalent in selected states, creates standardized GEOIDs, and exports analysis-ready CSV files for use in Python, SQL, or GIS workflows.

## Methodology
- Access the Census Bureau ACS API using a user-provided API key
- Pull county-level demographic variables for user-defined states
- Calculate age, race, and income summary fields
- Create county GEOIDs for seamless joins to Census county shapefiles
- Export one CSV table per state for further analysis

## Tools Used
- Python (data retrieval and processing)
- Census Bureau ACS API

## Example Output

### Excerpt of County-level result for Georgia:
<img width="1841" height="337" alt="image" src="https://github.com/user-attachments/assets/2b4e01d6-f90c-477a-aa16-26f81d69ab88" />

### Using the data as an input for mapping in GIS:
<img width="772" height="1006" alt="image" src="https://github.com/user-attachments/assets/43beefae-ef86-4c1f-8fb1-33663d9a2abc" />



## Key Insight
Census ACS demographic variables are granular enough to produce highly detailed county-level summaries. For example, the script can estimate populations by age, race, and income category for every county in a selected state. Including a GEOID for each county also allows for seamless integration into GIS workflows and SQL databases for downstream spatial or statistical analysis.

## Application
These datasets can support:
- county-level demographic analysis
- electoral outreach strategy
- voter turnout analysis
- geographic targeting and resource allocation
- GIS-based demographic visualization

## Reusability
The current version of the script focuses on demographic categories related to age, race, and income. Additional ACS variables can be incorporated by modifying the Census API field parameters while maintaining the overall workflow structure. The script is designed to be modular and scalable for broader Census data retrieval applications.
