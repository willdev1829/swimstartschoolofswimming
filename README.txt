Swim Start — website files
==========================

Everything in this folder is in use by the live website. Nothing else is
needed to put the site online.

What is here
------------

  index.html         Home
  about.html         About us
  timings.html       Location & timings
  merchandise.html   Prices & merchandise
  contact.html       Contact

  css/style.css      All the styling for every page
  js/main.js         The mobile menu and the year in the footer

  images/            Logo and the nine merchandise photos
  server.py          Optional: views the site on this computer only

To put the site online
----------------------

Upload the five .html files, plus the css, js and images folders, keeping
the folder structure exactly as it is here. index.html is the home page.

server.py is NOT needed on a web host — it is only for looking at the site
on this computer.

To view it on this computer
---------------------------

  python server.py

Then open http://127.0.0.1:8777 in a browser. Press Ctrl+C to stop.

Notes
-----

There is no booking system. Enquiries come in by phone (07976 399094) and
email (kerry.swimstart@gmail.com).

The "Meet the team" section on about.html is commented out until there are
real team photos. To bring it back, open about.html and delete the two
comment blocks marked TEMPORARILY HIDDEN. images/Swimstartteam.webp is kept
here for that reason — nothing on the site uses it at the moment.
