// MY DIRE SIMULATION PROGRAM
// mydire.cc is a part of the PYTHIA event generator.
// Copyright (C) 2021 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.
// Author: Stefano Veroni
// 10/07/2021
// Keywords: Dire, LHC, boh...
// Main inspirations: main04.cc, compass2.cmnd, main36.cc, main91.cc, main92.cc
// Running lines:
// make main999
// ./main999 main999.cmnd > main999.out

#include "Pythia8/Pythia.h" // Include Pythia headers.

// HEPMC3
//#ifdef HEPMC3
//#include "Pythia8Plugins/HepMC3.h"
//#endif


// ROOT, for histogramming.
#include "TH1.h"
// ROOT, for interactive graphics.
#include "TVirtualPad.h"
#include "TApplication.h"
// ROOT, for saving file.
#include "TFile.h"
// ROOT, for saving Pythia events as trees in a file.
#include "TTree.h"
#include "TFile.h"

// Include graphviz visualisation plugin.
#include "Pythia8Plugins/Visualisation.h"

#include <iostream>
//#include <algorithm> 

//====================================================================

using namespace Pythia8;    


int main(int argc, char* argv[]) { 

  // Generator. Shorthand for the event and info.
  Pythia pythia;
  Event& pythiaevent = pythia.event;
  //Info& info = pythia.info; //can't understand why not working

  //Uses settings in cardfile.
  pythia.readFile  (argv[1]); 
  
  // Create the ROOT application environment.
  TApplication theApp("hist", &argc, argv);
  // Create file on which histogram(s) can be saved.
  TFile* outFile = new TFile("main999hists.root", "RECREATE");
    
  //Histograms for kinematic variables (ROOT and system).
  double mA   = pythia.particleData.m0( pythia.mode("Beams:idA") );
  double eA   = std::max( pythia.parm("Beams:eA"), mA ); 
  double mB   = pythia.particleData.m0( pythia.mode("Beams:idB") );
  double eB   = std::max( pythia.parm("Beams:eB"), mB ); 
  double smax = 4. * eA * eB;
  double Wmax = sqrt(smax); 
  TH1F *Q2root = new TH1F("Q2root", "Q^2 [$GeV^2$]", 100, 0, 20); 
  TH1F *Wroot  = new TH1F("Wroot" , "W [GeV]", 100, 0., Wmax); 
  TH1F *xroot  = new TH1F("xroot" , "Bjorken Variable x", 100, 0, 1); 
  TH1F *yroot  = new TH1F("yroot" , "Virtual Photon Fractional Energy y", 100, 0, 1); 
  //Hist Q2hist ("Q^2 [$GeV^2$]", 100, 0, 20);
  //Hist Whist  ("W [GeV]", 100, 0., Wmax);
  //Hist xhist  ("Bjorken Variable x", 100, 0, 1);
  //Hist yhist  ("Virtual Photon Fractional Energy y", 100, 0, 1);

  // Define some vectors to store kinematic variables
  // Don't really know if useful
  //std::vector<double> Q2vec;
  //std::vector<double> xvec;
  //std::vector<double> yvec;
	
  // Extract settings to be used in the main program.
  int nEvent = pythia.mode("Main:numberOfEvents");

  // Initialize (for init settings see article page 10)
  if(!pythia.init()) { return EXIT_FAILURE; }
  
  // Set up the ROOT TFile and TTree.
  TFile *file  = TFile::Open("main999tree.root","recreate");
  Event *event = &pythia.event;
  TTree *Tree  = new TTree("Tree","ev1 Tree");
  Tree -> Branch("event",&event);

  // Begin event loop.
  int isuccess = 0;
  for (int iEvent = 0; iEvent < nEvent; ++iEvent) {       

	// Generate events.
        if (pythia.next()) ++isuccess;
        else continue;
        
        // Fill the pythia event into the TTree.
        // Warning: the files will rapidly become large if all events
   	// are saved. In some cases it may be convenient to do some
    	// processing of events and only save those that appear
    	// interesting for future analyses.
    	Tree -> Fill();
        
        // Terminate after N successful events: N-1 are analysed.
        // Used for testing
        if (isuccess == 51) break;
        
        // Four-momenta of proton, electron, virtual photon/Z^0/W^+-.
        Vec4 pProton = pythiaevent[2].p();
        Vec4 peIn    = pythiaevent[1].p();
	Vec4 peOut   = pythiaevent[5].p();
	Vec4 pPhoton = peIn - peOut;

	// Q2, W2, Bjorken x, y.
	double Q2    = - pPhoton.m2Calc();
	double W2    = (pProton + pPhoton).m2Calc();
	double x     = Q2 / (2. * pProton * pPhoton);
	double y     = (pProton * pPhoton) / (pProton * peIn);
	
	// Fill root kinematics histograms.
        Q2root->Fill( Q2 );
        Wroot ->Fill( sqrt(W2) );
        xroot ->Fill( x );
        yroot ->Fill( y );

	// Fill system kinematics histograms.
	//Q2hist.fill( Q2 );
	//Whist.fill( sqrt(W2) );
	//xhist.fill( x );
	//yhist.fill( y );
	
	// Might be useful.
	//double eCM = pythia.info.eCM();   
        //double s   = pythia.info.s();     //eCM^2      
        //Print the whole event
        //event.list();	
  // End event loop.
  }
     
  //Gets some statistics and print system histograms.
  pythia.stat(); 
  //std::cout << Q2hist << Whist << xhist << yhist;
  
  //  Write root tree.
  Tree -> Print();
  Tree -> Write();
  delete file;
  
  // Show root histograms. Possibility to close it.
  std::cout << "\nDouble click on the histogram window to quit.\n";
  Q2root -> Draw();
  gPad->WaitPrimitive();
  Wroot  -> Draw();
  gPad->WaitPrimitive();
  xroot  -> Draw();
  gPad->WaitPrimitive();
  yroot  -> Draw();
  gPad->WaitPrimitive();

  // Save histogram on file and close file.
  Q2root-> Write();
  Wroot -> Write();
  xroot -> Write();
  yroot -> Write();
  delete outFile;
  
  //Done
  return 0;

}           
