"""
This is an add-on for DocumentCloud.

It reads a csv of relative paths to PDF's to upload.
CSV File ought to be formatted as one relative file-path per row.
"""

from addon import AddOn
import csv
import os


class PDFSizeCheckUpload(AddOn):

    def main(self):
        
        # get the path to the CSV document from the 'params' input argument.
        """
        e.g. this was the tested command-ish:

        python3.8 test_addon.py --username "your-name" --password "your-pw" --params '{"name": "world", "pdf_csv": "path-to-your-csv"}'

        """
        csv_path = self.data["pdf_csv"]

        # read the csv at the end of that path and iterate through
        # the paths that are there.
        paths = []
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
            for row in reader:
                paths.append(row[0])

        for path in paths:
            if os.path.exists(path):
                print(path)
                fileSize = os.path.getsize(path)
                fileSizeMB = round(fileSize / (1024 * 1024), 3)
                if fileSizeMB <= 500:
                    print(f"    File size is: {fileSizeMB} MB, <500MB")
                    fileObj = self.client.upload(path)
                    fileObj.access = "private"
                    fileObj.put()
                    print("     File Uploaded.")
                else:
                    print("     File too large! >= 500MB")
            else:
                print(f"{path} doesn't exist.")



if __name__ == "__main__":
    PDFSizeCheckUpload().main()
