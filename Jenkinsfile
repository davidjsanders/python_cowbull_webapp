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
// -------------------------------------------------------------------
// 19 Aug 2019  | David Sanders               | Combine k8s plug-in
//              |                             | with Docker for simpler
//              |                             | builds.
//              |                             | Move Cowbull container
//              |                             | yaml into a string.
//              |                             | TODO: Change to
//              |                             | readFile into string.
// -------------------------------------------------------------------
// 20 Aug 2019  | David Sanders               | Move yaml manifest for
//              |                             | build containers to an
//              |                             | external file and read
//              |                             | on pipeline execution.
//              |                             | Add comments.
// -------------------------------------------------------------------
// 21 Aug 2019  | David Sanders               | Change build containers
//              |                             | to -local for minikube
//              |                             | based k8s
// -------------------------------------------------------------------
// 26 Aug 2019  | David Sanders               | Simple change to test
//              |                             | trigger for Dynamic
//              |                             | DNS based name.
// -------------------------------------------------------------------

// Define the variables used in the pipeline
def major = '19'    // The major version of the build - Major.Minor.Build
def minor = '08'    // The minor version of the build - Major.Minor.Build
def imageName = ''  // Variable to hold image name; depends on branch
def privateImage = '' // Variable for private hub image name
def yamlString = "" // Variable used to contain yaml manifests which are
                    // loaded from file.

// The manifestsFile to use - can vary depending on 'proper' cluster
// vs. minikube
//def manifestsFie = "jenkins/build-containers.yaml"
def manifestsFile = "jenkins/build-containers.yaml"

// DNS name and protocol for connecting to the Docker service
// TODO: Make into a global variable
def dockerServer = "tcp://jenkins-service.jenkins.svc.cluster.local:2375"

// Preparation stage. Checks out the source and loads the yaml manifests
// used during the pipeline. see ./jenkins/build-containers.yaml
node {
    stage('Prepare Environment') {
        checkout scm
        yamlString = readFile "${manifestsFile}"
    }
}

// Example of using a Windows node in the pipeline
// node('windows') {
//     stage('Check Windows') {
//         bat 'dir'
//     }
// }

// Define the pod templates to, run the containers and execute the
// pipeline.
podTemplate(yaml: "${yamlString}") {
  node(POD_LABEL) {

    // Setup environment stage. Set the image name depending on the
    // branch, use the python container and install the required pypi
    // packages from requirements.txt
    stage('Setup environment') {
        if ( (env.BRANCH_NAME).equals('master') ) {
            privateImage = "cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}"
            imageName = "dsanderscan/cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}"
        } else {
            privateImage = "cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
            imageName = "dsanderscan/cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
        }
        checkout scm
        container('python') {
            withCredentials([file(credentialsId: 'pip-conf-file', variable: 'pipconfig')]) {
                sh """
                    cp $pipconfig /etc/pip.conf
                    python --version
                    python -m pip install -r requirements.txt
                """
            }
        }
    }

    // Simple stage to ensure that redis is reachable; redis is required
    // for unit and system tests later in the pipeline.
    stage('Verify Redis is running') {
        container('redis') {
            sh 'redis-cli ping'
        }
    }

    // Execute the unit tests; while these should have already been
    // processed, they are re-run to ensure the source software is
    // good.
    stage('Execute Python unit tests') {
        container('python') {
            try {
                sh """
                    export PYTHONPATH="\$(pwd)"
                    coverage run tests/main.py
                    coverage xml -i
                """
            } finally {
                // Collect the unit test reports in junit format
                junit 'unittest-reports/*.xml'
            }
        }
    }

    // Execute the system tests; verify that the system as a whole is
    // operating as expected.
    stage('Execute Python system tests') {
        container('python') {
            try {
                sh """
                    echo "TBD"
                """
            } finally {
                echo "TBD"
                // junit 'unittest-reports/*.xml'
            }
        }
    }
 
    // Collect the coverage reports and pass them to the sonarqube
    // scanner for analysis.
    stage('Sonarqube code coverage') {
        container('maven') {
            def scannerHome = tool 'SonarQube Scanner';
            withSonarQubeEnv('Sonarqube') {
                sh """
                    pwd
                """
                sh """
                    # Remove cached files
                    rm -rf *.pyc

                    # Remove any previous scan outputs
                    rm -f /var/jenkins_home/workspace/cowbull-webapp/.scannerwork/report-task.txt
                    rm -f /var/jenkins_home/workspace/cowbull-webapp/.sonar/report-task.txt

                    # Run sonar-scanner; make sure it is executable first
                    # as there have been occurrences where it is not.
                    chmod +x ${scannerHome}/bin/sonar-scanner
                    ${scannerHome}/bin/sonar-scanner -X -Dproject.settings=./sonar-project.properties -Dsonar.python.coverage.reportPath=./coverage.xml -Dsonar.projectVersion="${major}"."${minor}"."${env.BUILD_NUMBER}"
                """
            }
        }
    }

    // Check the quality of the project. In this stage, the 
    // abortPipeline set to false ensures the pipeline continues
    // if the code quality is low - it could be set to true to stop
    // the pipeline if required.
    stage('Quality Gate') {
        container('maven') {
            def scannerHome = tool 'SonarQube Scanner';
            timeout(time: 10, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: false
            }
        }
    }

    // Build the application into a docker image and push it to the
    // Docker Hub and the private registry.
    // TODO: the registry URLs should be global variables.
    stage('Docker Build') {
        container('docker') {
            docker.withServer("$dockerServer") {
                // docker.withRegistry('http://k8s-master:32081', 'nexus-oss') {
                //     def customImage = docker.build("${privateImage}", "-f vendor/docker/Dockerfile .")
                //     customImage.push()
                // }
                docker.withRegistry('https://registry-1.docker.io', 'dockerhub') {
                    def customImage = docker.build("${imageName}", "-f Dockerfile .")
                    customImage.push()
                    sh """
                        docker run --rm dsanderscan/cowbull_webapp:move-2-alpine.6 /bin/sh -c "python3 tests/main.py"
                    """
                }
            }
            withEnv(["imageName=${imageName}"]) {
                sh 'echo "docker.io/${imageName}" > anchore_images'
            }
            // }
        }
    }

    stage('Test image') {
        /* Requires the Docker Pipeline plugin to be installed */
        container('docker') {
            sh """
                docker run --rm dsanderscan/cowbull_webapp:move-2-alpine.6 /bin/sh -c "python3 tests/main.py"
            """
        }
    }

    stage('Image Security scan') {
        anchore bailOnFail: false, bailOnPluginFail: false, engineCredentialsId: 'azure-azadmin', name: 'anchore_images'
    }

    // Tidy up. Nothing happens here at present.
    stage('Tidy up') {
        container('python') {
            sh """
                echo "Doing some tidying up :) "
            """
        }
    }
  }
}
