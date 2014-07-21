#!/usr/bin/env python
# -*- coding: utf-8

from PyQt4 import QtCore, QtGui, QtWebKit
import os
import oll
from __main__ import appInfo

class AbstractHtml(object):
    """Abstract class for HTML documentation objects"""
    def __init__(self, ollItem):
        # links to stylesheets
        self._stylesheets = []
        # links to script files
        self._scripts = []
        # cache for generated html code
        self._headHtml = ''
        self._bodyHtml = ''
        self._pageTitle = ''
        
        # partial templates for the generation of HTML
        self.templates = {
            'page': 
            '<html>\n{head}\n{body}\n</html>', 
            
            'head':
            '<head>\n{headcontent}\n</head>\n', 
            
            'page-title':
            '<title>{}</title>\n', 
            
            'script':
            '<link rel="script" href="{}" />\n', 
            
            'stylesheet':
            '<link rel="stylesheet" href="{}" />', 
            
            'body':
            '<body>\n{bodycontent}\n</body>\n', 
            
            'body-content':
            '<div id="content">\n{}</n>\n', 
        }
            
    
    # ##########################################
    # Methods to compose parts of or whole pages
    
    def body(self):
        """Returns the complete body of an HTML page.
        Results are cached, so data is only generated once."""
        if self._bodyHtml == '':
            self._bodyHtml = self.templates['body'].format(bodycontent = self.bodyContent())
        return self._bodyHtml
        
    def bodyContent(self):
        """Return HTML for the page body.
        Subclasses can override individual sub-methods 
        of the HTML generation or this whole method."""
        return self.templates['body-content'].format('No content specified here.')
        
    def head(self):
        """Returns the complete head of an HTML page.
        Results are cached, so data is only generated once."""
        if self._headHtml == '':
            self._headHtml = self.templates['head'].format(headcontent = self.headContent())
        return self._headHtml

    def headContent(self):
        """Content of the <head> section.
        Empty if no stylesheets are defined."""
        t = self._pageTitle if self._pageTitle else 'openlilylib documentation generator'
        html = self.templates['page-title'].format(t)
        html += self.stylesheets()
        html += self.scripts()
        return html
    
    def page(self):
        """Return a whole HTML page."""
        return self.templates['page'].format(
            head = self.head(), 
            body = self.body())
        
    def scripts(self):
        """If the 'scripts' list has entries
        they will be inserted in the <head> section
        of the generated page."""
        html = ''
        for s in self._scripts:
            html += self.templates['script'].format(s)
        return html

    def stylesheets(self):
        """If the 'stylesheets' list has entries
        they will be inserted in the <head> section
        of the generated page."""
        html = ''
        for s in self._stylesheets:
            html += self.templates['stylesheet'].format(s)
        return html
    
class AbstractOllHtml(AbstractHtml):
    """Base class for HTML objects with specific OLL relations."""
    def __init__(self, ollItem):
        super(AbstractOllHtml, self).__init__(ollItem)
        # hold references to the library objects
        self.ollItem = ollItem
        self.oll = ollItem.oll
        # display string for undefined field
        self._undefinedString = 'Undefined'
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
            'status':
            '{version}\n<h3>Compatibility:</h3>\n{compatibility}\n' +
                '<h3 class="subsection">Status information</h3>\n{status}\n',  
            'header':
            '<div class="oll-header">\n{title}\n</div>\n' +
                '<div class="oll-description">{description}\n</div>', 
        })
        self.fieldTemplates = {
            # generic field
            'field':
            '<div class="{f}">\n<span class="field-description">{t}: </span>\n' +
                '<span class="field-content">{c}</span>\n</div>\n', 
            
            # specific fields with non-standard templates
            'oll-title': '<h1 class="oll-title">{}</h1>\n', 
                            
            'oll-source':
            '<div class="oll-source"><span class="field-description">' +
                'Snippet source or other reference:</span><br />' +
                '<span class="field-content">{}</span></div>', 
                
            'oll-short-description':
                '<div class="oll-short-description">\n' +
                '<span class="field-content">{}</span>\n</div>\n', 
                
            'oll-description':
            '<div class="oll-description">{}</div>\n', 
            }

        self.listTemplate = ('<div class="{n}"><span class="field-description">' +
                '{t}: </span>\n<ul>\n{c}\n</ul>\n</div>\n')

    # ############################################
    # Generic functions to generate HTML fragments
    
    def fieldDoc(self, fieldName, default = False):
        """Return HTML code for a single field.
        Handles both generating of default values or hiding the field,
        handles single elements or lists."""
        
        content = self.ollItem.definition.headerFields[fieldName]

        # if the field has more than one values
        # defer to submethod
        if isinstance(content, list):
            return self.itemList(fieldName, content)
        else:
            # Return nothing or a default if the field has no value
            if content is None:
                if not default:
                    return ''
                content = self._undefinedString
            else:
                # convert double line breaks to HTML paragraphs
                content = content.replace('\n\n', '</p><p>')
            if fieldName in self.fieldTemplates:
                # use template if defined for the given field
                return self.fieldTemplates[fieldName].format(content)
            else:
                # use generic template
                # use defined field title or plain field name.
                fieldTitle = self.fieldTitles[fieldName] if fieldName in self.fieldTitles else fieldName
                return self.fieldTemplates['field'].format(
                   f = fieldName, 
                   t = fieldTitle, 
                   c = content)

    def fieldDocs(self, fieldNames, default = False):
        """Return HTML for a list of fields."""
        return ''.join([self.fieldDoc(f, default) for f in fieldNames])

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
            print "python-ly not installed, generating unformatted LilyPond code."
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
    
