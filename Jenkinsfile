pipeline {
    agent {
        docker { 
            image 'aist.fh-hagenberg.at:18444/repository/docker-util/aist-python:3.8'
            args '-u root:sudo'
            alwaysPull true
        }
    }
    options {
        gitLabConnection('Gitlab') 
        gitlabBuilds(builds: ['build'])
    }
    stages {
        stage('build') {
            steps {
                script {
                    // as tox does not differentiate between test/script/coding errors this is the best we can do... Too bad!
                    catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                        sh """
                        tox -r
                        . .tox/env/bin/activate
                        pylint src/geofiles/ --reports=n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > .tox/pylint.txt
                        """
                    }
                }
            }
            post {
                success {
                    updateGitlabCommitStatus name: 'build', state: 'success'
                }
                failure {
                    updateGitlabCommitStatus name: 'build', state: 'failed'
                }
                unstable {
                    updateGitlabCommitStatus name: 'build', state: 'failed'
                }
            }
        } 
    }
    post {
        always {
            sh """
            sonar-scanner \
                -Dsonar.projectKey=geofiles \
                -Dsonar.projectName=geofiles \
                -Dsonar.language=py \
                -Dsonar.python.pylint.reportPath=**/pylint.txt \
                -Dsonar.python.coverage.reportPaths=**/coverage.xml \
                -Dsonar.python.xunit.reportPath=.tox/junit.xml \
                -Dsonar.sources=.tox/env/lib/python3.8/site-packages/geofiles/ \
                -Dsonar.tests=tests/geofiles
            """
            junit '.tox/junit.xml'
            step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', 
                    failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false]) // for jenkins
        }
    }
}
