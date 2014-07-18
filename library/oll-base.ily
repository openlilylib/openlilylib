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
  snippet-title = "Undefined"
  snippet-short-description = "Undefined"
  snippet-author = "Undefined"
  snippet-source = "Undefined"
  snippet-description = "Undefined"
  snippet-category = "Undefined"
  snippet-tags = "Undefined"
  snippet-status = "Undefined"
  first-lilypond-version = "Undefined"
  last-lilypond-version = "Undefined"
  snippet-todo = "Undefined"
}
