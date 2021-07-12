The-Agora-Initiative
====================
The Agora Initiative is a french association.  
Our goal is to collectively build a digital tool for an agile and multi-scale participative democracy.  
The community is openned to anyone willing to contribute in the development of participative democracy.

For more infos, please visit : https://initiativeagora.wordpress.com/


Installing the Back-End on your machine
=======================================
In a terminal, run the following command :

    git clone https://github.com/will-afs/The-Agora-Initiative.git
    
Then, make sure to use Python>= 3.7.
You can check your Python version by running :

    python --version

You can use your own virtual environment.
If you are using Visual Studio Code as an IDE, you can find more info on : https://code.visualstudio.com/docs/python/environments

Then, make sure to install the necessary Python dependencies in it by running :
    
    pip install -r requirements.txt
    

Running the Back-End
====================

The Back-End is based upon the Django Framework

To run it, you need to run the following command :

    python manage.py runserver
    
You can 
    
Editing the Back-End
====================

Before going any further, if you are not familiar with the Django framework, please refer to the official documentation :
https://docs.djangoproject.com/en/3.2/

If you made modifications upon the data model (model.py files), you can visualize migrations by running :

    python manage.py makemigrations
    
And apply them to the database by running :

    python manage.py migrate
 
    
    
