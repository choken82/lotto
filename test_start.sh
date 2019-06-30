#!/bin/tcsh
###############################################
#
# Script to launch lotto check
#
# Created: 2011-12-15  ejohwen
#
###############################################
# Todo: What in .login and .cshrc is needed to get it working
# when running with crontab?? Then remove following lines.
source /home/${USER}/.login
source /home/${USER}/.cshrc

set SHELL="/bin/tcsh"

# Set correct perl version
module add perl/5.12.3

# Set proxies
setenv http_proxy 'http://www-proxy.ericsson.se:8080/'
setenv https_proxy 'http://www-proxy.ericsson.se:8080/'

# Launch the lotto script
perl /home/${USER}/lotto/lotto.pl /home/${USER}/lotto/lottorader.txt /home/${USER}/lotto/jokerrader.txt /home/${USER}/lotto/testadresser.txt

