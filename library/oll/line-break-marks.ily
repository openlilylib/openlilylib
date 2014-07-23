\version "2.16.0"

\include "oll-base.ily"

\header {
  oll-title = "Diplomatic line break indicator"
  oll-author = "Urs Liska"
  oll-short-description = \markup {
    Draw a dashed vertical line to indicate a line break
    in the original source.
  }
  
  oll-description = \markup \justify {
    When editing sketches and drafts one usually wants to indicate the
    line breaks of the original source. This can be achieved by either
    duplicating the original breaks in the engraving or by indicating
    the positions of the breaks with dedicated graphical signs.
    
    This snippet draws a dashed vertical line above the staff, which is
    a common notation for this purpose. Its use is independent from the
    position in the measure and can not only appear at barlines. Internally
    a custom rehearsal mark is used.
  }
  
  oll-usage = \markup \justify {
    Simply enter \ollCommand lineBreakMark at the musical position where
    you want the sign to appear. The example demonstrates that you can place
    it anywhere in the measure, and that it doesn't  interfere with regular
    rehearsal marks.
  }
  
  oll-category = "editorial-tools"
  oll-tags = "diplomatic-transcription,line-breaks,alignments"
  oll-status = "ready"
  
  oll-todo = \markup \justify {
    Currently the appearance of the dashed line cannot be configured.
    It would be nice if that could also be achieved using named styles.
  }
}

lineBreakMark = {
  \once \override Score.RehearsalMark.padding = #0
  \mark \markup {
    \override #'(on . 0.25)
    \override #'(off . 0.15)
    \override #'(thickness . 1.6)
    \draw-dashed-line #'(0 . 3)
  }
}
