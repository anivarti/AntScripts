#!/usr/bin/perl 

use warnings;
use strict;

use Digest::MD5;
use File::Find;
use PerlIO::gzip;

use vars qw/ $md5_file_ref $filename_md5_ref 
         $file_count $file_add $file_del 
         $file_lost /;

sub find_found;
sub load_md5 ($);
sub save_md5 ($);

sub save_md5 ($) {
 my $FILENAME = shift;

 my $FILE = ();
 open $FILE, ">:gzip", $FILENAME;

 foreach (keys %$md5_file_ref) {
   printf $FILE "%s|||%s\n", $_, $md5_file_ref->{$_};
 }
 close $FILE;
}

sub load_md5 ($) {
 my $FILENAME = shift;

 my $FILE = ();
 my $count = 1;

 open $FILE, "<:gzip", $FILENAME;

 while (<$FILE>) {
   chomp;
   my ($tmp_col1, $tmp_col2) = split '\|\|\|', $_;
   $md5_file_ref->{$tmp_col1} = $tmp_col2;
   $filename_md5_ref->{$tmp_col2} = $tmp_col1;
   $count++;
 }
 close $FILE;
 print "Loaded $count entries\n";
}

sub verify_files {
 foreach my $FILE (keys %$filename_md5_ref) {
   unless (-f $FILE) {
    my $md5 = $filename_md5_ref->{$FILE};
    delete $md5_file_ref->{$md5};
    delete $filename_md5_ref->{$FILE};
    print "   *** Not found: $FILE\n";
    $file_lost++;
   }
 }
}

sub find_found {
 my $FILE = $_;

 my $file_md5 = ();

 if ( -r $FILE && -f $FILE) {
   unless ($filename_md5_ref->{$FILE}) {
     open(FILE, $FILE)
       or return;
     binmode(FILE);
     $file_md5 = Digest::MD5->new->addfile(*FILE)->hexdigest;
     close(FILE);
     if ( $md5_file_ref->{$file_md5}) {
       chmod(0666, $FILE);
       if (unlink $FILE) {
         print "\n",
           "     *** DELETING ***\n",
           "   Duplicate file: $FILE\n",
           "     *** DELETING ***\n\n";
         $file_del++;
       } else {
         warn "Unable to delete $FILE\n\n";
       }
      } else {
       print "Added $file_md5 $FILE\n";
       $md5_file_ref->{$file_md5} = $FILE;
       $filename_md5_ref->{$FILE} = $file_md5;
       $file_add++;
     }
  }
  $file_count++;
 }
}

#####################
#####################
#####################

$file_count = 0;
$file_del = 0;
$file_add = 0;
$file_lost = 0;

my $FILE = "dups.csv.gz";

if ( -r $FILE && -f $FILE) {
 load_md5($FILE);
 verify_files;
}

find {
 bydepth         => 1,
 no_chdir        => 1,
 wanted          => \&find_found
} => @ARGV;

print "\nTOTAL files: $file_count\n";
print "  Added files: $file_add\n";
print "  Deleted files: $file_del\n";
print "  Files not found: $file_lost\n\n";
save_md5($FILE);
