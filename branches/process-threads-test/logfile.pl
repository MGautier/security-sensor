#!/usr/bin/perl -w

$LOGFILE = "server.log";
open(LOGFILE) or die("Could not open log file.");
foreach $line (<LOGFILE>) {

    ($site, $logName, $fullName, $date, $gmt, $req, $file, $proto, $status, $length) = split(' ',$line);
    $time = substr($date, 13);
    $date = substr($date, 1, 11);
    $req  = substr($req, 1);
    chop($gmt);
    chop($proto);
    # do line-by-line processing.
    print "Result: ".$site." ".$logName." ".$fullName." ".$date." ".$gmt." ".$req." ".$file." ".$proto." ". $status." ".$length."\n";
    print "Datetime: ".$time." ".$date." ".$req."\n";
}
close(LOGFILE);
