# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 13:33:16 2020

@author: MVSus
"""

import sys
import os 
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QLineEdit,
QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QMessageBox)
from form import *
from numpy import zeros, inf
from astropy.io import fits
import astroscrappy


class Window(QMainWindow):
    
    global filenames
    filenames = []
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.readn_text.setText('-')
        self.ui.gain_text.setText('-')
        self.ui.sigma_text.setText('-')
        
        self.ui.input_btn.clicked.connect(self.open_text)
        self.ui.output_btn.clicked.connect(self.save_text)
        self.ui.start_btn.clicked.connect(self.start_text)
        
        self.outdir = 'path'
        self.num = False
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('Cosmic Ray Removal')
    
    def open_text(self):
        files = QFileDialog.getOpenFileNames(self, 'Open Fits', os.getenv('HOME'))
        for i in range(len(files[0])):
            filenames.append(files[0][i])
    
    def save_text(self):
        self.outdir = str(QFileDialog.getExistingDirectory(self, 'Select Folder'))
        self.num = True
        
    def start_text(self):
        
        status = 0
        end = len(filenames)
        step = 100.0/end
        
        if (self.ui.readn_text.text() == '-') or (self.ui.gain_text.text() == '-') or (self.ui.sigma_text.text() == '-'):
            self.mbox()
        else:
            
            for path in filenames:
                
                hdul = fits.open(path)
                hdr = hdul[0].header
                data = hdul[0].data 
                hdul.close()
            
                read_noise = float(self.ui.readn_text.text())
                gain = float(self.ui.gain_text.text())
                sigma = float(self.ui.sigma_text.text())
                
                
                mask, clean = astroscrappy.detect_cosmics(indat=data, sigclip=sigma, gain=gain, 
                                        readnoise=read_noise, inmask=None, satlevel=inf, 
                                        sepmed=False, cleantype='medmask', fsmode='median') 
    
                maskd = zeros((len(mask),len(mask[0])))
                k = 0
                for i in range(len(mask)):
                    for j in range(len(mask[i])):
                        if mask[i][j] == True:
                            maskd[i][j] = 1.0
                            k += 1
                            
                name = os.path.basename(path)
                self.ui.filename_val.setText(name)
                self.ui.filename_val.update()
                self.ui.cosm_val.setText(str(k))
                self.ui.cosm_val.update()
                
                
                if self.num == False:
                    outdir = os.path.dirname(path)
                else:
                    outdir = self.outdir
                
                hdu1 = fits.PrimaryHDU(clean, hdr)
                hdu1.writeto(outdir + '/cosm_' + name)
                
                hdu2 = fits.PrimaryHDU(maskd, hdr)
                hdu2.writeto(outdir + '/mask_' + name)
                
                status += step
                self.ui.progbar.setValue(status)
                self.ui.progbar.update()
                QApplication.processEvents()
                
            
    def mbox(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText('No input parameters!')
        x = msg.exec_()
            
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())