#!/usr/bin/env python
# -*- coding: utf-8

from PyQt4 import QtCore, QtGui, QtWebKit
import os
import snippets
from __main__ import appInfo

class AbstractHtml(object):
    """Abstract class for HTML documentation objects"""
    def __init__(self, snippet):
        # links to stylesheets
        self.stylesheets = []
        # cache for generated html code
        self.pageHtml = ''
        
        # partial templates for the generation of HTML
        self.templates = {
            'page': 
            '<html>\n{head}\n{body}\n</html>', 
            
            'head':
            '<head>\n{headcontent}\n</head>', 
            
            'stylesheet':
            '<link rel="stylesheet" href="{}" />', 
            
            'body':
            '<body>\n{bodycontent}\n</body>', 
        }
            
    
    # ##########################################
    # Methods to compose parts of or whole pages
    
    def bodyContent(self):
        """Return HTML for the page body.
        Subclasses can override individual sub-methods 
        of the HTML generation or this whole method."""
        html = self.headerSection()
        html += self.metaSection()
        html += self.statusSection()
        html += self.customFieldsSection()
        html += self.definitionBodySection()
        html += self.exampleBodySection()
        
        return html

    def page(self):
        """Return a whole HTML page.
        Results are cached, so the page is only generated once."""
        if self.pageHtml == '':
            self.pageHtml = self.templates['page'].format(
                head = self.templates['head'].format(headcontent = self.headContent()), 
                body = self.templates['body'].format(bodycontent = self.bodyContent()))
        return self.pageHtml
    
    def stylesheetEntries(self):
        """If the 'stylesheets' list has entries
        they will be inserted in the <head> section
        of the generated page."""
        html = ''
        for s in self.stylesheets:
            html += self.templates['stylesheet'].format(s)
        return html
    
