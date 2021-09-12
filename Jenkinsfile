
pipeline {
    agent any

        stages {
        stage('Test') {
            steps {
                sh 'python3 ./cmhub/manage.py test cmapp'
            }
        }
    
        }
}