#!/usr/bin/perl

use strict;

my $rep = "/Volumes/ANANT2015/MyPictures";
die "Error: $rep/counter file not found enter the latest count in the same file\n" if (!-f "$rep/counter");
my $cnt = `cat $rep/counter`;
chomp($cnt);



foreach my $dir (@ARGV) {
        my @files = `find $dir -type f`;
        my %filehash;
        my %bfilehash;
        my $m;my $n;my $newfile;
        foreach my $file (@files) {
        chomp($file);
        next if ( $file !~ /jpeg$|jpg$|png$|tiff$|tif$|gif$|mov$|3gp$|aae$|flv$|mkv$|avi$|wmv$|mp4$/i);
        my $orig = $file;
        $newfile = $file;
        ### check for any special characters in the file
        if ( $file =~ / / or $file =~ /\[/ or $file =~ /\(/ ) { 
        $newfile =~ s/ /_/g;
        $newfile =~ s/\[/_/g;
        $newfile =~ s/\]/_/g;
        $newfile =~ s/\(/_/g;
        $newfile =~ s/\)/_/g;
	$newfile =~ s/\'/_/g;
	$newfile =~ s/\&/_/g;
	$file =~ s/\[/\\\[/g;	
	$file =~ s/\]/\\\]/g;
	$file =~ s/\(/\\\(/g;
	$file =~ s/\)/\\\)/g;
	$file =~ s/ /\\ /g;
	$file =~ s/\'/\\'/g;
	$file =~ s/\&/\\\&/g;
        }
        if ( -f "$orig") {
        print "$orig\n";        
        ### Fix file names
        my $bfile = `basename $newfile`;
        chomp($bfile);
        next if ( $bfile =~ /^\./);
        my @foo = split/\./,$bfile;
        $bfile = join(".$cnt.",@foo);
        $m = (stat $file)[9];
        $filehash{$file} = $m;
        $bfilehash{$file} = $bfile;
        $cnt++;
        }
        }
        system("echo $cnt > $rep/counter");        
        print "#### Sorted File List\n";
        foreach my $file (sort { $filehash{$a} <=> $filehash{$b} } keys %filehash) {
        my $n = localtime($filehash{$file});
        my @foo = split /\s+/,$n;
        system("mkdir -p $rep/$foo[4]/$foo[1]") if (! -d "$rep/$foo[4]/$foo[1]"); 
        system("cp -pf $file $rep/$foo[4]/$foo[1]/$bfilehash{$file}");
        }
}