class AbstractOllHtml(AbstractHtml):
    def __init__(self, snippet):
        super(AbstractOllHtml, self).__init__(snippet)
        self.snippet = snippet
        self.snippets = snippet.owner
        # display titles for used fields
        self.fieldTitles = {
            'oll-version': 'Code version', 
            'oll-title': 'Snippet title', 
            'oll-author': 'Author(s)', 
            'oll-short-description': 'Short description', 
            'oll-description': 'Description', 
            'oll-category': 'Category', 
            'oll-tags': 'Tags', 
            'first-lilypond-version': 'First known version', 
            'last-lilypond-version': 'Last known version', 
            'oll-status': 'Snippet status', 
            'oll-todo': 'TODOs, bugs and feature requests', 
            }
        self.templates.update( {
            'section':
            '<div class="container" id="{n}">\n{t}{c}\n</div>', 
            
            'section-heading':
            '<h2 class="section">{}</h2>\n', 
            
            # generic field
            'field':
            '<div class="{f}">\n<span class="field-description">{t}: </span>\n' +
                '<span class="field-content">{c}</span>\n</div>\n', 
            
            # specific fields with non-standard templates
            'header':
            '<div class="oll-header">\n{title}\n</div>\n' +
                '<div class="oll-description">{description}\n</div>', 
            
            'status':
            '{version}\n<h3>Compatibility:</h3>\n{compatibility}\n' +
                '<h3 class="subsection">Status information</h3>\n{status}\n',  
                
            'oll-title': "<h1>{}</h1>", 
                            
            'oll-source':
            '<div class="oll-source"><span class="field-description">' +
                'Snippet source or other reference:</span><br />' +
                '<span class="field-content">{}</span></div>', 
                
            'oll-short-description':
                '<div class="oll-short-description">\n' +
                '<span class="field-content">{}</span>\n</div>\n', 
                
            'oll-description':
            '<div class="oll-description">{}</div>\n', 
            
            'lilypond-code': '<pre class="lilypond">{}</pre>'
            }
            )

        self.listTemplate = ('<div class="{n}"><span class="field-description">' +
                '{t}: </span><ul>{c}</ul></div>')

    # ############################################
    # Generic functions to generate HTML fragments
    
    def fieldDoc(self, fieldName, default = False):
        """Return HTML code for a single field.
        Handles both generating of default values or hiding the field,
        handles single elements or lists."""
        
        content = self.snippet.definition.headerFields[fieldName]

        # if the field has more than one values
        # defer to submethod
        if isinstance(content, list):
            return self.itemList(fieldName, content)
        else:
            # Return nothing or a default if the field has no value
            if content is None:
                if not default:
                    return ''
                content = "Undefined"
            else:
                # convert double line breaks to HTML paragraphs
                content = content.replace('\n\n', '</p><p>')
            if fieldName in self.templates:
                # use template if defined for the given field
                return self.templates[fieldName].format(content)
            else:
                # use generic template
                # use defined field title or plain field name.
                fieldTitle = self.fieldTitles[fieldName] if fieldName in self.fieldTitles else fieldName
                return self.templates['field'].format(
                   f = fieldName, 
                   t = fieldTitle, 
                   c = content)

    def fieldDocs(self, fieldNames, default = False):
        """Return HTML for a number of fields."""
        result = ''
        for f in fieldNames:
            result += self.fieldDoc(f, default)
        return result

    def headContent(self):
        """Content of the <head> section.
        Empty if no stylesheets are defined."""
        html = '<title>{}</title>\n'.format(self.snippet.definition.headerFields['oll-title'])
        html += self.stylesheetEntries()
        return html
    
    def itemList(self, fieldName, content):
        """Return HTML for a list of field values."""
        lst = ""
        for line in content:
            lst += '<li>{}</li>\n'.format(line)
        # use defined title if available or plain field name.
        title = self.fieldTitles[fieldName] if fieldName in self.fieldTitles else fieldName
        return self.listTemplate.format(
            n = fieldName, 
            t = title, 
            c = lst)
    
    def lilypondToHtml(self, code):
        """Return formatted LilyPond code as HTML if possible.
        This works by using the python-ly module if it's installed."""
        
        # convert to string if code is passed as list
        if isinstance(code, list):
             # ensure there is exactly one newline at the end of each line
            tmp = ''
            for l in code:
                tmp += l.rstrip() + '\n'
            code = tmp
        try:
            # generate formatted HTML if python-ly is installed
            import ly.document, ly.colorize
            lyDoc = ly.document.Document(code)
            cursor = ly.document.Cursor(lyDoc)
            writer = ly.colorize.HtmlWriter()
            writer.full_html = False
            code = writer.html(cursor).replace(
                '<pre id="document">', '<pre class="lilypond">')
        except ImportError:
            # if python-ly isn't available we print plaintext output
            code = self.templates['lilypond-code'].format(code)
            
        return code

    def section(self, name, content, title = ''):
        """Generate a section of the page.
        If a title is given it will be converted to a heading,
        otherwise no title is generated."""
        if title != '':
            title = self.templates['section-heading'].format(title)
        return self.templates['section'].format(
            n = name, t = title, c = content)
    
    # ##########################################
    # Methods to compose the individual sections
    # Subclasses may override these methods to
    # generate alternative pages.
    
    def customFieldsSection(self):
        """Document custom fields if they are present
        in a snippet's header."""
        if not self.snippet.hasCustomHeaderFields():
            return ''
        html = ''
        for f in self.snippet.definition.custFieldNames:
            html += self.fieldDoc(f)
        return self.section('custom', 
                            html, 
                            'Custom fields')
    
    def definitionBodySection(self):
        """Return the snippet definition's LilyPond code."""
        return self.section('definition-body', 
            self.lilypondToHtml(''.join(self.snippet.definition.bodycontent)), 
            'Snippet definition')
        
    def exampleBodySection(self):
        """Return a usage example (if present) as LilyPond code."""
        if self.snippet.hasExample():
            return self.section('example-body', 
            self.lilypondToHtml(''.join(self.snippet.example.filecontent)), 
            'Usage example')
        else:
            return ''
        
    def headerSection(self):
        """Return  formatted title/author section."""
        html = self.templates['header'].format(
            title = self.fieldDocs( 
                ['oll-title','oll-short-description', 
                 'oll-author']), 
            description = self.fieldDoc('oll-description'))
        return self.section('header', html)
        
    def metaSection(self):
        """Return section with snippet metadata"""
        return self.section(
            'meta', self.fieldDocs(
                ['oll-source', 
                 'oll-category', 
                 'oll-tags']), 
             'Metadata')
             
    def statusSection(self):
        """Retrun section with status information."""
        return self.section(
            'status', 
            self.templates['status'].format(
                version = self.fieldDoc('oll-version', True), 
                compatibility = self.fieldDocs(['first-lilypond-version', 
                                                'last-lilypond-version'], True), 
                status = self.fieldDocs(['oll-status', 
                                         'oll-todo'])), 
            'Status information')

