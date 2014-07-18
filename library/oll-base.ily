\version "2.16.0"

%{
  Basic include file for openlilylib modules.
  It provides common functionality that every module 
  should share, e.g. for documentation purposes.
%}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Commands for consistency of documentation

% typeset a command name with leading backslash
#(define-markup-command (ollCommand layout props name)(markup?)
   (interpret-markup layout props
     #{
       \markup \typewriter \with-color #blue \concat { "\\" #name }
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
