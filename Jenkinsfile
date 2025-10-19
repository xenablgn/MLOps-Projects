pipeline{
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
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
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                '''
            }
        }

    }   
}