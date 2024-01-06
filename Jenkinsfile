pipeline {
    agent {
        label 'win11-amd64'
    }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        PORT = 5001
        SELENIUM_CONTAINER_NAME = "selenium-standalone-chrome"
        SELENIUM_PORT = 4444 // Port for Selenium server
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out the repository - managed by Jenkins"
                checkout scm
            }
        }

        stage('Build') {
            steps {
                bat "docker build -t ${IMAGE_NAME}:${env.BUILD_ID} ."
            }
        }

        stage('Run Application') {
            steps {
                bat "docker stop ${CONTAINER_NAME} || true"
                bat "docker rm -f ${CONTAINER_NAME} || true"
                bat "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${env.BUILD_ID}"
            }
        }

        stage('Run Selenium') {
            steps {
                bat "docker stop ${SELENIUM_CONTAINER_NAME} || true"
                bat "docker rm -f ${SELENIUM_CONTAINER_NAME} || true"
                bat "docker run -d -p ${SELENIUM_PORT}:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
            }
        }

        stage('Test') {
            steps {
                script {
                    checkServiceHealth("Flask app", "${PORT}")
                    checkServiceHealth("Selenium server", "${SELENIUM_PORT}")
                    bat 'python tests\\e2e.py'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'USER', passwordVariable: 'PASSWORD')]) {
                        bat "docker login -u $USER -p $PASSWORD registry.docker.io"
                        bat "docker tag ${IMAGE_NAME}:${env.BUILD_ID} ${USER}/world_of_games:${env.BUILD_ID}"
                        bat "docker push ${USER}/world_of_games:${env.BUILD_ID}"
                    }
                }
            }
        }
    }

    post {
        always {
            bat "docker stop ${CONTAINER_NAME} || true"
            bat "docker rm ${CONTAINER_NAME} || true"
            bat "docker stop ${SELENIUM_CONTAINER_NAME} || true"
            bat "docker rm ${SELENIUM_CONTAINER_NAME} || true"
            cleanWs()
        }
        failure {
            echo 'The build failed'
        }
    }
}

def checkServiceHealth(serviceName, port) {
    def healthy = false
    for (int i = 0; i < 10; i++) {
        if (bat(script: "curl -f http://localhost:${port}/health", returnStatus: true) == 0) {
            healthy = true
            break
        }
        echo "Waiting for ${serviceName} to become healthy..."
        sleep 5
    }
    if (!healthy) {
        error "${serviceName} did not start correctly"
    }
}
