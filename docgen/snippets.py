#!/usr/bin/env python
# -*- coding: utf-8

import os
import re
from PyQt4 import QtCore

import __main__

class OllItemFile(QtCore.QObject):
    """Snippet file (both definition and usage example.
    Has a filename and a filecontent field
    and an abstract parseFile() method."""
    def __init__(self, owner, filename):
        super(OllItemFile, self).__init__()
        self.owner = owner
        self.filename = filename
        self.version = None
        self.filecontent = None
        self.headercontent = []
        self.bodycontent = []
        try:
            f = open(self.filename)
            self.filecontent = f.readlines()
        finally:
            f.close()
        self.parseFile()
    
    def checkVersion(self, line):
        result = None
        if line.strip().startswith('\\version'):
            result = self.getFieldString(line)
        return result
        
    def getFieldString(self, line):
        """Return the part of 'line' between quotation marks if present."""
        result = re.search('\"(.*)\"', line)
        if result:
            result = result.group(1)
        return result
        
    def parseFile(self):
        raise Exception("OllItemFile.parseFile() has to be " +
                        "implemented in subclasses")
    
    def tagList(self, tagstring):
        """Return a list of tags stripped from whitespace.
        Argument is a comma-separated list."""
        return [ t.strip() for t in tagstring.split(',')]

class SnippetDefinition(OllItemFile):
    """Definition of a snippet"""
    def __init__(self, owner, filename):
        # Define expected header fields
        # Fields that are still None after parsing
        # have not been defined in the snippet
        self.initFieldNames()

        super(SnippetDefinition, self).__init__(owner, filename)
    
    def initFieldNames(self):
        self.stdFieldNames = [
            'oll-title', 
            'oll-short-description', 
            'oll-description', 
            'oll-author', 
            'oll-source', 
            'oll-category', 
            'oll-tags', 
            'oll-version', 
            'first-lilypond-version', 
            'last-lilypond-version', 
            'oll-status', 
            'oll-todo']
        self.custFieldNames = []
        self.headerFields = {}
        for f in self.stdFieldNames:
            self.headerFields[f] = None

    def parseFile(self):
        self.version = None
        i = 0
        while i < len(self.filecontent):
            line = self.filecontent[i]
            # Check for version string
            if self.version is None:
                self.version = self.checkVersion(line)
                
            if line.strip().startswith('\\header'):
                # Get the content of the \header section.
                # ATTENTION: The section is considered finished when
                # a line is encountered that has a '}' as its first character
                # and no more content (except whitespace) after that.
                i += 1
                while not self.filecontent[i].rstrip() == '}':
                    self.headercontent.append(self.filecontent[i])
                    i += 1
                
                # After the header the first line containing anything
                # except whitespace and comments is considered as starting
                # the snippet body.
                i += 1
                while ((self.filecontent[i].strip() == '') 
                            or self.filecontent[i].strip().startswith('%')):
                    i += 1
                self.bodycontent = self.filecontent[i:]
                break
                
            # this is only executed until a header is found.
            i += 1

        self.parseHeader()

    def parseHeader(self):
        self.initFieldNames()
        self.headerFields['oll-version'] = self.version
        i = 0
        # read in fields
        while i < len(self.headercontent):
            i = self.readField(i)
        # handle the comma-separated-list fields
        self.splitFields(['oll-author', 'oll-tags', 'oll-status'])
        # parse custom header fields
        for f in self.headerFields:
            if not f in self.stdFieldNames:
                self.custFieldNames.append(f)
        self.custFieldNames.sort()
        # add snippet to lists for browsing by type
        self.owner.addToAuthors(self.headerFields['oll-author'])
        self.owner.addToCategory(self.headerFields['oll-category'])
        self.owner.addToTags(self.headerFields['oll-tags'])

    def readField(self, i):
        while not re.search('(.*) =', self.headercontent[i]):
            i +=1
            if i == len(self.headercontent):
                return i
        line = self.headercontent[i].strip()
        fieldName = line[:line.find('=')-1].strip()
        fieldContent = self.getFieldString(line)
        if not fieldContent:
            fieldContent = ""
            i += 1
            while not self.headercontent[i].strip() == '}':
                fieldContent += self.headercontent[i].strip() + '\n'
                i += 1
            
        self.headerFields[fieldName] = fieldContent
        i += 1
        return i

    def splitFields(self, fields):
        """Split fields that are given as comma-separated lists
        into Python lists."""
        for f in fields:
            lst = self.tagList(self.headerFields[f])
            lst.sort()
            # if there is only one entry use a simple string
            if len(lst) == 1:
                lst = lst[0]
            self.headerFields[f] = lst
            
        
class SnippetExample(OllItemFile):
    """Usage example for a snippet"""
    def __init__(self, owner, filename):
        super(SnippetExample, self).__init__(owner, filename)

    def parseFile(self):
        #TODO: parse the example file
        pass