class OllDetailPage(AbstractOllHtml):
    def __init__(self, ollItem):
        super(OllDetailPage, self).__init__(ollItem)
        self.templates.update( {
            'section':
            '<div class="container" id="{n}">\n{t}{c}\n</div>', 
            
            'section-heading':
            '<h2 class="section">{}</h2>\n', 
        })

        self.listTemplate = ('<div class="{n}"><span class="field-description">' +
                '{t}: </span><ul>{c}</ul></div>')

    def bodyContent(self):
        """Return HTML for the page body.
        Subclasses can override individual sub-methods 
        of the HTML generation or this whole method."""
        return self.templates['body-content'].format(self.bodyDetail())

    def bodyDetail(self):
        html = self.headerSection()
        html += self.metaSection()
        html += self.statusSection()
        html += self.customFieldsSection()
        html += self.definitionBodySection()
        html += self.exampleBodySection()
        return html
        
    # ##########################################
    # Methods to compose the individual sections
    # Subclasses may override these methods to
    # generate alternative pages.
    
    def customFieldsSection(self):
        """Document custom fields if they are present
        in a snippet's header."""
        if not self.ollItem.hasCustomHeaderFields():
            return ''
        html = ''
        for f in self.ollItem.definition.custFieldNames:
            html += self.fieldDoc(f)
        return self.section('custom', 
                            html, 
                            'Custom fields')
    
    def definitionBodySection(self):
        """Return the snippet definition's LilyPond code."""
        return self.section('definition-body', 
            self.lilypondToHtml(''.join(self.ollItem.definition.bodycontent)), 
            'Snippet definition')
        
    def exampleBodySection(self):
        """Return a usage example (if present) as LilyPond code."""
        if self.ollItem.hasExample():
            return self.section('example-body', 
            self.lilypondToHtml(''.join(self.ollItem.example.filecontent)), 
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


class HtmlDetailInline(OllDetailPage):
    """Class for snippets to be displayed in the
    inline documentation viewer."""
    def __init__(self, ollItem):
        super(HtmlDetailInline, self).__init__(ollItem)


class HtmlDetailFile(OllDetailPage):
    """OLL that will be printed to files."""
    def __init__(self, ollItem):
        super(HtmlDetailFile, self).__init__(ollItem)
        self._stylesheets.append('css/detailPage-file.css')
        self.templates['body-content'] = ('<div id="nav">\n' +
        '<h2>openlilylib</h2>\n{nav}\n</div>\n' +
            '<div id="detail">{detail}</div>')
        
    def bodyContent(self):
        """The document body has a different template in file based
        detail pages. It has an additional navigation column."""            
        return self.templates['body-content'].format(
            nav = LibraryNavigation(self.oll, self.ollItem.name).content(), 
            detail = super(HtmlDetailFile, self).bodyDetail())

    def save(self):
        """Save the file to disk.
        Determine filename automatically from the snippet name
        and use cached content if possible."""
        filename = os.path.join(appInfo.docPath, self.ollItem.name + '.html')
        f = open(filename, 'w')
        try:
            f.write(self.page())
        finally:
            f.close()

class LibraryNavigation(object):
    """Generates a div container containing library navigation.
    Respects the currently opened snippet."""
    def __init__(self, oll, currentItemName):
        self.oll = oll
        self.currentItem = currentItemName
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
        dict = getattr(self.oll, group)
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
        
    def navLinkItem(self, itemName):
        """Create a single list item representing a snippet.
        If it points to the currently displayed snippet
        only the snippet title is returned, otherwise
        a link is generated."""
        ollItem = self.oll.byName(itemName)
        itemTitle = ollItem.definition.headerFields['oll-title']
        if itemName != self.currentItem:
            return self.templates['link-li'].format(
                link = itemName + '.html', 
                title = itemTitle)
        else:
            return self.templates['link-li-act'].format(itemTitle)
        
    def navLinks(self, group):
        """Create link items for all snippets in a group."""
        html = ''
        for entry in group:
            html += self.navLinkItem(entry)
        return html
        
        

