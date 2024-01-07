pipeline {
    agent { label 'win11-amd64' }

    environment {
        IMAGE_NAME = 'worldofgames'
        CONTAINER_NAME = 'wog_web_app'
        DOCKERHUB_REPO = 'azprince/world_of_games'
        PORT = 5001
        SELENIUM_CONTAINER_NAME = 'selenium-standalone-chrome'
        SELENIUM_PORT = 4444
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat 'echo Repository checked out in workspace'
            }
        }

        stage('Build Docker Image') {
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

        stage('Run Application and Selenium') {
            steps {
                script {
                    containerOperations('start')
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    runHealthChecks()
                    runTests()
                }
            }
        }
    }

    post {
        always {
            script {
                containerOperations('stop')
                cleanWorkspace()
            }
        }
        success {
            script {
                dockerPush()
            }
        }
        failure {
            echo 'The build failed'
        }
    }
}

def containerOperations(operation) {
    if (operation == 'start') {
        bat "docker rm -f ${CONTAINER_NAME} || exit 0"
        bat "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${env.BUILD_ID}"
        bat "docker rm -f ${SELENIUM_CONTAINER_NAME} || exit 0"
        bat "docker run -d -p ${SELENIUM_PORT}:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
    } else if (operation == 'stop') {
        bat "docker stop ${CONTAINER_NAME} || exit 0"
        bat "docker rm ${CONTAINER_NAME} || exit 0"
        bat "docker stop ${SELENIUM_CONTAINER_NAME} || exit 0"
        bat "docker rm ${SELENIUM_CONTAINER_NAME} || exit 0"
    }
}

def runHealthChecks() {
    checkHealth('${PORT}', 'Flask app')
    checkHealth('${SELENIUM_PORT}', 'Selenium server')
}

def checkHealth(port, service) {
    def healthy = false
    for (int i = 0; i < 10; i++) {
        if (bat(script: "curl -f http://localhost:${port}/health", returnStatus: true) == 0) {
            healthy = true
            break
        }
        echo "Waiting for ${service} to become healthy..."
        sleep 5
    }
    if (!healthy) error "${service} did not start correctly"
}

def runTests() {
    try {
        bat 'python tests\\e2e.py'
    } catch (Exception e) {
        error "Tests failed: ${e.message}"
    }
}

def dockerPush() {
    bat "docker build -t ${DOCKERHUB_REPO}:${env.BUILD_ID} -f ${WORKSPACE}/Dockerfile ${WORKSPACE} --no-cache"
    docker.withRegistry('https://registry.hub.docker.com', 'dockerHubCredentials') {
        def dockerImage = docker.build("${DOCKERHUB_REPO}:${env.BUILD_ID}")
        dockerImage.push("${env.BUILD_ID}")
        dockerImage.push("latest")
    }
}

def cleanWorkspace() {
    echo "Cleaning up the workspace"
    cleanWs()
}
