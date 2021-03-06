def SCAN_REPOSITORY="flaskjenkins"
def SMART_CHECK_SERVER="af74cf86041fc47cab01925b331c9b84-2074456903.ap-southeast-1.elb.amazonaws.com"
def AWS_REGION="ap-southeast-1"
def GIT_REPO="https://github.com/OmarR00t/flask.git" 
def GIT_CREDENTIALS="29ef4442-e29e-46d6-8f6f-f91004fe0bbc"
def DSSC_CREDENTIALS="DSSC"
def REPO_CREDENTIALS="omar_almulhim"
def SCAN_REGISTRY="650143975734.dkr.ecr.ap-southeast-1.amazonaws.com"
def BRANCH_NAME = "main"
import groovy.json.JsonOutput
node {
    cleanWs()
    stage "Checkout Code"
    sh "echo $SCAN_REPOSITORY"
    sh "printenv"
    
    checkout changelog: false, poll: false, scm: [$class: 'GitSCM', branches: [[name: BRANCH_NAME]], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: '.']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: GIT_CREDENTIALS, url: GIT_REPO]]]

    stage "Build Image"
    
    sh "docker build -t $SCAN_REPOSITORY ."
    sh "printenv"
    stage "Send to Repository"
    sh("eval \$(aws ecr get-login --no-include-email | sed 's|https://||')")*//
	
    sh "docker tag $SCAN_REPOSITORY:latest $SCAN_REGISTRY/$SCAN_REPOSITORY:$BUILD_ID"
    sh "docker push $SCAN_REGISTRY/$SCAN_REPOSITORY:$BUILD_ID"
 
 

    stage "Smart Check"

     def SCAN_IMAGE="$SCAN_REGISTRY/$SCAN_REPOSITORY:$BUILD_ID"
     sh "echo $SCAN_IMAGE"


    withCredentials([
        usernamePassword([
            credentialsId: DSSC_CREDENTIALS,
            usernameVariable: "DSSC_USER",
            passwordVariable: "DSSC_PASSWORD",
        ])
    ]){
        withCredentials([
            usernamePassword([
                credentialsId: REPO_CREDENTIALS,
            usernameVariable: "Access_ID",
            passwordVariable: "Secret_ID",
            ])
        ]){
            smartcheckScan([
                imageName: SCAN_IMAGE,
                smartcheckHost: SMART_CHECK_SERVER,
                smartcheckUser: DSSC_USER,
                smartcheckPassword: DSSC_PASSWORD,
                insecureSkipTLSVerify: true,
                findingsThreshold: JsonOutput.toJson([
                    "malware": 1,
                    "vulnerabilities": [
                        "critical": 1,
                        "high": 1,
                    ],
                    "contents": [
                        "critical": 1,
                        "high": 3,
                    ]
                ]).toString(),
                imagePullAuth: JsonOutput.toJson([
                    "aws": [
						"region": "ap-southeast-1",
						"accessKeyID": Access_ID,
						"secretAccessKey": Secret_ID,
						]
                ]).toString(),
            ])
        }
    }
    sh "cat "
    stage "Certify Release"
    sh "docker tag $SCAN_REPOSITORY:latest $SCAN_REGISTRY/$SCAN_REPOSITORY:$BRANCH_NAME"
    stage "Deploy to Production"

    sh "docker push $SCAN_REGISTRY/$SCAN_REPOSITORY:$BRANCH_NAME"
}
