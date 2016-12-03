#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# Tue 08 Dec 2015 11:18:06 CET 
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the ipyplotied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Given a model ID, open and save the image files from the nivl database
"""


import os
import bob.db.nivl
import bob.io.image
import bob.io.base
import numpy

def normalize4save(img):
  return (255 * ((img - numpy.min(img)) / (numpy.max(img)-numpy.min(img)))).astype("uint8")


def main():

  protocol  = "idiap-search_2011-VIS-NIR_split1"
  models    = ['nd1S05456','nd1S05880','nd1S05624']
  #input_dir = '/idiap/resource/database/nivl/nivl-dataset-v1.0/'
  input_dir = '/idiap/temp/tpereira/HTFace/NIVL/2011/search_split1_p2s/ISV/g512_u160/preprocessed/'
  #extension = '.png'
  extension = '.hdf5'
  output_dir = '/idiap/home/tpereira/dev_projects/bioidiap/bob.db.nivl/temp'

  #enroll_dir = os.path.join(output_dir, "enroll")
  #probe_dir  = os.path.join(output_dir, "probe")

  #bob.io.base.create_directories_safe(enroll_dir)
  #bob.io.base.create_directories_safe(probe_dir)
  db = bob.db.nivl.Database(original_directory = input_dir, original_extension=extension)

  for m in models:

    #Saving enroll data
    for o in db.objects(protocol="idiap-search_2011-VIS-NIR_split1", groups='dev', purposes="enroll",  model_ids=[m]):
      img = bob.io.base.load( 
            os.path.join(input_dir,o.make_path()+extension)
            )
        
      img = normalize4save(img).astype('uint8')
        
      file_name = os.path.join(output_dir,m,"enroll",o.make_path()+".jpg")
      bob.io.base.create_directories_safe(os.path.dirname(file_name))
      bob.io.base.save(img,file_name)


    #Saving enroll data
    for o in db.objects(protocol="idiap-search_2011-VIS-NIR_split1", groups='dev', purposes="probe",  model_ids=[m]):

     if(o.client_id==m):
       img = bob.io.base.load( 
             os.path.join(input_dir,o.make_path()+extension)
             )
       img = normalize4save(img).astype('uint8')
    
       file_name = os.path.join(output_dir,m,"probe",o.make_path()+".jpg")
       print(file_name)
       bob.io.base.create_directories_safe(os.path.dirname(file_name))

       bob.io.base.save(img,file_name)


