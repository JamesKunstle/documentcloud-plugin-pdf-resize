"""
This is an add-on for DocumentCloud.

It reads a csv of relative paths to PDF's to upload.
CSV File ought to be formatted as one relative file-path per row.
"""

from addon import AddOn
import csv
import os
import time


class PDFSizeCheckUpload(AddOn):

    def main(self):
        
        # get the path to the CSV document from the 'params' input argument.
        """
        e.g. this was the tested command-ish:

        python3.8 test_addon.py --params '{"pdf_csv": "./pdf_csv.csv", "default_access": "private"}'
        """
        csv_path = self.data["pdf_csv"]

        access_options = ["public", "private", "organization"]
        access = self.data["default_access"]
        if access not in access_options or access is None:
            access = "private"

        # read the csv at the end of that path and iterate through
        # the paths that are there.
        paths = []
        with open(csv_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
            for row in reader:
                paths.append(row[0])

        # for each of the paths we were given:
        for path in paths:
            # confirm path exists.
            if os.path.exists(path):

                if os.path.isdir(path):
                    print(f"{path} is directory- not currently supported.")
                    continue

                print(path)
                # calculate file size.
                fileSize = os.path.getsize(path)
                fileSizeMB = round(fileSize / (1024 * 1024), 3)

                if fileSizeMB <= 500:
                    print(f"    File size is: {fileSizeMB} MB, <500MB")
                    fileObj = self.client.documents.upload(path)
                    print("     Waiting for Successful Upload")

                    # confirm that document is being uploaded.
                    while fileObj.status != 'success':
                        time.sleep(5)
                        fileObj = self.client.documents.get(fileObj.id)
                        print("     ...")

                    # automatically set document upload status to private.
                    fileObj.access = access
                    # update status of document.
                    fileObj.put()
                    print("     File Uploaded.")
                else:
                    print("     File too large! >= 500MB")
            else:
                print(f"{path} doesn't exist.")



if __name__ == "__main__":
    PDFSizeCheckUpload().main()
