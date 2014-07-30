\version "2.18.0" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "Cross-voice elements"
  oll-short-description = \markup \justify {
    Workaround to simplify typesetting of elements across voices.
  }
  oll-author = "Urs Liska"
  oll-source = "Scores of Beauty post - to-be-written"
  oll-description = \markup \justify {
    LilyPond can engrave some sort of spanner object (e.g. slurs, dynamic
    hairpins, glissandi etc.) only within the same voice context. Therefore
    it requires a workaround to make such items appear to cross voices,
    namely the use of a hidden voice. The suggestion to use \ollCommand
    hideNotes is misleading: as this only makes the notation objects
    \italic transparent they are still considered for collision avoidance,
    which results for example in invisible flags being avoided by ties etc.

    This file provides the command \ollCommand hideVoiceForCrossVoice which
    removes the stencils for all necessary grobs for the following note
    or music expression. Additionally it suppresses the warnings about
    clashing note columns that usually arise from such constructs.
  }
  oll-usage = \markup \justify {
    Write \ollCommand "hideVoiceForCrossVoice <grobname> <music>"
    immediately before the note that starts the cross-voice element.
    \typewriter <grobname> denotes the type of grob that will cross
    the voices, \typewriter <music> can be a single note or a compound
    music expression.
  }
  oll-category = "workarounds"
  % add comma-separated tags to make searching more effective.
  % preferrably use tags that already exist (see ???).
  % tag names should use lowercase and connect words using dashes.
  oll-tags = "cross-voice,ties,spanners,lines"
  % is this snippet ready?  See ??? for valid entries
  oll-status = ""

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


% This looks like just an alias for hideNotes
% But it is used especially for use in tying/slurring between voices
% In addition to hideNotes it removes everything except
% the notehead completely (namely the Flag which often
% disturbs this construct)
% and is \once
% Furthermore it suppresses a warning about clashing note columns
% as this will surely surely the case when using this shorthand for cross voice curves

hideVoiceForCrossVoice =
#(define-music-function (parser location grob music)(string? ly:music?)
   (display dev-mode)
   (if dev-mode
       #{
         \omit Stem
         \omit Dots
         \omit Beam
         \omit Flag
         \temporary \override NoteColumn #'ignore-collision = ##t
         \temporary \override NoteHead #'layer = 100
         \temporary \override NoteHead #'color = #dev-mode-color-switch
         \temporary \override $grob #'color = #dev-mode-color-switch
         #music
         \undo \omit Stem
         \undo \omit Dots
         \undo \omit Beam
         \undo \omit Flag
         \revert NoteColumn.ignore-collision
         \revert NoteHead.layer
         \revert NoteHead.color
         \revert $grob #'color
       #}
       #{
         \once \override NoteHead #'transparent = ##t
         \once \override Stem #'stencil = ##f
         \once \override Dots #'stencil = ##f
         \once \override Beam #'stencil = ##f
         \once \override Flag #'stencil = ##f
         \once \override NoteColumn #'ignore-collision = ##t
         #music
       #}))
