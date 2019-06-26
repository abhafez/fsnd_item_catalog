# Udacity Item Catalog
A simple web application that provides a list of programming languages filled with some frameworks and libraries. Authenticated users can add, edit, and delete their framework or library.

### How to start Set Up
Clone the [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm).


Remove the catalog folder and with in the folder run this command

`git clone https://github.com/abhafez/fsnd_item_catalog.git`

#### You Need to install
[Vagrant](https://www.vagrantup.com/downloads.html) - A virtual environment builder and manager

[VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) - An open source virtualiztion product.


#### Steps
Start the Vagrant VM from inside the vagrant folder with:

`vagrant up
`

Then access the shell with:

`vagrant ssh
`

Then change directory to the catalog folder:

cd /vagrant/catalog

Then run the application:

python app.py

After the last command you are able to browse the application at this URL:

http://localhost:5000/


