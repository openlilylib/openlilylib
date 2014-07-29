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

#(define dummy-usage-variable #f)
% This is a temporary variable to start harvesting the definition section from here

% Define message strings to pretty-print console output
#(define isc-separator "######")

#(define (isc-top-separator heading)
   (format "\n~a\n# ~a\n" isc-separator heading))

#(define isc-bottom-separator (format "#\n~a\n\n" isc-separator))
  

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

   It is basically a syntax for entering short comments,
   and it enables devMode to color the corresponding grob
   with the default 'dev-mode-color-comment color.
   When devMode is active this can be used to access the source comment
   through point-and-click.
%}
comment =
#(define-music-function (parser location grob comment)
   (string? string?)
   (if dev-mode
       #{
         \once \override $grob #'color = #dev-mode-color-comment
       #}
       #{
         % issue void music expression
       #}))

%{ \discuss
   Post an editor's comment in the source file and attach it to a grob.
   It is very similar to \comment, but additionally issues a warning to the console.
   The comment parameter isn't used in the function because it is visible in the
   warning anyway. It should be used as a reminder for musical (or technical) issues that
   should still be taken care of.
   The comment will be shown as part of the "location" excerpt in the console output,
   so it hould be a rather short string. If there is the need for a longer comment, it should
   be entered as a regular (multi-line) comment and only referenced
   in the function.
   devMode also colors the grob with #dev-mode-color-discuss.
   When the issue is dealt with, \discuss should be either removed or changed to \comment,
   but without devMode it doesn't have any effect on the layout.
%}
discuss =
#(define-music-function (parser location grob comment)
   (string? string?)
   (ly:message (isc-top-separator "Editor's remark:"))
   (ly:input-message location "")
   (ly:message isc-bottom-separator)
   (if dev-mode
       #{
         \once \override $grob #'color = #dev-mode-color-discuss
       #}
       #{
         % issue void music expression
       #}))

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
   (ly:message (isc-top-separator "Editor's TODO item:"))
   (ly:input-warning location "")
   (ly:message isc-bottom-separator)
   #{
     \once \override $grob #'color = #dev-mode-color-todo
   #})

%{
  \followup
  Post an editor's comment in the source file in reply to a comment
  entered through one of the preceding functions.

  Usage: \followup author comment

  Unlike these a \followup isn't attached to a grob, but issues a compiler message.
  This can be used to comment on comments and see have an overview in the console window.
  It probably works best when placed at the beginning of a new line.
  the comment argument isn't used in the function but shown in the console as
  the 'relevant' part of the input file
%}

followup =
#(define-music-function (parser location author comment)
   (string? string?)
   (ly:message (isc-top-separator "Follow-up:"))
   (ly:input-message location "")
   (ly:message isc-bottom-separator)
   #{
     % issue void music expression
   #})
