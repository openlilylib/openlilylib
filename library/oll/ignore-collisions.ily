\version "2.16.2" % absolutely necessary!

\include "oll-base.ily"

\header {
  oll-title = "Ignore Collision(s)"
  oll-author = "Urs Liska"
  oll-short-description = "Suppress warnings about clashing note columns"
  oll-description = \markup \justify {
    LilyPond issues warnings when two or more notes share the same note column.
    However, sometimes it is necessary to do that deliberately, for example when
    doing some polyphony tricks. In this case it is useful to suppress the warnings
    so that the - expected - warnings don't "\"hide\"" the real ones.

    This snippet provides shorthands to simplify the handling of such situations.
  }
  oll-usage = \markup \justify {
    \ollCommand ignoreCollision will suppress a compiler warning about clashing
    note columns that is triggered immediately afterwards. The command affects
    only the current voice, so it is very to the point of the expected note column
    clash. Usually that is the  preferred way to use this snippet. When \typewriter
    devMode is active \ollCommand ignoreCollision will be colored with \typewriter
    {dev-mode-color-comment.}
    \ollCommand ignoreCollisions will suppress \italic all compiler warnings (about clashing note
    columns) until \ollCommand warnOnCollisions is used. Use this variant with care
    as it will also suppress valid warnings that you may \italic not expect.
  }
  oll-category = "input-shorthand"
  oll-tags = "notecolumn, compiler-warning"
  oll-status = "ready"
}

%%%%%%%%%%%%%%%%%%%%%%%%%%
% here goes the snippet: %
%%%%%%%%%%%%%%%%%%%%%%%%%%


% Suppress a warning about clashing note columns
% Use when you deliberately use clashing note columns
% e.g. when merging voices to one stem
% or when hiding voices (although for tying the
% \hideVoiceForTie approach is recommended)
%
ignoreCollision =
#(define-music-function (parser location)()
       (if dev-mode
       #{
          \once \override NoteHead #'color = #dev-mode-color-comment
          \once \override NoteColumn #'ignore-collision = ##t
       #}
       #{
          \once \override NoteHead #'color = #dev-mode-color-comment
       #}))


% Use this one with care, as it will prevent lilypond from
% warning you about real problems
ignoreCollisions = \override NoteColumn #'ignore-collision = ##t
warnOnCollisions = \override NoteColumn #'ignore-collision = ##f
