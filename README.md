# xenith_trainer
Manage the training data and the pretrained models included in
[xenith](https://github.com/wfondrie/xenith).

The purpose of this repository is to provide a reproducible pipeline for
generating the pretrained models included in the **xenith** package. It also
provides a means to integrate additional search engines and new versions of
[Kojak](http://kojak-ms.org) in subsequent **xenith** releases. 

Ideally, this repository will allow you to download the raw mass spectrometry
data, convert it to mzML format, download the correct protein database, perform
the database search, and train a xenith model with minimal input. Unfortunately,
full automation is not possible on Linux and MacOS platforms unless the Docker
image of msconvert is used.
