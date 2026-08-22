pipeline {
    agent any

    environment {
        // Change these to match your own Docker Hub account / repo name
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')   // Jenkins credential ID (username/password)
        DOCKER_IMAGE          = "yourdockerhubusername/simple-devops-pipeline"
        IMAGE_TAG             = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Clone Github Repository') {
            steps {
                echo 'Cloning source code from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/vamshii9989/simple-devops-pipeline.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r app/requirements.txt
                    pip install -r tests/requirements-test.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests with pytest...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Compile') {
            steps {
                echo 'Byte-compiling Python source to verify it is syntactically valid...'
                sh '''
                    . venv/bin/activate
                    python -m py_compile app/app.py
                '''
            }
        }

        stage('Docker image Build') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
            }
        }

        stage('Docker image Tag') {
            steps {
                echo 'Tagging Docker image as latest...'
                sh "docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging in to Docker Hub...'
                sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
            }
        }

        stage('Docker Image Push') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Clean Work Space') {
            steps {
                echo 'Cleaning up workspace and dangling Docker resources...'
                sh 'docker logout || true'
                sh 'docker image prune -f || true'
                cleanWs()
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
    }
}
