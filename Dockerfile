FROM octoprint/octoprint

RUN pip install "cookiecutter>=1.4,<1.7"

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
