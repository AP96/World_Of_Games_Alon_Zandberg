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
                    // Initialize health check flags
                    def appHealthy = false
                    def seleniumHealthy = false

                    // Check Flask app health
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${PORT}/health", returnStatus: true) == 0) {
                            appHealthy = true
                            break // Exit loop if app is healthy
                        }
                        echo "Waiting for Flask app to become healthy..."
                        sleep(5) // Wait for 5 seconds
                    }
                    if (!appHealthy) {
                        error "Flask app did not start correctly"
                    }

                    // Check Selenium server health
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${SELENIUM_PORT}", returnStatus: true) == 0) {
                            seleniumHealthy = true
                            break // Exit loop if Selenium is healthy
                        }
                        echo "Waiting for Selenium server to become healthy..."
                        sleep(5) // Wait for 5 seconds
                    }
                    if (!seleniumHealthy) {
                        error "Selenium server did not start correctly"
                    }

                    // Run tests only if both are healthy
                    if (appHealthy && seleniumHealthy) {
                        bat 'python tests\\e2e.py'
                    } else {
                        error "One or more services are not healthy."
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
