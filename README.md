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

$env:PROJECT_ID='dk-medical-solutions'
$env:REGION='asia-northeast3'
$env:APP='dk-ghmh'
$env:TAG="gcr.io/$env:PROJECT_ID/$env:APP"

# Cloud build
gcloud builds submit --secret id=creds,src=.streamlits/secrets.toml --project=%PROJECT_ID% --tag %TAG%
gcloud builds submit --project=%PROJECT_ID% --tag %TAG%
gcloud builds submit --project=$env:PROJECT_ID --tag $env:TAG

# Cloud Run deployment
gcloud run deploy %APP% --project %PROJECT_ID% --image %TAG% --platform managed --region %REGION% --allow-unauthenticated --port 8501

gcloud run deploy $env:APP --project $env:PROJECT_ID --image $env:TAG --platform managed --region $env:REGION --allow-unauthenticated --port 8501
