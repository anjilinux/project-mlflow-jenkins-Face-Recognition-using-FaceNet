pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PYTHON = "python3"
        VENV_DIR = "venv"
        APP_PORT = "8005"

        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "Face-Recognition-FaceNet"

        IMAGE_NAME = "face-recognition"
        IMAGE_TAG = "latest"
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage("Checkout Code") {
            steps {
                git(
                    branch: 'master',
                    url: 'https://github.com/anjilinux/project-mlflow-jenkins-Face-Recognition-using-FaceNet.git'
                )
            }
        }

        stage("Setup Virtual Environment") {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage("Data Validation") {
            steps {
                sh '''
                    echo "🔍 Validating dataset structure..."
                    test -d data/raw || (echo "❌ data/raw missing" && exit 1)
                    if [ "$(ls -A data/raw)" = "" ]; then
                        echo "❌ No class folders in data/raw"
                        exit 1
                    fi
                    if ! ls data/raw/*/*.jpg >/dev/null 2>&1; then
                        echo "❌ No JPG images found"
                        exit 1
                    fi
                    echo "✅ Data validation passed"
                '''
            }
        }

        stage("Model Training (MLflow)") {
            steps {
                sh '''
                    export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                    export MLFLOW_EXPERIMENT_NAME=$MLFLOW_EXPERIMENT_NAME
                    venv/bin/python train.py
                '''
            }
        }

        stage("Model Evaluation") {
            steps {
                sh '''
                    venv/bin/python evaluate.py
                '''
            }
        }

        stage("Run PyTests") {
            steps {
                sh '''
                    venv/bin/pytest test_preprocessing.py --disable-warnings
                    venv/bin/pytest test_model.py --disable-warnings
                '''
            }
        }

        stage("Model Artifact Check") {
            steps {
                sh '''
                    test -f models/classifier.pkl || (echo "❌ Model not found" && exit 1)
                '''
            }
        }

        stage("FastAPI Smoke Test (Local)") {
            steps {
                sh '''#!/bin/bash
                set -e
                . venv/bin/activate
                export PYTHONPATH=$WORKSPACE

                echo "🚀 Starting FastAPI..."
                uvicorn main:app --host 0.0.0.0 --port $APP_PORT > uvicorn.log 2>&1 &

                echo "⏳ Waiting for FastAPI to become healthy..."
                for i in {1..15}; do
                    if curl -s -f http://localhost:$APP_PORT/health > /dev/null; then
                        echo "✅ FastAPI healthy"
                        pkill -f "uvicorn main:app" || true
                        exit 0
                    fi
                    echo "⏱️ Attempt $i: not ready yet..."
                    sleep 20
                done

                echo "❌ FastAPI failed to start"
                cat uvicorn.log
                exit 1
                '''
            }
        }

        stage("Docker Build") {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage("Docker Smoke Test") {
            steps {
                sh '''#!/bin/bash
                set -e
                IMAGE_NAME="face-recognition"
                CONTAINER_NAME="face_recog_test"
                docker rm -f $CONTAINER_NAME || true

                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo "🌐 Using port $HOST_PORT"

                docker run -d -p $HOST_PORT:$APP_PORT --name $CONTAINER_NAME $IMAGE_NAME:$IMAGE_TAG

                echo "⏳ Waiting for FastAPI..."
                for i in {1..30}; do
                    if curl -s http://localhost:$HOST_PORT/health | grep -q ok; then
                        echo "✅ Docker FastAPI is healthy"
                        docker rm -f $CONTAINER_NAME
                        exit 0
                    fi
                    sleep 32
                done

                echo "❌ FastAPI failed to start"
                docker logs $CONTAINER_NAME
                docker rm -f $CONTAINER_NAME
                exit 1
                '''
            }
        }

        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '''
                    models/classifier.pkl,
                    mlruns/**,
                    uvicorn.log
                ''', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Face Recognition MLOps Pipeline Completed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Jenkins Logs"
        }
    }
}
