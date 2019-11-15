#!/usr/bin/perl

use strict;

my $dir = $ARGV[0];
my @files = `ls -1 $dir`;
my %filehash;
my $cnt = 0;
foreach my $file (@files) {
	chomp($file);
	#print ".... $file\n" if ( $file =~ /\(/);
	$file =~ s/\[/\\\[/g;	
	$file =~ s/\]/\\\]/g;
	$file =~ s/\(/\\\(/g;
	$file =~ s/\)/\\\)/g;
	$file =~ s/ /\\ /g;
	$cnt = sprintf("%04d",$cnt);
	system("mv $file IMG_CAM_$cnt.JPG") if( $file =~ /\(/);
	$cnt++ if( $file =~ /\(/);
	print "$file duplicate\n" if (defined $filehash{$file});
	$filehash{$file} = 1;
}
