import groovy.json.JsonSlurper

def website = '10.10.33.5/flask'

def postmanGet = new URL('http://10.10.33.5/flask/urls')
def getConnection = postmanGet.openConnection()
def response_code = getConnection.responseCode
def urls = getConnection.inputStream.text
def card = new JsonSlurper().parse(postmanGet)

println "groovy project for job creation for every single monitored webpage, stright from zabbix API http://10.10.33.5/flask/urls"
println "response code: " + response_code

for (url in card) {

    // println url.values()[1]

    job('test/website ' + url.values()[1]) {

      //Name of the job in Jenkins
      displayName('test' + url.values()[1])
      println "job for: " + url.values()[1]

      triggers {
          //Run every 30 minutes
          cron('H/30 * * * * ')
      }

      steps {
        environmentVariables {
          env('TIMEOUT', 5)
          env('ATTEMPTS', 5)
        }

        //Run a shell script from the workspace
        shell(readFileFromWorkspace("""job-dsl/test/web30.sh """ + url.values()[1]))
      }

      logRotator {
        //Remove logs after two days
        daysToKeep(2)
      }

      publishers {
        extendedEmail {

            recipientList('pawel.borowski@opi.org.pl')
            defaultSubject('Oops')
            defaultContent('Something broken')
            contentType('text/html')

            triggers {
                    failure {
                        subject('DSL Task website offline!')
                        content('website '+ url.values()[1] + ' is offline!')
                        sendTo {
                            recipientList('pawel.borowski@opi.org.pl')
                        }
                    }
                    fixed {
                        subject('DSL Task website fixed!')
                        content('website '+ url.values()[1] + ' is fixed!')
                        sendTo {
                            recipientList('pawel.borowski@opi.org.pl')
                        }
                    }
                }
        }
      }
    }


} // end for
