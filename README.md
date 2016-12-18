# slackemoji
slackemoji is a simple emoji uploader.

## Installation
The latest release of slackemoji can be installed via pip

```
$ pip install slackemoji
```

An alternative install method would be manually installing it leveraging `setup.py`

```
$ git clone https://github.com/penta515/slackemoji
$ cd slackemoji
$ python setup.py install
```

## Usage examples

```python
from slackemoji import SlackEmoji

slack = SlackEmoji("YOUR_TEAM_NAME", "YOUR_EMAIL", "YOUR_PASSWORD")
slack.upload_emoji("EMOJI_NAME", "EMOJI_FILE_PATH")
```

## Running tests

```
$ py.test tests
```


## License

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
