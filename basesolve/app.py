from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DNA Complement Mapping
complement_map = str.maketrans("ATCG", "TAGC")

def reverse_complement(sequence):
    """Returns the reverse complement of a DNA sequence."""
    return sequence.translate(complement_map)[::-1] if isinstance(sequence, str) else sequence

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Read CSV file
        df = pd.read_csv(filepath, skip_blank_lines=False, header=None)

        # Identify section indices
        header_index = df[df.iloc[:, 0] == "[Header]"].index
        reads_index = df[df.iloc[:, 0] == "[Reads]"].index
        settings_index = df[df.iloc[:, 0] == "[Settings]"].index
        data_index = df[df.iloc[:, 0] == "[Data]"].index

        # Debugging prints (remove later if needed)
        print(f"Header index: {header_index}")
        print(f"Reads index: {reads_index}")
        print(f"Settings index: {settings_index}")
        print(f"Data index: {data_index}")

        # Check if all sections exist
        if len(header_index) == 0 or len(reads_index) == 0 or len(settings_index) == 0 or len(data_index) == 0:
            return "Error: CSV file is missing required sections!"

        # Extract sections
        header = df.iloc[header_index[0]:reads_index[0]].dropna(axis=1, how="all").to_string(index=False)
        reads = df.iloc[reads_index[0]:settings_index[0]].dropna(axis=1, how="all").to_string(index=False)
        settings = df.iloc[settings_index[0]:data_index[0]].dropna(axis=1, how="all").to_string(index=False)
        data = df.iloc[data_index[0] + 1:].dropna(axis=1, how="all")

        # Ensure column names are set
        data.columns = data.iloc[0]  # Set first row as headers
        data = data[1:].reset_index(drop=True)  # Remove first row and reset index

        # Save original data for future downloads
        data.to_csv(os.path.join(UPLOAD_FOLDER, "original.csv"), index=False)

        return render_template("index.html", header=header, reads=reads, settings=settings, tables=data.to_html(index=False), filename=file.filename)

    return render_template("index.html")

@app.route("/reverse_complement", methods=["POST"])
def reverse_complement_column():
    filepath = os.path.join(UPLOAD_FOLDER, "original.csv")

    if not os.path.exists(filepath):
        return "Error: No uploaded file found."

    df = pd.read_csv(filepath)

    if "index2" not in df.columns:
        return "Error: Column 'index2' not found in CSV file."

    # Reverse complement the "index2" column
    df["index2"] = df["index2"].apply(reverse_complement)

    # Save modified CSV
    modified_filepath = os.path.join(UPLOAD_FOLDER, "modified_reverse_complement.csv")
    df.to_csv(modified_filepath, index=False)

    return df.to_html(index=False)  # Return updated table to display in HTML

@app.route("/download")
def download_file():
    modified_filepath = os.path.join(UPLOAD_FOLDER, "modified_reverse_complement.csv")
    if os.path.exists(modified_filepath):
        return send_file(modified_filepath, as_attachment=True)
    return "Error: No modified file found."

if __name__ == "__main__":
    app.run(debug=True,port=5001)
