
pipeline {

    agent {
        label 'MI_AG'
    }

    environment {
        DOCKERHUB_USER = 'abdoulaye940'
        IMAGE_NAME     = 'backend-employe'
        IMAGE_TAG      = "1.${BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = 'backend-gestion-employe'
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker Environment') {
            steps {
                sh '''
                    set -eu

                    docker --version
                    docker compose version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu

                    docker build \
                        -t "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}" .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        set -eu
                        set +x

                        printf '%s' "$DOCKER_PASS" | docker login \
                            --username "$DOCKER_USER" \
                            --password-stdin

                        docker push \
                            "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"

                        echo "Image publiée avec succès : ${IMAGE_TAG}"

                        docker logout
                    '''
                }
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh '''
                    set -eu

                    docker compose \
                        -p "${COMPOSE_PROJECT_NAME}" config -q

                    echo "Configuration Docker Compose valide."
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                    set -eu

                    echo "Déploiement de l'image ${IMAGE_TAG}"

                    docker compose \
                        -p "${COMPOSE_PROJECT_NAME}" \
                        pull backend-service

                    docker compose \
                        -p "${COMPOSE_PROJECT_NAME}" \
                        up -d --no-build backend-service

                    echo "Déploiement du backend terminé."
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -eu

                    docker ps \
                        --filter "name=backend-employe-prod" \
                        --format "table {{.Names}}\\t{{.Status}}\\t{{.Image}}"

                    docker inspect \
                        --format='{{.State.Status}}' \
                        backend-employe-prod
                '''
            }
        }
    }

    post {
        success {
            echo "Déploiement Backend Gestion Employé réussi !"
            echo "Image déployée : ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo "Le pipeline a échoué. Consultez les logs Jenkins."
        }

        always {
            echo "Fin du pipeline CI/CD."
        }
    }
}
