pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Train Model') {
            steps {
                sh 'venv/bin/python train.py'
            }
        }

        stage('Test') {
            steps {
                sh 'venv/bin/pytest test_model.py '
                sh 'venv/bin/pytest test_preprocessing.py
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t facenet-api .'
            }
        }
    }
}
