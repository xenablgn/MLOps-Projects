pipeline {
    agent any

    // Prevent Jenkins from doing its automatic checkout at the start
    options {
        skipDefaultCheckout(true)
    }

    environment {
        VENV_DIR = "venv"
        GCP_PROJECT ="mlops-project1"
        GCLOUD_PATH= "/var/jenkins_home/gcloud/google-cloud-sdk/bin"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo 'Cleaning workspace...'
                deleteDir()
            }
        }

        stage('Clone Git Repository') {
            steps {
                echo 'Cloning Git repository from GitHub...'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/xenablgn/MLOps-Projects.git'
                    ]]
                )
                // Debug: verify contents after cloning
                sh 'echo "Repository structure:" && ls -R'
            }
        }

        stage('Set up Python Virtual Environment') {
            steps {
                echo 'Setting up Python Virtual Environment...'
                sh '''
                    cd Project_1_Hotel_Reservation_Prediction && \
                    python3 -m venv venv && \
                    . venv/bin/activate && \
                    pip install --upgrade pip && \
                    pip install -e .
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                echo 'Verifying environment setup...'
                sh '''
                    cd Project_1_Hotel_Reservation_Prediction && \
                    . venv/bin/activate && \
                    pip list
                '''
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps { 
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR...'
                        sh '''
                            export PATH=$GCLOUD_PATH:$PATH
                            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                            gcloud config set project $GCP_PROJECT
                            gcloud auth configure-docker --quiet

                            cd Project_1_Hotel_Reservation_Prediction
                            docker build -t gcr.io/$GCP_PROJECT/mlops-project1:latest .
                            docker push gcr.io/$GCP_PROJECT/mlops-project1:latest
                        '''
                    }

        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            
                        '''
                    }
                
                
                }

            }
        }

    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above for details.'
        }
    }
}
