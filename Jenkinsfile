pipeline{
    agent any
    stages {
        stage('Cloning Git Repository to Jenkins') {
            steps {
                echo 'Cloning Git Repository to Jenkins...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/xenablgn/MLOps-Projects.git']])
            }
        }

    }   
}