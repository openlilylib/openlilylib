\version "2.17.3"

% TODO: add oll/snippets headers, add example. Move description to README? Split into several files?

\include "../includes/ulLibrary/draftMode_colors.ily"

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Variable definitions for use throughout this file
% We define a few variables to provide coherence

% Font size for smaller items
#(define smF -3)

% Definition of the dash pattern
edDashDefinition = #'(( 0 1 0.5 1.25 ))

%TODO: separate the 'productivity' tools and create a new file inSourceCommunication.ily




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 'Generic' additions by the editor
% These are considered deprecated, because - as there will be more definitions of grobs
% there will be more chances of several grobs starting at the same musical moment.
% So it is preferred to  define individual functions for different grobs.
% Additions by the Editor are marked by a smaller font-size

% beginEditorialAddition
bEdAdd = {
  \override NoteHead #'font-size = #smF
  \override Rest #'font-size = #smF
  \override Stem #'font-size = #smF
  \override Beam #'font-size = #smF
  %TODO: Are there more elements to resize?
}
% endEditorialAddition
eEdAdd = {
  \revert NoteHead #'font-size
  \revert Rest #'font-size
  \revert Stem #'font-size
  \revert Beam #'font-size
}
% single EditorialAddition
EdAdd = {
  \once \override NoteHead #'font-size = #smF
  \once \override Rest #'font-size = #smF
  \once \override Stem #'font-size = #smF
  \once \override Beam #'font-size = #smF
}

% Curves added by the editor are dashed
% We don't use the predefined commands to have more control over the dash definition
% and for draftMode to be able to color it

% Editorial Slur
edSlur = {
  \once \override Slur #'dash-definition = \edDashDefinition
  \once \override Slur #'thickness = #1.7
}

% Editorial PhrasingSlur
edPhrasingSlur = {
  \once \override PhrasingSlur #'dash-definition = \edDashDefinition
  \once \override PhrasingSlur #'thickness = #1.7
}

% Editorial Tie
edTie = {
  \once \override Tie #'dash-definition = \edDashDefinition
  \once \override Tie #'thickness = #1.7
}

%TODO: Add support for LaisserVIbrerTie and repeatTie


%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Articulation

edArticulation =
#(define-music-function (parser location mus)
   (ly:music?)
   #{
     \parenthesize #mus
   #})


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Lines

% editorialHairPin
edHP = {
  \once \override Hairpin #'style = #'dashed-line
}

% editorialStaffSwitch
edSS = {
  \once \override VoiceFollower #'style = #'dashed-line
  \once \override VoiceFollower #'dash-period = #1.8
  \once \override VoiceFollower #'dash-fraction = #0.5
}

% editorial arpeggio
% Place \edArpeggio immediately before the arpeggiated chord
% Function provided by David Nalesnik

edArpeggio= {
  \once \override Arpeggio #'stencil =
  #(lambda (grob)
     (parenthesize-stencil (ly:arpeggio::print grob) 0.1 0.5 0.5 0.2))
  \once \override Arpeggio #'before-line-breaking =
  #(lambda (grob)
     (set! (ly:grob-property grob 'X-extent)
           (ly:stencil-extent (ly:grob-property grob 'stencil) X)))
}

% editorial Fermata
% Place \edFermata immediately before the musical moment
% Works on \fermata as well as \fermataMarkup

edFermata = {
  \once \override Script #'font-size = #-2
  \once \override MultiMeasureRestText #'font-size = #-2
}

edTuplet = {
  \once \override TupletBracket #'style = #'dashed-line
}

% Editorial Stem
% As a Stem can't be dashed one has to attach a dashed line to it
% The music function has been provided by David Nalesnik
% and enhanced by Thomas Morley and David Kastrup
% The line width automatically reflects the original Stem's
% and the dash pattern can be given as arguments
% Note: It is in the caller's responsibility to make sure
% that the dashed stem's end matches the end of the stem
% (and isn't broken or ended with a gap)

#(define (make-round-filled-box x1 x2 y1 y2 blot-diameter)
   (ly:make-stencil (list 'round-filled-box (- x1) x2 (- y1) y2 blot-diameter)
     (cons x1 x2)
     (cons y1 y2)))

#(define (build-pos-list len on off)
   (let helper ((lst '()) (next 0) (on on) (off off))
     (if (< next len)
         (helper (cons next lst) (+ next on) off on)
         (reverse! lst (list len)))))

#(define (dashed-stem on off)
   (lambda (grob)
     (let* ((blot (ly:output-def-lookup (ly:grob-layout grob) 'blot-diameter))
            (stencil (ly:stem::print grob))
            (X-ext (ly:stencil-extent stencil X))
            (thickness (interval-length X-ext))
            (Y-ext (ly:stencil-extent stencil Y))
            (len (interval-length Y-ext))
            (new-stencil empty-stencil)
            (factors (build-pos-list len on off)))

       (define (helper args)
         (if (<= 2 (length args))
             (begin
              (set! new-stencil
                    (ly:stencil-add
                     new-stencil
                     (ly:stencil-translate-axis
                      (make-round-filled-box (/ thickness -2) (/ thickness 2)
                        (car args) (cadr args)
                        blot)
                      (interval-start Y-ext)
                      Y)))
              (helper (cddr args)))
             new-stencil))

       (if (or (zero? on) (zero? off))
           stencil
           (helper factors)))))

edStem =
#(define-music-function (parser location on off) (number? number?)
   #{
     \once \override Stem #'stencil = #(dashed-stem on off)
   #})
