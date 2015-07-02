#!/usr/bin/perl -w

$LOGFILE = "source.log";
open(LOGFILE) or die("Could not open log file.");
foreach $line (<LOGFILE>){
    ($month, $day, $hour) = split(' ',$line);
    print "$month $day $hour \n";
}
close(LOGFILE);
