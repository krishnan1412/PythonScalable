pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "python-scalable-app"
        DOCKER_TAG = "latest"
        DOCKERHUB_USER = "krishnan14"
        SERVER_USER = "ubuntu"
        SERVER_IP = "54.180.124.46"
    }

    stages {
        stage("login to ssh and clone the git repo") {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'SSH_ID', keyFileVariable: 'EC2_KEY')]) {
                sh """
                ssh -o StrictHostKeyChecking=no -i ${EC2_KEY} ${SERVER_USER}@${SERVER_IP}'
                rm -rf PythonScalable &&
                git clone https://github.com/krishnan1412/PythonScalable.git &&
                cd PythonScalable
                '
                """
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'SSH_ID', keyFileVariable: 'EC2_KEY')]) {
                script {
                    sh """
                    ssh -o StrictHostKeyChecking=no -i ${EC2_KEY} ${SERVER_USER}@${SERVER_IP}'
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    '
                    """
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'Docker_Cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKERHUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                        sh """
                        echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin
                        docker push ${DOCKERHUB_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'SSH_ID', keyFileVariable: 'EC2_KEY')]) {
                    script {
                        sh """
                        ssh -o StrictHostKeyChecking=no -i ${EC2_KEY} ${SERVER_USER}@${SERVER_IP} '
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
