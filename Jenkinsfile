pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Cloning Git Repository to Jenkins') {
            steps {
                echo 'Cloning Git Repository to Jenkins...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/xenablgn/MLOps-Projects.git']])
            }
        }

        stage('Setting up Python Virtual Environment') {
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
    }
}