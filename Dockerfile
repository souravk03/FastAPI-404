#base image
FROM python:3.7

#working directory
WORKDIR /app

#copying file
COPY . /app

#installing dependencies
RUN pip install -r requirements.txt

#ports expose
EXPOSE 8501

#running the app
CMD ["streamlit", "run", "app.py"]