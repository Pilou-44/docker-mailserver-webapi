<a name="readme-top"></a>

<div align="center">
  <h2 align="center">Docker Mailserver - Web API</h2>
  <div align="center">
    <p align="center">a REST API that helps you efficiently manage your <a href="https://github.com/docker-mailserver/docker-mailserver" title="Docker Mailserver">docker-mailserver</a> configuration.</p>
    <div>
        <a href="https://github.com/bramanda48/docker-mailserver-webapi/releases/"><img src="https://img.shields.io/github/release/bramanda48/docker-mailserver-webapi?include_prereleases=&sort=semver&color=blue" alt="GitHub release"></a>
        <a href="https://github.com/bramanda48/docker-mailserver-webapi#license"><img src="https://img.shields.io/badge/License-MIT-blue" alt="License"></a>
    </div>
    <p>Based on <a href="https://github.com/bramanda48/docker-mailserver-webapi">docker-mailserver-webapi </a></p>
  </div>
</div>

---
## Requirements
- python3.10

Install the requirements by doing: `pip install -r requirements.txt`

## Installation & Usage

1. Locally

Execute the file `main.py`.
```bash
python main.py
```
2. Compose
```yaml
services:
  docker-mailserver:
    env_file: "dockermailserver.env"
    ...
    volumes:
    - ./XXX:/tmp/docker-mailserver

  web_api:
    build: ./docker-mailserver-webapi # IF This is the name of the folder
    command: python main.py
    ports:
    - "8080:3000"
    env_file:
    - "webapi.env"
    - "dockermailserver.env"
```
3. By default, this application will run on port 3000.
2. The env variables are:
```env
WEB_API_LISTEN_PORT
WEB_API_DMS_CONFIG_PATH
WEB_API_FAIL2BAN_SQLITE_PATH
WEB_API_KEY
```

### Build
You can also build an image before adding it to the compose:
```bash
docker build -t dockermailserver_webapi .
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/bramanda48/docker-mailserver-webapi/blob/master/LICENSE.md) file for details.

## Acknowledgments

Inspiration, code snippets, icon, etc.
* [Docker Mailserver](https://github.com/docker-mailserver/docker-mailserver) by The Docker Mailserver Organization & Contributors.
