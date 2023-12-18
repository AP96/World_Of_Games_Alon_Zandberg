pipeline {
    agent {
        label 'win11-amd64'
    }

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        DOCKERHUB_REPO = "azprince/world_of_games"
        PORT = 8777
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AP96/World_Of_Games_Alon_Zandberg.git'
            }
        }

        stage('Build') {
            steps {
                script {
                    try {
                        dockerImage = docker.build("${IMAGE_NAME}:${env.BUILD_ID}")
                    } catch(Exception e) {
                        error "Build failed: ${e.message}"
                    }
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    try {
                        bat "docker rm -f ${CONTAINER_NAME} || exit 0"
                        bat "type nul > scores.txt"
                        dockerImage.run("-d", "--name ${CONTAINER_NAME}", "-p ${PORT}:5000", "-v ${pwd()}\\scores.txt:/app/scores.txt")
                    } catch(Exception e) {
                        error "Run failed: ${e.message}"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        bat 'python e2e.py'
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
                bat "docker stop ${CONTAINER_NAME} || exit 0"
                bat "docker rm ${CONTAINER_NAME} || exit 0"
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
