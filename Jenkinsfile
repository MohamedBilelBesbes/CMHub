pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhubtoken')
    }
    stages {
        stage('Dockerization') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker-compose build'
                sh 'docker push mohamedbilelbesbes/cmhubproject:latest'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 ./cmhub/manage.py test cmapp'
            }
        }
    }
}
