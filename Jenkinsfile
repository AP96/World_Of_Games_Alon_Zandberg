pipeline {
    agent {
        label 'win11-amd64'
    }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        DOCKERHUB_REPO = "azprince/world_of_games"
        PORT = 5001
        CHROME_DRIVER_VERSION = '120.0.6099.62'
        SELENIUM_CONTAINER_NAME = "selenium-standalone-chrome"
    }

    stages {
        stage('Checkout') {
            steps {
               echo "Checking out the repository - managed by Jenkins"
            }
        }

        stage('Build') {
            steps {
                script {
                    try {
                        bat "docker build -t ${IMAGE_NAME}:${env.BUILD_ID} ."
                    } catch(Exception e) {
                        error "Build failed: ${e.message}"
                    }
                }
            }
        }

        stage('Run Application') {
            steps {
                script {
                    try {
                        bat(script: "docker rm -f ${CONTAINER_NAME} || exit 0", returnStatus: true)
                        bat "type nul > scores.txt"
                        bat "docker run -d --dns 8.8.8.8 --dns 8.8.4.4 --name ${CONTAINER_NAME} -p ${PORT}:5000 -v ${pwd()}\\scores.txt:/app/scores.txt ${IMAGE_NAME}:${env.BUILD_ID}"
                    } catch(Exception e) {
                        error "Run failed: ${e.message}"
                    }
                }
            }
        }

        stage('Run Selenium') {
            steps {
                script {
                    bat(script: "docker rm -f ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                    bat "docker run -d --dns 8.8.8.8 --dns 8.8.4.4 -p 4444:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
                }
            }
        }

        stage('Prepare Test Environment') {
            steps {
                script {
                    bat 'pip install selenium'
                    bat "pip install chromedriver-binary==${CHROME_DRIVER_VERSION}"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        bat 'python tests\\e2e.py'
                    } catch(Exception e) {
                        error "Tests failed: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                bat(script: "docker stop ${CONTAINER_NAME} || exit 0", returnStatus: true)
                bat(script: "docker rm ${CONTAINER_NAME} || exit 0", returnStatus: true)
                bat(script: "docker stop ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                bat(script: "docker rm ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                bat "del scores.txt"
            }
            cleanWs()
        }
        success {
            script {
                docker.withRegistry('https://registry.hub.docker.com', 'dockerHubCredentials') {
                    dockerImage.push("${env.BUILD_ID}")
                    dockerImage.push("latest")
                }
            }
        }
        failure {
            script {
                echo 'The build failed'
            }
        }
    }
}