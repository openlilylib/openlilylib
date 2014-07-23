% Headers for openlilylib documentation pages
% Currently an empty stub

\paper {
  #(include-special-characters)

  bookTitleMarkup = \markup {
    \column {
      { \bold \huge \fromproperty #'header:oll-title }
      { \fromproperty #'header:oll-short-description }

      \concat { \vspace #1.5 "Author(s): " \fromproperty #'header:oll-author }
      
      \section "Introduction:"
      \fromproperty  #'header:oll-description

      \section "Usage:"
      \line { File to include: #includeName }
      \vspace #1
      \fromproperty #'header:oll-usage
      \vspace #1
    }
  }
}

\header {
  copyright = \markup { Part of \typewriter openlilylib - licensed under the
                      CreativeCommons ... }
}
