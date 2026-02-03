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

        // CI-safe MLflow (no external dependency)
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "Face-Recognition-FaceNet"

        IMAGE_NAME = "face-recognition"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages{



        stage("Checkout Code") {
            
            steps {
                git(
                    branch: 'master',
                    url: 'https://github.com/anjilinux/project-mlflow-jenkins-Face-Recognition-using-FaceNet.git'
                )
            }
        }

        /* ================= SETUP ENV ================= */
        stage("Setup Virtual Environment") {
            steps {
                sh """
                    ${PYTHON} -m venv ${VENV_DIR}
                 
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                """
            }
        }

        /* ================= DATA VALIDATION ================= */
/* ================= DATA VALIDATION ================= */
stage("Data Validation") {
    steps {
        sh '''
            echo "🔍 Validating dataset structure..."

            # Check raw directory
            test -d data/raw || (echo "❌ data/raw directory missing" && exit 1)

            # Check at least one class folder exists
            if [ "$(ls -A data/raw)" = "" ]; then
                echo "❌ No class folders found in data/raw"
                exit 1
            fi

            # Check JPG images inside class folders
            if ! ls data/raw/*/*.jpg >/dev/null 2>&1; then
                echo "❌ No JPG images found inside class folders"
                exit 1
            fi

            echo "✅ Data validation passed"
        '''
    }
}


        /* ================= FEATURE ENGINEERING ================= */
        stage("Feature Engineering") {
            steps {
                sh """
                    ${VENV_DIR}/bin/python feature_engineering.py
                """
            }
        }

        /* ================= PREPROCESSING ================= */
        stage("Data Preprocessing") {
            steps {
                sh """
                    ${VENV_DIR}/bin/python preprocessing.py
                """
            }
        }

        /* ================= MODEL TRAINING ================= */
        stage("Model Training (MLflow)") {
            steps {
                sh """
                    export MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
                    export MLFLOW_EXPERIMENT_NAME=${MLFLOW_EXPERIMENT_NAME}
                    ${VENV_DIR}/bin/python train.py
                """
            }
        }

        /* ================= MODEL EVALUATION ================= */
        stage("Model Evaluation") {
            steps {
                sh """
                    ${VENV_DIR}/bin/python evaluate.py
                """
            }
        }

        /* ================= UNIT TESTS ================= */
        stage("Run PyTests") {
            steps {
                sh """
                    export PYTHONPATH=${WORKSPACE}
                    ${VENV_DIR}/bin/pytest test_preprocessing.py --disable-warnings
                    ${VENV_DIR}/bin/pytest  test_model.py --disable-warnings
                """
            }
        }

        /* ================= MODEL CHECK ================= */
        stage("Model Artifact Check") {
            steps {
                sh """
                    test -f models/classifier.pkl || (echo "❌ Model not found" && exit 1)
                """
            }
        }

        /* ================= FASTAPI LOCAL SMOKE TEST ================= */
        stage("FastAPI Smoke Test (Local)") {
            steps {
                sh """#!/bin/bash
                    set -e

                    export PYTHONPATH=${WORKSPACE}
                    ${VENV_DIR}/bin/uvicorn main:app \
                        --host 0.0.0.0 \
                        --port ${APP_PORT} \
                        > uvicorn.log 2>&1 &

                    sleep 8

                    curl -f http://localhost:${APP_PORT}/health
                    pkill -f uvicorn
                """
            }
        }

        /* ================= DOCKER BUILD ================= */
        stage("Docker Build") {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                """
            }
        }

        /* ================= DOCKER SMOKE TEST ================= */
        stage("Docker Smoke Test") {
            steps {
                sh """#!/bin/bash
                    set -e

                    docker rm -f face_recognition_test || true

                    docker run -d \
                        -p 8888:${APP_PORT} \
                        --name face_recognition_test \
                        ${IMAGE_NAME}:latest

                    sleep 10
                    curl -f http://localhost:8888/health
                    docker rm -f face_recognition_test
                """
            }
        }

        /* ================= DEPLOY (MAIN ONLY) ================= */
        stage("Deploy (Main Branch)") {
            when {
                branch "main"
            }
            steps {
                sh """
                    docker rm -f face-recognition || true
                    docker run -d \
                        -p ${APP_PORT}:${APP_PORT} \
                        --name face-recognition \
                        ${IMAGE_NAME}:latest
                """
            }
        }

        /* ================= ARCHIVE ARTIFACTS ================= */
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
