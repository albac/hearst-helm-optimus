#!groovy
import groovy.json.JsonOutput

// Global Variables 
REGION = 'us-east-1'
REGISTRY_URL = '197398802565.dkr.ecr.us-east-1.amazonaws.com' //AWS-ECR Registry URL
IMAGE_NAME = 'backbase-tomcat' // Global Docker Image & App Name
REPO_URL = 'https://github.com/zerosinitiative/backbase-helm.git' // Repositroy URL of the JOB
TAG = 'latest'
TOPIC_ARN = 'arn:aws:sns:us-east-1:197398802565:backbase-build-notif'

pipeline{
    agent any
    stages{
        stage("Docker Login To ECR"){
            steps{
                dockerLogin()
                notifySNS()
            }
        }
        stage("Docker Build Image") {
            steps {
                dockerBuildImage()
                notifySNS()
            }
        }
        stage("Docker Image Tag") {
            steps {
                dockerTag()
                notifySNS()
            }
        }
        stage("Docker Image Scanning") {
            steps {
                dockerImageScanning()
                notifySNS()
            }
        }
        stage("Docker Push To ECR") {
            steps {
                dockerImagePushToECR()
                notifySNS()
            }
        }
        stage("Deploy Helm App") {
            steps {
                deployHelmApp()
                notifySNS()
            }
        }
        stage("Cleanup") {
            steps { sh('docker image prune -af') }
        }
    }
}  

def dockerLogin() {
    sh(script:"aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${REGISTRY_URL}")
}

def dockerBuildImage() {
    sh(script:"docker build -t ${IMAGE_NAME} .")
}

def dockerTag() {
    sh(script:"docker tag ${IMAGE_NAME}:${TAG} ${REGISTRY_URL}/${IMAGE_NAME}:${TAG}")
}

def dockerImageScanning() {
    sh(script:"trivy image ${REGISTRY_URL}/${IMAGE_NAME}:${TAG}")
}

def dockerImagePushToECR() {
    sh(script:"docker push ${REGISTRY_URL}/${IMAGE_NAME}:${TAG}")
}

def deployHelmApp(){
    sh(script:"helm upgrade --debug --wait --atomic --install ${IMAGE_NAME} .")
}

def notifySNS(){
    sh(script: "aws sns publish --region ${REGION} --topic-arn ${TOPIC_ARN} --message '${env.STAGE_NAME} Successful'")
}
