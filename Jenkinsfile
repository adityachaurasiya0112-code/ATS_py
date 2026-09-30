pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME       = 'ats-py'
        IMAGE_NAME     = 'ats-py'
        DOCKERHUB_USER = 'ayushman21'
        REGISTRY_URL   = 'docker.io'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --pretty="%h %an %s"'
            }
        }

        stage('Prepare') {
            steps {
                script {
                    env.SHORT_SHA = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    env.BRANCH = env.BRANCH_NAME?.trim() ?: 'manual'

                    env.IMAGE_TAG = env.BRANCH == 'main'
                        ? 'latest'
                        : "${env.BRANCH}-${env.SHORT_SHA}"

                    env.FULL_IMAGE = "${env.REGISTRY_URL}/${env.DOCKERHUB_USER}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"

                    echo "Building ${env.FULL_IMAGE}"
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
                sh 'docker build -t "$FULL_IMAGE" .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    sh '''
                        echo "$DOCKERHUB_PASS" | docker login \
                            -u "$DOCKERHUB_USER" \
                            --password-stdin "$REGISTRY_URL"

                        docker push "$FULL_IMAGE"
                    '''
                }
            }
        }
    }

    post {
        success {
            script {
                sh 'docker rmi "$FULL_IMAGE" || true'
            }

            echo "Build successful: ${env.FULL_IMAGE}"
        }

        failure {
            echo "Build failed for commit ${env.SHORT_SHA}"
        }

        always {
            cleanWs()
        }
    }
}
