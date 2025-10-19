pipeline {
    agent any

    // Prevent Jenkins from doing its automatic checkout at the start
    options {
        skipDefaultCheckout(true)
    }

    environment {
        VENV_DIR = "venv"
        GCP_PROJECT = "plenary-edition-475508-v1"
        GCLOUD_PATH = "/var/jenkins_home/gcloud/google-cloud-sdk/bin"
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
                sh 'echo "Repository structure:" && ls -R'
            }
        }

        stage('Set up Python Virtual Environment') {
            steps {
                echo 'Setting up Python Virtual Environment...'
                sh '''
                    cd Project_1_Hotel_Reservation_Prediction
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                '''
            }
        }

        stage('Verify Installation') {
            steps {
                echo 'Verifying environment setup...'
                sh '''
                    cd Project_1_Hotel_Reservation_Prediction
                    . $VENV_DIR/bin/activate
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

                            # Authenticate service account
                            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

                            # Set project
                            gcloud config set project $GCP_PROJECT

                            # Configure Docker to authenticate with GCR
                            gcloud auth configure-docker gcr.io --quiet

                            cd Project_1_Hotel_Reservation_Prediction

                            # Build Docker image
                            docker build --platform linux/amd64 -t gcr.io/$GCP_PROJECT/mlops-project1:latest .

                            # Push Docker image
                            docker push gcr.io/$GCP_PROJECT/mlops-project1:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Google Cloud Run...'
                        sh '''
                            export PATH=$GCLOUD_PATH:$PATH

                            # Authenticate service account
                            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

                            # Set project
                            gcloud config set project $GCP_PROJECT

                            # Deploy service
                            gcloud run deploy mlops-project1 \
                                --image=gcr.io/$GCP_PROJECT/mlops-project1:latest \
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
