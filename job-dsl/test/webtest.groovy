def website = '10.10.33.5/flask'

import groovy.sql.Sql
// postgresql://postgres:postgres@postgres:5432/postgres
def url = 'jdbc:postgresql://postgres:5432/postgres'
def user = 'postgres'
def password = 'postgres'
def driver = 'org.postgresql.Driver'
def sql = Sql.newInstance(url, user, password, driver)

def first = sql.firstRow('SELECT ip FROM host')
echo first


// use 'sql' instance ...

sql.close()


//Optional pre-send script, see further in this article for more info.
//If removed, make sure to also remove the 'presendScript' variable
//in the publisher block below.
//def localPreSendScript = readFileFromWorkspace('<path to script>/pre_send_script.groovy_script')

for ( i in 0..2 ) {
    //Job identifier, also used for the directory
    job('test/website-monitors-test'+i) {

      //Name of the job in Jenkins
      displayName('Website status of multiple containers test'+i)

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

}
