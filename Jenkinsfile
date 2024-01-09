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
        SELENIUM_PORT = 4444
        CHROME_DRIVER_VERSION = '120.0.6099.62'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out the repository."
                checkout scm
                bat "dir"  // Display checked out files
            }
        }

        stage('Build Image') {
            steps {
                script {
                    buildDockerImage()
                }
            }
        }

        stage('Deploy Application and Selenium') {
            steps {
                script {
                    deployDockerContainer(CONTAINER_NAME, "${PORT}:5000")
                    deployDockerContainer(SELENIUM_CONTAINER_NAME, "${SELENIUM_PORT}:4444", "selenium/standalone-chrome:latest")
                }
            }
        }

        stage('Health Checks and Tests') {
            steps {
                script {
                    performHealthChecks(PORT, "Flask app")
                    performHealthChecks(SELENIUM_PORT, "Selenium server")
                    runTests()
                }
            }
        }
    }

    post {
        always {
            cleanUpDockerContainers()
            echo "Post-build cleanup completed."
        }
        success {
            pushToDockerHub()
        }
        failure {
            echo 'Build failed.'
        }
    }
}

// Helper methods
def buildDockerImage() {
    try {
        echo "Building Docker Image."
        bat "docker build -t ${IMAGE_NAME}:${env.BUILD_ID} . --no-cache"
    } catch(Exception e) {
        error "Build failed: ${e.message}"
    }
}

def deployDockerContainer(name, portMapping, image = "${IMAGE_NAME}:${env.BUILD_ID}") {
    try {
        bat(script: "docker rm -f ${name} || exit 0", returnStatus: true)
        bat "docker run -d --name ${name} -p ${portMapping} ${image}"
    } catch(Exception e) {
        error "Deployment of ${name} failed: ${e.message}"
    }
}

def performHealthChecks(port, serviceName) {
    def healthy = false
    for (int i = 0; i < 10; i++) {
        if (bat(script: "curl -f http://localhost:${port}", returnStatus: true) == 0) {
            healthy = true
            break
        }
        echo "Waiting for ${serviceName} to become healthy."
        sleep 5
    }
    if (!healthy) {
        error "${serviceName} did not start correctly."
    }
}

def runTests() {
    try {
        bat 'python tests\\e2e.py'
    } catch(Exception e) {
        error "Tests failed: ${e.message}"
    }
}

def cleanUpDockerContainers() {
    bat(script: "docker stop ${CONTAINER_NAME} || exit 0", returnStatus: true)
    bat(script: "docker rm ${CONTAINER_NAME} || exit 0", returnStatus: true)
    bat(script: "docker stop ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
    bat(script: "docker rm ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
}

def pushToDockerHub() {
    echo "Pushing image to Docker Hub."
    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
        def dockerImage = docker.build("${DOCKERHUB_REPO}:${env.BUILD_ID}")
        dockerImage.push("${env.BUILD_ID}")
        dockerImage.push("latest")
    }
}
