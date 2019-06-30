#!perl
#
# Lotto checking script
#
# - Fetches the correct rows from Text-Tv
# - Matches against played rows from files
# - Sends result by mail/sms to participants from file
#
# Author: Johan Wennberg
#

use strict;
use warnings;
use LWP::Simple;
use MIME::Lite;

# Check number of arguments and print usage if needed
my $num_args = $#ARGV + 1;
if ($num_args != 3) {
  print "\nUsage: lotto.pl <file with lotto rows> ";
  print "<file with joker rows> <file with e-mail addresses>\n";
  exit;
}

# Read played lotto rows from a file
open(FILE,$ARGV[0]) or die "file cannot be opened.";
my @tippadeRader = <FILE>;
close (FILE);


# Read played joker rows from a file
open(FILEJOKER,$ARGV[1]) or die "file cannot be opened.";
my @jokerRader = <FILEJOKER>;
close (FILEJOKER);

# Read e-mail addresses from a file
open(MAILFILE,$ARGV[2]) or die "file cannot be opened.";
my @mailAdresser = <MAILFILE>;
close (MAILFILE);

my $i = 0;
my @formatteradeAdresser = ();

# Store mail addresses in an array
foreach my $mail (@mailAdresser)
{
  chomp($mail);
  $formatteradeAdresser[$i] = $mail;
  $i++;
}

my $sendlist = "";

# Compose a sendlist
for($i=0;$i<scalar(@formatteradeAdresser);$i++)
{
  if($i<(scalar(@formatteradeAdresser)-1))
  {
    $sendlist = sprintf("%s%s,", $sendlist, $formatteradeAdresser[$i]);
  }
  else
  {
    $sendlist = sprintf("%s%s", $sendlist, $formatteradeAdresser[$i]);
  }
}

# Call the python script to get the result
my $sms = `/home/$ENV{'USER'}/lotto/lotto.py`;

# Create mail/sms
my $msg = MIME::Lite->new(From     =>'Lotto',
                          To       =>$sendlist,
                          Cc       =>'',
                          Subject  =>'Lottoresultat',
                          Data     =>$sms);

# Send the mail/sms
$msg->send;

