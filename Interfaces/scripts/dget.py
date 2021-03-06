#!/usr/bin/env python

"""
download files from storage element
"""

import os

import DIRAC
from COMDIRAC.Interfaces import critical
from COMDIRAC.Interfaces import DSession
from COMDIRAC.Interfaces import DCatalog
from COMDIRAC.Interfaces import pathFromArgument

from DIRAC.Core.Base import Script

Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s lfn... [local_path]' % Script.scriptName,
                                     'Arguments:',
                                     ' lfn:          file to download',
                                     ' local_path:   destination directory',] )
                        )


Script.parseCommandLine( ignoreErrors = True )
args = Script.getPositionalArgs()

session = DSession( )
catalog = DCatalog( )

if len( args ) < 1:
  print "\nError: not enough arguments provided\n%s:" % Script.scriptName
  Script.showHelp( )
  DIRAC.exit( -1 )

# lfn
lfn = pathFromArgument( session, args[ 0 ] )

# default local_path: same file name as lfn.
local_path = os.path.basename( lfn )
# STRANGE: dirac only accepts directories for download destination
#pairs = [ ( lfn, local_path ) ]
pairs = [ ( lfn, os.getcwd( ) ) ]

if len( args ) > 1:
  # local_path provided must be last argument
  local_path = args[ -1 ]
  lfns = args[ :-1 ]
  pairs = [ ]

  # STRANGE: dirac only accepts directories for download destination
  if not os.path.isdir( local_path ):
    print "Error: Destination local path must be a directory"
    DIRAC.exit( -1 )

  if os.path.isdir( local_path ):
    # we can accept one ore more lfns
    for lfn in lfns:
      # STRANGE: dirac only accepts directories for download destination
      #pairs.append( (pathFromArgument( session, lfn ), os.path.join( local_path, os.path.basename( lfn )) ))
      pairs.append( (pathFromArgument( session, lfn ), local_path ))
  else:
    if len( lfns ) > 1:
      print "Error: Destination path must be a directory when downloading multiple local files"
      DIRAC.exit( -1 )

    # local filename replace lfn filename
    pairs.append( (pathFromArgument( session, lfn ), local_path ))

Script.enableCS( )

from DIRAC.DataManagementSystem.Client.FileCatalogClientCLI import FileCatalogClientCLI

fccli = FileCatalogClientCLI( catalog.catalog )

for lfn, local_path in pairs:
  fccli.do_get( lfn + " " + local_path )
