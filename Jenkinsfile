
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        DOCKERHUB_USER = 'abdoulaye940'
        IMAGE_NAME = 'backend-employe'
        IMAGE_TAG = "1.${BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = 'backend-gestion-employe'
    }

    stages {
        stage('Vérifier Docker') {
            steps {
                sh '''
                    set -eu
                    docker --version
                    docker compose version
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                checkout scm

                sh '''
                    set -eu
                    test -f Dockerfile
                    test -f docker-compose.yaml || test -f docker-compose.yml

                    echo "Code source récupéré avec succès."
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -eu

                    echo "Construction de l'image ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"

                    docker build \
                        -t "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}" .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set -eu
                        set +x

                        trap 'docker logout >/dev/null 2>&1 || true' EXIT

                        echo "$DOCKER_PASS" | docker login \
                            --username "$DOCKER_USER" \
                            --password-stdin

                        docker push \
                            "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"

                        echo "Image publiée avec succès."
                    '''
                }
            }
        }

        stage('Vérifier Compose') {
            steps {
                sh '''
                    set -eu

                    echo "Vérification de la configuration Compose..."

                    docker compose \
                        -p "${COMPOSE_PROJECT_NAME}" config --quiet

                    echo "Configuration Compose valide."
                '''
            }
        }

        stage('Déployer le backend') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        set -eu
                        set +x

                        trap 'docker logout >/dev/null 2>&1 || true' EXIT

                        echo "$DOCKER_PASS" | docker login \
                            --username "$DOCKER_USER" \
                            --password-stdin

                        echo "Téléchargement de l'image ${IMAGE_TAG}..."

                        docker compose \
                            -p "${COMPOSE_PROJECT_NAME}" \
                            pull backend-service

                        echo "Déploiement du backend..."

                        docker compose \
                            -p "${COMPOSE_PROJECT_NAME}" \
                            up -d --no-build backend-service

                        echo "Conteneur déployé :"

                        docker ps \
                            --filter "name=backend-employe-prod"

                        echo "Image réellement utilisée :"

                        docker inspect \
                            -f '{{.Config.Image}}' \
                            backend-employe-prod
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline réussi : ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo 'Échec du pipeline. Consultez la console Jenkins.'
        }
    }
}
