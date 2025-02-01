# Intro

# Setup

1. Install vscode
2. Install vscode packages: git package(s), language packages, data manipulating packages, code assist packages, etc.
3. Install python
4. Install MS VS Build Tools for cx_Oracle old version to connect to Oracle 8i
   (Oracle Instance Client 10.2)
4. Install python packages with requirements.txt
   (oracledb, streamlit, etc. )
5. Install ipython package for jupyter note
6. Install oracle instant client (for below 10g, thick client is necessary)
   (https://www.oracle.com/kr/database/technologies/instant-client.html)
   10.2 for 8i / 11.2 for 9i / 12.1 for 10g

=======
* Oracle Instant Client Install
    instantclient from oracle version limitations

* Python Install
    Windows Store Python 3.12

* Python Package Install
    pip install -r requirements.txt

* Google Cloud Platform command line interface(CLI) download & install
    (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
    & $env:Temp\GoogleCloudSDKInstaller.exe


# Streamlit 실행
streamlit run gh_app.py

# Deploy Cloud Run
pip freeze > requirements.txt

# Environment setup for Cloud Build
set PROJECT_ID=dk-medical-solutions
set REGION=asia-northeast3
set APP=dk-ghmh
set TAG=gcr.io/%PROJECT_ID%/%APP%

# Cloud build
gcloud builds submit --secret id=creds,src=.streamlits/secrets.toml --project=%PROJECT_ID% --tag %TAG%

# Cloud Run deployment
gcloud run deploy %APP% --project %PROJECT_ID% --image %TAG% --platform managed --region %REGION% --allow-unauthenticated --port 8501
