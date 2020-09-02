map SR :source /home/anivarti/.vimrc
map = o#############################################################################j
map + o###                                                                       ###^4lR
map _ o/***************************************************************************/j
map - o/*                                                                         */^3lR
command! -nargs=1 Ss let @/ = escape(<q-args>, '/][')|normal! /<C-R>/<CR>
"command! -nargs=1 Ss let @/ = <q-args>|set hlsearch
"set nowrapscan