class OllItem(QtCore.QObject):
    """Object representing a single snippet.
    Contains a definition and an example object."""
    def __init__(self, owner, name):
        super(OllItem, self).__init__()
        self.owner = owner
        self.name = name
        defFilename = os.path.join(__main__.appInfo.defPath, name) + '.ily'
        self.definition = SnippetDefinition(self, defFilename)
        self.example = None
        self._displayHtml = None
        self._fileHtml = None

    def addExample(self):
        """Read an additional usage-example."""
        xmpFilename = os.path.join(__main__.appInfo.xmpPath, self.name) + '.ly'
        self.example = SnippetExample(self, xmpFilename)
    
    def addToAuthors(self, authors):
        self.owner.addTo(self.owner.authors, self.name, authors)
        
    def addToCategory(self, catname):
        self.owner.addTo(self.owner.categories, self.name, catname)
    
    def addToTags(self, tags):
        self.owner.addTo(self.owner.tags, self.name, tags)
        
    def hasCustomHeaderFields(self):
        return len(self.definition.custFieldNames) > 0
        
    def hasExample(self):
        """return true if an example is defined."""
        return True if self.example is not None else False

    def htmlForDisplay(self):
        import html
        if self._displayHtml is None:
            self._displayHtml = html.HtmlDetailInline(self)
        return self._displayHtml
        
    def htmlForFile(self):
        import html
        if self._fileHtml is None:
            self._fileHtml = html.HtmlDetailFile(self)
        return self._fileHtml
        
    def saveHtml(self):
        """Save HTML documentation for the snippet."""
        # htmlForFile() uses caching.
        self.htmlForFile().save()
        

class OLL(QtCore.QObject):
    """Object holding a dictionary of snippets"""
    def __init__(self, owner):
        super(OLL, self).__init__()
        self.mainwindow = owner
        self.current = ''
        self.initLists()

    def addTo(self, target, snippet, entry):
        if isinstance(entry, list):
            for e in entry:
                self.addToTarget(target, snippet, e)
        else:
            self.addToTarget(target, snippet, entry)
    
    def addToTarget(self, target, snippet, entry):
        if not target.get(entry):
            target[entry] = []
            target['names'].append(entry)
            target['names'].sort()
        target[entry].append(snippet)
        target[entry].sort()

    def byName(self, name):
        """Return a OLL object if it is defined."""
        return self.snippets.get(name, None)
        
    def initLists(self):
        self.snippets = {}
        self.names = []
        self.categories = {'names': []}
        self.tags = {'names': []}
        self.authors = {'names': []}
    
    def missingExamples(self):
        result = []
        for d in self.names:
            if not self.snippets[d].hasExample():
                result.append(d)
        return result
    
    def read(self):
        """Read in all snippets and their examples."""
        self.initLists()
        self.names = self.readDirectory(__main__.appInfo.defPath, ['.ily'])
        xmps = self.readDirectory(__main__.appInfo.xmpPath, ['.ly'])
        
        # read all snippets
        for d in self.names:
            self.snippets[d] = OllItem(self, d)
        # read all examples, ignore missing ones
        for x in xmps:
            self.snippets[x].addExample()
        
        # try to keep the current snippet open
        if (self.current != '') and (self.current in self.names):
            self.mainwindow.showSnippet(self.snippets[self.current])
    
    def readDirectory(self, dir, exts = []):
        """Read in the given dir and return a sorted list with
        all entries matching the given exts filter"""
        result = []
        for item in os.listdir(dir):
            (file, ext) = os.path.splitext(item) 
            if ext in exts:
                result.append(file)
        result.sort()
        return result

    def saveToHtml(self):
        """Write out all snippets' documentation pages."""
        for s in self.snippets:
            self.snippets[s].saveHtml()

    # TEMPORARY
    # Create lists of the different items
    # to be used in preliminary visualization
    def displayCategories(self):
        numcats = ' (' + str(len(self.categories)) + ')'
        result = ['Categories' + numcats, '==========', '']
        for c in self.categories['names']:
            result.append(c + ' (' + str(len(self.categories[c])) + ')')
            for i in self.categories[c]:
                result.append('- ' + i)
            result.append('')
        return result

    def displayOLL(self):        
        numsnippets = ' (' + str(len(self.snippets) - 
                                 len(self.missingExamples())) + ')' 
        result = ['OLL' + numsnippets, '========', '']
        for s in self.names:
            if self.byName(s).hasExample():
                result.append('- ' + s)
        return result

    def displayTags(self):
        numtags = ' (' + str(len(self.tags['names'])) + ')'
        result = ['Tags' + numtags,  '====', '']
        for t in self.tags['names']:
            result.append(t + ' (' + str(len(self.tags[t])) + ')')
            for i in self.tags[t]:
                result.append('- ' + i)
            result.append('')
        return result
        
