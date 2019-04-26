FROM python:2.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com
ENV OAUTHLIB_INSECURE_TRANSPORT=true

CMD ["./start.sh"]
