// -------------------------------------------------------------------
//
// Module:         python_cowbull_server
// Submodule:      Jenkinsfile
// Environments:   all
// Purpose:        Jenkins scripted pipeline to perform the CI and CD
//                 build of the python cowbull server image.
//                 NOTE: Scripted pipeline
//
// Created on:     30 July 2019
// Created by:     David Sanders
// Creator email:  dsanderscanada@nospam-gmail.com
//
// -------------------------------------------------------------------
// Modifed On   | Modified By                 | Release Notes
// -------------------------------------------------------------------
// 30 Jul 2019  | David Sanders               | First release.
// -------------------------------------------------------------------
// 06 Aug 2019  | David Sanders               | Change python3 to use
//              |                             | default python rather
//              |                             | than specific version.
// -------------------------------------------------------------------
// 06 Aug 2019  | David Sanders               | Add multi-branch
//              |                             | support and push non-
//              |                             | master branches as dev
//              |                             | and promote major/minor
//              |                             | to year month format.
// -------------------------------------------------------------------

def major = '19'
def minor = '08'
def imageName = ''

podTemplate(containers: [
    containerTemplate(name: 'redis', image: 'k8s-master:32080/redis:5.0.3-alpine', ttyEnabled: true, command: 'redis-server'),
    containerTemplate(name: 'python', image: 'k8s-master:32080/python:3.7.4-alpine3.10', ttyEnabled: true, command: 'cat'),
    containerTemplate(name: 'cowbull-server', image: 'k8s-master:32080/dsanderscan/cowbull:19.08.37', ttyEnabled: true, command: 'cat'),
    // containerTemplate(
    //     name: 'cowbull', 
    //     image: 'k8s-master:32080/dsanderscan/cowbull:19.08.37', 
    //     ttyEnabled: true,
    //     // change this
    //     workingDir: '/cowbull',
    //     command: 'gunicorn',
    //     args: '-b 8080 -w 4 app:app',
    //     envVars: [
    //         envVar(key: 'PYTHONPATH', value: '/cowbull'),
    //         envVar(key: 'PERSISTER', value: '{"engine_name": "redis", "parameters": {"host": "localhost", "port": 6379, "db": 0, "password": ""}}'),
    //         envVar(key: 'LOGGING_LEVEL', value: '10')
    //     ]
    // ),
    containerTemplate(name: 'maven', image: 'k8s-master:32080/maven:3.6.1-jdk-11-slim', ttyEnabled: true, command: 'cat'),
    containerTemplate(name: 'docker', image: 'k8s-master:32080/docker:19.03.1-dind', ttyEnabled: true, privileged: true),
  ]) {
  node(POD_LABEL) {
    stage('Setup environment') 
    {
        if ( (env.BRANCH_NAME).equals('master') ) {
            imageName = "dsanderscan/cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}"
        } else {
            imageName = "dsanderscan/cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
        }
        checkout scm
        container('python') {
            sh """
                python --version
                python -m pip install -q -r requirements.txt
            """
        }
    }
    // stage('Test cowbull server') {
    //     container('cowbull-server') {
    //         sh """
    //             pwd
    //             ls -als
    //         """
    //     }
    // }
    // stage('Execute unit tests') {
    //     container('python') {
    //         sh """
    //             export COWBULL_SERVER=localhost
    //             export COWBULL_PORT=8080
    //             export PYTHONPATH=\$(pwd):\$(pwd)/tests
    //             python -m unittest tests
    //         """
    //     }
    // }
  }
}
