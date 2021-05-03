# Trying out a docker image from gorialis that will hopefully fix some things

FROM gorialis/discord.py
ENV TZ="America/Phoenix"

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "discord_integration.py"]