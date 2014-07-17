#!/usr/bin/env python
# -*- coding: utf-8

from PyQt4 import QtCore, QtGui, QtWebKit
import os
import snippets
from __main__ import appInfo

class AbstractHtml(object):
    """Abstract class for HTML documentation objects"""
    def __init__(self, snippet):
        self.snippet = snippet
        # links to stylesheets
        self.stylesheets = []
        # cache for generated html code
        self.pageHtml = ''
        # display titles for used fields
        self.fieldTitles = {
            'snippet-version': 'Code version', 
            'snippet-title': 'Snippet title', 
            'snippet-author': 'Author(s)', 
            'snippet-short-description': 'Short description', 
            'snippet-description': 'Description', 
            'snippet-category': 'Category', 
            'snippet-tags': 'Tags', 
            'first-lilypond-version': 'First known version', 
            'last-lilypond-version': 'Last known version', 
            'snippet-status': 'Snippet status', 
            'snippet-todo': 'TODOs, bugs and feature requests', 
            }
        
        # partial templates for the generation of HTML
        self.templates = {
            'page': 
            '<html>\n<head>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>', 
            
            'stylesheet':
            '<link rel="stylesheet" href="{}" />', 
            
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
            '<div class="snippet-header">\n{title}\n</div>\n' +
                '<div class="snippet-description">{description}\n</div>', 
            
            'status':
            '{version}\n<h3>Compatibility:</h3>\n{compatibility}\n' +
                '<h3 class="subsection">Status information</h3>\n{status}\n',  
                
            'snippet-title': "<h1>{}</h1>", 
                            
            'snippet-source':
            '<div class="snippet-source"><span class="field-description">' +
                'Snippet source or other reference:</span><br />' +
                '<span class="field-content">{}</span></div>', 
                
            'snippet-short-description':
                '<div class="snippet-short-description">\n' +
                '<span class="field-content">{}</span>\n</div>\n', 
                
            'snippet-description':
            '<div class="snippet-description">{}</div>\n', 
            
            'lilypond-code': '<pre class="lilypond">{}</pre>'
            }

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
        html = '<title>{}</title>\n'.format(self.snippet.definition.headerFields['snippet-title'])
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
        """Return formatted LilyPond code as HTML.
        (This is a stub for a to-be-developed function)."""
        
        # convert to string if code is passed as list
        if isinstance(code, list):
             # ensure there is exactly one newline at the end of each line
            tmp = ''
            for l in code:
                tmp += l.rstrip() + '\n'
            code = tmp
            
        #TODO: use Frescobaldi's ly-music module
        return self.templates['lilypond-code'].format(code)

    def section(self, name, content, title = ''):
        """Generate a section of the page.
        If a title is given it will be converted to a heading,
        otherwise no title is generated."""
        if title != '':
            title = self.templates['section-heading'].format(title)
        return self.templates['section'].format(
            n = name, t = title, c = content)
    
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
                head = self.headContent(), 
                body = self.bodyContent())
        return self.pageHtml
    
    def stylesheetEntries(self):
        """If the 'stylesheets' list has entries
        they will be inserted in the <head> section
        of the generated page."""
        html = ''
        for s in self.stylesheets:
            html += self.templates['stylesheet'].format(s)
        return html
    
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
                ['snippet-title','snippet-short-description', 
                 'snippet-author']), 
            description = self.fieldDoc('snippet-description'))
        return self.section('header', html)
        
    def metaSection(self):
        """Return section with snippet metadata"""
        return self.section(
            'meta', self.fieldDocs(
                ['snippet-source', 
                 'snippet-category', 
                 'snippet-tags']), 
             'Metadata')
             
    def statusSection(self):
        """Retrun section with status information."""
        return self.section(
            'status', 
            self.templates['status'].format(
                version = self.fieldDoc('snippet-version', True), 
                compatibility = self.fieldDocs(['first-lilypond-version', 
                                                'last-lilypond-version'], True), 
                status = self.fieldDocs(['snippet-status', 
                                         'snippet-todo'])), 
            'Status information')
                


class HtmlInline(AbstractHtml):
    """Class for snippets to be displayed in the
    inline documentation viewer."""
    def __init__(self, snippet):
        super(HtmlInline, self).__init__(snippet)


class HtmlFile(AbstractHtml):
    """Snippets that will be printed to files."""
    def __init__(self, snippet):
        super(HtmlFile, self).__init__(snippet)
        self.stylesheets.append('css/detailPage-file.css')
        self.templates['body'] = ('<div id="nav">\n' +
        '<h2>openlilylib</h2><pre>{nav}</pre>\n</div>\n' +
            '<div id="detail">{detail}</div>')
        
    def bodyContent(self):
        return self.templates['body'].format(
            nav = self.navContent(), 
            detail = super(HtmlFile, self).bodyContent())
    
    def navContent(self):
        snippets = self.snippet.owner
        html = '<div class="container"><h2>By name</h2>'
        html += '<ul>\n'
        for s in snippets.names:
            html += '<li><a href="' + s + '.html">' + s + '</a></li>\n'
        html += '</ul>\n</div>'
        
        html += '<div class="container"><h2>By category</h2>'
        html += '<ul>\n'
        
        for c in snippets.categories['names']:
            html += '<div>{}</div>'.format(c)
            html += '<ul>\n'
            for s in snippets.categories[c]:
                html += '<li><a href="' + s + '.html">' + s + '</a></li>\n'
            html += '</ul>\n'
        html += '</ul>\n</div>'
        
        html += '<div class="container"><h2>By tag</h2>'
        html += '<ul>\n'
        
        for c in snippets.tags['names']:
            html += '<div>{}</div>'.format(c)
            html += '<ul>\n'
            for s in snippets.tags[c]:
                html += '<li><a href="' + s + '.html">' + s + '</a></li>\n'
            html += '</ul>\n'
        html += '</ul>\n</div>'
        
        html += '<div class="container"><h2>By author</h2>'
        html += '<ul>\n'
        
        for c in snippets.authors['names']:
            html += '<div>{}</div>'.format(c)
            html += '<ul>\n'
            for s in snippets.authors[c]:
                html += '<li><a href="' + s + '.html">' + s + '</a></li>\n'
            html += '</ul>\n'
        html += '</ul>\n</div>'
        
        return  html
        
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
