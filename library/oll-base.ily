\version "2.16.0"

%{
  Basic include file for openlilylib modules.
  It provides common functionality that every module
  should share, e.g. for documentation purposes.
%}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initialization for various aspects of openlilylib

% dev-mode flag
% If this is set to #t in an input file it indicates that the score
% is still under development. openlilylib functions may use this
% (or rather are encouraged to do so) to conditionally highlight affected
% items in the score.
#(cond ((not (defined? 'dev-mode))
        (define dev-mode #f)))

devModeOn = #(define dev-mode #t)

% dev-mode colors
#(cond ((not (defined? 'dev-mode-color-comment))
        (define dev-mode-color-comment darkgreen)))
#(cond ((not (defined? 'dev-mode-color-discuss))
        (define dev-mode-color-discuss green)))
#(cond ((not (defined? 'dev-mode-color-todo))
        (define dev-mode-color-todo magenta)))
#(cond ((not (defined? 'dev-mode-color-switch))
        (define dev-mode-color-switch cyan)))
#(cond ((not (defined? 'dev-mode-color-tweak))
        (define dev-mode-color-tweak blue)))



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Commands for consistency of documentation

% typeset a command name with leading backslash
#(define-markup-command (ollCommand layout props name)(markup?)
   (interpret-markup layout props
     #{
       \markup \typewriter \with-color #blue \concat { "\\" #name }
     #}))

% typeset a ollItem name as a reference to another file in the library
#(define-markup-command (ollRef layout props name)(markup?)
   (interpret-markup layout props
     #{
       \markup \typewriter \with-color #darkred #name
     #}))

% Ensure that all header fields are initialized with a default value.
\header {
  oll-title = "Undefined"
  oll-short-description = "Undefined"
  oll-author = "Undefined"
  oll-source = "Undefined"
  oll-description = "Undefined"
  oll-category = "Undefined"
  oll-tags = "Undefined"
  oll-status = "Undefined"
  first-lilypond-version = "Undefined"
  last-lilypond-version = "Undefined"
  oll-todo = "Undefined"
}