class OllDetailPage(AbstractOllHtml):
    def __init__(self, snippet):
        super(OllDetailPage, self).__init__(snippet)
    
class HtmlInline(OllDetailPage):
    """Class for snippets to be displayed in the
    inline documentation viewer."""
    def __init__(self, snippet):
        super(HtmlInline, self).__init__(snippet)


class HtmlFile(OllDetailPage):
    """Snippets that will be printed to files."""
    def __init__(self, snippet):
        super(HtmlFile, self).__init__(snippet)
        self.stylesheets.append('css/detailPage-file.css')
        self.templates['body'] = ('<div id="nav">\n' +
        '<h2>openlilylib</h2><pre>{nav}</pre>\n</div>\n' +
            '<div id="detail">{detail}</div>')
        
    def bodyContent(self):
        """The document body has a different template in file based
        detail pages. It has an additional navigation column."""
        return self.templates['body'].format(
            nav = LibraryNavigation(self.snippets, self.snippet.name).content(), 
            detail = super(HtmlFile, self).bodyContent())

    def save(self):
        """Save the file to disk.
        Determine filename automatically from the snippet name
        and use cached content if possible."""
        filename = os.path.join(appInfo.docPath, self.snippet.name + '.html')
        f = open(filename, 'w')
        try:
            f.write(self.page())
        finally:
            f.close()

class LibraryNavigation(object):
    """Generates a div container containing library navigation.
    Respects the currently opened snippet."""
    def __init__(self, snippets, currentSnippetName):
        self.snippets = snippets
        self.currentSnippet = currentSnippetName
        self.templates = {
            'container': '<div class="container" id="nav">\n{}\n</div>', 
            'nav-section': ('<div class="container" id="{id}">\n' +
                '<h2>{label}</h2>\n{content}\n</div>\n'), 
            'nav-group': ('<div class="group">{entry}</div>\n' +
                '<ul>\n{entries}\n</ul>\n'), 
            'link-li': '<li><a href="{link}">{title}</a></li>\n', 
            'link-li-act': '<li class="act">{} (current snippet)\n', 
        }
    
    def content(self):
        """Generate the content for the whole navigation column."""
        html = self.navSection('names', 'By name:')
        html += self.navSection('categories', 'By category:')
        html += self.navSection('tags', 'By tag:')
        html += self.navSection('authors', 'By author:')
                
        return  html
        
    def html(self):
        return self.templates['container'].format(self.content)
    
    def navSection(self, group, label):
        """Create a whole navigation section.
        The function takes care of 'by name' too,
        which has one level less. This is done by checking
        whether 'group' is a list or a dictionary."""
        dict = getattr(self.snippets, group)
        if isinstance(dict, list):
            content = '<ul>\n{}\n</ul>\n'.format(self.navLinks(dict))
        else:
            content = self.navGroup(dict)
            
        html = self.templates['nav-section'].format(
                id = group, 
                label = label, 
                content = content)
        return html
            

    def navGroup(self, dict):
        """Create a navigational group consisting of
        a title div and an <ul> with link items."""
        html = ''
        for entry in dict['names']:
            html += self.templates['nav-group'].format(
                    entry = entry, 
                    entries = self.navLinks(dict[entry]))
        return html
        
    def navLinkItem(self, snippetName):
        """Create a single list item representing a snippet.
        If it points to the currently displayed snippet
        only the snippet title is returned, otherwise
        a link is generated."""
        snippet = self.snippets.byName(snippetName)
        snippetTitle = snippet.definition.headerFields['oll-title']
        if snippetName != self.currentSnippet:
            return self.templates['link-li'].format(
                link = snippetName + '.html', 
                title = snippetTitle)
        else:
            return self.templates['link-li-act'].format(snippetTitle)
        
    def navLinks(self, group):
        """Create link items for all snippets in a group."""
        html = ''
        for entry in group:
            html += self.navLinkItem(entry)
        return html
        
        

