# Web App for downloading reverse complemented csv 

This is a simple Flask web application that allows users to upload a CSV file, extract different sections (Header, Reads, Settings, and Data), process the `index2` column to get the reverse complement, and download the modified CSV.

## Features
Upload CSV files  
Extract `[Header]`, `[Reads]`, `[Settings]`, and `[Data]` sections  
Display data table  
Reverse complement the `index2` column  
Download modified CSV  

---
## requirement 
you can install library "pip install flask pandas"

or 

pip install -r requirements.txt


## Installation

1. **Clone this repository**  
   git clone git clone https://github.com/Komal-Madiwal/basesolve_assignm.git
   cd basesolve


## run web app 
python app.py
The app will start on http://127.0.0.1:5000/

## how to use web app 
1.Upload a CSV File
Go to the web interface (http://127.0.0.1:5000/).
Click "Choose File" and select a CSV file.
Click "Upload."
example:- 

![Upload CSV](screenshot/upload_csv_file_ss.PNG)

2 View Extracted Sections
After uploading, the app will display [Header], [Reads], [Settings], and [Data] sections.
![Extracted Sections](screenshot/extracted_header.PNG)


3️.Reverse Complement the index2 Column
Click the "Reverse Complement index2" button.
The modified table will be displayed.
Example Screenshot:
![reverse_complement](screenshot/reverse_comp_button.PNG)

4️.Download the Modified CSV
After processing, click the "Download Modified CSV" button.
Example Screenshot:
![download_modified_csv](screenshot/reverse.PNG)


