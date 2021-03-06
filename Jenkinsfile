// Define the variables used in the pipeline
def major = '19'    // The major version of the build - Major.Minor.Build
def minor = '08'    // The minor version of the build - Major.Minor.Build
def imageName = ''  // Variable to hold image name; depends on branch
def privateImage = '' // Variable for private hub image name
def scanImage = ''  // Variable to hold short image name
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
    stage('Prepare') {
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
    stage('Setup') {
        if ( (env.BRANCH_NAME).equals('master') ) {
            privateImage = "k8s-master:32081/cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}"
            imageName = "dsanderscan/cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}"
            scanImage = "nexus-docker.default.svc.cluster.local:18081/cowbull_webapp:${major}.${minor}.${env.BUILD_NUMBER}.prescan"
        } else {
            privateImage = "k8s-master:32081/cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
            imageName = "dsanderscan/cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
            scanImage = "nexus-docker.default.svc.cluster.local:18081/cowbull_webapp:${env.BRANCH_NAME}.${env.BUILD_NUMBER}.prescan"
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
    stage('Verify Redis') {
        container('redis') {
            sh 'redis-cli ping'
        }
    }

    // Execute the unit tests; while these should have already been
    // processed, they are re-run to ensure the source software is
    // good.
    stage('Unit test') {
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
    stage('System test') {
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
    stage('Code coverage') {
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
    stage('Stage Build') {
        container('docker') {
            docker.withServer("$dockerServer") {
                docker.withRegistry('http://k8s-master:32081', 'nexus-oss') {
                    def customImage = docker.build("${privateImage}.prescan", "-f Dockerfile .")
                    customImage.push()
                }
            }
            withEnv(["image=${scanImage}"]) {
                sh """
                    echo "Add image $image to anchore_images scan file"
                    echo "$image" > anchore_images
                """
            }
        }
    }

    // Re-execute the unit and system tests using the image, to ensure
    // the images function as expected - i.e. there have been no Docker
    // build errors introduced.
    stage('Test image') {
        container('docker') {
            docker.withServer("$dockerServer") {
                withEnv(["image=${privateImage}.prescan"]) {
                    sh """
                        docker run --rm $image /bin/sh -c "python3 tests/main.py"
                    """
                }
            }
        }
    }

    // Scan the image using the OSS anchore engine to check for vulnerability
    // and image policy issues. NOTE: bailOnFail is false; if it were set to
    // true, the pipeline would fail if the image fails to meet policy.
    stage('Anchore scan') {
        anchore bailOnFail: false, bailOnPluginFail: true, engineCredentialsId: 'azure-azadmin', name: 'anchore_images'
    }

    // The finalize step of the pipeline (i.e. everything is good), produces
    // final Docker images and pushes them to the private registry AND
    // Docker Hub.
    stage('Finalize') {
        container('docker') {
            docker.withServer("$dockerServer") {
                docker.withRegistry('http://k8s-master:32081', 'nexus-oss') {
                    def customImage = docker.build("${privateImage}", "-f Dockerfile .")
                    customImage.push()
                }
                docker.withRegistry('https://registry-1.docker.io', 'dockerhub') {
                    def customImage = docker.build("${imageName}", "-f Dockerfile .")
                    customImage.push()
                }
            }
        }
    }
  }
}
