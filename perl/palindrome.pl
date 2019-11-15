#!/usr/bin/perl

use strict;

my $foo = $ARGV[0];

die "Error please input a string" if ($ARGV[0] eq "");

print "Detecting if $ARGV[0] is a palindrome or not\n";

my @foo = split //,$ARGV[0];

#print "$#foo\n";
my $result = 1;
for (my $i=0; $i<=int($#foo+1/2); $i++) {
        print "$ARGV[0] is not a palindrome \n" if ($foo[$i] ne $foo[$#foo-$i]); 
        $result = 0 if ($foo[$i] ne $foo[$#foo-$i]); 
        last if ($foo[$i] ne $foo[$#foo-$i]); 
}

print "Success: $ARGV[0] is a palindrome\n" if ($result == 1);
