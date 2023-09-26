import requests

class Capsolver:
    def __init__(self, api_key, site_url, site_key, page_action='', min_score=0.9):
        self.api_key = api_key
        self.site_url = site_url
        self.site_key = site_key
        self.page_action = page_action
        self.min_score = min_score

    def create_task(self):
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": "ReCaptchaV3TaskProxyLess",
                "websiteURL": self.site_url,
                "websiteKey": self.site_key,
                "pageAction": "submit",
                "minScore": self.min_score,
            }
        }
        while True:
            try:
                resp = requests.post('https://api.capsolver.com/createTask', json=payload)
                task_id = resp.json()['taskId']
                return task_id
            except Exception as error:
                print(f'ERROR getting task ID: {error}')


    def get_captcha_solution(self, task_id):
        payload = {
            "clientKey": self.api_key,
            "taskId": task_id
        }
        while True:
            try:
                resp = requests.post('https://api.capsolver.com/getTaskResult', json=payload)
                status = resp.json()['status']
                if (status == 'ready'):
                    token = resp.json()['solution']['gRecaptchaResponse']
                    return token
            except Exception as error:
                print(f'ERROR getting captcha solution: {error}')
