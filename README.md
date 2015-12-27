FCC Political Ads
==================

FCC Political Ads tracks political ad buy documents across television stations, and powers PoliticalAdSleuth.com

Most data comes directly from the FCC's RSS feed, but this code also contains functionality to (i) scrape station websites in case the RSS feed goes down temporarily and (ii) accept manual uploads/entry of documents and metadata by volunteers.

This code was originally written prior to 2012 and 2014 developments in which the FCC ordered affiliates of the top broadcast networks to begin posting their political ad files online. As such, volunteer document entry was key to how the project was conceptualized at the time, but generates a significantly smaller share of the data now. This shift in the primary purpose of the code warrants an overall refactor at such point that additional major pieces of functionality are being considered.




Setting up for local development
---------------------------

**Installing packages**

These instructions assume that you'll be developing inside a virtual environment.

1. Once you've cloned this repository, navigate to the top level of `fcc_political_ads`. You should see a `requirements.txt` file here.

2. Create and activate your virtual environment, and install packages by running:

     ```pip install -r requirements.txt```

3. Note that if you don't already have Mercurial installed on your system, you'll see errors related to the hg command when you run the command above, and your installations will not begin. To address this, first run this command on its own:

     ```pip install mercurial```

     and then run

     ```pip install -r requirements.txt```  
  
  
**Configuring local settings** 

4. Navigate to `fcc_politicalads/fcc_adtracker/fcc_adtracker`
You should see both a `settings.py` file and a `local_settings.py.example` file.

5. Create a copy of `local_settings.py.example` and name it `local_settings.py`.
This code is set up such that settings.py pulls from `local_settings.py`, and `local_settings.py` is excluded from version control. The rest of the steps in this section are for changes you shold make to `local_settings.py`.

6. In your database settings, fill in at least the `'ENGINE'` and `'NAME'` fields:

    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',                      # Or path to database file if using sqlite3.
            ....
        }
    }
    ```

    So, for example, the following is fine for development in sqlite3: 
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'adsleuth.sqlite3',

    If you are using another backend, you'll need to fill out additional fields (at least user and password).

7. Change the `SECRET_KEY` to any string you'd like, and share this with no one.

8. Fill in `DOCUMENTS_PATH` in the DocumentCloud section as follows:

    ```DOCUMENTS_PATH = os.path.join(MEDIA_ROOT, 'documents')```

9. You'll need to add something to the `STATIC_URL`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` fields to avoid authorization handler errors and be able to launch the development server without errors.
While not vital to backend development, these values will need to be the actual URL and credentials of this system's Amazon S3 bucket in order for css files and images to appear correctly during development.
As an alternative, you can configure local_settings.py differently to pull static files from a local source (but these changes should NOT be made to settings.py)

10. If you plan to develop on and test features that use email (such as volunteer signup), you'll also need to fill out email settings:
    ```
    EMAIL_HOST = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_HOST_USER = ''
    EMAIL_PORT = ''
    ```

    If these are left blank, you can expect 'connection refused' errors upon triggering email functions.

    Note that if you are using a personal Gmail account to test, you will need to turn on "Access for less secure apps" in your account's security settings in order to avoid authentication errors. You'll also need to add these lines to your local_settings:

    ```
    EMAIL_USE_TLS   = True  
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ```



**Database setup and synchronization** 

FCC Political Ads was written for Django 1.4<1.5, and uses South to manage schema migrations (Django's built-in funcionality did not appear until 1.7).

Dependencies (sometimes circular, as is to be expected for a system whose purpose has changed significantly over time) exist across the six apps in the FCC Political Ads system: fecdata, scraper, locations, broadcasters, volunteers, and fccpublicfiles. The less intuitive commands at the end of these instructions, if executed in order, are intended to resolve dependencies so that a fresh install can be performed for local development.


To set up your local database and update migrations:

1. (Skip this step if you are using sqlite3) Once you've filled in your database settings (see above), run your database create command using the database name you entered in your settings.

2. Then, run the following to create database tables:

    ```./manage.py syncdb```

3. And run the following to create a migrations history on your machine (helps with any future migrations):

    ```./manage.py migrate --fake```

4. Finally, execute the following commands in this order to resolve issues with dependencies:
    ```./manage.py schemamigration fccpublicfiles --initial```
    
    ```./manage.py schemamigration scraper --initial```

    ```./manage.py schemamigration volunteers --initial```
    
    ```./manage.py migrate```


5. The database needs a Site object with ID=1 in order to load components properly. To do this, first run:
    ```./manage.py shell```

    Once the shell opens, run the following commands:
    ```
    >>> from django.contrib.sites.models import Site  
    >>> site = Site.objects.create(domain='politicaladsleuth.com', name = 'politicaladsleuth.com')  
    >>> print site.id
    ```
    You are looking here for a site ID of 1 to print out, at which point you can exit the shell.

6. If the database is not holding any ad buy data, you will encounter errors in loading some pages (e.g. pages at the links for Enter an Ad / Newest Ads / Market Report). Sample or backup data will need to be entered, or variables will need to be commented out in views.py and the page template.


App structure and other context clues for developers
----------------------------------------------------


1. **App structure** [forthcoming]

2. **Instructions for manually scraping and backing up data** [forthcoming]

3. **Email functionality**: If you are using a personal email to send account activation emails for new users (see configuring local settings section on how to set this up), note that this will send activation emails with the following link format:
    
    ```http://politicaladsleuth.com/account/activate/XXXXXXXXXXXXXXXXXX/```

Replace ```http://politicaladsleuth.com``` with your local server's URL (e.g. `http://127.0.0.1:8000/`) and visit the link to activate an account on your local database.