.. streamsense_docs documentation master file, created by
   sphinx-quickstart on Thu Aug  9 20:19:21 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Stream Sense documentation!
============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Device
============================================
Construction
++++++++++++++++++++++++++++++++++++++++++++
* `Particle Photon <https://store.particle.io/collections/photon/>`_ (use `Electron <https://store.particle.io/collections/electron/>`_ if cellular connectivity is required)
* `HC-SR04 ultrasonic sensor <https://www.sparkfun.com/products/13959>`_
* `3.7V LiPo battery <https://www.sparkfun.com/products/13813>`_
* `5V LiPo battery charger and booster <https://www.sparkfun.com/products/14411>`_
* `5V Solar Panel <https://www.amazon.com/ALLPOWERS-Encapsulated-Battery-Charger-130x150mm/dp/B00CBT8A14>`_
* `3D printed parts <https://www.thingiverse.com/rohanmenon/designs>`_

The microcontroller, ultrasonic sensor, battery and charge/boost converter are enclosed in a 3D printed enclosure with a rubber seal to prevent against water damage. The only exposed electronics are the transceivers of the ultrasonic sensor. Switching to a waterproof ultrasonic sensor, while increasing cost, could extend the lifetime of the device.

.. image:: _static/Exploded-01.png

Operation
++++++++++++++++++++++++++++++++++++++++++++
In order to conserve battery, the device stays in a deep sleep until it's ready to send a stage measurement. After waking up, it takes a series of 10 ultrasonic measurements spaced one second apart. These are averaged and then subtracted from the ``HEIGHT_OFF_GROUND`` to produce the stage height value. By default the device sends a measurement every five minutes. In order to simplify the code running on the physical device, the stream flow is computed by the server each time it receives a stage measurement.

Currently, the device does not send POST requests directly to the server. It uses the built in ``Particle.publish()`` to trigger an IFTTT applet to make the POST request. This is mainly because Particle events are stored in a small buffer, so if the server goes down for a brief period of time, the data points are not lost.

Server
============================================
Communication
++++++++++++++++++++++++++++++++++++++++++++
Communicating with the server is easy, it just requires a POST request made to ``stagesense.menon.pro/post``. The request body should be in this format:

``time@siteName@stage@batteryLevel@statusCode``

Each value should be formatted like this:

+--------------+------------------------------------------+---------------------------+
|Value         |Format                                    | Example                   |
+==============+==========================================+===========================+
|time          |[MonthName] [Day], [Year] at 00:00[AM/PM] | August 4, 2018 at 05:21PM |
+--------------+------------------------------------------+---------------------------+
|siteName      |Location name (where the device is placed)| Lisha Kill Preserve       |
+--------------+------------------------------------------+---------------------------+
|stage         |Water height from base of stream (in cm)  | 26                        |
+--------------+------------------------------------------+---------------------------+
|batteryLevel  |Number between 0 and 6 indicating the     | 5                         |
|              |battery level                             |                           |
+--------------+------------------------------------------+---------------------------+
|statusCode    |3 digit error code number (see below)     | 001                       |
+--------------+------------------------------------------+---------------------------+

Here's what an example request would look like:
``August 4, 2018 at 05:21PM@Lisha Kill Preserve@26@5@000``

Each status code corresponds to a specific device state:

+-----------+---------------------------------------------+
|Status Code|Description                                  |
+===========+=============================================+
|    000    |normal operation                             |
+-----------+---------------------------------------------+
|    001    |invalid stage reading                        |
+-----------+---------------------------------------------+
|    002    |battery error                                |
+-----------+---------------------------------------------+
|    003    |water damage detected                        |
+-----------+---------------------------------------------+
