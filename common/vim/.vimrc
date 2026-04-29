
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                                                        "
"                  My Vimrc                              "
"                                                        "
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" For more options see ":help option-list" and ":options".

set nocompatible
filetype plugin indent on

" Save 1,000 items in history
set history=1000

" Show the line and column number of the cursor position
set ruler

" Keep paste mode on by default for your usual paste-heavy workflow.
set paste

" Display the incomplete commands in the bottom right-hand side of your screen
set showcmd

" Display completion matches on your status line
set wildmenu

" Auto Complete To The Longest Available Character For Widemenu
" set wildmode=list:longest,full

" Show a few lines of context around the cursor
" set scrolloff=5

" Highlight search matches
" set hlsearch

" Enable incremental searching
set incsearch

" Ignore case when searching
set ignorecase

" Override the 'ignorecase' option if the search pattern contains upper case characters
set smartcase

" Disable audible bell because it's annoying.
set noerrorbells visualbell t_vb=

" Enable mouse support which can sometimes be convenient.
" set mouse+=a

" Turn on line numbering
set number

" Turn on file backups
" set backup

" Change backup extension
" set bex=[SOMETHING]

" Don't line wrap mid-word
set lbr

" Copy the indentation from the current line
set autoindent

" Enable smart autoindenting
set smartindent

" Use spaces instead of tabs (especially useful for Python)
set expandtab

" Enable smart tabs (Insert Tab at the beginning of the line, use spaces in  other places.)
set smarttab

" Make a tab equal to 4 spaces
set shiftwidth=4
set tabstop=4
set softtabstop=4

set showmatch           " highlight matching [{()}]

set splitbelow          " Open new vertical split bottom
set splitright          " Open new horizontal splits right

" Show tab with ^I and append $ to the end of each line
" set list

" Replace all tabs with spaces (useful when a project require use certain number of  spaces to replace Tab)
" set expandtab

" When expandtab is enabled, configure the number of spaces inserted after  pressing Tab
" set softtabstop=4

" Specifiy a color scheme
colorscheme slate

" Tell vim what background you are using
" set bg=light
set bg=dark

" Map Y to act like D and C, i.e. yank until EOL, rather than act like yy
" map Y y$

" Remap VIM 0 to first non-blank character
" map 0 ^

" Quickly save your file
map <leader>w :w!<cr> " By default, <leader> is the \ key.

" map <leader>/ to :/
nnoremap <leader>/ :/

" map <leader>a to Ack!
nnoremap <leader>a :Ack! <c-r><c-w><cr>

