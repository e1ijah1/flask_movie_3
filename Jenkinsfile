String appWebConfig = 'production'
String appMysqlHost = 'database'
String appMysqlDB = 'cili_db'
String appMysqlUser = env.APP_MU
String appMysqlPwd = env.APP_MP
String appRedisHost = 'redis'
String appMailServer = env.APP_MAILS
String appMailUser = env.APP_MAILU
String appMailPwd = env.APP_MAILP
String appMailSender = env.APP_SENDER
String dbMysqlUser = env.DB_MU
String dbMysqlPwd = env.DB_MUP
String dbMysqlRootPwd = env.DB_MRP


pipeline {
    agent any

    options {
        timeout(time: 1, unit: 'DAYS')
        disableConcurrentBuilds()
    }
    stages {
        stage('Checkout Project') {
            steps {
                // getCode()
                echo 'pass'
            }
            post {
                failure {
                    echo 'Checkout failed, pls check log'
                }
            }
        }

        stage('Build') {
            steps { initialize() }
            post {
                failure {
                    echo 'Build failed, pls check log'
                }
            }
        }
        stage('SetUp') {
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
        export APP_WEBC=${appWebConfig} APP_MH=${appMysqlHost} APP_MDB=${appMysqlDB} APP_MU=${appMysqlUser} APP_MP=${appMysqlPwd} APP_RH=${appRedisHost} APP_MAILS=${appMailServer} APP_MAILU=${appMailUser} APP_MAILP=${appMailPwd} APP_SENDER=${appMailSender} DB_MU=${dbMysqlUser} DB_MUP=${dbMysqlPwd} DB_MRP=${dbMysqlRootPwd} 
        docker-compose -f zbuild/docker-compose.yml up -d --build
    """
}

def setUpApp() {
    String containerName = 'f_app'
    sh """
        docker exec ${containerName} sh -c "echo \$WEB_CONFIG \$MYSQL_HOST \$MYSQL_DB \$MYSQL_USR \$MYSQL_PWD \$REDIS_HOST \$MAIL_SERVER \$MAIL_USERNAME \$MAIL_PASSWORD \$MAIL_SENDER"
        docker exec ${containerName} sh -c "mysql -hdatabase -u${appMysqlUser} -p${appMysqlPwd} < initial.sql"
        docker exec ${containerName} sh -c "python manage.py initialize"
        docker exec ${containerName} sh -c "gunicorn manage:app -c gunicorn.conf.py"
    """
}