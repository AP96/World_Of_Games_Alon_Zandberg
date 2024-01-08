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