#!/usr/bin/perl
use strict;

my $file = $ARGV[0];
my $rep = "/Volumes/ANANTBLUE4TB/MyPhotos";

open(FP,"$file");
while(<FP>) {
next if /^#/;
chomp;
my $dir = $_;
$dir =~ s/\s/\\ /g;
print "Working on $dir ...\n";
system("/Users/anivarti/bin/piccopy.pl \"$dir\"");
}
close FP;
system("/Users/anivarti/bin/picmove.pl $rep/1969");
my @dirs = `find $rep -type d`;
chdir($rep);
foreach my $dir (@dirs) {
system("cd $rep; /Users/anivarti/bin/findduplicates.pl $dir");
}
