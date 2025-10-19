pipeline {
    agent any

    // Prevent Jenkins from doing its automatic checkout at the start
    options {
        skipDefaultCheckout(true)
    }

    environment {
        VENV_DIR = "venv"
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
