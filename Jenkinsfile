
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
           stage('Build') {
               steps {
                   sh 'docker-compose build -t mohamedbilelbesbes/cmhubproject:latest'
               }
           }
           stage('Login') {
               steps {
                   sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stding''
               }
           }
           stage('Push') {
               steps {
                   sh 'docker push mohamedbilelbesbes/cmhubproject:latest'
               }
           }
        }
        post {
            always {
                sh 'docker logout'
            }
        }
}
