import requests


class UploadFile:
    def __init__(self) -> None:
        self.api_url = "https://basket.irannk.com/Products/UploadFile/upload-file"
        self.file_path = "/home/mahnaz/akam/upload_file/assets/akam.png"
        
    def uplaod_file(self):
        try:
            with open(self.file_path, "rb") as file:
                files = {"file": file}
                response = requests.post(self.api_url, files=files)
                if response.status_code == 200:
                    print("File Uploaded Successfully.")
                else:
                    print(response.status_code)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            
            




# with open(file_path, "rb") as file:
#     files = {"file": file}
#     response = requests.post(api_url, files=files)
#     if response.status_code == 200:
#         print("File uploaded successfully.")
#     else:
#         print(response.status_code)