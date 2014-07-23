#!/usr/bin/env python
# -*- coding: utf-8

from PyQt4 import QtCore, QtGui, QtWebKit
import os
import re
import oll
import __main__

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
            '<body>\n{headercontent}\n{bodycontent}\n</body>\n', 
            
            'body-content':
            '<div id="content">\n{}</div>\n', 
            
            'header-content': '', 
        }
            
    
    # ##########################################
    # Methods to compose parts of or whole pages
    
    def body(self):
        """Returns the complete body of an HTML page.
        Results are cached, so data is only generated once."""
        if self._bodyHtml == '':
            self._bodyHtml = self.templates['body'].format(
                headercontent = self.headerContent(), 
                bodycontent = self.bodyContent())
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
    
    def headerContent(self):
        # Temporary implementation
        return self.templates['header-content'].format(
            '<a href="index.html">Back to index page</a>')
        
    def page(self):
        """Return a whole HTML page."""
        return self.templates['page'].format(
            head = self.head(), 
            body = self.body())
        
    def save(self):
        """Save the file to disk.
        Filename has to be determined in the __init__
        method of subclasses."""
        
        if self.filename != '':
            f = open(self.filename, 'w')
            try:
                f.write(self.page())
            finally:
                f.close()

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
        self.oll = None
        if ollItem:
            self.oll = ollItem.oll
        self.markupParser = LilyPondMarkup()
        # display string for undefined field
        self._undefinedString = 'Undefined'
        # display titles for used fields
        self.fieldTitles = {
            'oll-version': 'Code version', 
            'oll-title': 'Snippet title', 
            'oll-author': 'Author(s)', 
            'oll-short-description': 'Short description', 
            'oll-description': 'Description', 
            'oll-usage': 'Usage', 
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
                '<div class="oll-description">{description}\n</div>' +
                '<div class="oll-usage">\n{usage}\n</div>', 
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
                'Source or other reference:</span><br />' +
                '<span class="field-content">{}</span></div>', 
                
            'oll-short-description':
                '<div class="oll-short-description">\n' +
                '<span class="field-content">{}</span>\n</div>\n', 
                
            'oll-description':
            '{}\n', 
            
            'oll-usage':
            '<h3>Usage</h3>\n{}\n', 
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
            # convert \markup formatting to HTML
            content = self.markupParser.toHtml(content)
            # pass content to the right template
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

class OllIndexPage(AbstractOllHtml):
    def __init__(self, oll):
        super(OllIndexPage, self).__init__(None)
        self.oll = oll
        self.filename = os.path.join(__main__.appInfo.docPath, 'index.html')
        self._stylesheets.append('css/detailPage.css')
        self.templates['toc'] = ('<div class="container" id="toc">\n' +
            '<h1>openlilylib</h1>\n<h2>Overview</h2>\n{}</div>\n')
        
    def bodyContent(self):
        nav = LibraryNavigation(self.oll)
        html = nav.navSection('names', 'By name:')
        html += nav.navSection('categories', 'By category:')
        
        return self.templates['toc'].format(html)
    
    
class OllDetailPage(AbstractOllHtml):
    def __init__(self, ollItem):
        super(OllDetailPage, self).__init__(ollItem)
        self.templates.update( {
            'section':
            '<div class="container" id="{n}">\n{t}{c}\n</div>', 
            
            'section-heading':
            '<h2 class="section">{}</h2>\n', 
        })
        self.templates['body-content'] = ('<div id="col1">\n{col1content}\n' +
            '</div>\n<div id="col2">\n{col2content}\n</div>')

        self.listTemplate = ('<div class="{n}"><span class="field-description">' +
                '{t}: </span><ul>{c}</ul></div>')

    def bodyContent(self):
        """Return HTML for the page body.
        Subclasses can override individual sub-methods 
        of the HTML generation or this whole method."""
        return self.templates['body-content'].format(
            col1content = self.bodyDetail(), 
            col2content = self.bodyMeta())

    def bodyDetail(self):
        html = self.headerSection()
        html += self.exampleBodySection()
        html += self.definitionBodySection()
        return html
    
    def bodyMeta(self):
        html = self.metaSection()
        html += self.customFieldsSection()
        html += self.statusSection()
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
            description = self.fieldDoc('oll-description'), 
            usage = self.fieldDoc('oll-usage'))
        return self.section('header', html)
        
    def metaSection(self):
        """Return section with snippet metadata"""
        content = self.fieldDoc('oll-category')
        # Add a list of links to other items in the same category (if available)
        itemsInCategory = self.oll.categories[self.ollItem.definition.headerFields['oll-category']]
        otherItems = [i for i in itemsInCategory if i != self.ollItem.name]
        if len(otherItems) > 0:
            content += '<p>Other items in that category:</p>\n'
            content += '<ul>\n{}\n</ul>\n'.format(
                LibraryNavigation(self.oll).navLinks(otherItems))
        content += self.fieldDocs(
            ['oll-tags', 
             'oll-source'])
        return self.section(
            'meta', content, 
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
        self.filename = os.path.join(__main__.appInfo.docPath, self.ollItem.name + '.html')
        self._stylesheets.append('css/detailPage-file.css')
#         self.templates['body-content'] = ('<div id="nav">\n{nav}\n</div>\n' +
#            '<div id="detail">{detail}</div>')
        self.templates['header-content'] = ('<div class="container" id="page-header">\n' +
            '<h1>openlilylib</h1>\n{}\n</div>\n')
        
#    def bodyContent(self):
#
#    This function is only commented out for now because it is possible
#    that we might need it again later.
#
#        """The document body has a different template in file based
#        detail pages. It has an additional navigation column."""            
#        return self.templates['body-content'].format(
#            nav = LibraryNavigation(self.oll, self.ollItem.name).content(), 
#            detail = super(HtmlDetailFile, self).bodyDetail())

class LibraryNavigation(object):
    """Generates a div container containing library navigation.
    Respects the currently opened snippet."""
    def __init__(self, oll, currentItemName = ''):
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
                title = itemTitle), itemTitle
        else:
            return self.templates['link-li-act'].format(itemTitle), itemTitle
        
    def navLinks(self, group):
        """Create link items for all snippets in a group.
        The list is sorted by the displayed text."""
        #TODO: Somehow this looks not really Pythonic to me ...
        html = ''
        entries = {}
        titles = []
        for entry in group:
            link, title = self.navLinkItem(entry)
            entries[title] = link
            titles.append(title)
        titles.sort()
        for t in titles:
            html += entries[t]
        return html
        
