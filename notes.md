## 02020.08.27  
Next steps for DownloaderGUI:  
* Currently relies on defaults of the ImageScraper class. Controls need to be added to DowndloaderGUI to  
  * Load a predefined search list.
  * Change the number of images to be found.
  * Allow a user to decide whether only URLs are to be saved.
  * Change the target where images are to be saved
* Add a separate method to process the list of search terms.
* Remove the search seed: having a separate window to handle nearest neighbor discovery renders it redundant and weird.

## 02020.10.20  
Targets:  
* Pause, Cancel, and Save buttons.

## 02020.10.29  
* Inter-thread messages need to be streamlined.
* CandidateScraperGUI needs something to handle thread messages when it closes.
