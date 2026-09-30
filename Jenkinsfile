pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aditya20266/ats-py"
        CREDENTIALS_ID = "dockerhub-credentials" // Ensure this credential ID exists in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                // Fixed quotes and format string for git log
                sh 'git log -1 --pretty=format:"%h %an %s"'
            }
        }

        stage('Prepare') {
            steps {
                script {
                    env.GIT_COMMIT_SHORT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    env.IMAGE_TAG = "${env.DOCKER_IMAGE}:manual-${env.GIT_COMMIT_SHORT}"
                    echo "Building ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint & Syntax Check') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m py_compile main.py
                '''
            }
        }

        stage('Test - Dependencies Import') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -c "import streamlit, PyPDF2, pdfplumber, nltk, matplotlib, docx; print('all imports OK')"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${env.IMAGE_TAG} ."
            }
        }

        stage('Docker Push') {
            steps {
                // Fixed the variable interpolation syntax for credentialsId
                withCredentials([usernamePassword(credentialsId: "${CREDENTIALS_ID}", 
                                                   usernameVariable: 'DOCKERHUB_USER', 
                                                   passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh '''
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin docker.io
                        docker push ${IMAGE_TAG}
                    '''
                }
            }
        }
    }

    post {
        success {
            cleanWs()
            echo "Pipeline completed successfully!"
        }
        failure {
            cleanWs()
            echo "Build failed!"
        }
    }
}
