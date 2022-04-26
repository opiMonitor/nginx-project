def website = '10.10.33.5/flask'

//Optional pre-send script, see further in this article for more info.
//If removed, make sure to also remove the 'presendScript' variable
//in the publisher block below.
//def localPreSendScript = readFileFromWorkspace('<path to script>/pre_send_script.groovy_script')

//Job identifier, also used for the directory
job('website-monitor') {

  //Name of the job in Jenkins
  displayName('Website status of flask container')

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
    shell(readFileFromWorkspace('job-dsl/test/web30.sh'))
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
                    content('website '+ website + ' is offline!')
                    sendTo {
                        recipientList('pawel.borowski@opi.org.pl')
                    }
                }
                fixed {
                    subject('DSL Task website fixed!')
                    content('website '+ website + ' is fixed!')
                    sendTo {
                        recipientList('pawel.borowski@opi.org.pl')
                    }
                }
            }
    }
  }
}
