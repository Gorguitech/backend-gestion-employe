pipeline {

    // agent any

    agent {
        label 'MI_AG'  
       
    }
    

    environment {
        DOCKERHUB_USER = "abdoulaye940"
        IMAGE_NAME     = "backend-employe"
        IMAGE_TAG      = "1.${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                //windows
                //bat "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                //linux
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    // windows 
                    /*bat """
                        docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                        docker push %DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%
                    """
                    */
                    //linux
                    sh """
                        echo "$DOCKER_PASS" 
                    
                        docker login -u %DOCKER_USER% --password-stdin
                        docker push %DOCKERHUB_USER%/%IMAGE_NAME%:%IMAGE_TAG%
                    """
                }
            }
        }
    // stage docker compose
        stage('Deploy with Docker Compose') {
            steps {
                //windows os
                //bat "docker-compose up -d --build"
                //linux
                sh "docker-compose up -d --build"
    
            }
        }
    }

    post {
        success {
            echo "Déploiement Backend Gestion employé réussiiiii !"
        }
        failure {
            echo "Le déploiement a échoué, vérifiez les logs Jenkinssss."
        }
    }
}