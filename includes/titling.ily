% Headers for openlilylib documentation pages
% Currently an empty stub

\paper {
  #(include-special-characters)

  bookTitleMarkup = \markup {
    \column {
      { \bold \huge \fromproperty #'header:snippet-title }
      { \fromproperty #'header:snippet-short-description }
      
      \concat { \vspace #1.5 "Author(s): " \fromproperty #'header:snippet-author }
      \line { File to include: #includeName }

      \section "Introduction:"
      \fromproperty  #'header:snippet-description
    }
  }
}
