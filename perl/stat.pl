use File::stat;
my $sb = stat($ARGV[0]);
printf "File is %s, size is %s, perm %04o, mtime %s\n", $filename, $sb->size, $sb->mode & 07777, scalar localtime $sb->mtime;
$m = $sb->mtime;
my $n = localtime($m);
print "$m : $n\n";

