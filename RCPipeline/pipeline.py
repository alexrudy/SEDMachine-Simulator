#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#  pipeline.py
#  SEDM-Dev
#  
#  Created by Alexander Rudy on 2012-04-19.
#  Copyright 2012 Alexander Rudy. All rights reserved.
# 

# Python Imports
import shutil
import os
import collections

# Numpy Imports
import numpy as np

# Package Resources Imports
from pkg_resources import resource_filename

# PyRAF Imports
from pyraf import iraf
from iraf import imred, ccdred

from AstroObject.AstroSimulator import Simulator
from AstroObject.AstroSimulator import (
    optional,
    description,
    include,
    replaces,
    depends,
    excepts,
    collect,
    ignore,
    help
)
from AstroObject.AstroImage import ImageStack
from AstroObject.iraftools import UseIRAFTools
from AstroObject.AstroObjectLogging import logging
ImageStack = UseIRAFTools(ImageStack)

class RCPipeline(Simulator):
    """A task manager for the RC Pipeline"""
    def __init__(self):
        super(RCPipeline, self).__init__(commandLine=True,version="0.3.9-p3")
        self.config.load(resource_filename(__name__,"Defaults.yaml"))
        self.config.setFile("Main")
        self.config.load()
        self.collect()
    
    @ignore
    def load_type(self,key,stack):
        """Load a specific type of files using a generalized loading procedure"""
        if isinstance(self.config[key]["Files"],collections.Sequence):
            for filename in self.config[key]["Files"]:
                stack.read(filename)
                self.log.debug("Loaded %s: %s" % (key,filename))
        else:
            self.log.error("No %s files are given." % key)
            raise IOError("No %s files are given." % key)
    
    def load_bias(self):
        """Loading Raw Bias Frames"""
        # Load individual bias frames.
        self.bias = ImageStack()
        self.load_type("Bias",self.bias)
        # Set Header Values for each image.
        for frame in self.bias.values():
            frame.header.update('IMAGETYP','zero')
            self.log.debug("Set IMAGETYP=zero for frame %s" % frame)
        self.log.debug("Set Header IMAGETYP=zero for frames %r" % self.bias.list())
        
    def load_dark(self):
        """Loading Dark Frames"""
        # Load individual bias frames.
        self.dark = ImageStack()
        self.load_type("Dark",self.dark)
        # Set Header Values for each image.
        for frame in self.dark.values():
            frame.header.update('IMAGETYP','dark')
            self.log.debug("Set IMAGETYP=dark for frame %s" % frame)
        self.log.debug("Set Header IMAGETYP=dark for frames %r" % self.dark.list())
        
    def load_flat(self):
        """Loading Dark Frames"""
        # Load individual bias frames.
        self.flat = ImageStack()
        self.load_type("Flat",self.flat)
        # Set Header Values for each image.
        for frame in self.flat.values():
            frame.header.update('IMAGETYP','flat')
            self.log.debug("Set IMAGETYP=flat for frame %s" % frame)
        self.log.debug("Set Header IMAGETYP=flat for frames %r" % self.dark.list())
    
        
        
    @help("Create bias frames from the configured bias list.")
    @depends("load-bias")
    def create_bias(self):
        """Creating Combined Bias Frame"""
        self.log.debug("Running iraf.zerocombine on image list...")
        iraf.unlearn(iraf.zerocombine)
        iraf.zerocombine(self.bias.iinat(),
            output=self.bias.iout("Bias"),
            combine=self.config["Bias.Combine"], 
            ccdtype="zero", 
            reject=self.config["Bias.Reject"], 
            scale="none", nlow=0, nhigh=1, nkeep=1, mclip="yes", lsigma=3.0, hsigma=3.0, rdnoise="0.", gain ="1."
            )
        self.bias.idone()
    
    @help("Create Dark Frames")
    @depends("load-dark")
    def create_dark(self):
        """Creating Combined Dark Frame"""
        self.log.debug("Running iraf.darkcombine on image list...")
        iraf.unlearn(iraf.darkcombine)
        iraf.darkcombine(self.dark.iinat(),
            output=self.dark.iout("Dark"),
            combine=self.config["Dark.Combine"], 
            ccdtype="dark", 
            reject=self.config["Dark.Reject"], 
            process="no", scale="exposure", nlow=0, nhigh=1, nkeep=1, mclip="yes", lsigma=3.0, hsigma=3.0, rdnoise="0.", gain ="1."
            )
        self.dark.idone()
    
    @help("Create Flat Frames")
    @depends("load-flat")
    def create_flat(self):
        """Creating Combined Flat Frame"""
        self.log.debug("Runnign iraf.flatcombine on image list...")
        iraf.unlearn(iraf.flatcombine)
        iraf.flatcombine(self.flat.iraf.inatfile(),
            output=self.flat.iraf.outfile("Flat"), 
            combine=self.config["Flat.Combine"], 
            ccdtype="flat",
            reject=self.config["Flat.Reject"],
            scale=self.config["Flat.Scale"], 
            process="no", subsets="no", nlow=0, nhigh=1, nkeep=1, mclip="yes", lsigma=3.0, hsigma=3.0, rdnoise="0.", gain ="1.")
        self.flat.iraf.done()
        
    def load_data(self):
        """Loading Raw Data into the system."""
        self.data = ImageStack()
        self.load_type("Data",self.data)
        
    @include
    @depends("create-bias","load-data")
    @help("Subtract Bias Frame")
    def subtract_bias(self):
        """Subtracting Bias Frame"""
        iraf.unlearn(iraf.ccdproc)
        iraf.ccdproc(self.data.iraf.modatfile(), 
            ccdtype="", fixpix="no", overscan="no", trim ="no", zerocor="yes", darkcor="no", flatcor ="no", 
            zero=self.bias.iin("Bias"))
        self.data.idone()
       
    @include
    @depends("create-dark","load-data")
    @help("Subtract Dark Frame")
    def subtract_dark(self):
        """Subtracting Dark Frame"""
        iraf.unlearn(iraf.ccdproc)
        iraf.ccdproc(self.data.iraf.modatfile(), 
            ccdtype="", fixpix="no", overscan="no", trim ="no", zerocor="no", darkcor="yes", flatcor ="no", 
            dark=self.dark.iin("Dark"))
        self.data.idone()
    
    @include
    @depends("create-flat","load-data")
    @help("Divide out flat frame")
    def divide_flat(self):
        """Dividing by Flat Frame"""
        iraf.unlearn(iraf.ccdproc)
        iraf.ccdproc(self.data.iraf.inatfile(), 
            output=self.data.iraf.outatfile(append="-Flat"),
            flat=self.flat.iin("Flat"),
            ccdtype="", fixpix="no", overscan="no", trim ="no", zerocor="no", flatcor="yes", darkcor ="no")
        self.data.iraf.done()
    
    @include 
    @depends("load-data")
    def save_file(self):
        """Save the new fits file"""
        self.data.write("DataFile.fits",frames=[self.data.framename],clobber=True)
        
    @help("Save Partial Images")
    @depends("create-flat","create-dark","create-bias")
    def save_partials(self):
        """Saving partial images"""
        self.bias.write(frames=["Bias"],filename=self.config["Bias.Master"],clobber=True)
        self.dark.write(frames=["Dark"],filename=self.config["Dark.Master"],clobber=True)
        self.flat.write(frames=["Flat"],filename=self.config["Flat.Master"],clobber=True)
        
        
def main():
    pipeline = RCPipeline()
    pipeline.run()     
                
    
        
if __name__ == '__main__':
    main()
