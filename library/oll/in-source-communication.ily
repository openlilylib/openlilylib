\version "2.16.2" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "In-source communication"
  oll-short-description = \markup \justify {
    Add annotations and comments to elements of a score.
  }
  oll-author = "Urs Liska"
  oll-source = ""
  oll-description = \markup \justify {
    This module contains commands to enter annotations and comments to elements of
    a score.
  }
  oll-usage = \markup \justify {
    
  }
  % add one single category.
  % see ??? for the list of valid entries
  oll-category = "markup"
  % add comma-separated tags to make searching more effective.
  % preferrably use tags that already exist (see ???).
  % tag names should use lowercase and connect words using dashes.
  tags = "string, markup, utility"
  % is this snippet ready?  See ??? for valid entries
  status = "unfinished"

  % add information about LilyPond version compatibility if available
  first-lilypond-version = ""
  last-lilypond-version = ""

% optionally add comments on issues and enhancements
  oll-todo = ""
}

%%%%%%%%%%%%%%%%%%%%%%%%
% here goes the snippet:
% Anything below this line will be ignored by generated documentation.
% The snippet itself should (usually) *not* produce any output because
% it will be included in end-user files. To provide usage examples
% please create a file with the same name but an .ly extension
% in the /usage-examples directory.
%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Editorial productivity tools: comment, discuss, todo and poke

%{ \comment
   Post an editor's comment in the source file and attach it to a grob.
   Meant for communication between different editors of a file
   and for musically documenting the source file.

   Usage: \comment grob-name comment. Place immediately before the grob in question.
          \comment DynamicText "mf according to autograph" a\mf

   grob-name
   is the name of the affected grob (works with or without quotation marks)
   comment
   isn't used in the function itself, but only serves as the practical place for the comment,
   which is also consistent with \discuss and \todo, so the are interchangeable.
   Should be a rather short string. If there is the need for a longer comment, it should
   be entered as a regular (multi-line) comment and only referenced
   in the function.

   It is basically a syntax for entering short comments,
   and it enables draftMode to color the corresponding grob
   with the default #editorial-remark-color
   In this file it is just a void music function,
   necessary to provide a coherent input syntax
%}
comment =
#(define-music-function (parser location grob comment)
   (string? string?)
   #{
     % issue void music expression
   #})

%{
  \discuss
  Post an editor's comment in the source file and attach it to a grob.
  It is very similar to \comment, but additionally issues a warning to the console.
  The comment parameter isn't used in the function because it is visible in the
  warning anyway. It should be used as a reminder for musical (or technical) issues that
  should still be taken care of.
  DraftMode also colors the grob with #editorial-remark-color.
  When the issue is dealt with, \discuss should be either removed or changed to \comment,
  but without draftMode it doesn't have any effect on the layout.
%}

discuss =
#(define-music-function (parser location grob comment)
   (string? string?)
   (ly:input-warning location "Editor's remark")
   #{
     % issue void music expression
   #})

%{
  \todo
  Post a comment in the source file and attach it to a grob.
  Meant for communication between different editors of the file

  Same as \discuss, but the act of coloring is hard-coded here and not left for draft mode
  (while the color itself could be overridden in the source).
  This is because \todo indicates an issue that must be solved.
  So it should be also visible in pub mode to indicate that isn't solved yet.
  When the issue is solved \todo must be removed or renamed to \comment
%}

todo =
#(define-music-function (parser location grob comment)
   (string? string?)
   (ly:input-warning location "Editor's warning")
   #{
     \once \override $grob #'color = #todo-warning-color
   #})

%{
  \followup
  Post an editor's comment in the source file in reply to a comment
  entered through one of the preceding functions.

  Usage: \followup author comment

  Unlike these a \followup isn't attached to a grob, but issues a compiler warning.
  This can be used to comment on comments and see have an overview in the console window.
  It probably works best when placed at the beginning of a new line.
  the comment argument isn't used in the function but shown in the console as
  the 'relevant' part of the input file
%}

followup =
#(define-music-function (parser location author comment)
   (string? string?)
   (ly:input-warning location author)
   #{
     % issue void music expression
   #})

%{ \poke
   Similar to Facebook's poke function
   this command is used to bring someone's attention to a speficic item

   Usage: \poke grob-name. Place immediately before the grob in question.
          \poke Slur ...

   grob-name
   is the name of the affected grob (works with or without quotation marks)

   \poke enables draftMode to color the corresponding grob
   with the special #poke-color
   In this file it is just a void music function,
   necessary to provide a coherent input syntax
%}
poke =
#(define-music-function (parser location grob)
   (string?)
   #{
     % issue void music expression
   #})

