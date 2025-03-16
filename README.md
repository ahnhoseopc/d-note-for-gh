* Oracle Instant Client Install
    instantclient from oracle version limitations

* Python Install
    Windows Store Python 3.12

* Python Package Install
    pip install -r requirements.txt

* Google Cloud Platform command line interface(CLI) download & install
    (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
    & $env:Temp\GoogleCloudSDKInstaller.exe


#### Streamlit 실행
streamlit run gh_app.py

##### Deploy Cloud Run
pip freeze > requirements.txt


# Cloud Build and Deploy in Windows Command

### Environment setup
set PROJECT_ID=dk-medical-solutions
set REGION=asia-northeast1
set APP=dk-dma
set TAG=gcr.io/%PROJECT_ID%/%APP%

### Cloud build
gcloud builds submit --secret id=creds,src=.streamlits/secrets.toml --project=%PROJECT_ID% --tag %TAG%
gcloud builds submit --project=%PROJECT_ID% --tag %TAG%

### Cloud Run deployment
gcloud run deploy %APP% --project %PROJECT_ID% --image %TAG% --platform managed --region %REGION% --allow-unauthenticated --port 8501

# Cloud Build and Deploy in Powershell

### Environment setup for powershell
$env:PROJECT_ID='dk-medical-solutions'
$env:REGION='asia-northeast1'
$env:APP='dk-dma'
$env:TAG="gcr.io/$env:PROJECT_ID/$env:APP"

### Cloud build
gcloud builds submit --project=$env:PROJECT_ID --tag $env:TAG

### Cloud Run deployment
gcloud run deploy $env:APP --project $env:PROJECT_ID --image $env:TAG --platform managed --region $env:REGION --allow-unauthenticated --port 8501