class LilyPondMarkup(object):
    """Tries to parse LilyPond \markup sections
    into HTML. It's not clear whether this is a
    promising approach."""
    def __init__(self):
        self.processors = {
            '\\ollCommand': '<code>\\{}</code>', 
            '\\italic': '<i>{}</i>', 
            '\\bold': '<b>{}</b>', 
            '\\typewriter': '<code>{}</code>', 
            }
    
    def getExpression(self, text, start):
        """Split a string in an expression and a remainder.
        The expression may be a single token or a string
        surrounded by curly braces.
        Currently no nesting is supported whatsoever."""
        
        remainder = text[start:].lstrip()
        if remainder[0] != '{':
            expr = remainder.split()[0]
            remainder = remainder[len(expr):]
        else:
            end = remainder.find('}')
            expr = remainder[1:end-1].rstrip()
            remainder = remainder[end+1:]
        return expr, remainder
        
    def process(self, processor, text, start):
        """Process a single instance of a known markup."""
        expr, remainder = self.getExpression(text, start + len(processor) + 1)
        return text[:start] +  self.processors[processor].format(expr) + remainder
        
    def toHtml(self, markup):
        """Parse a given markup and replace LilyPond markup with HTML markup."""
        result = markup
        # Go through the list of known markup commands
        for p in self.processors:
            occurences = [m.start() for m in re.finditer('\\' + p, result)]
            occurences.reverse()
            # process all instances of a given markup command.
            for o in occurences:
                result = self.process(p, result, o)
        return result
