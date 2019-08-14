// -------------------------------------------------------------------
//
// Module:         python_cowbull_webapp
// Submodule:      Jenkinsfile
// Environments:   all
// Purpose:        Jenkins scripted pipeline to perform the CI and CD
//                 build of the python cowbull webapp image.
//                 NOTE: Scripted pipeline
//
// Created on:     13 August 2019
// Created by:     David Sanders
// Creator email:  dsanderscanada@nospam-gmail.com
//
// -------------------------------------------------------------------
// Modifed On   | Modified By                 | Release Notes
// -------------------------------------------------------------------
// 13 Aug 2019  | David Sanders               | First release.

def major = '19'
def minor = '08'
def imageName = ''

podTemplate(containers: [
    containerTemplate(name: 'redis', image: 'k8s-master:32080/redis:5.0.3-alpine', ttyEnabled: true, command: 'redis-server'),
    containerTemplate(name: 'python', image: 'k8s-master:32080/python:3.7.4', ttyEnabled: true, command: 'cat'),
    containerTemplate(name: 'cowserver', workingDir: '/cowbull', image: 'dsanderscan/cowbull:19.08.38', ttyEnabled: true, command: 'cat'),
    // containerTemplate(
    //     name: 'cowserver', 
    //     image: 'k8s-master:32080/dsanderscan/cowbull:19.08.38', 
    //     workingDir: '/cowbull/',
    //     command: 'cat',
    //     ttyEnabled: false,
    //     privileged: true,
    //     alwaysPullImage: false,
    //     resourceRequestCpu: '200m',
    //     resourceLimitCpu: '500m',
    //     resourceRequestMemory: '500Mi',
    //     resourceLimitMemory: '2000Mi',
    //     ports: [portMapping(name: 'cowbull', containerPort: 8080, hostPort: 8080)]
    //  ),
    containerTemplate(name: 'maven', image: 'k8s-master:32080/maven:3.6.1-jdk-11-slim', ttyEnabled: true, command: 'cat'),
    containerTemplate(name: 'docker', image: 'k8s-master:32080/docker:19.03.1-dind', ttyEnabled: true, privileged: true),
  ]) {
  node(POD_LABEL) {
    stage('Setup environment') {
        if ( (env.BRANCH_NAME).equals('master') ) {
            imageName = "dsanderscan/cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}"
        } else {
            imageName = "dsanderscan/cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
        }
        checkout scm
        container('python') {
            sh """
                python --version
                python -m pip install -r requirements.txt
            """
        }
        container('cowserver') {
            sh """
                pwd
                ls -als
            """
        }
    }
    stage('Verify Redis is running') {
        container('redis') {
            sh 'redis-cli ping'
        }
    }
    stage('Run cowbull as a Docker container') {
        container('docker') {
            sh """
                docker run -p 18080:8080 --rm --name cowbull -d dsanderscan/cowbull:19.08.38
            """
        }
    }
    stage('Execute Python unit tests') {
        container('python') {
            try {
                sh """
                    export PYTHONPATH="\$(pwd)"
                    export COWBULL_SERVER=localhost
                    export COWBULL_PORT=8080
                    coverage run tests/main.py
                    coverage xml -i
                """
            } finally {
                junit 'unittest-reports/*.xml'
            }
        }
    }
    stage('Execute Python system tests') {
        container('python') {
            try {
                sh """
                    export PYTHONPATH="\$(pwd)"
                    export COWBULL_SERVER=localhost
                    export COWBULL_PORT=8080
                    python tests/main.py
                """
            } finally {
                junit 'unittest-reports/*.xml'
            }
        }
    }
    stage('Stop cowbull in Docker') {
        container('docker') {
            sh """
                docker kill cowbull
            """
        }
    }
    stage('Sonarqube code coverage') {
        container('maven') {
            def scannerHome = tool 'SonarQube Scanner';
            withSonarQubeEnv('Sonarqube') {
                sh """
                    pwd
                """
    //             sh """
    //                 rm -rf *.pyc
    //                 rm -f /var/jenkins_home/workspace/cowbull-server/.scannerwork/report-task.txt
    //                 rm -f /var/jenkins_home/workspace/cowbull-server/.sonar/report-task.txt
    //                 echo "Run sonar scanner"
    //                 chmod +x ${scannerHome}/bin/sonar-scanner
    //                 ${scannerHome}/bin/sonar-scanner -X -Dproject.settings=./sonar-project.properties -Dsonar.python.coverage.reportPath=./coverage.xml -Dsonar.projectVersion="${major}"."${minor}"."${env.BUILD_NUMBER}"
    //             """
            }
        }
    }
    stage('Quality Gate') {
        container('maven') {
            def scannerHome = tool 'SonarQube Scanner';
            sh """
                echo "TBD"
            """
//             timeout(time: 10, unit: 'MINUTES') {
//                 waitForQualityGate abortPipeline: true
//             }
        }
    }
    stage('Docker Build') {
        container('docker') {
            withCredentials([
                [$class: 'UsernamePasswordMultiBinding', 
                credentialsId: 'dockerhub',
                usernameVariable: 'USERNAME', 
                passwordVariable: 'PASSWORD']
            ]) {
                sh """
                    echo "Paused while testing."
                """
                // try {
                //     sh """
                //         docker login -u "${USERNAME}" -p "${PASSWORD}"
                //         echo "Building "${imageName}
                //         docker build -t ${imageName} -f vendor/docker/Dockerfile .
                //         docker push ${imageName}
                //         docker image rm ${imageName}
                //     """
                // } finally {
                //     echo "In the finally block"
                // }
            }
        }
    }
//     stage('Tidy up') {
//         container('mono') {
//             sh """
//                 echo "Doing some tidying up :) "
//             """
//         }
//     }
  }
}