" map <leader>g to grep
nnoremap <leader>g :grep <c-r><c-w> */**<cr>

" Hide buffer unsaving warning except quitting
set hidden

syntax enable " Enable syntax highlighting
filetype plugin indent on " Enable filetype detection and indentation

" Disable the default Vim startup message.
set shortmess-=I

" Always show the status line at the bottom, even if you only have one window open.
set laststatus=2

" Use @c to quickly copy all content
let @c = ':1,$y+'

" Set language to en_US
set langmenu=en_US.UTF-8
language en_US.UTF-8

" Prettier long sentence
set display+=lastline

" Have lines wrap instead of continue off-screen
set linebreak

set ttyfast             " Improve redrawing

nmap Q <Nop>
" 'Q' in normal mode enters Ex mode. You almost never want this.
" Unbind for tmux
map <C-a> <Nop>
map <C-x> <Nop>

" set swap file location
set directory=$HOME/.vim/swap//

" Enable permanent undo for all files
set undofile
if !isdirectory("$HOME/.vim/undodir")
  call mkdir("$HOME/.vim/undodir", "p")
endif
set undodir="$HOME/.vim/undodir"

" 针对手动管理插件
" packloadall               " 加载所有插件
" silent! helptags ALL      " 为所有插件加载帮助文档

" 关闭缓冲区而不关闭窗口（使用`:Bd`关闭缓冲区而不关闭窗口）
command! Bd :bp | :sp | :bn | :bd

" 添加折叠功能
" set foldmethod=diff " 对比代码时，折叠显示相同之处
" set foldmethod=manual " 手动折叠，不适用于长文本
set foldmethod=indent " 基于缩进的折叠（适用于python）
" set foldmethod=expr " 基于正则表达式的折叠
" set foldmethod=marker " 基于文本中特殊的符号进行折叠（如{{{和}}}，但在除了.vimrc之外的地方不常用）
" set foldmethod=syntax " 提供可识别语法的折叠（不适用于python）

let NERDTreeShowBookmarks = 1 " 启动NERDTree时显示书签

" 如果没安装过vim-plug，则下载安装
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
     \https://raw.GitHub.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" 使用vim-plug管理插件
call plug#begin()
Plug 'mileszs/ack.vim'
Plug 'easymotion/vim-easymotion'
Plug 'tpope/vim-unimpaired'
Plug 'tpope/vim-fugitive'
Plug 'godlygeek/tabular'
Plug 'preservim/nerdtree'
Plug 'junegunn/vim-plug'
Plug 'junegunn/goyo.vim'
Plug 'mbbill/undotree'
Plug 'christoomey/vim-tmux-navigator'
Plug 'tpope/vim-dispatch'
Plug 'janko-m/vim-test'
Plug 'dense-analysis/ale'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'preservim/vim-markdown'
Plug 'dhruvasagar/vim-table-mode'
call plug#end()

" Markdown reading / writing workflow
let g:vim_markdown_folding_level = 6
let g:vim_markdown_toc_autofit = 1
let g:vim_markdown_conceal = 1
let g:vim_markdown_conceal_code_blocks = 0
let g:vim_markdown_follow_anchor = 1
let g:vim_markdown_frontmatter = 1
let g:vim_markdown_toml_frontmatter = 1
let g:vim_markdown_json_frontmatter = 1
let g:vim_markdown_strikethrough = 1
let g:vim_markdown_autowrite = 1
let g:vim_markdown_no_extensions_in_markdown = 1
let g:vim_markdown_edit_url_in = 'current'
let g:vim_markdown_borderless_table = 1

" Force Markdown-friendly table borders.
let g:table_mode_corner = '|'

function! s:set_markdown_paste(enabled) abort
  if a:enabled
    set paste
    echo 'Markdown workflow: paste on'
  else
    set nopaste
    echo 'Markdown workflow: paste off'
  endif
endfunction

function! s:realign_markdown_table() abort
  silent! TableModeRealign
  echo 'Markdown workflow: table realigned'
endfunction

function! s:markdown_table_column_count() abort
  let l:line = getline('.')
  let l:trimmed = trim(l:line)
  if l:trimmed =~# '^|'
    let l:parts = split(l:trimmed, '|')
    return max([len(l:parts) - 2, 2])
  endif
  return 2
endfunction

function! s:insert_markdown_table_row() abort
  let l:columns = <SID>markdown_table_column_count()
  let l:row = '|' . repeat('  |', l:columns)
  call append(line('.'), l:row)
  call cursor(line('.') + 1, 3)
  normal! a
endfunction

function! s:is_at_start_of_line(mapping) abort
  let l:text_before_cursor = getline('.')[0 : col('.') - 1]
  let l:mapping_pattern = '\V' . escape(a:mapping, '\')
  let l:comment_pattern = '\V' . escape(substitute(&l:commentstring, '%s.*$', '', ''), '\')
  return l:text_before_cursor =~? '^' . '\v(' . l:comment_pattern . ')?\s*' . l:mapping_pattern . '$'
endfunction

augroup markdown_workflow
  autocmd!
  autocmd FileType markdown setlocal wrap linebreak nolist
  autocmd FileType markdown setlocal conceallevel=2 concealcursor=nc
  autocmd FileType markdown setlocal foldenable foldlevel=6
  autocmd FileType markdown nnoremap <buffer> <leader>mo :Toc<CR>
  autocmd FileType markdown nnoremap <buffer> <leader>mp :call <SID>set_markdown_paste(1)<CR>
  autocmd FileType markdown nnoremap <buffer> <leader>mn :call <SID>set_markdown_paste(0)<CR>
  autocmd FileType markdown nnoremap <buffer> <leader>ma :call <SID>insert_markdown_table_row()<CR>
  autocmd FileType markdown nnoremap <buffer> <leader>mt :TableModeToggle<CR>
  autocmd FileType markdown nnoremap <buffer> <leader>mr :call <SID>realign_markdown_table()<CR>
  autocmd FileType markdown xnoremap <buffer> <leader>mz :Tableize<CR>
  autocmd FileType markdown inoreabbrev <buffer> <expr> <bar><bar>
        \ <SID>is_at_start_of_line('\|\|') ?
        \ '<c-o>:TableModeEnable<cr><bar><space><bar><left><left>' : '<bar><bar>'
  autocmd FileType markdown inoreabbrev <buffer> <expr> __
        \ <SID>is_at_start_of_line('__') ?
        \ '<c-o>:silent! TableModeDisable<cr>' : '__'
augroup END

" 为Undotree设置快捷键
nnoremap <F8> :UndotreeToggle<CR>

" 使用`:make`时替换默认的语法检查器为pylint
autocmd filetype python let &l:makeprg = "pylint --reports=n --msg-template=\"{path}:{line}:{msg_id}{symbol},{obj}{msg}\" %:p"
autocmd filetype python setlocal errorformat=%f:%l:%m

" 让%支持HTML的<>成对标签（左< 匹配 右>）
set matchpairs+=<:>
" 让%支持自定义的成对符号（如【】，中文方括号）
set matchpairs+=【:】

" 自定义不可见字符显示样式（整合常用+你的原有配置，无冲突）
set listchars=tab:>>,nbsp:~,trail:·,space:·,eol:↵,lead:·
" 说明：tab(制表符)、nbsp(非断行空格)、trail(行尾多余空格)、space(普通空格)、eol(行尾换行符)、lead(行首空格)

" 使用F4一键切换不可见字符显示开关
nnoremap <F4> :set list!

set autochdir " automatically set current directory to directory of last opened file

" quicker window movement
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-h> <C-w>h
nnoremap <C-l> <C-w>l

" Bind hotkeys to open CtrlP
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
