def recipients = 'pawel.borowski@opi.org.pl pborowskiopi@gmail.com'
def website = 'https://intranet.opi.org.pl'

//Optional pre-send script, see further in this article for more info.
//If removed, make sure to also remove the 'presendScript' variable
//in the publisher block below.
 //def localPreSendScript = readFileFromWorkspace('<path to script>/pre_send_script.groovy_script')

//Job identifier, also used for the directory
job('website-monitor') {

  //Name of the job in Jenkins
  displayName('Website status of ExampleWebsite')

  triggers {
      //Run every 5 minutes
      cron('H/5 * * * * ')
  }

  steps {
    environmentVariables {
      env('WEBSITE', websie)
      env('TIMEOUT', 5)
      env('ATTEMPTS', 5)
    }

    //Run a shell script from the workspace
    shell(readFileFromWorkspace('web30.sh'))
  }

  logRotator {
    //Remove logs after two days
    daysToKeep(2)
  }

  publishers {
    extendedEmail(recipients, 'Website is offline') {

      //Events on which a email is sent
      trigger(triggerName: 'Failure', subject: 'Website offline!', body: 'Website ' + website + ' is offline!')
      trigger(triggerName: 'Fixed', subject: 'Website online!', body: 'Website ' + website + ' is back online!')

      //Custom configuration
      configure { node ->
        node << {
          contentType 'text/html'
          //Make sure that recipients mail to each other and not back to the system
          replyTo recipients
          //Optional script for extra conditions
          // presendScript localPreSendScript
        }
      }
    }
  }
}
