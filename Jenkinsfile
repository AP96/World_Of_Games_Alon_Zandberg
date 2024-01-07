pipeline {
    agent {
        label 'win11-amd64'
    }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        DOCKERHUB_REPO = "azprince/world_of_games"
        PORT = 5001
        SELENIUM_CONTAINER_NAME = "selenium-standalone-chrome"
        SELENIUM_PORT = 4444 // Port for Selenium server
        CHROME_DRIVER_VERSION = '120.0.6099.62' // Updated to match the first Jenkinsfile
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
                script {
                    try {
                        echo "Current Directory:"
                        bat "cd"  // Prints the current directory in Windows
                        echo "Directory Contents:"
                        bat "dir"  // Lists the contents of the current directory in Windows
                        echo "Building Docker Image:"
                        bat "docker build -t ${IMAGE_NAME}:${env.BUILD_ID} . --no-cache"
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
                        bat "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${env.BUILD_ID}"
                    } catch(Exception e) {
                        error "Run Application failed: ${e.message}"
                    }
                }
            }
        }

        stage('Run Selenium') {
            steps {
                script {
                    try {
                        bat(script: "docker rm -f ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                        bat "docker run -d -p ${SELENIUM_PORT}:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
                    } catch(Exception e) {
                        error "Run Selenium failed: ${e.message}"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Health check for Flask app
                    def appHealthy = false
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${PORT}/health", returnStatus: true) == 0) {
                            appHealthy = true
                            break
                        }
                        echo "Waiting for Flask app to become healthy..."
                        sleep 5 // Wait for 5 seconds before the next try
                    }
                    if (!appHealthy) {
                        error "Flask app did not start correctly"
                    }

                    // Health check for Selenium server
                    def seleniumHealthy = false
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${SELENIUM_PORT}", returnStatus: true) == 0) {
                            seleniumHealthy = true
                            break
                        }
                        echo "Waiting for Selenium server to become healthy..."
                        sleep 5 // Wait for 5 seconds before the next try
                    }
                    if (!seleniumHealthy) {
                        error "Selenium server did not start correctly"
                    }

                    // Run tests
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
                echo "Cleaning up the workspace"
                cleanWs() // Cleans the workspace after the build is completed
            }
        }
        success {
            script {
                // Updated to use the WORKSPACE environment variable
                bat "docker build -t ${DOCKERHUB_REPO}:${env.BUILD_ID} ${WORKSPACE} --no-cache"
                docker.withRegistry('https://registry.hub.docker.com', 'dockerHubCredentials') {
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
