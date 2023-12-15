pipeline {
    agent any

    environment {
        IMAGE_NAME = "worldofgames"
        CONTAINER_NAME = "wog_web_app"
        DOCKERHUB_REPO = "azprince/world_of_games"
        PORT = 8777
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AP96/World_Of_Games_Alon_Zandberg.git'
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
                        sh "touch Scores.txt"
                        container = dockerImage.run("-d --name ${CONTAINER_NAME} -p ${PORT}:5000 -v ${pwd()}/Scores.txt:/app/Scores.txt ${IMAGE_NAME}:${env.BUILD_ID}")
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
                        sh 'python e2e.py'
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
                // Clean up container and temporary files
                sh "docker stop ${CONTAINER_NAME}"
                sh "docker rm ${CONTAINER_NAME}"
                sh "rm -f Scores.txt"
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
                // Implement notification logic here
                echo 'The build failed'
            }
        }
    }
}
