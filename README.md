# archc0n2016

!!! SETUP !!!

I demo and teach Windows IR workshops with Windows, shockingly. If you want to follow along you should have a Windows VM handy - 7 or higher is fine. 

Examples are written in Python 2.7. To use the precompiled Windows Python bindings in the workshop, you'll want the x86 installer here: https://www.python.org/downloads/release/python-2711/.

I like PyCharm as an IDE - you can snag the community edition here: https://www.jetbrains.com/pycharm/download. If you don't want to clutter your machine with an IDE, Python's IDLE will work fine. 

I use the ELK stack to demo log ingestion and hunting automation. There are many big data solutions that you could use for this, but if you'd like to follow along you should install these: 

-ElasticSearch https://www.elastic.co/products/elasticsearch

-LogStash https://www.elastic.co/products/logstash

The data for logstash will come from running CrowdResponse, a freeware tool from CrowdStrike: https://www.crowdstrike.com/resources/community-tools/. 

Resource Hacker will be used to demonstrate build automation - before you use it READ THE EULA for all the things: http://www.angusj.com/resourcehacker/. You want the portable version.

I'll be opening some files in a hex editor. If you'd like to follow along you'll need one too - on Windows I use Notepad++ with the hex editor plugin: https://notepad-plus-plus.org/download/v6.9.2.html

You may also want FTK imager to view files on your local Windows machine: http://accessdata.com/product-download/digital-forensics/ftk-imager-version-3.4.2. If you want to mess with it beforehand, here's a simple guide I put together: https://drive.google.com/open?id=1802LtrMIz1LSK1D2wqcSlKqSaNyO2uIbZo6XIrhBmZ4. 

Never EVER distribute other peoples' code or tools without reading the associated licenses for their tools and understanding their distribution terms. 



