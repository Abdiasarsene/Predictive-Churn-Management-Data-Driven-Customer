pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.yml"
        MLFLOW_TRACKING_URI = "http://mlflow:5000"
    }

    options {
        skipStagesAfterUnstable()
        timestamps()
    }
    
    parameters {
        booleanParam(name: "CLEAN_BUILD", defaultValue:false, description: "Clean up before build")
    }

    stages {
        stage("🔃 Checkout Code") {
            steps {
                checkout scm
            }
        }

        stage("🧹 CLean") {
            when{
                expression {
                    retunr params.CLEAN_BUILD == true
                }
            }
            steps{
                sh "task clean"
            }
        }

        stage("⚙️ Docker Build") {
            steps {
                sh "task build"
            }
        }

        stage("🚀 Start Services") {
            steps {
                sh "task up"
                sleep 15
            }
        }

        stage("🚇 Unit Testing") {
            when {
                anyOf {
                    expression{fileExists("test/")}
                    expression{fileExists("app/test/")}
                }
            }
            steps{
                sh "pytest -v"
            }
        }

        stage("🫸 Stop Services"){
            steps{
                sh "task down"
            }
        }
    }

    post {
        always{
            echo "🚇 Pipeline finished"
        }
        success{
            echo "✅ Pipeline ended up sucessfully"
            bat '''
            powershell -c "(New-Object Media.SoundPlayer \\"C:\\Windows\\Media\\Windows Notify Calendar.wav\\").PlaySync();"
            '''
        }
        failure{
            echo "❌ Pipeline failed ! Check logs"
            bat '''
            powershell -c "(New-Object Media.SoundPlayer \\"C:\\Windows\\Media\\Windows Critical Stop.wav\\").PlaySync();"
            '''
        }
    }
}