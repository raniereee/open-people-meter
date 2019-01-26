# Open People Meter
Project of software for create a identify what tv channel is synthonized

## System Architecture
![Alt text](imgs/architecture.jpeg?raw=true "Architecture System")

## Software

### Dependencies
This is principal dependency of project.

[Dejavu](github.com/worldveil/dejavu/)

Another very important dependency it is:

github.com/jiaaro/pydub

### Modules

#### Base Stations
Hardware remote that capture and process it, generating the fingerprints files and send to server for comparations. Only 7 seconds of audio are processed and sent to server the fingerprints file.

#### Servers
* Bases for capure
	* Bases (cubieboard) that capture 30s of audio of the TV receiver. These 30 seconds must contain the 7seconds of the audio captured on bases stations.

* Audio processing
	* Server tha receive data fingerprints of bases and make comparations after finish the processing a minute of audio in server side

* Data base for comparation
	* Data base that store the fingerprints of audios captured for bases of capture, and used for compatarion in each minute.

* Reports data base

	* Data base for store result of comparation and web server will use.

* Web server
	* Server of application

## Hardware

All stations bases use as base a cubieboard A10 platform, because there is a auxiliar audio input native in this board.
![Alt text](imgs/cubieboard.jpeg?raw=true "CubieBoard")

In this system, the capture board is connected on auxiliar output of TV device.

![Alt text](imgs/audio_tv.jpg?raw=true "AuxOutput")
