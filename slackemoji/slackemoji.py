from bs4 import BeautifulSoup
import os
import requests
import re


class SlackEmoji(object):

    MAX_RETRY = 10

    def __init__(self, team_name, email, password):
        self.team_name = team_name
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.is_login = False
        self.existing_emoji_names = []

        self.session.mount("https://",
                           requests.adapters.HTTPAdapter(max_retries=self.MAX_RETRY))

    def upload_emoji(self, name, path):
        if name in self.existing_emoji():
            raise Exception("There is already an emoji named %s." % name)

        if not os.path.exists(path):
            raise Exception("%s file not found." % path)

        self.__login()
        response = self.session.get(self.__emoji_url())
        response.raise_for_status()
        bs = BeautifulSoup(response.text, "html.parser")
        auth_token = bs.find(attrs={"name": "crumb"}).get("value")

        payload = {
            "add": 1,
            "crumb": auth_token,
            "name": name,
            "mode": "data",
        }

        emoji_file = {"img": open(path, "rb")}
        upload_response = self.session.post(self.__emoji_url(),
                                            data=payload,
                                            files=emoji_file,
                                            allow_redirects=False)
        response.raise_for_status()

        if "alert_error" in upload_response.content:
            bs = BeautifulSoup(upload_response.text, "html.parser")
            error = bs.find("p", attrs={"class": "alert_error"})
            raise Exception(error.text)


    def existing_emoji(self):
        if self.existing_emoji_names:
            return self.existing_emoji_names

        self.__login()
        response = self.session.get(self.__emoji_url())
        response.raise_for_status()
        self.existing_emoji_names = re.findall("data-emoji-name=\"(.*)\" ", response.text)
        return self.existing_emoji_names

    def __login_url(self):
        return "https://%s.slack.com/" % self.team_name
    def __emoji_url(self):
        return "https://%s.slack.com/customize/emoji" % self.team_name

    def __login(self):
        if self.is_login:
            return None

        payload = {
            "signin": "1",
            "email": self.email,
            "password": self.password
        }

        response = self.session.get(self.__login_url(),
                                    stream=True,
                                    timeout=(10.0, 30.0))
        response.raise_for_status()

        bs = BeautifulSoup(response.text, "html.parser")
        auth_token = bs.find(attrs={"name": "crumb"}).get("value")
        payload["crumb"] = auth_token

        self.session.post(self.__login_url(), data=payload)
        response.raise_for_status()
        self.is_login = True
