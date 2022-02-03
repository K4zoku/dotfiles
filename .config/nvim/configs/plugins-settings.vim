" Theme: {{{
"let ayucolor="light"  " for light version of theme
"let ayucolor="mirage" " for mirage version of theme
let ayucolor="dark"   " for dark version of theme
autocmd vimenter * ++nested colorscheme ayu
" }}}

" Minimap: {{{
" let g:minimap_auto_start=1
" let g:minimap_auto_start_win_enter=1
" }}}

" NERDTree: {{{
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists('s:std_in') |
    \ execute 'NERDTree' argv()[0] | wincmd p | enew | execute 'cd '.argv()[0] | endif

let g:NERDTreeWinSize=40
" }}}

" Coc.nvim: {{{
" Map Ctrl + Space để show list functions/biến autocomplete
inoremap <silent><expr> <c-space> coc#refresh()

" Tự động import file của biến/function khi chọn và nhấn Tab
inoremap <expr> <TAB> pumvisible() ? "\<C-y>" : "\<C-g>u\<TAB>"

" Hightlight con tro
autocmd CursorHold * silent call CocActionAsync('highlight')

" Use tab for trigger completion with characters ahead and navigate.
inoremap <silent><expr> <TAB>
      \ pumvisible() ? "\<C-n>" :
      \ <SID>check_back_space() ? "\<TAB>" :
      \ coc#refresh()
inoremap <expr><S-TAB> pumvisible() ? "\<C-p>" : "\<C-h>"

function! s:check_back_space() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1]  =~# '\s'
endfunction

"Multi cursor
hi CocCursorRange guibg=#282a36 guifg=#f8f8f2
nmap <expr> <silent> <C-d> <SID>select_current_word()
function! s:select_current_word()
  if !get(b:, 'coc_cursors_activated', 0)
    return "\<Plug>(coc-cursors-word)"
  endif
  return "*\<Plug>(coc-cursors-word):nohlsearch\<CR>"
endfunc

" Enhance bracket
inoremap <silent><expr> <cr> pumvisible() ? coc#_select_confirm()
				\: "\<C-g>u\<CR>\<c-r>=coc#on_enter()\<CR>"

" }}}

" AirLine: {{{
"
let g:airline_powerline_fonts = 1
" }}}


" Discord Rich Presence: {{{
"
" let g:presence_neovim_image_text = "n-words vim (nvim) - Nuoc tay rua bon cau mau den"
" }}}
