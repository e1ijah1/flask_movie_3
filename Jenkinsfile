pipeline {
    agent any

    environment {
        WEB_CONFIG = 'production'
        DB_HOST = 'database'
        DB_PORT = 3306
        DB_NAME = 'cili_db'
        REDIS_HOST = 'redis'
        MAIL_SERVER = credentials('MAIL_SERVER')
        MAIL_USERNAME = credentials('MAIL_USERNAME')
        MAIL_PASSWORD = credentials('MAIL_PASSWORD')
        SITE_MAIL_SENDER= credentials('SITE_MAIL_SENDER')
    }

    options {
        timeout(time: 1, unit: 'DAYS')
        disableConcurrentBuilds()
    }
    stages {
        stage ('Build') {
            steps { initialize() }
            post {
                failure {
                    echo 'Build failed, pls check log'
                }
            }
        }
        stage ('SetUp') {
            steps { setUpApp() }
            post {
                failure {
                    sh 'docker-compose -f zbuild/docker-compose.yml down'
                    echo 'SetUp failed, pls check log'
                }
            }
        }
    }
}

def initialize() {
    sh """
        docker-compose -f zbuild/docker-compose.yml up -d --build
    """
}

def setUpApp() {
    def containerName = 'f_app'
    sh """
        docker exec ${containerName} sh -c 'export WEB_CONFIG=${WEB_CONFIG} DB_HOST=${DB_HOST} DB_PORT=${DB_PORT} DB_NAME=${DB_NAME} REDIS_HOST=${REDIS_HOST} MAIL_SERVER=${MAIL_SERVER} MAIL_USERNAME=${MAIL_USERNAME} MAIL_PASSWORD=${MAIL_PASSWORD} SITE_MAIL_SENDER=${SITE_MAIL_SENDER}'
        docker exec ${containerName} sh -c 'mysql -uroot -p < initial.sql'
        docker exec ${containerName} sh -c 'python manage.py initialize'
        docker exec ${containerName} sh -c 'gunicorn manage:app -c gunicorn.conf.py'
    """
}