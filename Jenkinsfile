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
    containerTemplate(name: 'python', image: 'k8s-master:32080/python:3.7.4-alpine3.10', ttyEnabled: true, command: 'cat'),
    containerTemplate(
        name: 'cowbull-server', 
        workingDir: '/cowbull',
        image: 'k8s-master:32080/dsanderscan/cowbull:19.08.37', 
        ttyEnabled: true
    ),
    // containerTemplate(name: 'maven', image: 'k8s-master:32080/maven:3.6.1-jdk-11-slim', ttyEnabled: true, command: 'cat'),
    // containerTemplate(name: 'docker', image: 'k8s-master:32080/docker:19.03.1-dind', ttyEnabled: true, privileged: true),
    // containerTemplate(name: 'mono', image: 'k8s-master:32080/mono:6.0.0.313', ttyEnabled: true, privileged: true),
  ]) {
  node(POD_LABEL) {
    stage('Setup environment') {
        if ( (env.BRANCH_NAME).equals('master') ) {
            imageName = "dsanderscan/cowbull:${major}.${minor}.${env.BUILD_NUMBER}"
        } else {
            imageName = "dsanderscan/cowbull:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
        }
        checkout scm
        container('python') {
            sh """
                python --version
                python -m pip install -q -r requirements.txt
            """
        }
    }
    stage('Verify Redis is running') {
        container('redis') {
            sh 'redis-cli ping'
        }
    }
    // stage('Execute Python unit tests') {
    //     container('python') {
    //         try {
    //             sh """
    //                 export PYTHONPATH="\$(pwd)"
    //                 coverage run unittests/main.py
    //                 coverage xml -i
    //             """
    //         } finally {
    //             junit 'unittest-reports/*.xml'
    //         }
    //     }
    // }
    // stage('Execute Python system tests') {
    //     container('python') {
    //         try {
    //             sh """
    //                 export PYTHONPATH="\$(pwd)"
    //                 export PERSISTER='{"engine_name": "redis", "parameters": {"host": "localhost", "port": 6379, "db": 0, "password": ""}}'
    //                 export LOGGING_LEVEL=30
    //                 python systests/main.py
    //             """
    //         } finally {
    //             junit 'systest-reports/*.xml'
    //         }
    //     }
    // }
    // stage('Sonarqube code coverage') {
    //     container('maven') {
    //         def scannerHome = tool 'SonarQube Scanner';
    //         withSonarQubeEnv('Sonarqube') {
    //             sh """
    //                 rm -rf *.pyc
    //                 rm -f /var/jenkins_home/workspace/cowbull-server/.scannerwork/report-task.txt
    //                 rm -f /var/jenkins_home/workspace/cowbull-server/.sonar/report-task.txt
    //                 echo "Run sonar scanner"
    //                 chmod +x ${scannerHome}/bin/sonar-scanner
    //                 ${scannerHome}/bin/sonar-scanner -X -Dproject.settings=./sonar-project.properties -Dsonar.python.coverage.reportPath=./coverage.xml -Dsonar.projectVersion="${major}"."${minor}"."${env.BUILD_NUMBER}"
    //             """
    //         }
    //     }
    // }
//     stage('Quality Gate') {
//         container('maven') {
//             def scannerHome = tool 'SonarQube Scanner';
//             timeout(time: 10, unit: 'MINUTES') {
//                 waitForQualityGate abortPipeline: true
//             }
//         }
//     }
//     stage('Docker Build') {
//         container('docker') {
//             withCredentials([
//                 [$class: 'UsernamePasswordMultiBinding', 
//                 credentialsId: 'dockerhub',
//                 usernameVariable: 'USERNAME', 
//                 passwordVariable: 'PASSWORD']
//             ]) {
//                 try {
//                     sh """
//                         docker login -u "${USERNAME}" -p "${PASSWORD}"
//                         echo "Building "${imageName}
//                         docker build -t ${imageName} -f vendor/docker/Dockerfile .
//                         docker push ${imageName}
//                         docker image rm ${imageName}
//                     """
//                 } finally {
//                     echo "In the finally block"
//                 }
//             }
//         }
//     }
//     stage('Tidy up') {
//         container('mono') {
//             sh """
//                 echo "Doing some tidying up :) "
//             """
//         }
//     }
  }
}
