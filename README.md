The-Agora-Initiative
====================
The Agora Initiative is a french association.  
Our goal is to collectively build a digital tool for an agile and multi-scale participative democracy.  
The community is openned to anyone willing to contribute in the development of participative democracy.

For more infos, please visit : https://initiativeagora.wordpress.com/

Back-End
========
The Back-End is based upon the Django Framework.

If you are not familiar with it, please refer to the official documentation :
https://docs.djangoproject.com/en/3.2/

Installing the project on your machine
--------------------------------------
In a terminal, run the following command :

    git clone https://github.com/will-afs/The-Agora-Initiative.git

Installing the Back-End on your machine
---------------------------------------   
Make sure to use Python>= 3.7.
You can check your Python version by running :

    python --version

You can use your own virtual environment.
If you are using Visual Studio Code as an IDE, you can find more info on : https://code.visualstudio.com/docs/python/environments

Then, make sure to install the necessary Python dependencies in it by running :
    
    pip install -r requirements.txt
    
To avoid compromising the Django Secret Key, it is not stored in clear in the settings.py file.
Thus, one should create a .env file into the backend/agorabackend directory, which contains the following fields :

    DEBUG = True
    SECRET_KEY = <django generated secret key (as a string)>
    
And to generate a django secret key, run the following command with the python interpreter:

    from django.core.management.utils import get_random_secret_key  
    get_random_secret_key()


Running the Back-End
--------------------
You should work within the backend directory.

To run the Back-End, you need to run the following command :

    python manage.py runserver
    

    
Editing the Back-End
--------------------
If you made modifications upon the data model (model.py files), you can visualize migrations by running :

    python manage.py makemigrations
    
And apply them to the database by running :

    python manage.py migrate
    
 
    
    
