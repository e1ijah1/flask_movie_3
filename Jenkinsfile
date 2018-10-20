pipeline {
    agent any

    environment {
        WEB_CONFIG = 'production'
        MYSQL_HOST = 'database'
        MYSQL_DB = 'cili_db'
        // MYSQL_USR = credentials('MYSQL_USR')
        // MYSQL_PWD = credentials('MYSQL_PWD')
        REDIS_HOST = 'redis'
        // MAIL_SERVER = credentials('MAIL_SERVER')
        // MAIL_USERNAME = credentials('MAIL_USERNAME')
        // MAIL_PASSWORD = credentials('MAIL_PASSWORD')
        // SITE_MAIL_SENDER = credentials('SITE_MAIL_SENDER')
    }

    options {
        timeout(time: 1, unit: 'DAYS')
        disableConcurrentBuilds()
    }
    stages {
        stage ('Checkout Project') {
            steps { getCode() }
            post {
                failure {
                    echo 'Checkout failed, pls check log'
                }
            }
        }
        }
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


def getCode() {
    if (srcType == 'Git') {
        checkout([
        $class: 'GitSCM',
        branches: [[name: '*/master']],
        doGenerateSubmoduleConfigurations: false,
        extensions: [], submoduleCfg: [],
        userRemoteConfigs: [[
            credentialsId: 'github_pk',
            url: 'https://github.com/F1renze/flask_movie_3'
        ]]
        ])
    }
}

def initialize() {
    sh """
        docker-compose -f zbuild/docker-compose.yml up -d --build
    """
}

def setUpApp() {
    String containerName = 'f_app'
    sh """
        docker exec ${containerName} sh -c "export WEB_CONFIG=${WEB_CONFIG} MYSQL_HOST=${MYSQL_HOST} MYSQL_DB=${MYSQL_DB} MYSQL_USR=${MYSQL_USR} MYSQL_PWD=${MYSQL_PWD} REDIS_HOST=${REDIS_HOST} MAIL_SERVER=${MAIL_SERVER} MAIL_USERNAME=${MAIL_USERNAME} MAIL_PASSWORD=${MAIL_PASSWORD} SITE_MAIL_SENDER=${SITE_MAIL_SENDER}"
        docker exec ${containerName} sh -c "echo $WEB_CONFIG $MYSQL_HOST $MYSQL_DB $MYSQL_USR $MYSQL_PWD $MAIL_SERVER $MAIL_USERNAME $MAIL_PASSWORD $SITE_MAIL_SENDER"
        docker exec ${containerName} sh -c "mysql -hdatabase -u${MYSQL_USR} -p${MYSQL_PWD} < initial.sql"
        docker exec ${containerName} sh -c "python manage.py initialize"
        docker exec ${containerName} sh -c "gunicorn manage:app -c gunicorn.conf.py"
    """
}