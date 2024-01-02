pipeline {
    agent {
        label 'win11-amd64'
    }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        PORT = 5001
        SELENIUM_CONTAINER_NAME = "selenium-standalone-chrome"
        CHROME_DRIVER_VERSION = '120.0.6099.62' // Ensure this is set as per your requirements
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
                bat(script: "docker rm -f ${CONTAINER_NAME} || exit 0", returnStatus: true)
                bat "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:5000 ${IMAGE_NAME}:${env.BUILD_ID}"
            }
        }

        stage('Run Selenium') {
            steps {
                bat(script: "docker rm -f ${SELENIUM_CONTAINER_NAME} || exit 0", returnStatus: true)
                bat "docker run -d -p 4444:4444 --name ${SELENIUM_CONTAINER_NAME} selenium/standalone-chrome:latest"
            }
        }

        stage('Prepare Test Environment') {
            steps {
                bat 'pip install selenium'
                bat "pip install chromedriver-binary==${CHROME_DRIVER_VERSION}"
            }
        }

        stage('Test') {
            steps {
                script {
                    // Health check for Flask app
                    def healthy = false
                    for (int i = 0; i < 10; i++) {
                        if (bat(script: "curl -f http://localhost:${PORT}/health", returnStatus: true) == 0) {
                            healthy = true
                            break
                        }
                        echo "Waiting for Flask app to become healthy..."
                        sleep 5 // Wait for 5 seconds before the next try
                    }
                    if (!healthy) {
                        error "Flask app did not start correctly"
                    }

                    bat 'python tests\\e2e.py'
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
