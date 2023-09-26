from requests import post
from requests.exceptions import HTTPError
from json import dumps


class Post:
    def __init__(self):
        self.url = "https://basket.irannk.com/Products/UploadFile/upload-file"
        self.data = {
            "memebr1" : "SpongeBob SquarePants",
            "member2" : "Patric Star"
        }
        self.json = dumps(self.data)

    def upload(self):
        try:
            data = {"file": self.json}
            response = post(self.url, files=data)
            statuscode = response.status_code

            if statuscode == 200:
                print("File Uploaded Successfully.")
                print(response.content)
            else:
                print(statuscode)

        except HTTPError as e:
            print(f'HTTP error occurred: {e}')
        except Exception as e:
            print(f"An error occurred: {e}")
