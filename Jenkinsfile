pipeline {
  agent any

    stages{

      stage('Test'){
        steps{
          sleep 5
          sh 'curl http://localhost:5200'
          sh 'curl http://localhost:5200/start'
        }
      }

      stage('Build') {
        steps {
          sh 'docker build -t whalerider02/hangman-app-mp:latest --platform linux/amd64,linux/arm64 .'
        }
      }

      stage('Push') {
        steps {
          sh 'docker push whalerider02/hangman-app-mp:latest'
        }
      }
  }
}