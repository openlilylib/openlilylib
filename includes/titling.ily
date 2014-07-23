% Headers for openlilylib documentation pages
% Currently an empty stub

\paper {
  #(include-special-characters)

  bookTitleMarkup = \markup {
    \column {
      { \bold \huge \fromproperty #'header:oll-title }
      { \fromproperty #'header:oll-short-description }

      \concat { \vspace #1.5 "Author(s): " \fromproperty #'header:oll-author }
      \line { File to include: #includeName }

      \section "Introduction:"
      \fromproperty  #'header:oll-description

      \section "Usage:"
      \fromproperty #'header:oll-usage
    }
  }
}

\header {
  copyright = \markup { Part of \typewriter openlilylib - licensed under the
                      CreativeCommons ... }
}
