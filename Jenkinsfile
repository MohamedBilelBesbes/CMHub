pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhubtoken')
    }
    stages {
        stage('Dockerization') {
            steps {
                sh 'docker-compose build -t mohamedbilelbesbes/cmhubproject:latest .'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker push mohamedbilelbesbes/cmhub_web:latest'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 ./cmhub/manage.py test cmapp'
            }
        }
    }
}
