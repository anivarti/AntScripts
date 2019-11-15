#!/usr/bin/perl

use strict;

my $dir = $ARGV[0];
my @files = `find $dir -type f`;
my %filehash;
my $cnt = 0;
my $newfile;
foreach my $file (@files) {
	chomp($file);
        my $orig = $file;
        if ( $file =~ / / or $file =~ /\[/ or $file =~ /\(/ ) { 
        $newfile = $file;
        $newfile =~ s/ /_/g;
        $newfile =~ s/\[/_/g;
        $newfile =~ s/\]/_/g;
        $newfile =~ s/\(/_/g;
        $newfile =~ s/\)/_/g;
	$newfile =~ s/\'/_/g;
	$newfile =~ s/&/_/g;
	$file =~ s/\[/\\\[/g;	
	$file =~ s/\]/\\\]/g;
	$file =~ s/\(/\\\(/g;
	$file =~ s/\)/\\\)/g;
	$file =~ s/ /\\ /g;
	$file =~ s/\'/\\'/g;
	$file =~ s/&/\\&/g;
	$filehash{$file} = 1;
        if ( -f "$orig") {
        print "moving file $file ...\n";        
	system("mv $file $newfile");
        }
        }
}
