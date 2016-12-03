#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# @date:   Tue Aug  11 14:07:00 CEST 2015
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This script creates the Near-Infrared and Visible-Light (NIVL) Dataset in a single pass.


--- TEXT REMOVED FROM THE Readme.txt of the database -----

II.  NIVL Dataset Structure

The NIVL dataset spans multiple directories of images and metadata files that can be used as inputs to face recognition experiments.  There are three types of metadata files:

Image list - a sequence of paths to images of one subject photographed during a single session with a particular sensor, with one path per line.  A pair of image lists constitues a (non-)match pair if both lists correspond to the same (different) subject(s).

Image list collection - a sequence of paths to image lists, with one path per line.  An image list collection can describe the entries of a gallery or probe set.

Label list - a comma-separated value (CSV) listing of the subject identifiers for image lists.  A label list provides the information needed for determining which pairs of image lists match.  Each line of a label list should adhere to the following format:

{image list path},{subject identifier}


"""

import os

from .models import *
from .models import PROTOCOLS, GROUPS, PURPOSES
import pkg_resources
import numpy
numpy.random.seed(10)


def _update(session, field):
  """Add, updates and returns the given field for in the current session"""
  session.add(field)
  session.flush()
  session.refresh(field)
  return field


def parse_file_name(file_name):
  """
    Parse the filenames  
    VIS - ANN_XXXYY_Z_VI_fMM
    
    The images has the following pattern

    ANN_XXXYY_Z_VI_fMM like this example (A01_IOD87_B_VI_f01.png) where:
    - NN is the client id
    - XXXYY means inter-ocular distance (XXX) and distance (YY)
    - Z is the condition B=Baseline (neutral expression) and E=Expression (the clients where asked to count from 1 to n)
    - VI means visible spectra
    - MM is the shot (from 1-4)
        
    
    THERMAL - ANN_RM_Z_XX_fWW where:
    - NN is the client id
    - M is the range (1-3 (2.5m, 5m, 7.5m))
    - Z is the condition B=Baseline (neutral expression) and E=Expression (the clients where asked to count from 1 to n)
    - XX is the type of the polarization (S0 (real thermal), S1, S2, DP (DoLP))
    - WW is the shot (from 1-4)
  """

  elements = file_name.split("_")
  if file_name.find("_VI_") > 0:
    client = elements[0]
    capture_range = "R1"
    condition = elements[2]
    polarization = "VIS"
    shot = elements[4]
    modality = "VIS"
  else
    client = elements[0]
    capture_range = elements[1]
    condition = elements[2]
    polarization = elements[3]
    shot = elements[4]
    modality = "THERMAL"
    
  return client, capture_range, condition, polarization, shot, modality


def add_clients_files(session, image_dir, verbose = True):
  """
  Add the clients and files in one single shot
  
  """

  annotations_l = [106, 65]
  annotations_r = [106, 140]

  directories = ['Visible/IOD87_B/','Polarimetric'] # Files with the labels ({image list path},{subject identifier})

  clients  = {} #Controling the clients and the sessions captured for each client
  files    = []
  file_id_offset = 0

  # Navigating in the direcoty
  for d in directories:  
    for f in os.listdir(os.path.join(image_dir, d)):
  
      file_name, extension = os.path.splitext(f)
      
      # Adding only PNG
      if extension==".png" and file_name.find("_S1_") < 0 and file_name.find("_S2_") < 0 :
        client, capture_range, condition, polarization, shot, modality = parse_file_name(file_name)
      
        # Adding client
        if(not client in clients):
          clients[client] = 1
          if verbose>=1: print("  Adding client {0}".format(client_name))  
          session.add(Client(id=client_name,group='world'))
        else:
          clients[client_name] += 1 #If the client already exists in the database, include the session

        if verbose>=1: print("  Adding file {0}".format(file_name))
        file_id_offset += 1
        f = File(file_id=file_id_offset,
                 client_id = client,
                 image_name = file_name,
                 modality=modality,
                 polarization=polarization,
                 shot=shot)
        session.add(f)
        session.add(Annotation(file_id = file_id_offset, re_x=annotations_r[0], re_y=annotations_r[1], le_x=annotations_l[0], le_y=annotations_l[1]))
        files.append([file_name])

        return files


def add_protocols (files, split_number):

  total_clients = range(len(clients))
  numpy.shuffle(total_clients)

  train_clients = [0:25]
  test_clients = [25:]
  
  polarization = ['thermal', 'overall']
  expression = ['overall', 'expression']
  range_number = ['R1', 'R2', 'R3']
  
  for e in expression:
    for p in polarization:
      protocol = 'VIS-{0}-{1}-split{2}'.format(p, e, split_number)
      
      for f in files:
        
        if p in f and e in f:
          
          session()



def add_protocols_original(session, verbose = True):
  """
  Adding the two original protocols described in:
  
  Near-IR to Visible Light Face Matching: Effectiveness of Pre-Processing Options for Commercial Matchers
  
  
  For the first protocol, called `original_2011-2012` the VIS-2011 images are used as gallery and the NIR-2012 images are used as probes.
  For the first protocol, called `original_2012-2011` the VIS-2012 images are used as gallery and the NIR-2011 images are used as probes.
  
  """
  if verbose>=1: print("  Adding original protocols")

  galery_years = [2011,2012]
  probe_years  = [2012,2011]
  group   = "eval"
  purpose = "enroll"

  #Adding galery
  for i in range(len(galery_years)):
    galery = galery_years[i]
    probe  = probe_years[i]    
    protocol = "original_{0}-{1}".format(galery,probe)
   
    query = session.query(File) \
     .filter(File.year     == galery) \
     .filter(File.modality == 'VIS')

    for f in query.all():
      _update(session,Protocol_File_Association(protocol, group, purpose, f.id))


  #Adding probes
  purpose = "probe"  
  for i in range(len(galery_years)):
    galery = galery_years[i]
    probe = probe_years[i]
    
    protocol = "original_{0}-{1}".format(galery,probe)
   
    query = session.query(File) \
     .filter(File.year     == probe) \
     .filter(File.modality == 'NIR')

    for f in query.all():
      _update(session,Protocol_File_Association(protocol, group, purpose, f.id))




def add_protocol_search(session, verbose = True):
  """
  Adding the Idiap CUSTOMISED SEARCH protocol
  
  This protocol uses:
    344 clients for training
    230 clients for development set
  
    Here I will create 10 protocols (split):

     - idiap-search_VIS-NIR_split[1-5]
       - Training: 344 clients (pairs VIS-NIR)
       - Development: 230 clients. VIS Images from 2011 for enrollment and NIR images (both years) for probing
                                   **** IF IS NOT POSSIBLE TO GET ONE IMAGE FROM 2011 FOR ENROLLMENT, GET THE FIRST FROM 2012 ****

  """
  n_clients_per_group = {'world':344,
                         'dev':230} #THE NUMBER OF CLIENTS IN EACH GROUP IS HARDCODED
  groups       = ["dev", "world"]

  import numpy
  numpy.random.seed(10)  #Stabilizing the list
    
  
  for split in range(1,6):
  

    #Shuffle the clients
    client_indexes = range(574)
    numpy.random.shuffle(client_indexes)

    clients = session.query(Client).all();
    client_ids = numpy.array([c.id for c in clients])

    offset = 0

    protocol = "idiap-search_VIS-NIR_split{0}".format(split)
    protocol_VIS = "idiap-search_VIS-VIS_split{0}".format(split) #Protocol to do VIS-VIS comparison
      
    
    if verbose>=1: print("  Adding the protocol %s " % protocol)
    
    for g in groups:

      indexes = client_indexes[offset:offset+n_clients_per_group[g]]
      clients_per_group = client_ids[indexes]
      offset += n_clients_per_group[g]
      
      if verbose>=1: print("    Group %s " % g)

      #Adding the world set data
      if (g=='world'):

        #Adding the VIS-NIR
        query = session.query(File) \
        .filter(File.client_id.in_(clients_per_group))        
        for f in query.all():
          _update(session,Protocol_File_Association(protocol, g, "train", f.id))

        #Adding the VIS-VIS
        query = session.query(File) \
        .filter(File.client_id.in_(clients_per_group))\
        .filter(File.modality == 'VIS')

        for f in query.all():
          _update(session,Protocol_File_Association(protocol_VIS, g, "train", f.id))

      else:
      
        ## Inserting each client
        for c in clients_per_group:

          #Adding the enrollment data - VIS-NIR and VIS-VIS
          ## FIRST TRY TO FIND SOME 2011 images
          query = session.query(File) \
          .filter(File.client_id==str(c)) \
          .filter(File.modality == 'VIS') \
          .filter(File.year == 2011)

          files = query.all()
          if(len(files) == 0):
            #IF DOES NOT HAVE ANY FILE FROM 2011, TAKE THE FIRST FROM 2012
            query = session.query(File) \
            .filter(File.client_id==str(c)) \
            .filter(File.modality == 'VIS') \
            .filter(File.year == 2012)

            files = query.all()
            assert len(files)>0
            files = [files[0]] #first from 2012

          for f in query.all():
            _update(session,Protocol_File_Association(protocol, g, "enroll", f.id))
            _update(session,Protocol_File_Association(protocol_VIS, g, "enroll", f.id))            


        #Adding the probing data - VIS-NIR
        query = session.query(File) \
        .filter(File.client_id.in_(clients_per_group)) \
        .filter(File.modality == 'NIR')

        for f in query.all():
          _update(session,Protocol_File_Association(protocol, g, "probe", f.id))


        #Adding the probing data - VIS-VIS
        query = session.query(File) \
        .filter(File.client_id.in_(clients_per_group)) \
        .filter(File.modality == 'VIS') \
        .filter(File.year == '2012')

        for f in query.all():
          _update(session,Protocol_File_Association(protocol_VIS, g, "probe", f.id))


def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2));
  Client.metadata.create_all(engine)
  File.metadata.create_all(engine) 
  Annotation.metadata.create_all(engine)
  #Protocol_File_Association.metadata.create_all(engine)


# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))
  add_clients_files(s, args.image_dir, annotation_dir, args.verbose)
  #add_protocol_search(s, args.verbose)

  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
  parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?')
  parser.add_argument('-d', '--image-dir', default='/idiap/resource/database/nivl/nivl-dataset-v1.0/', help="Change the relative path to the directory containing the images of the NIVL database.")

  parser.set_defaults(func=create) #action
