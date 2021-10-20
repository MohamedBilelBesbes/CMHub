pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhubtoken')
    }
    stages {
        stage('Test') {
            steps {
                sh 'python3 ./cmhub/manage.py test cmapp'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script{
                       def scannerHome = tool 'sonarqube'
                        withSonarQubeEnv('sonarqube') {
                            sh "${scannerHome}/bin/sonar-scanner"
                        }
                }
            }
        }
        stage('Dockerization') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker-compose build'
                sh 'docker tag cmhubproject_develop_web:latest mohamedbilelbesbes/cmhubpr'
                sh 'docker push mohamedbilelbesbes/cmhubpr'
            }
        }
    }
}
