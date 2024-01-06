pipeline {
    agent {
        label 'win11-amd64'
    }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        PORT = 5001
        SELENIUM_CONTAINER_NAME = "selenium-standalone-chrome"
        CHROME_DRIVER_VERSION = '118.0'
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
                bat(script: "docker stop ${CONTAINER_NAME} || exit 0", returnStatus: true)
                bat(script: "docker rm -f ${CONTAINER_NAME} || exit 0", returnStatus: true)
                bat "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${env.BUILD_ID}"
            }
        }

        stage('Run Selenium') {
            steps {
                bat(script: "docker stop ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                bat(script: "docker rm -f ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                bat "docker run -d -p ${SELENIUM_PORT}:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
            }
        }

        stage('Test') {
            steps {
                script {
                    def appHealthy = false
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${PORT}/health", returnStatus: true) == 0) {
                            appHealthy = true
                            break
                        }
                        echo "Waiting for Flask app to become healthy..."
                        sleep 5
                    }
                    if (!appHealthy) {
                        error "Flask app did not start correctly"
                    }

                    def seleniumHealthy = false
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${SELENIUM_PORT}", returnStatus: true) == 0) {
                            seleniumHealthy = true
                            break
                        }
                        echo "Waiting for Selenium server to become healthy..."
                        sleep 5
                    }
                    if (!seleniumHealthy) {
                        error "Selenium server did not start correctly"
                    }

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
            bat(script: "docker stop ${CONTAINER_NAME} || exit 0", returnStatus: true)
            bat(script: "docker rm ${CONTAINER_NAME} || exit 0", returnStatus: true)
            bat(script: "docker stop ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
            bat(script: "docker rm ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
            cleanWs()
        }
        failure {
            echo 'The build failed'
        }
    }
}
