pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "python-scalable-app"
        DOCKER_TAG = "latest"
        DOCKERHUB_USER = "krishnan14"
        DOCKERHUB_CREDENTIALS = credentials('Docker_Cred') // Jenkins credential ID
        SERVER_USER = "ubuntu"
        SERVER_IP = "54.180.124.46"
        SSH_KEY = credentials('SSH_ID') // Jenkins credential ID
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/krishnan1412/PythonScalable.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Tag the image for Docker Hub
                    sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKERHUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}"

                    // Login and push
                    sh """
                    echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                    docker push ${DOCKERHUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                script {
                    // Pull and run the image on EC2
                    sh """
                    ssh -i ${SSH_KEY} ${SERVER_USER}@${SERVER_IP} '
                        docker pull ${DOCKERHUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG} &&
                        docker stop python-app || true &&
                        docker rm python-app || true &&
                        docker run -d --name python-app -p 80:5000 ${DOCKERHUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Image pushed to Docker Hub and deployed to EC2!'
        }
        failure {
            echo '❌ Something went wrong during CI/CD.'
        }
    }
}
