pipeline {
    agent { label 'win11-amd64' }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        DOCKERHUB_REPO = "azprince/world_of_games"
        PORT = 5001
        SELENIUM_CONTAINER_NAME = "selenium-standalone-chrome"
        SELENIUM_PORT = 4444
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out the repository"
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    try {
                        bat "docker build -t ${IMAGE_NAME}:${env.BUILD_ID} . --no-cache"
                    } catch (Exception e) {
                        error "Build failed: ${e.message}"
                    }
                }
            }
        }

        stage('Run Application') {
            steps {
                script {
                    bat "docker rm -f ${CONTAINER_NAME} || exit 0"
                    bat "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${env.BUILD_ID}"
                }
            }
        }

        stage('Run Selenium') {
            steps {
                script {
                    bat "docker rm -f ${SELENIUM_CONTAINER_NAME} || exit 0"
                    bat "docker run -d -p ${SELENIUM_PORT}:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    def appHealthy = false
                    def seleniumHealthy = false

                    (1..10).each {
                        if (!appHealthy && bat(script: "curl -f http://localhost:${PORT}/health", returnStatus: true) == 0) {
                            appHealthy = true
                        }
                        if (!seleniumHealthy && bat(script: "curl -f http://localhost:${SELENIUM_PORT}", returnStatus: true) == 0) {
                            seleniumHealthy = true
                        }
                        if (appHealthy && seleniumHealthy) break
                        sleep 5
                    }
                    if (!appHealthy) error "Flask app did not start correctly"
                    if (!seleniumHealthy) error "Selenium server did not start correctly"

                    try {
                        bat 'python tests\\e2e.py'
                    } catch (Exception e) {
                        error "Tests failed: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        always {
            bat "docker stop ${CONTAINER_NAME} || exit 0"
            bat "docker rm ${CONTAINER_NAME} || exit 0"
            bat "docker stop ${SELENIUM_CONTAINER_NAME} || exit 0"
            bat "docker rm ${SELENIUM_CONTAINER_NAME} || exit 0"
            echo "Post-build actions completed"
        }
        success {
            script {
                docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                    def dockerImage = docker.build("${DOCKERHUB_REPO}:${env.BUILD_ID}")
                    dockerImage.push("${env.BUILD_ID}")
                    dockerImage.push("latest")
                }
            }
        }
        failure {
            echo 'The build failed'
        }
    }
}
